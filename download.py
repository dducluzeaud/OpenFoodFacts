#!/usr/bin/env python
# coding: utf-8

import urllib.error
import urllib.request
import pandas

class CsvAnalysis():

    def __init__(self):
        self.url = "http://fr.openfoodfacts.org/data/fr.openfoodfacts.org.products.csv"
        self.file_name = 'data.csv'
        # Column of interest
        self.column = ['product_name', 'url', 'quantity','packaging', 'brands', 'origins', 'countries_fr',
                        'ingredients_text','allergens', 'traces_fr', 'additives_n','additives_fr',
                        'nutrition_grade_fr','main_category_fr']

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
            # Remove empty row countries_fr from dataframe
            self.food_cat = self.food_cat[~self.food_cat['main_category_fr'].isnull()]


    def download_file(self):
        try:
            urllib.request.urlretrieve(self.url, self.file_name)
        except urllib.error.URLError:
            print('Wrong url')

    def find_categories_fr(self, category):
        mask = self.food_cat["main_category_fr"].str.contains(category)
        return self.food_cat[mask]


    def data_analysis(self):

        sugar_snack = self.find_categories_fr('Snacks sucrés')
        spread = self.find_categories_fr("Pâtes à tartiner")
        butter = self.find_categories_fr("Beurres")
        desert = self.find_categories_fr("Desserts")
        jam = self.find_categories_fr("Confitures")

        sugar_snack.to_csv('sugar_snack.tsv', sep='\t', encoding='utf-8')
        spread.to_csv('spread.tsv', sep='\t', encoding='utf-8')
        butter.to_csv('butter.tsv', sep='\t', encoding='utf-8')
        desert.to_csv('desert.tsv', sep='\t', encoding='utf-8')
        jam.to_csv('jam.tsv', sep='\t', encoding='utf-8')
        
csv = CsvAnalysis()
csv.data_analysis()
