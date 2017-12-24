#!/usr/local/bin/python3
#coding: utf_8

import urllib.error
import urllib.request
import pandas
import records


class CsvAnalysis:
    """ Analysis the csv with pandas dataframe. """

    _url = "http://fr.openfoodfacts.org"
    _url += "/data/fr.openfoodfacts.org.products.csv"

    def __init__(self):
        self.file_name = 'data.csv'
        # Column of interest
        self._col = ['product_name', 'url', 'quantity', 'packaging']
        self._col += ['brands', 'origins', 'countries_fr', 'allergens']
        self._col += ['traces_fr', 'additives_n', 'additives_fr']
        self._col += ['nutrition_grade_fr', 'categories_fr']
        self._col += ['main_category_fr']

        # Check if the csv is already in the file
        try:
            with open(self.file_name, 'r'):
                pass
        except FileNotFoundError:
            CsvAnalysis.download_file()
        finally:
            # Read the csv file, and create a dataframe
            self.food_cat = pandas.read_csv(self.file_name,
                                            sep="\t",
                                            low_memory=False,
                                            usecols=self._col,
                                            encoding="utf8")

            # Remove countries which aren't France
            mask = self.food_cat['countries_fr']
            self.food_cat = self.food_cat[mask == 'France']

            # Delete column countries_fr
            del self.food_cat['countries_fr']

            # Remove empty row countries_fr from dataframe
            columns = ['main_category_fr', 'product_name', 'nutrition_grade_fr']
            for column in columns:
                self.food_cat = self.food_cat[~self.food_cat[column].isnull()]

            # Remove empty row from product_name
            self.food_cat.sort_values(by='categories_fr')

            # Select the last value from categories_fr
            # to use it as a subcategory
            col = 'categories_fr'
            self.food_cat[col] = self.food_cat[col].str.split(',').str.get(-1)
            self.food_cat.sort_values(by='categories_fr')

    @classmethod
    def download_file(cls):
        try:
            urllib.request.urlretrieve(cls._url, 'data.csv')
        except urllib.error.URLError:
            print('Wrong url')

    def find_categories_fr(self, category):
        mask = self.food_cat["main_category_fr"] == category
        return self.food_cat[mask].sort_values(by='categories_fr')

    def get_subcategories(self, category):
        return category.categories_fr.unique()


class Singleton(type):
    """ Create a singleton"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DataToMySql(metaclass=Singleton):
    """ Insert the value from the dataframe to database"""
    def __init__(self):
        url = 'mysql+mysqldb://root:MyNewPass@localhost/OpenFoodFacts'
        self._db = records.Database(url)
        self._category_list = ['Snacks sucrés', 'Pâtes à tartiner']
        self._category_list += ['Beurres', 'Desserts', 'Confitures']
        self._csv = CsvAnalysis()

    def _load_categories_to_db(self):
        for category in self._category_list:
            sql = 'INSERT INTO Categories(category_name) VALUES ("%s")'
            self._db.query(sql % category)

    def _load_subcategories_to_db(self):
        for category in self._category_list:
            categories_product = self._csv.find_categories_fr(category)
            subcategories = self._csv.get_subcategories(categories_product)
            sql = 'INSERT INTO Subcategories'
            sql += ' (subcategory_name, name_category)'
            sql += 'VALUES ("%s", (SELECT category_name '
            sql += 'FROM categories WHERE category_name = "%s"))'
            for subcategory in subcategories:
                self._db.query(sql % (subcategory, category))


    def _load_products_to_db(self):
        for category in self._category_list:
            categories_product = self._csv.find_categories_fr(category)

            product_list = []
            product_name = categories_product.product_name
            for name in product_name:
                product_list.append(name)

            quantity_list = []
            quantities = categories_product.quantity
            for quantity in quantities:
                quantity_list.append(quantity)

            url_list = []
            urls = categories_product.url
            for url in urls:
                url_list.append(url)

            packaging_list = []
            packaging = categories_product.packaging
            for package in packaging:
                packaging_list.append(package)

            brand_list = []
            brands = categories_product.brands
            for brand in brands:
                brand_list.append(brand)

            origin_list = []
            origins = categories_product.origins
            for origin in origins:
                origin_list.append(origin)

            allergens_list = []
            allergens = categories_product.allergens
            for allegern in allergens:
                allergens_list.append(allegern)

            traces_list = []
            traces = categories_product.traces_fr
            for trace in traces:
                traces_list.append(trace)

            additives_n_list = []
            additives_n = categories_product.additives_n
            for additive_n in additives_n:
                additives_n_list.append(additive_n)

            additive_list = []
            additives = categories_product.additives_fr
            for additive in additives:
                additive_list.append(additive)

            nutrition_score_list = []
            nutrition_scores = categories_product.nutrition_grade_fr
            for nutrition_score in nutrition_scores:
                nutrition_score_list.append(nutrition_score)

            subcategory_product_list = []
            subcategories = categories_product.categories_fr
            for subcategory in subcategories:
                subcategory_product_list.append(subcategory)

            ind = 0
            for _ in product_list:
                sql = 'INSERT INTO Products'
                sql += '(product_name, quantity, url_text, packaging,'
                sql += 'brand, origin, allergens,'
                sql += ' traces, additives_number, '
                sql += 'additives, nutrition_score, subcategory_id) '
                sql += 'VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s",'
                sql += ' "%s", "%s", "%s", "%s",'
                sql += ' (SELECT id_subcategory FROM subcategories AS s '
                sql += 'INNER JOIN categories as c ON '
                sql += 'c.category_name=s.name_category'
                sql += ' WHERE subcategory_name = "%s" '
                sql += 'AND category_name= "%s"))'
                self._db.query(sql % (product_list[ind], quantity_list[ind], url_list[ind], packaging_list[ind], brand_list[ind], origin_list[ind], allergens_list[ind], traces_list[ind], additives_n_list[ind], additive_list[ind], nutrition_score_list[ind], subcategory_product_list[ind], category))
                ind += 1

    def insert_into_db(self):
        self._load_categories_to_db()
        self._load_subcategories_to_db()
        self._load_products_to_db()


if __name__ == '__main__':
    d = DataToMySql()
    d.insert_into_db()
    csv = CsvAnalysis()
    csv.download_file()
