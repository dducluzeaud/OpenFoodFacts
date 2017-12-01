import records


class Data():

    def __init__(self):
        _connect = 'mysql+mysqldb://root:MyNewPass@localhost/OpenFoodFacts'
        self._db = records.Database(_connect)

    def select_categories(self, nb_element=25, page=1):
        page_number = nb_element * page
        categories = self._db.query('SELECT category_name FROM categories LIMIT %i' % (page_number))
        categories_list = self.list_items(categories)
        return categories_list

    def select_subcategories(self, category, nb_element=25, page=1):
        page_number = nb_element * page
        subcategories = self._db.query('SELECT subcategory_name FROM subcategories INNER JOIN categories ON subcategories.category_id = categories.id_category WHERE category_name = "%s" LIMIT %i' % (category, page_number))
        subcategories_list = self.list_items(subcategories)
        return subcategories_list

    def select_products(self, subcategory, nb_element=25, page=1):
        page_number = nb_element * page
        products = self._db.query('SELECT product_name from product INNER JOIN categories on categories.id_category = product.category_id INNER JOIN subcategories ON subcategories.category_id=categories.id_category WHERE subcategory_name = "%s" LIMIT %i' % (subcategory, page_number))
        products_list = self.list_items(products)
        return products_list

    def select_substitutes(self, subcategory, product_name, nb_element=25, page=1):
        page_number = nb_element * page
        substitutes = self._db.query('SELECT product_name, brand, url_text from product INNER JOIN categories on categories.id_category = product.category_id INNER JOIN subcategories ON subcategories.category_id=categories.id_category WHERE subcategory_name = "%s" AND product_name != "%s" ORDER BY nutrition_score ASC LIMIT %i' % (subcategory, product_name, page_number)) 
        return substitutes
        
    def list_items(self, items):
        list = []
        for value in items:
            list.append(value[0])
        return list

    def add_substitute(self, substitute, product):
        self._db.query('INSERT INTO Replaced_product(product_name_replaced) VALUES ("%s")' % (substitute))
        self._db.query('UPDATE Product SET product_name_replaced_id = (SELECT id_product_replaced FROM Replaced_product WHERE product_name_replaced="%s") WHERE product_name="%s"' % (substitute, product))

    def update_database(self):
        
class UserChoice():

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

user = UserChoice()
user.choose_subsitute(1)