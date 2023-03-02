## Github [link](https://github.com/Md557/python-phone-inventory)


## Starting instructions
* Install python 3.8 or greater
* Start a new terminal (or venv), and run command `python manage.py`

To view optional arguments, use `python manage.py -h`

## Model notes 

Database schema will be created automatically (if installing postgres):
 * `db.models.PSQLDriver`
 * `python manage.py --create_tables`

In order to properly store the data in normalized form (i.e. no columns with lists), 3 tables are recommended.
