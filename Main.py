#!/usr/bin/env python
# coding: utf-8
from Interface import UserChoice, Data

class Interface:

    def __init__(self):
        self._user = UserChoice()
        self._data = Data()

    def display_category_list(self, page=1):
        categories = self._data.select_categories()
        choice = self.display_form('Categories', categories, page)
        if choice == 'n':
            page += 1
            self.display_category_list(page)
        elif choice == 'b' and page > 1:
            page -= 1
            self.display_category_list(page)
        else:
            return choice

    def display_subcategory_list(self, page=1):
        category = self._user.chosen_category
        subcategories = self._data.select_subcategories(category, page)
        choice = self.display_form('Sous-Categories', subcategories, page)
        if choice == 'n':
            page += 1
            self.display_subcategory_list(page)
        elif choice == 'b' and page > 1:
            page -= 1
            self.display_subcategory_list(page)
        else:
            return choice

    def display_product_list(self, page=1):
        subcategory = self._user.chosen_subcategory
        products = self._data.select_products(subcategory)
        choice = self.display_form('Produits', products, page)
        if choice == 'n':
            page += 1
            self.display_product_list(page)
        elif choice == 'b' and page > 1:
            page -= 1
            self.display_product_list(page)
        else:
            return choice

    def display_subsitute_list(self, page=1):
        subcategory = self._user.chosen_subcategory
        product_name = self._user.chosen_product
        substitutes = self._data.select_substitutes(subcategory, product_name)
        choice = self.display_subsitutes(substitutes)
        if choice == 'n':
            page += 1
            self.display_subsitute_list(page)
        elif choice == 'b' and page > 1:
            page -= 1
            self.display_subsitute_list(page)
        else:
            return choice
        

    def display_help():
        print('')

    def display_subsitutes(self, substitutes):
        print('#########################')
        print('       Substitues      ')
        print('#########################')
        print()

        for key, val in enumerate(substitutes, start=1):
            prod_name, brand, url = val.product_name, val.brand, val.url_text

            print(key, ' ', prod_name)
            print("    Marque =", brand)
            print("    Site   =", url)
            print()

        user_choice = self.user_choice()

        return user_choice

    def display_form(self, table, list, page):
        print('#########################')
        print('      ', table)
        print('#########################')
        print()

        for indice, value in enumerate(list, start=1):
            print(indice, value)
        
        print()
        print('        <', page,'>')
        action = self.user_choice()

        return action

    def homepage(self):
        display_homepage = True

        print('#########################')
        print('#        Bienveue !     #')
        print('#########################')
        print('')
        print(' Que souhaitez vous faire ?')
        print(' 1 - Subsituez un produit ')
        print(' 2 - Retrouver mes aliments substitués ?')
        print(' 3 - Mettre à jour la base de donnée ?')

        while display_homepage:
            try:
                number = int(input())
                if number == 1:
                    display_homepage = False
                elif number == 2:
                    display_homepage = False
                elif number == 3:
                    self._data.update_database()
                elif number == 'q':
                    print('Fin du programme ! Au revoir. ')
                    display_homepage = False
                else:
                    print('Tapez 1 ou 2 pour faire un choix.')
            except ValueError:
                print('Vous devez saisir un chiffre')

            return number

    def user_choice(self):
        action = input('>> ')
        if action in 'qnab':
            return action
        elif action in '1234567890':
            return int(action)

    def main(self):
        action = self.homepage()
        if action == 1:
            page_category = 1
            choice_category = self.display_category_list(page_category)
            if choice_category == 'n':
                page_category += 1
                self.display_category_list(page_category)
            elif choice_category == 'b':
                page_category -= 1
                self.display_category_list(page_category)
            else:
                self._user.choose_category(choice_category)

            choice_subcategory = self.display_subcategory_list()
            self._user.choose_subcategory(choice_subcategory)

            choice_product = self.display_product_list()
            if choice_product == 'n':
                self.display_product_list()
            elif choice_product =='b':
                self.display_product_list()
            else:
                self._user.choose_product(choice_product)

            choice_substitute = self.display_subsitute_list()
            if choice_substitute == 'n':
                self.display_subsitute_list()
            elif choice_substitute == 'b':
                self.display_subsitute_list()
            else:
                self._user.choose_subsitute(choice_substitute)
                self._data.add_substitute(self._user.chosen_substitute, self._user.chosen_product)
                print('Produits substitué !')
        elif action == 2:
            pass
        elif action == 3:
            pass
        else:
            print('Mauvais choix !')


inter = Interface()
inter.main()
