#! /usr/bin/env python3
# coding: utf-8
import sys

from data_management import UserChoice, Data


class Interface:
    """ Main class connecting data with the user.
    """

    def __init__(self):
        self._user = UserChoice()
        self._data = Data()

    def display_category_list(self):
        cat = self._data.select_categories()
        choice_category, new_page = self.choice('Catégories', cat)
        self._user.choose_category(choice_category, cat)

    def display_subcategory_list(self, page=1):
        cat = self._user.chosen_category
        id_subs, subcats = self._data.select_subcategories(cat, page)
        choice, new_page = self.choice('Sous-Catégories', subcats, page)

        if new_page != page:
            self.display_subcategory_list(new_page)
        else:
            self._user.chosen_subcategory = id_subs[choice]

    def display_product_list(self, page=1):
        subcategory = self._user.chosen_subcategory
        id_products, products = self._data.select_products(subcategory, page)
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
                        self._user.chosen_product = id_prod
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
                elif action.lower() == 'o':                    self._user.chosen_substitute = id_sub
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
        prod_id, repl_sub_id, prod_and_subs = self._data.select_product_and_substitute(page)
        title = 'Produits substitués'
        choice, new_page = self.choice(title, prod_and_subs, page)
        if page != new_page:
            self.display_product_and_substitute(new_page)
        elif isinstance(choice, tuple):
            if choice[0] == 'i':
                id_subst = repl_sub_id[choice[1]]
                id_prod = prod_id[choice[1]]
                self.display_info(id_subst)

                no_action = True
                while no_action:
                    action = input('Remplacer ce produit ? (O/N) : ')
                    if action.lower() == 'n':
                        self.display_product_and_substitute(page)
                        no_action = False
                    elif action.lower() == 'o':
                        self._user.chosen_product = id_prod
                        self.replace_sub(id_prod)
                        return id_prod
                        no_action = False
                    else:
                        print('O ou N sont les deux choix possibles.')

    def replace_sub(self, id_subst):
        self._user.chosen_subcategory = self._data.select_subcategory(id_subst)


    def display_help(self):
        print(' - Utiliser les chiffres de votre clavier pour faire un choix.')
        print(" - A pour revenir à la page d'accueil.")
        print(" - N pour aller à la page suivante.")
        print(" - B pour aller à la page précédente.")
        print(" - I espacé d'un chiffre pour afficher des informations d'un produit.")
        print(" - Utilisez Q pour quitter le programme.")


    def choice(self, title, cat, page=1):
        """
        :param title: title to display
        :param cat: list to display
        :param page: page to display (int)
        :return: choice allowed char or tuple (i + digit) or int
                 page (int)
        """
        self.print_n_times(60, '#')
        print(title.center(60))
        self.print_n_times(60, '#')
        print()

        self._unpack_data(title, cat, page)

        # Check title to allow to display info about a product
        is_prod = False
        title_allowed = 'Produits de substitution,'
        title_allowed += 'Produits,'
        title_allowed += 'Produits substitués'
        if title in title_allowed.split(','):
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
                            msg += ' après la lettre i.'
                            print(msg)
                    else:
                        msg = " Le format doit être i + espace + chiffre"
                        print(msg)
                else:
                    try:
                        action = int(action)
                        if 0 <= action <= len(cat) - 1:
                            return action, page
                        else:
                            print("Valeur inexistante !")
                    except ValueError:
                        err_msg = "Mauvais choix ! "
                        err_msg += "Rééssayez ou tapez H pour afficher l'aide"
                        print(err_msg)
            except IndexError:
                print('Saisie obligatoire !')

    def _unpack_data(self, title, cat, page):
        """
        :param title: title to display
        :param cat: list to unpack
        :param page: page to select data
        """
        if title == 'Produits substitués':
            for key, val in enumerate(cat):
                print(key, " Produit original = ", val[1])
                print('   Produit de substitution = ', val[0])
                print()
            print()
            print('                     <', page, '>')
        elif title == 'Produits de substitution':
            for key, val in enumerate(cat):
                prod_name = val.product_name
                brand = val.brand
                url = val.url_text
                nutriscore = val.nutrition_score

                print(' - ', key,  prod_name)
                print("      Marque =", brand)
                print("      Site   =", url)
                print("      Nutriscore =", nutriscore.upper())
                print()
            print()
            print('                     <', page, '>')
        else:
            for ind, value in enumerate(cat):
                print(ind, value)
            print()
            print('                     <', page, '>')

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
                print(' Quantitée = ', quantity)
            if packaging != 'nan':
                print(' Packaging = ', packaging)
            if origin != 'nan':
                print(' Origine = ', origin)
            if allergens != 'nan':
                print(' Allergènes = ', allergens)
            if additives_n != '0.0':
                print(" Nombre d'additifs = ", additives_n)
            if additives != 'nan':
                additives = additives.split(',')
                for num, additive in enumerate(additives):
                    if num == 0:
                        print(' Additifs = ', additives[num])
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
        print(' 1 - Subsituer un produit.')
        print(' 2 - Retrouver mes aliments substitués.')
        print(' 3 - Mettre à jour la base de données.')

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
                        no_action = False
                    except ValueError:
                        msg = " Mauvais choix ! Rééssayez ou tapez H"
                        msg += " afficher l'aide."
                        print(msg)
                return action

    def print_n_times(self, n, char):
        for _ in range(0, n):
            print(char, end="")
        print()

    def main(self):
        """ Main function  """

        action = self.homepage()

        if action == 1:
            self.display_category_list()
            self.display_subcategory_list()
            self.display_product_list()
            self.display_substitute_list()
            chosen_prod = self._user.chosen_product
            chosen_sub = self._user.chosen_substitute
            self._data.add_substitute(chosen_prod, chosen_sub)

            msg = " Produit substitué !\n Appuyez sur n'importe quelle touche"
            msg += " pour retournez à la page d'accueil ou Q pour quitter !"
            choice = input(msg + ' ')

            if choice == "q":
                sys.exit(0)
            else:
                # Reset UserChoice and display the homepage
                self._user.__init__()
                self.main()

        elif action == 2:
            prod = self.display_product_and_substitute()
            self.display_substitute_list()
            old_sub = self._user.chosen_product
            new_sub = self._user.chosen_substitute
            self._data.change_substitute(prod, old_sub, new_sub)

            msg = " Produit substitué !\n Appuyez sur n'importe quelle touche"
            msg += " pour retournez à la page d'accueil ou Q pour quitter !"
            choice = input(msg + ' ')

            if choice == "q":
                sys.exit(0)
            else:
                # Reset UserChoice and display the homepage
                self._user.__init__()
                self.main()

        elif action == 3:
            self._data.update_database()
            print('Mise à jour réussie.')
            self.main()


if __name__ == '__main__':
    i = Interface()
    i.main()
