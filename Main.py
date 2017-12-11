#!/usr/local/bin/python3 
# coding: utf-8

from Interface import UserChoice, Data


class Interface:

    def __init__(self):
        self._user = UserChoice()
        self._data = Data()

    def display_category_list(self, page=1):
        categories = self._data.select_categories()
        return self.display_form('Categories', categories, page)

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

    def display_substitute_list(self, page=1):
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
    
    def display_product_and_substitute(self, page=1):
        prod_and_subs = self._data.select_product_and_substitute()
        
        print('#########################')
        print('    Poduits substitués')
        print('#########################')
        print()
        print(prod_and_subs)

        for indice, value in enumerate(prod_and_subs, start=1):
            print(indice, value)

        print()
        print('        <',page,'>')

        action = self.user_choice

        if action == 'n':
            page += 1
            self.display_product_and_substitute(page)
        elif action == 'b' and page > 1:
            page -= 1
            self.display_product_and_substitute(page)
        else:
            return action

    def display_help(self):
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

        return self.user_choice

    def display_form(self, table, list, page):
        print('#########################')
        print('      ', table)
        print('#########################')
        print()

        for indice, value in enumerate(list, start=1):
            print(indice, value)

        print()
        print('        <',page,'>')

        return self.user_choice



    def homepage(self):
        print('#########################')
        print('#      Bienvenue !      #')
        print('#########################')
        print('')
        print(' Que souhaitez vous faire ?')
        print(' 1 - Subsituez un produit ')
        print(' 2 - Retrouver mes aliments substitués ?')
        print(' 3 - Mettre à jour la base de donnée ?')

        return self.user_choice

    @property
    def user_choice(self):
        action = input('>> ')
        try:
            if action in 'qnab':
                return action
            elif action in '1234567890':
                return int(action)
        except:
            print("Mauvais choix ! Rééssayez ou tapez h pour de l'aide")

    def main(self):
        action = self.homepage()
        if action == 1:
            choice_category = self.display_category_list()
            self._user.choose_category(choice_category)

            choice_subcategory = self.display_subcategory_list()
            self._user.choose_subcategory(choice_subcategory)

            choice_product = self.display_product_list()
            self._user.choose_product(choice_product)

            choice_substitute = self.display_substitute_list()
            self._user.choose_subsitute(choice_substitute)
            self._data.add_substitute(self._user.chosen_substitute, self._user.chosen_product)
            print('Produits substitué !')

            self.homepage()

        elif action == 2:
            self.display_subsitute_list()
        elif action == 3:
            self._data.update_database()
            print('Mise a jour réussi !')
            self.homepage()
        else:
            print('Mauvais choix !')
            self.homepage()

inter = Interface()
inter.main()
