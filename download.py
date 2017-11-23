#!/usr/bin/env python
# coding: utf-8

import urllib.error
import urllib.request
import pandas
import MySQLdb
import records
import unidecode 

class CsvAnalysis():

    def __init__(self):
        self._url = "http://fr.openfoodfacts.org/data/fr.openfoodfacts.org.products.csv"
        self._file_name = 'data.csv'
        # Column of interest
        self._column = ['product_name', 'url', 'quantity','packaging', 'brands', 'origins', 'countries_fr',
                        'allergens', 'traces_fr', 'additives_n','additives_fr',
                        'nutrition_grade_fr','categories_fr', 'main_category_fr']

        # Dataframe from pandas module
        try:
            with open(self._file_name):
                pass
        except FileNotFoundError:
            self.download_file()
        finally:
            self.food_cat = pandas.read_csv(self._file_name, sep="\t", low_memory=False, usecols=self._column, encoding='utf-8')
            # Remove countries which aren't France
            self.food_cat = self.food_cat[self.food_cat['countries_fr'] == 'France']
            del self.food_cat['countries_fr']
            # Remove empty row countries_fr from dataframe
            columns = ['main_category_fr', 'product_name', 'nutrition_grade_fr']
            for column in columns:
                self.food_cat = self.food_cat[~self.food_cat[column].isnull()]
            # Remove empty row from product_name
            #self.food_cat = self.food_cat[~self.food_cat['product_name'].isnull()]
            self.food_cat.sort_values(by='categories_fr')
            
            self.food_cat['categories_fr'] = self.food_cat['categories_fr'].str.split(',').str.get(-1)
            self.food_cat.sort_values(by='categories_fr')


    def download_file(self):
        try:
            urllib.request.urlretrieve(self.url, self.file_name)
        except urllib.error.URLError:
            print('Wrong url')

    def find_categories_fr(self, category):
        mask = self.food_cat["main_category_fr"] == (category)
        return self.food_cat[mask].sort_values(by='categories_fr')

    def get_subcategories(self, category):
        return category.categories_fr.unique()       


class DataToMySql():

    def __init__(self):
        self._db=records.Database('mysql+mysqldb://root:MyNewPass@localhost/OpenFoodFacts')
        self._category_list = ['Snacks sucrés', 'Pâtes à tartiner', 'Beurres', 'Desserts', 'Confitures']
        self._csv = CsvAnalysis()

    def load_categories_to_db(self):
        for category in self._category_list:
            self._db.query('INSERT INTO Categories(category_name) VALUES ("%s")' % (category))

    def load_subcategories_to_db(self):
        for category in self._category_list:
            categories_product = self._csv.find_categories_fr(category)
            subcategories = self._csv.get_subcategories(categories_product)
            for subcategory in subcategories:
                self._db.query('INSERT INTO Subcategories (subcategory_name, category_id) VALUES (("%s"), (SELECT id_category from categories where category_name = "%s"))' % (subcategory, category ))

    def load_products_to_db(self):
        products = {}
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

            allegerns_list = []
            allegerns = categories_product.allergens
            for allegern in allegerns:
                allegerns_list.append(allegern)

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

            index = 0
            for _ in product_list:
                self._db.query('INSERT INTO Product (product_name, quantity, url_text, packaging, brand, origin, allegerns, traces, additives_number, additives, nutrition_score, category_id, subcategory_id) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", (SELECT id_category FROM categories WHERE category_name = "%s"), (SELECT id_subcategory FROM subcategories WHERE id_subcategory = "%s"))' % (product_list[index] ,quantity_list[index] ,url_list[index] ,packaging_list[index] ,brand_list[index] ,origin_list[index] ,allegerns_list[index] ,traces_list[index] ,additives_n_list[index] ,additive_list[index] ,nutrition_score_list[index], category, subcategory_product_list[index]))
                index += 1

                
