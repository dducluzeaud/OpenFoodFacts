#!/usr/local/bin/python3
# coding: utf-8
import sys

from Interface import UserChoice, Data


class Interface:

    def __init__(self):
        self._user = UserChoice()
        self._data = Data()
        self._running = True

    def display_category_list(self):
        cat = self._data.select_categories()
        choice_category, page = self.display_form('Categories', cat)
        self._user.choose_category(choice_category, cat)

    def display_subcategory_list(self, page=1):
        cat = self._user.chosen_category
        subcat = self._data.select_subcategories(cat, page)
        choice, page = self.display_form('Sous-Categories', subcat, page)
        if isinstance(choice, str):
            if choice.lower() == 'n' or choice.lower() == 'b':
                self.display_subcategory_list(page)
        else:
            self._user.choose_subcategory(choice, subcat)

    def display_product_list(self, page=1):
        subcategory = self._user.chosen_subcategory
        products = self._data.select_products(subcategory, page)
        if len(products) == 1:
            print("Il n'y a qu'un seul produit pour cette sous-catégorie.")
            input("Appuyez sur une touche pour revenir à la page d'accueil.")
            self._user.__init__()
            self.main()
        else:
            choice, page = self.display_form('Produits', products, page)
            if isinstance(choice, str):
                if choice.lower() == 'n' or choice.lower() == 'b':
                    self.display_product_list(page)
            else:
                self._user.choose_product(choice, products)

    def display_substitute_list(self, page=1):
        subcat = self._user.chosen_subcategory
        prod_name = self._user.chosen_product
        substits = self._data.select_substitutes(subcat, prod_name, page)
        choice, page = self.display_subsitutes(substits)
        if isinstance(choice, str):
            if choice.lower() == 'n' or choice.lower() == 'b':
                self.display_substitute_list(page)
        else:
            self._user.choose_substitute(choice, substits)

    def display_subsitutes(self, substitutes, page=1):
        print('#########################')
        print(' Produit de substitution ')
        print('#########################')
        print()

        for key, val in enumerate(substitutes):
            prod_name, brand, url = val.product_name, val.brand, val.url_text

            print(key, ' ', prod_name)
            print("    Marque =", brand)
            print("    Site   =", url)
            print()
        print()
        print('        <',page,'>')


        return self.choice(substitutes, page)


    def display_product_and_substitute(self, page=1):
        prod_and_subs = self._data.select_product_and_substitute(page)

        print('#########################')
        print('    Poduits substitués')
        print('#########################')
        print()

        for key, value in enumerate(prod_and_subs):
            prod_name, subs = value.product_name, value.product_name_replacement
            print(key, " produit original = ", prod_name)
            print('   produit de substitution = ', subs)
            print()
        print()
        print('        <',page,'>')

    def display_help(self):
        print(' - Utiliser les chiffres de votre clavier pour faire un choix.')
        print(" - Utilisez A pour revenir à la page d'accueil.")
        print(" - Utilisez N pour aller à la page suivante lors de sélection.")
        print(" - Utilisez B pour aller à la page précédente lors de sélection.")
        print(" - Utilisez Q pour quitter le programme.")


    def display_form(self, table, cat, page=1):
        print('#########################')
        print(table.center(25))
        print('#########################')
        print()

        for ind, value in enumerate(cat):
            print(ind, value)

        print()
        print('        <',page,'>')

        return self.choice(cat, page)

    def choice(self, cat, page):

        no_action = True
        while no_action:
            action = input('» ')
            if action in 'qanbh':
                print('2')
                print(action, type(action))
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
                            if 1 <= page and data != 0:
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
            else:
                try:
                    action = int(action)
                    return action, page
                except ValueError:
                    error_msg = "Mauvais choix ! "
                    error_msg += "Rééssayez ou tapez h pour de l'aide"
                    print(error_msg)




    def homepage(self):
        print('#########################')
        print('#      Bienvenue !      #')
        print('#########################')
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
                        print("Mauvais choix ! Rééssayez ou tapez h pour de l'aide")
                return action

    def main(self):

        action = self.homepage()
        print(type(action), 'main')

        if action == 1:
            self.display_category_list()
            self.display_subcategory_list()
            self.display_product_list()
            self.display_substitute_list()

            chosen_sub = self._user.chosen_substitute
            chosen_prod = self._user.chosen_product
            self._data.add_substitute(chosen_sub, chosen_prod)

            msg = "Produits substitué ! \n Appuyez sur n'importe quelle touche"
            msg += " pour retournez à la page d'accueil ou q pour quitter"
            choice = input(msg)

            if choice == "q":
                sys.exit(0)
            else:
                # Reset UserChoice and display the homepage
                self._user.__init__()
                self.main()

        elif action == 2:
            self.display_product_and_substitute()
            msg = "Appuyez sur n'importe quelle touche"
            msg += " pour retournez à la page d'accueil ou q pour quitter"
            choice = input(msg)

            if choice == "q":
                sys.exit(0)
            else:
                # Reset UserChoice and display the homepage
                self._user.__init__()
                self.main()
        elif action == 3:
            success = self._data.update_database()
            if success == False:
                print('Echec de la mise à jour.')
            else:
                print('Mise à jour réussi.')
            self.main()


inter = Interface()
inter.main()
