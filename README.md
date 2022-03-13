# Michal project
[מהאתר הזה משווים שמות ונוסחה כימית](https://pubchem.ncbi.nlm.nih.gov/)  
[אם לא מוצאים את החומר באתר הקודם אז צריך לבדוק פה. מהאתר הזה גם לוקחים את הנתונים לעמודה KI לפי הפרמטר non polar column ---> HP-5MS](https://webbook.nist.gov/chemistry/name-ser/)  
לפעמים אין HP -5MS אז האופציות במקום זה הן: HP-5 MS או HP-5 או HP-1 TU או DB-5 או DB-1 (זה לפי הסדר חשיבות)


## installation
```bash
pip install -r /path/to/requirements.txt
python main.py
```

arguments:
  - **-h, --help**            show the help message  
  - **-c COMPOUND [COMPOUND ...], --compound COMPOUND [COMPOUND ...]**
                        a list or a single compound to collect data from PubChem and NIST  
  - **--workbook WORKBOOK**   xlsx workbook path   
                        path to the xlsx workbook
  - **-o OUT, --out OUT**     xlsx workbook output path  
                        path to the **output** xlsx workbook

