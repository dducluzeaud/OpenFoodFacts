#!/usr/local/bin/python3
# coding: utf-8
import sys

from data_management import UserChoice, Data


class Interface:

    def __init__(self):
        self._user = UserChoice()
        self._data = Data()

    def display_category_list(self, page=1):
        cat = self._data.select_categories()
        choice_category, new_page = self.choice('Categories', cat)
        self._user.choose_category(choice_category, cat)

    def display_subcategory_list(self, page=1, msg=None):
        if msg is not None:
            print(msg)

        cat = self._user.chosen_category
        id_subs, subcats = self._data.select_subcategories(cat, page)
        choice, new_page = self.choice('Sous-Categories', subcats, page)

        if new_page != page:
            self.display_subcategory_list(new_page)
        else:
            id_sub = id_subs[choice]
            self._user.chosen_subcategory = id_subs[choice]

    def display_product_list(self, page=1):
        subcategory = self._user.chosen_subcategory
        id_products, products = self._data.select_products(subcategory, page)
        if len(products) == 1:
            return 1
        else:
            choice, new_page = self.choice('Produits', products, page)
            if page != new_page:
                self.display_product_list(new_page)
            elif isinstance(choice, tuple):
                if choice[0] == 'i':
                    id_prod = id_products[choice[1]]
                    self.display_info(id_prod)

                    no_action = True
                    while no_action:
                        action = input('Confirmer ce produit? (O/N) : ')
                        if action.lower() == 'n':
                            self.display_product_list(page)
                            no_action = False
                        elif action.lower() == 'o':
                            self._user.chosen_product = id_products[choice[1]]
                            no_action = False
                        else:
                            print('O ou N sont les deux choix possibles.')
            else:
                self._user.chosen_product = id_products[choice]


    def display_substitute_list(self, page=1):
        subcat = self._user.chosen_subcategory
        prod_name = self._user.chosen_product
        id_subs, subs = self._data.select_substitutes(subcat, prod_name, page)
        choice, new_page = self.display_subsitutes(subs, page)
        if page != new_page:
            self.display_substitute_list(new_page)
        elif isinstance(choice, tuple):
            if choice[0] == 'i':
                id_sub = id_subs[choice[1]]
                self.display_info(id_sub)

            no_action = True
            while no_action:
                action = input('Confirmer ce produit? (O/N) : ')
                if action.lower() == 'n':
                    self.display_substitute_list(page)
                elif action.lower() == 'o':
                    self._user.chosen_substitue = id_subs[choice[1]]
                    no_action = False
                else:
                    print('O ou N sont les deus choix possibles.')
        else:
            id_subst = id_subs[choice]
            self._user.chosen_substitute = id_subst

    def display_subsitutes(self, substitutes, page=1):
        table = 'Produits de substitution'
        return self.choice(table, substitutes, page)

    def display_product_and_substitute(self, page=1):
        prod_and_subs = self._data.select_product_and_substitute(page)
        title = 'Produits substitués'
        choice, new_page = self.choice(title, prod_and_subs, page)
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
        print(" - I espacé d'un chiffre pour afficher des informations.")
        print(" - Utilisez Q pour quitter le programme.")


    def choice(self, title, cat, page=1):
        self.print_n_times(60, '#')
        print(title.center(60))
        self.print_n_times(60, '#')
        print()

        if title == 'Produits substitués':
            for key, val in enumerate(cat):
                print(key, " produit original = ", val[1])
                print('   produit de substitution = ', val[0])
                print()
            print()
            print('                     <', page, '>')
        elif title == 'Produits de substitution':
            for key, val in enumerate(cat):
                prod_name = val.product_name
                brand = val.brand
                url = val.url_text

                print(' - ', key,  prod_name)
                print("       Marque =", brand)
                print("       Site   =", url)
                print()
            print()
            print('                     <', page, '>')
        else:
            for ind, value in enumerate(cat):
                print(ind, value)
            print()
            print('                     <', page, '>')

        is_prod = False
        if title == 'Produits de substitution' or title == 'Produits':
            is_prod = True

        while True:
            try:
                action = input('» ')
                allowed_actions = 'q a n b h'.lower().split()
                if action in allowed_actions:
                    # Check if there is data in the selection
                    data = len(cat) // 10
                    if action == 'h':
                        self.display_help()
                    elif action == 'a':
                        self.main()
                    elif action == 'q':
                        sys.exit(0)
                    elif page is not None:
                        if action == 'n':
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
                elif action.split()[0] == 'i' and is_prod:
                    if len(action.split()) == 2:
                        try:
                            number = action.split()[1]
                            number = int(number)

                            if number >len(cat):
                                msg = "Le chiffre ne correspond pas "
                                msg += "aux chiffres des produits affichés"
                                print(msg)
                            else:
                                return (action.split()[0], number, ), page

                        except ValueError:
                            msg = 'Veuillez renseigner un chiffre'
                            msg += ' après la lettre i'
                            print(msg)
                    else:
                        msg = " Le format doit être i + chiffre"
                        print(msg)
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
            except IndexError:
                print('Saisie obligatoire')

    def display_info(self, id_prod):

        info = self._data.select_information_products(id_prod)

        for val in info:
            prod_name = val.product_name
            quantity = val.quantity
            packaging = val.packaging
            origin = val.origin
            allergens = val.allergens
            traces = val.traces
            additives_n = val.additives_number
            additives = val.additives

            self.print_n_times(60, '-')
            print(prod_name.center(60))
            self.print_n_times(60, '-')

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
        self.print_n_times(60, '#')
        print('Bienvenue !'.center(60))
        self.print_n_times(60, '#')
        print('')
        print(' Que souhaitez vous faire ?')
        print(' 1 - Subsituez un produit ')
        print(' 2 - Retrouver mes aliments substitués ?')
        print(' 3 - Mettre à jour la base de donnée ?')

        no_action = True
        while no_action:
            action = input('» ')
            allowed_actions = '1 2 3 h q'.lower().split()
            if action in allowed_actions:
                if action == 'h':
                    self.display_help()
                elif action == 'q':
                    sys.exit(0)
                else:
                    try:
                        action = int(action)
                    except ValueError:
                        msg = " Mauvais choix ! Rééssayez ou tapez h"
                        msg += " pour de l'aide"
                        print(msg)
                return action

    def print_n_times(self, n, char):
        for _ in range(0, n):
            print(char, end="")
        print()

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
                    msg = "Un seul produit pour la sous-catégories choisie"
                    self.display_subcategory_list(msg=msg)
                else:
                    product_alone = False

            self.display_substitute_list()


            chosen_prod = self._user.chosen_product
            chosen_sub = self._user.chosen_substitute
            self._data.add_substitute(chosen_prod, chosen_sub)

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
            self._data.update_database()
            print('Mise à jour réussi.')
            self.main()

if __name__ == '__main__':
    i = Interface()
    i.main()
