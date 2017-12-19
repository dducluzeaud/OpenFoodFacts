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
        if isinstance(choice_category, int) and choice_category <= 9:
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
            return 1, page
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
        choice, page = self.display_subsitutes(substits, page)

        if isinstance(choice, str):
            if choice.lower() == 'n' or choice.lower() == 'b':
                self.display_substitute_list(page)
        elif isinstance(choice, int):
            self._user.choose_substitute(choice, substits)
        elif isinstance(choice, tuple):
            prod = choice[1]

            product = ""
            id_prod = 0
            for indice, subs in enumerate(substits):
                if prod == indice:
                    product = subs.product_name
                    id_prod = subs.id_product
                    break
            self.display_info(id_prod, product, subcat)

            no_action = True
            while no_action:
                action = input('Confirmer ce produit? (O/N) : ')
                if action.lower() == 'n':
                    self.display_substitute_list(page)
                elif action.lower() == 'o':
                    self._user.choose_substitute(prod, substits)
                    no_action = False
                else:
                    print('O ou N sont les deus choix possibles.')
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

        choice, page = self.choice(prod_and_subs, page)
        if isinstance(choice, str):
            if choice.lower() == 'n' or choice.lower() == 'b':
                self.display_product_and_substitute(page)
        else:
            print('Mauvais choix')
            self.display_substitute_list(page)

    def display_help(self):
        print(' - Utiliser les chiffres de votre clavier pour faire un choix.')
        print(" - A pour revenir à la page d'accueil.")
        print(" - N pour aller à la page suivante.")
        print(" - B pour aller à la page précédente.")
        print(" - I + chiffre pour afficher des informations sur le produit.")
        print(" - Utilisez Q pour quitter le programme.")

    def display_form(self, table, cat, page=1):
        print('#############################################')
        print(table.center(45))
        print('#############################################')
        print()
        for ind, value in enumerate(cat):
            print(ind, value)
        print()
        print('                     <', page, '>')

        return self.choice(cat, page)

    def choice(self, cat, page):
        while True:
            action = input('» ')
            if action in 'q Q a A n N b B h H'.split():
                # Check if there is data in the selection
                data = len(cat) // 10
                if action.lower() == 'h':
                    self.display_help()
                elif action.lower() == 'a':
                    self.main()
                elif action.lower() == 'q':
                    sys.exit(0)
                elif page is not None:
                    if action.lower() == 'n':
                        if 1 <= page and data != 0:
                            page += 1
                            return action, page
                        else:
                            print("Pas de page suivante!")
                    if action.lower() == 'b':
                        if 1 < page:
                            page -= 1
                            print(action, page)
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
                        msg = '  Mauvais choix, utilisez la syntaxe suivante: '
                        msg += 'i + chiffre'
                        print(msg)
                return choice, page
            elif '0 1 2 3 4 5 6 7 8 9'.split():
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
            if action in '1 2 3 H h Q q'.split():
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

            product_alone = True
            while product_alone:
                product_n = self.display_product_list()
                if product_n == 1:
                    subcat = self._user.chosen_subcategory
                    print("Un seul produit pour la sous-catégorie: ", subcat)
                    self.display_subcategory_list()
                else:
                    product_alone = False

            self.display_substitute_list()

            chosen_sub = self._user.chosen_substitute
            chosen_prod = self._user.chosen_product
            self._data.add_substitute(chosen_sub, chosen_prod)

            msg = " Produits substitué !\n Appuyez sur n'importe quelle touche"
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
