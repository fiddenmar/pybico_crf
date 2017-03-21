import getopt
import locale
import shutil
import sys
from itertools import cycle
from subprocess import Popen, PIPE

import docx
from docx.table import Table
from docx.text.paragraph import Paragraph


class Doc2TextError(Exception):
    pass


def consist_table(file):
    if '|' in file:
        return True
    return False


def smart_strip(cells):
    cells[:] = [' '.join(cell.split()) for cell in cells]
    return ';'.join(cells)


def parse_word_tables(file):
    """
    parse doc tables
    restrictions: all cells must be filled (no empty cells)
    """
    lines = file.splitlines()
    result = []
    cells = []
    for line in lines:
        if not line:
            continue
        if line[0] != '|' and line[-1] != '|':
            result.append(smart_strip(cells))
            result.append(line)
        else:
            row_line = line.split('|')
            is_new_line = all(not cell_line.isspace() for cell_line in row_line)

            if is_new_line:
                result.append(smart_strip(cells))
                cells = row_line
            else:
                row_line_cycle = cycle(row_line)
                cells[:] = [cell + next(row_line_cycle) for cell in cells]
    return result


def paragraphs_tables(docx):
    """
    merge tables and paragraphs together in docx
    need it to keep order of text and tables of docx documents
    """
    p_t_list = []
    for content in docx._body._body.getchildren():
        if content.tag == '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p':
            p_t_list.append(Paragraph(content, docx._body));
        elif content.tag == '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tbl':
            p_t_list.append(Table(content, docx._body));
        else:
            print(content.tag);
    return p_t_list


def doc2text(filename):
    if filename[-5:] == '.docx':
        text = []
        document = docx.Document(filename)
        for t in paragraphs_tables(document):
            if type(t) is Table:
                for r in t.rows:
                    text.append(';'.join([' '.join(cell.text.split()) for cell in r.cells]))
            else:
                text.append(t.text)
        return '\n'.join(text)
    elif filename[-4:] == '.doc':
        locale.setlocale(locale.LC_ALL, ('ru', 'utf8'))
        antiword = shutil.which('antiword')
        if antiword is None:
            raise Doc2TextError('Antiword utility must be installed and added to PATH!')
        cmd = [antiword, filename]
        p = Popen(cmd, stdout=PIPE)
        stdout, stderr = p.communicate()
        result = stdout.decode('utf8')
        if consist_table(result):
            result = parse_word_tables(result)
        return result
    else:
        raise Doc2TextError('Unknown document type')


def main(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:", ["ifile=", ])
        if len(opts) == 0:
            print('doc2text.py -i <inputfile>')
            return

        for opt, arg in opts:
            if opt == '-h':
                print('doc2text.py -i <inputfile>')
                sys.exit()
            elif opt in ("-i", "--ifile"):
                inputfile = arg

        if inputfile is not None:
            text = doc2text(inputfile)
            print(text)
    except getopt.GetoptError:
        print('doc2text.py -i <inputfile>')
        sys.exit(2)
    except Doc2TextError as e:
        print(e.args[0])
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
