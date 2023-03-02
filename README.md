## Github [link](https://github.com/Md557/python-phone-inventory)


## Starting instructions
* install python 3.9
Start command `python manage.py`

To view optional arguments, use `python manage.py -h`

## Model notes 

Database schema will not be created automatically, but a class with functions to create the DDL is in:
 * db.models.PSQLDriver

In order to properly store the data in normalized form (i.e. no columns with lists), 3 tables are recommended.
