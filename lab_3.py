def get_valid_input(input_string, valid_options):
    '''Get the input until the answer is correct and listed
    in the options.'''
    input_string += " ({}) ".format(", ".join(valid_options))
    response = input(input_string)
    while response.lower() not in valid_options:
        response = input(input_string)
    return response


class Property:
    # Class that describes property
    def __init__(self, square_feet='', beds='',baths='', **kwargs):
        super().__init__(**kwargs)
        self.square_feet = square_feet
        self.num_bedrooms = beds
        self.num_baths = baths

    def display(self):
        # Prints information about a certain property
        print("PROPERTY DETAILS")
        print("================")
        print("square footage: {}".format(self.square_feet))
        print("bedrooms: {}".format(self.num_bedrooms))
        print("bathrooms: {}".format(self.num_baths))
        print()

    def prompt_init():
        # Creates a dictionary of values that can be passed into init
        return dict(square_feet=input("Enter the square feet: "),
                    beds=input("Enter number of bedrooms: "),
                    baths=input("Enter number of baths: "))
    prompt_init = staticmethod(prompt_init)


class Apartment(Property):
    # Extends property, a class for apartments.
    valid_laundries = ("coin", "ensuite", "none")
    valid_balconies = ("yes", "no", "solarium")

    def __init__(self, balcony='', laundry='', **kwargs):
        super().__init__(**kwargs)
        self.balcony = balcony
        self.laundry = laundry

    def display(self):
        # Print information about apartment and update on laundry and balcony
        super().display()
        print("APARTMENT DETAILS")
        print("laundry: %s" % self.laundry)
        print("has balcony: %s" % self.balcony)
        parent_init = Property.prompt_init()
        laundry = ''
        while laundry.lower() not in Apartment.valid_laundries:
            laundry = input("What laundry facilities does "
                             "the property have? ({})".format(
                            ", ".join(Apartment.valid_laundries)))
        balcony = ''
        while balcony.lower() not in Apartment.valid_balconies:
            balcony = input("Does the property have a balcony? "
                "({})".format(", ".join(Apartment.valid_balconies)))
        parent_init.update({
                "laundry": laundry,
                "balcony": balcony
        })
        return parent_init

    def prompt_init():
        # Getting values from parent class (Property) and adding some new ones.
        parent_init = Property.prompt_init()
        laundry = get_valid_input("What laundry facilities does "
        "the property have? ", Apartment.valid_laundries)
        balcony = get_valid_input("Does the property have a balcony? ",
            Apartment.valid_balconies)
        parent_init.update({
            "laundry": laundry,
            "balcony": balcony
        })
        return parent_init
    prompt_init = staticmethod(prompt_init)


class House(Property):
    # Extends property, a class for houses.
    valid_garage = ("attached", "detached", "none")
    valid_fenced = ("yes", "no")

    def __init__(self, num_stories='',
                 garage='', fenced='', **kwargs):
        super().__init__(**kwargs)
        self.garage = garage
        self.fenced = fenced
        self.num_stories = num_stories

    def display(self):
        # Print information about a house
        super().display()
        print("HOUSE DETAILS")
        print("# of stories: {}".format(self.num_stories))
        print("garage: {}".format(self.garage))
        print("fenced yard: {}".format(self.fenced))

    def prompt_init():
        # Getting values from parent class (Property) and adding some new ones.
        parent_init = Property.prompt_init()
        fenced = get_valid_input("Is the yard fenced? ",
                                 House.valid_fenced)
        garage = get_valid_input("Is there a garage? ",
                                 House.valid_garage)
        num_stories = input("How many stories? ")
        parent_init.update({
            "fenced": fenced,
            "garage": garage,
            "num_stories": num_stories
        })
        return parent_init
    prompt_init = staticmethod(prompt_init)


class Purchase:
    # Class for property that can be bought
    def __init__(self, price='', taxes='', **kwargs):
        super().__init__(**kwargs)
        self.price = price
        self.taxes = taxes

    def display(self):
        # Prints information about a purchase
        super().display()
        print("PURCHASE DETAILS")
        print("selling price: {}".format(self.price))
        print("estimated taxes: {}".format(self.taxes))

    def prompt_init():
        # Gets information about price and taxes of a property
        return dict(
            price=input("What is the selling price? "),
            taxes=input("What are the estimated taxes? "))
    prompt_init = staticmethod(prompt_init)


class Rental:
    # Class for property, that can be rented
    def __init__(self, furnished='', utilities='',
                 rent='', **kwargs):
        super().__init__(**kwargs)
        self.furnished = furnished
        self.rent = rent
        self.utilities = utilities

    def display(self):
        # Print information about rent
        super().display()
        print("RENTAL DETAILS")
        print("rent: {}".format(self.rent))
        print("estimated utilities: {}".format(
            self.utilities))
        print("furnished: {}".format(self.furnished))

    def prompt_init():
        # Gets information about rent and property for rent
        return dict(
            rent=input("What is the monthly rent? "),
            utilities=input(
                "What are the estimated utilities? "),
            furnished=get_valid_input(
                "Is the property furnished? ",
                ("yes", "no")))
    prompt_init = staticmethod(prompt_init)


class HouseRental(Rental, House):
    # Class for House that can be rented
    def prompt_init():
        # Get all the information updates from prompt_init in parent classes
        init = House.prompt_init()
        init.update(Rental.prompt_init())
        return init
    prompt_init = staticmethod(prompt_init)


class ApartmentRental(Rental, Apartment):
    # Class for Apartment that can be rented
    def prompt_init():
        # Get all the information updates from prompt_init in parent classes
        init = Apartment.prompt_init()
        init.update(Rental.prompt_init())
        return init
    prompt_init = staticmethod(prompt_init)


class ApartmentPurchase(Purchase, Apartment):
    # Class for Apartment that can be bought
    def prompt_init():
        # Get all the information updates from prompt_init in parent classes
        init = Apartment.prompt_init()
        init.update(Purchase.prompt_init())
        return init
    prompt_init = staticmethod(prompt_init)


class HousePurchase(Purchase, House):
    # Class for a house that can be bought
    def prompt_init():
        # Get all the information updates from prompt_init in parent classes
        init = House.prompt_init()
        init.update(Purchase.prompt_init())
        return init
    prompt_init = staticmethod(prompt_init)


class Agent:
    # Responsible for creating new listings and displaying existing ones
    def __init__(self):
        self.property_list = []

    def display_properties(self):
        # Print all the properties
        for property in self.property_list:
            property.display()

    type_map = {
        ("house", "rental"): HouseRental,
        ("house", "purchase"): HousePurchase,
        ("apartment", "rental"): ApartmentRental,
        ("apartment", "purchase"): ApartmentPurchase
    }

    def add_property(self):
        # Add a property to the list
        property_type = get_valid_input(
            "What type of property? ",
            ("house", "apartment")).lower()
        payment_type = get_valid_input(
            "What payment type? ",
            ("purchase", "rental")).lower()
        PropertyClass = self.type_map[(property_type, payment_type)]
        init_args = PropertyClass.prompt_init()
        self.property_list.append(PropertyClass(**init_args))

    def display_enumerated(self):
        # Print enumerated property
        number = 1
        for p in self.property_list:
            print('\nNUMBER ' + str(number) + '\n')
            p.display()
            number += 1

    def del_property(self):
        # Delete property from the list
        self.display_enumerated()
        try:
            i = int(input('Which property number to remove?'))
            self.property_list.pop(i - 1)
            print('REMOVAL SUCCESSFUL!')
        except (ValueError, TypeError):
            print('WRONG INPUT')

    def replace_property(self):
        # Replace property with another one (maybe update)
        self.display_enumerated()
        try:
            i = int(input('Which property number to replace?'))
            self.property_list.pop(i - 1)
            print('ENTER NEW PROPERTY')
            self.add_property()
        except (ValueError, TypeError):
            print('WRONG INPUT')

agent = Agent()
agent.add_property()
agent.add_property()
agent.replace_property()
agent.display_properties()
