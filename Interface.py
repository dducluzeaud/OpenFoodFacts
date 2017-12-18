#!/usr/local/bin/python3
# coding: utf8

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
            success = self.update_database()
            if success is False:
                print("Une erreur s'est produite avec la base de donnée")

    def select_categories(self):
        sql = 'SELECT category_name FROM categories '
        categories = self._db.query(sql)
        categories_list = self.list_items(categories)
        return categories_list

    def select_subcategories(self, cat, page=1, nb_element=10):
        f_element = (nb_element * (page - 1))
        query = 'SELECT subcategory_name FROM subcategories AS s '
        query += 'INNER JOIN categories AS c ON s.category_id = c.id_category '
        query += 'WHERE category_name = "%s" LIMIT %i OFFSET %i'
        subcategories = self._db.query(query % (cat, nb_element, f_element))
        subcategories_list = self.list_items(subcategories)
        return subcategories_list

    def select_products(self, subcategory, page=1, nb_element=10):
        f_element = (nb_element * (page - 1))
        query = 'SELECT id_product, product_name from products AS p '
        query += 'INNER JOIN subcategories AS s '
        query += 'ON p.subcategory_id= s.id_subcategory '
        query += 'WHERE subcategory_name = "%s"'
        query += 'AND product_replacement_id is NULL '
        query += 'LIMIT %i OFFSET %i'
        products = self._db.query(query % (subcategory, nb_element, f_element))
        id_prod = []
        product_name = []
        for value in products:
            id_prod.append(value.id_product)
            product_name.append(value.product_name)

        return id_prod, product_name

    def select_substitutes(self, subcat, prod_name,  page=1, nb_element=10):
        f_element = (nb_element * (page - 1))
        sql = 'SELECT product_name, brand, url_text FROM products AS p '
        sql += 'INNER JOIN subcategories AS s '
        sql += 'ON s.id_subcategory=p.subcategory_id '
        sql += 'WHERE subcategory_name = "%s" AND product_name != "%s" '
        sql += 'ORDER BY nutrition_score'
        sql += ' ASC LIMIT %i OFFSET %i'
        substitutes = self._db.query(sql % (subcat, prod_name, nb_element, f_element))
        return substitutes

    def select_product_and_substitute(self, page=1, nb_element=10):
        f_element = (nb_element * (page - 1))
        sql = 'SELECT p.product_name, r.product_name_replacement '
        sql += 'FROM products AS p '
        sql += 'INNER JOIN replacement_products AS r '
        sql += 'ON p.product_replacement_id = r.id_product_replacement '
        sql += 'LIMIT %i OFFSET %i'
        products_substitutes = self._db.query(sql % (nb_element, f_element))
        return products_substitutes

    def select_information_products(self, id_prod, product_name, subcategory):
        sql = 'SELECT quantity, packaging, origin, allergens, traces, '
        sql += 'additives_number, additives '
        sql += 'FROM products AS p '
        sql += 'INNER JOIN subcategories AS s '
        sql += 'ON p.subcategory_id= s.id_subcategory '
        sql += 'WHERE product_name= "%s" AND subcategory_name = "%s" '
        sql += 'AND id_product = %i'
        info = self._db.query(sql % (product_name, subcategory, id_prod))
        return info

    def list_items(self, items):
        cat = []
        for value in items:
            cat.append(value[0])
        return cat

    def add_substitute(self, substitute, product):
        # Check if the substitute is not already in the table
        sql = 'SELECT product_name_replacement FROM Replacement_products'
        sub_known = self._db.query(sql)
        if sub_known != " ":
            insert = "INSERT INTO Replacement_products"
            insert += '(product_name_replacement) VALUES ("%s")'
            self._db.query(insert % (substitute))

        update = 'UPDATE Products SET product_replacement_id = '
        update += '(SELECT id_product_replacement FROM replacement_products '
        update += 'WHERE product_name_replacement="%s") '
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
        insert = db.insert_into_db()
        return insert


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

    def choose_category(self, number, *cat):
        for key, value in enumerate(*cat):
            if key == number:
                self._chosen_category = value
                break

    def choose_subcategory(self, number, *subcat):
        for key, value in enumerate(*subcat):
            if key == number:
                self._chosen_subcategory = value
                break

    def choose_product(self, number, *prod):
        for key, value in enumerate(*prod):
            if key == number:
                self._chosen_product = value
                break

    def choose_substitute(self, number, *sub):
        for key, value in enumerate(*sub):
            if key == number:
                self._chosen_substitute = value.product_name
                break
