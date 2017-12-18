#!/usr/local/bin/python3
# coding: utf-8
import sys

from Interface import UserChoice, Data


class Interface:

    def __init__(self):
        self._user = UserChoice()
        self._data = Data()

    def display_category_list(self, page=1):
        cat = self._data.select_categories()
        choice_category, page = self.display_form('Categories', cat)
        if isinstance(choice_category, int) and len(choice_category) == 1:
            self._user.choose_category(choice_category, cat)
        else:
            print('Mauvais choix')
            self.display_category_list(page)

    def display_subcategory_list(self, page=1):
        cat = self._user.chosen_category
        subcat = self._data.select_subcategories(cat, page)
        choice, page = self.display_form('Sous-Categories', subcat, page)
        if isinstance(choice, str):
            if choice.lower() == 'n' or choice.lower() == 'b':
                self.display_subcategory_list(page)
        elif isinstance(choice, int):
            self._user.choose_subcategory(choice, subcat)
        else:
            print('Mauvais choix')
            self.display_subcategory_list(page)

    def display_product_list(self, page=1):
        subcategory = self._user.chosen_subcategory
        id_products, products = self._data.select_products(subcategory, page)
        if len(products) == 1:
            print("Il n'y a qu'un seul produit pour cette sous-catégorie.")
            self.display_subcategory_list()
        else:
            choice, page = self.display_form('Produits', products, page)
            if isinstance(choice, str):
                if choice.lower() == 'n' or choice.lower() == 'b':
                    self.display_product_list(page)
            elif isinstance(choice, tuple):
                prod = choice[1]

                product = ""
                for indice, product_name in enumerate(products):
                    if prod == indice:
                        product = product_name
                        break

                id_prod = 0
                for indice, id_product in enumerate(id_products):
                    if indice == prod:
                        id_prod = id_product
                        break

                self.display_info(id_prod, product, subcategory)

                no_action = True
                while no_action:
                    action = input('Confirmer ce produit? (O/N) : ')
                    if action.lower() == 'n':
                        self.display_product_list(page)
                    elif action.lower() == 'o':
                        self._user.choose_product(prod, products)
                        no_action = False
                    else:
                        print('O ou N sont les deus choix possibles.')
            elif isinstance(choice, int):
                self._user.choose_product(choice, products)
            else:
                print('Mauvais choix')
                self.display_product_list(page)

    def display_substitute_list(self, page=1):
        subcat = self._user.chosen_subcategory
        prod_name = self._user.chosen_product
        substits = self._data.select_substitutes(subcat, prod_name, page)
        choice, page = self.display_subsitutes(substits)
        if isinstance(choice, str):
            if choice.lower() == 'n' or choice.lower() == 'b':
                self.display_substitute_list(page)
        elif isinstance(choice, int):
            self._user.choose_substitute(choice, substits)
        else:
            print('Mauvais choix')
            self.display_substitute_list(page)

    def display_subsitutes(self, substitutes, page=1):
        table = 'Produits de substitution'
        print('#############################################')
        print(table.center(45))
        print('#############################################')
        print()

        for key, val in enumerate(substitutes):
            prod_name, brand, url = val.product_name, val.brand, val.url_text

            print(' - ', key,  prod_name)
            print("       Marque =", brand)
            print("       Site   =", url)
            print()
        print()
        print('                     <', page, '>')

        return self.choice(substitutes, page)

    def display_product_and_substitute(self, page=1):
        prod_and_subs = self._data.select_product_and_substitute(page)
        title = 'Produits subsitués'

        print('#############################################')
        print(title.center(45))
        print('#############################################')
        print()

        for key, val in enumerate(prod_and_subs):
            prod_name, subs = val.product_name, val.product_name_replacement
            print(key, " produit original = ", prod_name)
            print('   produit de substitution = ', subs)
            print()
        print()
        print('                     <', page, '>')

        return self.choice(prod_and_subs, page)

    def display_help(self):
        print(' - Utiliser les chiffres de votre clavier pour faire un choix.')
        print(" - Utilisez A pour revenir à la page d'accueil.")
        print(" - Utilisez N pour aller à la page suivante.")
        print(" - Utilisez B pour aller à la page précédente.")
        print(" - Utilisez i + chiffre pour afficher des informations sur le produit.")
        print(" - Utilisez Q pour quitter le programme.")

    def display_form(self, table, cat, page=1):
        print('#############################################')
        print(table.center(45))
        print('#############################################')
        print()

        for ind, value in enumerate(cat):
            print(ind, value)

        print()
        print('        <',page,'>')

        return self.choice(cat, page)

    def choice(self, cat, page):
        while True:
            action = input('» ')
            if action in 'qanbh':
                # Check if there is data in the selection
                data = len(cat) // 10
                if action.lower() == 'h':
                    self.display_help()
                elif action.lower() == 'a':
                    self.main()
                elif action.lower() == 'q':
                    sys.exit(0)
                elif page is not None:
                    if action.lower() in 'nb':
                        if action.lower() == 'n':
                            if 1 <= page and data == 1:
                                page += 1
                                return action, page
                            else:
                                print("Pas de page suivante!")
                        if action.lower() == 'b':
                            if 1 < page:
                                page -= 1
                                return action, page
                            else:
                                print("Pas de page précédente")
            elif 'i' in action and len(action) == 2:
                choice = ()
                for ind, letter in enumerate(action, start=1):
                    if ind == 1 and letter == 'i':
                        choice += (letter, )
                    elif ind == 2:
                        try:
                            letter = int(letter)
                            choice += (letter, )
                        except ValueError:
                            msg = 'Veuillez renseigner un chiffre'
                            msg += 'après la lettre i'
                            print(msg)
                    else:
                        msg = 'Mauvais choix, utilisez la syntaxe suivante: '
                        msg += 'i + chiffre'
                        print(msg)
                return choice, page
            else:
                try:
                    action = int(action)
                    if 0 <= action <= len(cat) - 1:
                        return action, page
                    else:
                        print("Valeur inexistante.")
                except ValueError:
                    error_msg = "Mauvais choix ! "
                    error_msg += "Rééssayez ou tapez h pour de l'aide"
                    print(error_msg)

    def display_info(self, id_prod, prod, subcat):
        print('---------------------------------------------')
        print(prod.center(45))
        print('---------------------------------------------')
        info = self._data.select_information_products(id_prod, prod, subcat)

        for val in info:
            quantity = val.quantity
            packaging = val.packaging
            origin = val.origin
            allergens = val.allergens
            traces = val.traces
            additives_n = val.additives_number
            additives = val.additives

            if quantity != 'nan':
                print(' Quantity = ', quantity)
            if packaging != 'nan':
                print(' Packaging = ', packaging)
            if origin != 'nan':
                print(' Origin = ', origin)
            if allergens != 'nan':
                print(' Allergens = ', allergens)
            if additives_n != '0.0':
                print(" Nombre d'additifs = ", additives_n)
            if additives != 'nan':
                additives = additives.split(',')
                for num, additive in enumerate(additives):
                    if num == 0:
                        print(' Additives = ', additives[num])
                    else:
                        print('             ', additives[num])

            if traces != 'nan':
                print(' Traces = ', traces)

    def homepage(self):
        print('#############################################')
        print('#                Bienvenue !                #')
        print('#############################################')
        print('')
        print(' Que souhaitez vous faire ?')
        print(' 1 - Subsituez un produit ')
        print(' 2 - Retrouver mes aliments substitués ?')
        print(' 3 - Mettre à jour la base de donnée ?')

        no_action = True
        while no_action:
            action = input('» ')
            if action in '123hq':
                if action.lower() == 'h':
                    self.display_help()
                elif action.lower() == 'q':
                    sys.exit(0)
                elif action in '123':
                    try:
                        action = int(action)
                    except ValueError:
                        msg = "Mauvais choix ! Rééssayez ou tapez h"
                        msg += " pour de l'aide"
                        print(msg)
                return action

    def main(self):

        action = self.homepage()

        if action == 1:
            self.display_category_list()
            self.display_subcategory_list()
            self.display_product_list()
            self.display_substitute_list()

            chosen_sub = self._user.chosen_substitute
            chosen_prod = self._user.chosen_product
            self._data.add_substitute(chosen_sub, chosen_prod)

            msg = "Produits substitué !\n Appuyez sur n'importe quelle touche"
            msg += " pour retournez à la page d'accueil ou q pour quitter"
            choice = input(msg)

            if choice == "q":
                sys.exit(0)
            else:
                # Reset UserChoice and display the homepage
                self._user.__init__()
                self.main()

        elif action == 2:
            choice, page = self.display_product_and_substitute()
            if isinstance(choice, str):
                if choice.lower() == 'n' or choice.lower() == 'b':
                    self.display_product_and_substitute(page)
                else:
                    print()
        elif action == 3:
            success = self._data.update_database()
            if success is False:
                print('Echec de la mise à jour.')
            else:
                print('Mise à jour réussi.')
            self.main()


inter = Interface()
inter.main()
