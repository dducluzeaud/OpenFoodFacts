from Interface import UserChoice, Data

class Interface():

    def __init__(self):
        self.user = UserChoice()
        self.data = Data()

    def display(self, item):
        number = 0
        selection = ""
        if item == 'category':
            categories = self.data.select_categories()
            number = self.display_form(item, categories)
            selection = self.user.choose_category(number)
        elif item == 'subcategory':
            category = self.user.chosen_category
            subcategories = self.data.select_subcategories(category)
            number = self.display_form(item, subcategories)
            selection = self.user.choose_subcategory(number)
        elif item == 'produit':
            subcategory = self.user.chosen_subcategory
            produit = self.data.select_products(subcategory)
            number = self.display_form(item, produit)
            selection = self.user.choose_product(number)
        elif item == 'substitute':
            subcategory = self.user.chosen_subcategory
            product_name = self.user.chosen_product
            substitute = self.data.select_substitutes(subcategory, product_name)
            number = self.display_form(item, substitute)
            selection = self.user.choose_substitute(number)
        return selection

    def display_form(self, table, index):
        print('#########################')
        print('#      ', table, '      #')
        print('#########################')
        print()

        action = 0
        if table == 'substitue':
            for key, value in index.items():
                print(value)
        else:
            for key, value in index.items():
                print(key, value)


        action = int(input())
        return action

        

    def homepage(self):
        display_homepage = True

        print('#########################')
        print('#        Bienveue !     #')
        print('#########################')
        print(' Que souhaitez vous faire ?')
        print(' 1 - Subsituez un produit ')
        print(' 2 - Consultez la liste des produits substitués ?')

        while display_homepage:
            try:
                number = int(input())
                if number == 1:
                    display_homepage = False
                    return 'category'
                elif number == 2:
                    display_homepage = False
                    return 'substitute'
                elif number == 'q':
                    print('Fin du programme ! Au revoir. ')
                    display_homepage = False
                else:
                    print('Tapez 1 ou 2 pour faire un choix.')
            except ValueError:
                print('Vous devez saisir un chiffre')

    def main(self):
        selection = ""
        action = self.homepage()
        if action == 'category':
            self.display(action)
            self.display('subcategory')
            self.display('produit')
            self.display('substitute')






inter = Interface()
inter.main()
