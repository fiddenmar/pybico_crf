PYthon BIbliography COnverter, based on Conditional Random Fields  
  
Requirements:  
python3  
python3-pip  
mysql
antiword
scikit-learn (pip3 install scikit-learn)  
sklearn-crfsuite (pip3 install sklearn_crfsuite)
pymyql (pip3 install pymysql)
docx (pip3 install docx)
  
Usage:  
python3 learn.py  
python3 pybico_crf.py
<Input>  
  
Example:  
$ ipython3 learn.py   
             precision    recall  f1-score   support  
  
   T_AUTHOR      1.000     1.000     1.000        68  
T_DELIMITER      0.939     1.000     0.969        31  
  T_JOURNAL      0.948     0.970     0.959       132  
 T_LOCATION      1.000     0.857     0.923         7  
    T_PAGES      0.893     1.000     0.943        25  
T_PUBLISHER      1.000     0.800     0.889        10  
    T_TITLE      1.000     1.000     1.000       147  
    T_TJSEP      1.000     1.000     1.000        10  
   T_VOLUME      0.917     0.846     0.880        13  
     T_YEAR      0.889     0.727     0.800        22  
  
avg / total      0.968     0.968     0.967       465  

Interactive input:
$ ipython3 pybico_crf.py
Enter the bibliography string
Author A.A. Title title title title. Awesome journal, 2016. - №2. - 13.
{'T_PAGES': '13.', 'T_AUTHOR': 'Author A.A.', 'T_TITLE': 'Title title title title.', 'T_JOURNAL': 'Awesome journal,', 'T_VOLUME': '№2.', 'T_YEAR': '2016.'}

Input using command line argument:
$ ipython3 pybico_crf.py -b "Author A.A. Title title title title. Awesome journal, 2016. - №2. - 13."
{'T_TITLE': 'Title title title title.', 'T_YEAR': '2016.', 'T_PAGES': '13.', 'T_AUTHOR': 'Author A.A.', 'T_JOURNAL': 'Awesome journal,', 'T_VOLUME': '№2.'}

Load result to database:
$ ipython3 pybico_crf.py -b "Author A.A. Title title title title. Awesome journal, 2016. - №2. - 13." -l -u root -p 123456
