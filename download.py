#!/usr/bin/env python
# coding: utf-8

import urllib.error
import urllib.request
import pandas
import MySQLdb


class CsvAnalysis():

    def __init__(self):
        self.url = "http://fr.openfoodfacts.org/data/fr.openfoodfacts.org.products.csv"
        self.file_name = 'data.csv'
        # Column of interest
        self.column = ['product_name', 'url', 'quantity','packaging', 'brands', 'origins', 'countries_fr',
                        'allergens', 'traces_fr', 'additives_n','additives_fr',
                        'nutrition_grade_fr','categories_fr', 'main_category_fr']

        # Dataframe from pandas module
        try:
            with open(self.file_name):
                pass
        except FileNotFoundError:
            self.download_file()
        finally:
            self.food_cat = pandas.read_csv(self.file_name, sep="\t", low_memory=False, usecols=self.column, encoding='utf-8')
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
            #self.food_cat['categories_fr'] = self.food_cat['subcategories']

            self.food_cat.to_csv('noob.tsv', sep='\t')


    def download_file(self):
        try:
            urllib.request.urlretrieve(self.url, self.file_name)
        except urllib.error.URLError:
            print('Wrong url')

    def find_categories_fr(self, category):
        mask = self.food_cat["main_category_fr"] == (category)
        return self.food_cat[mask]


    def data_analysis(self):
        
        """
        categories_list = ['Snacks sucrés', 'Pâtes à tartiner', 'Beurres', 'Desserts', 'Confitures']
        categories_chosen = []
        for category in categories_list:
            categories_chosen.append(self.find_categories_fr(category).drop_duplicates())

        print(len(categories_chosen))
        for category in categories_chosen:
            print(category)
        """

        sugar_snack = self.find_categories_fr('Snacks sucrés')
        spread = self.find_categories_fr("Pâtes à tartiner")
        butter = self.find_categories_fr("Beurres")
        desert = self.find_categories_fr("Desserts")
        jam = self.find_categories_fr("Confitures")

        categories_chosen = sugar_snack + spread + butter + desert + jam
        categories_chosen.drop_duplicates()
        print(len(categories_chosen))
        print(type(categories_chosen))
        print(len(sugar_snack)+len(spread)+len( butter) +len(desert)+len(jam))

        """
        print('sugar_snack: ;' ,len(sugar_snack))
        print('spread: ', len(spread))     
        print('butter: ', len(butter))    
        print('desert: ', len(desert))
        print('jam: ', len(jam))
        """

        sugar_snack.to_csv('sugar_snack.tsv', sep='\t', encoding='utf-8')
        spread.to_csv('spread.tsv', sep='\t', encoding='utf-8')
        butter.to_csv('butter.tsv', sep='\t', encoding='utf-8')
        desert.to_csv('desert.tsv', sep='\t', encoding='utf-8')
        jam.to_csv('jam.tsv', sep='\t', encoding='utf-8')       



class DataToMySql():

    def __init__(self):
        db = MySQLdb.connect(user="root", passwd="MyNewPass", db="OpenFoodFacts")
        c=db.cursor()
        c.execute("""SELECT category_name FROM categories""")
        print(c.fetchall())

csv = CsvAnalysis()
csv.data_analysis()

#d_sql = DataToMySql()
