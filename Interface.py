import records


class Data():

    def __init__(self):
        _connect = 'mysql+mysqldb://root:MyNewPass@localhost/OpenFoodFacts'
        self._db = records.Database(_connect)

    def select_categories(self):
        categories = self._db.query('SELECT category_name FROM categories')
        categories_index = self.index_items(categories)
        return categories_index

    def select_subcategories(self, category):
        subcategories = self._db.query('SELECT subcategory_name FROM subcategories INNER JOIN categories ON subcategories.category_id = categories.id_category WHERE category_name = "%s"' % (category))
        subcategories_index = self.index_items(subcategories)
        return subcategories_index

    def select_products(self, subcategory):
        products = self._db.query('SELECT product_name from product INNER JOIN categories on categories.id_category = product.category_id INNER JOIN subcategories ON subcategories.category_id=categories.id_category WHERE subcategory_name = "%s"' % (subcategory))
        products_index = self.index_items(products)
        return products_index

    def select_substitutes(self, subcategory, product_name):
        substitutes = self._db.query('SELECT product_name, brand, url_text from product INNER JOIN categories on categories.id_category = product.category_id INNER JOIN subcategories ON subcategories.category_id=categories.id_category WHERE subcategory_name = "%s" AND product_name != "%s" ORDER BY nutrition_score ASC' % (subcategory, product_name))

        product_col = []
        products_att = []
        for value in substitutes:
            product_col = [value.product_name, value.brand, value.url_text]
            products_att.append(product_col)

        index = {}
        number = 1
        for value in products_att:
            index[number] = value
            number += 1

        return index

    def index_items(self, items):
        index = {}
        number = 1
        for value in items:
            index[number] = value[0]
            number += 1
        return index


class UserChoice():

    def __init__(self):
        self._dt = Data()
        self._chosen_category = ""
        self._chosen_subcategory = ""
        self._chosen_product = ""

    @property
    def chosen_category(self):
        return self._chosen_category

    @property
    def chosen_subcategory(self):
        return self._chosen_subcategory

    @property
    def chosen_product(self):
        return self._chosen_product

    def choose_category(self, number):
        dic = self._dt.select_categories()
        for key, value in dic.items():
            if key == number:
                self._chosen_category = value
                break
            
    def choose_subcategory(self, number):
        dic = self._dt.select_subcategories(self._chosen_category)
        for key, value in dic.items():
            if key == number:
                self._chosen_subcategory = value
                break

    def choose_product(self, number):
        dic = self._dt.select_products(self._chosen_subcategory)
        for key, value in dic.items():
            if key == number:
                self._chosen_product = value
                break

    def choose_subsitute(self, number):
        chosen_substitue = ""
        sub = self._chosen_subcategory
        prod = self._chosen_product
        dic = self._dt.select_substitutes(sub, prod)
        for key, value in dic.items():
            if key == number:
                chosen_substitue = value
                break
