# Openfoodfacts

This project allows you to manage categories of products. The categories are imported from openfoodfacts.com. The user will use the program to select the best product for his needs in terms of nutrition benefits. To navigate between categories and product use numeric key. To quit the programm use q.

### Installing

 - pip install -r /path/to/requirements.txt`
 - Create a database and run the sql script database.sql
 - Create a config file (name it config.ini) to access your database.

   The config file has to be like this:
   ```
    [mysql]
    host =
    user =
    passwd =
    db =
 - The first time you run the program, the database will load automatically

### Help

 - Use digital key betwen 0 and 9 to make a choice.
 - Use A to go to the homepage at anytime.
 - Use N to move to the next page.
 - Use B to move to the previous page.
 - Use i + digital key to show information about a product or a substitute
   (example: i 1 to show the product n°1 displayed). If you use that method in the substituted products, you can replace the substituted product by another one.
 - Use H to display help at anytime.
 - Use Q to quit.

## Built With

* [Pandas](http://pandas.pydata.org/index.html) - Python Data Analysis Library
* [Records](https://github.com/kennethreitz/records) - Records: SQL for Humans™
* [Python3](https://docs.python.org/3/) - Python 3

## Authors

* **Ducluzeaud David** - *Initial work* - [Github](https://github.com/SneakyPeat)
