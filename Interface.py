#!/usr/local/bin/python3 
# coding: utf-8

import records
from download import DataToMySql


class Data:

    def __init__(self):
        _connect = 'mysql+mysqldb://root:MyNewPass@localhost/OpenFoodFacts'
        self._db = records.Database(_connect)

        # Check if the databse is not empty
        data = self._db.query('SELECT product_name FROM products LIMIT 1')
        # If the database is empty, load the database 
        
        if data.first() is None:
            self.update_database()

    def select_categories(self):
        sql = 'SELECT category_name FROM categories '
        categories = self._db.query(sql)
        categories_list = self.list_items(categories)
        return categories_list

    def select_subcategories(self, category, page=1, nb_element=10):
        first_element = (nb_element * (page - 1))
        query = 'SELECT subcategory_name FROM subcategories AS s '
        query += 'INNER JOIN categories AS c ON s.category_id = c.id_category '
        query += 'WHERE category_name = "%s" LIMIT %i OFFSET %i'
        subcategories = self._db.query(query % (category, nb_element, first_element))
        subcategories_list = self.list_items(subcategories)
        return subcategories_list

    def select_products(self, subcategory, page=1, nb_element=10):
        first_element = (nb_element * (page - 1))
        query = 'SELECT product_name from products AS p '
        query += 'INNER JOIN subcategories AS s ON p.subcategory_id= s.id_subcategory '
        query += 'WHERE subcategory_name = "%s" LIMIT %i OFFSET %i'
        products = self._db.query(query % (subcategory, nb_element, first_element))
        products_list = self.list_items(products)
        return products_list

    def select_substitutes(self, subcategory, product_name,  page=1, nb_element=10):
        first_element = (nb_element * (page - 1))
        sql = 'SELECT product_name, brand, url_text FROM products AS p '
        sql += 'INNER JOIN subcategories AS s ON s.subcategory_id= p.subcategory_id'
        sql += 'WHERE subcategory_name = "%s" AND product_name != "%s" ORDER BY nutrition_score'
        sql += 'ASC LIMIT %i OFFSET %i'
        substitutes = self._db.query(sql % (subcategory, product_name, nb_element, first_element))
        return substitutes

    def select_product_and_substitute(self, page=1, nb_element=10):
        first_element = (nb_element * (page - 1))
        sql = 'SELECT p.product_name, r.replacement_product_name FROM products AS p '
        sql += 'INNER JOIN replacement_product AS r '
        sql += 'ON p.replacement_product_id = r.product_replacement_id'
        sql += ' LIMIT %i OFFSET %i'
        products_substitutes = self._db.query(sql % (nb_element, first_element))
        return products_substitutes

    def list_items(self, items):
        list = []
        for value in items:
            list.append(value[0])
        return list

    def add_substitute(self, substitute, product):
        # Check if the substitute is not already in the table
        sub_known = self._db.query('SELECT product_replacement_name FROM Replacement_products')
        if sub_known != " ":
            insert = "INSERT INTO Replacement_products(product_name_replacement)"
            insert += ' VALUES ("%s")'
            self._db.query(insert % (substitute))

        update = 'UPDATE Products SET product_name_replacement_id = '
        update += '(SELECT id_product_replacement FROM replacement_product '
        update += 'WHERE product_name_replacement="%s")'
        update += 'WHERE product_name="%s"'
        self._db.query(update % (substitute, product))

    def update_database(self):
        db = DataToMySql()
        # Remove all the data in the database
        self._db.query('DELETE FROM subcategories')
        self._db.query('DELETE FROM categories')
        self._db.query('DELETE FROM products')
        self._db.query('DELETE FROM replacement_products')
        # Insert new value from internet
        db.insert_into_db()


class UserChoice:

    def __init__(self):
        self._dt = Data()
        self._chosen_category = ""
        self._chosen_subcategory = ""
        self._chosen_product = ""
        self._chosen_substitute = ""

    @property
    def chosen_category(self):
        return self._chosen_category

    @property
    def chosen_subcategory(self):
        return self._chosen_subcategory

    @property
    def chosen_product(self):
        return self._chosen_product

    @property
    def chosen_substitute(self):
        return self._chosen_substitute

    def choose_category(self, number):
        cat_list = self._dt.select_categories()
        for key, value in enumerate(cat_list, start=1):
            print(key, value)
            if key == number:
                self._chosen_category = value
                break

    def choose_subcategory(self, number):
        sub_list = self._dt.select_subcategories(self._chosen_category)
        for key, value in enumerate(sub_list, start=1):
            if key == number:
                self._chosen_subcategory = value
                break

    def choose_product(self, number):
        prod_list = self._dt.select_products(self._chosen_subcategory)
        for key, value in enumerate(prod_list, start=1):
            if key == number:
                self._chosen_product = value
                break

    def choose_subsitute(self, number):
        sub = self._chosen_subcategory
        prod = self._chosen_product
        substitutes_list = self._dt.select_substitutes(sub, prod)
        for key, value in enumerate(substitutes_list, start=1):
            if key == number:
                self._chosen_substitute = value.product_name
                break