import records
from download import DataToMySql

class Data:

    def __init__(self):
        _connect = 'mysql+mysqldb://root:MyNewPass@localhost/OpenFoodFacts'
        self._db = records.Database(_connect)

    def select_categories(self, page=1, nb_element=10):
        first_element = (nb_element  * (page - 1))
        query = 'SELECT category_name FROM categories '
        query += 'LIMIT %i OFFSET %i'
        categories = self._db.query(query  % (nb_element, first_element))
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
        query = 'SELECT product_name from product AS p '
        query += 'INNER JOIN categories AS c on c.id_category = p.category_id '
        query += 'INNER JOIN subcategories AS s ON s.category_id= c.id_category '
        query += 'WHERE subcategory_name = "%s" LIMIT %i OFFSET %i'
        products = self._db.query(query % (subcategory, nb_element, first_element))
        products_list = self.list_items(products)
        return products_list

    def select_substitutes(self, subcategory, product_name,  page=1, nb_element=10):
        first_element = (nb_element * (page - 1))
        query = 'SELECT product_name, brand, url_text FROM product AS p '
        query += 'INNER JOIN categories AS c on c.id_category = p.category_id'
        query += 'INNER JOIN subcategories AS s ON s.category_id= c.id_category'
        query += 'WHERE subcategory_name = "%s" AND product_name != "%s" ORDER BY nutrition_score'
        query += 'ASC LIMIT %i OFFSET %i'
        substitutes = self._db.query(query % (subcategory, nb_element, first_element))
        return substitutes

    def list_items(self, items):
        list = []
        for value in items:
            list.append(value[0])
        return list

    def add_substitute(self, substitute, product):
        insert = ''
        self._db.query('INSERT INTO Replaced_product(product_name_replaced) VALUES ("%s")' % (substitute))
        self._db.query('UPDATE Product SET product_name_replaced_id = (SELECT id_product_replaced FROM Replaced_product WHERE product_name_replaced="%s") WHERE product_name="%s"' % (substitute, product))

    def update_database(self):
        insert_into_db()

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
