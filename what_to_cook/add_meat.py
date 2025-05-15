def meat():
    meat_choice = input("Do want to add meat to this meal?").lower()
    if meat_choice == "yes":
        meat = input("What meat do would you like to add?\nChicken\nBeef\nLamb\nFish").lower()
        meat_choices = ["chicken", "beef", "lamb", "fish"]
        if meat not in meat_choices:
            print("Sorry this is not a valid option. Please select a meat from the list.")
    elif meat_choice == "no":
        return None
    else:
        print("Sorry this is an invalid input. Please input Yes or No.")
    return meat

def carbs():
    carb_choice = input("Do want to a carb to this meal?").lower()
    if carb_choice == "yes":
        carb = input("What carb do would you like to add?\nRice\nPasta\nNoodles\nDumplings\nBread\nPotato\nSweet Potato\nRoti").lower()
        carb_choices = ["rice", "pasta", "noodles", "dumplings", "bread", "potato", "sweet potato", "roti"]
        if carb not in carb_choices:
            print("Sorry this is not a valid input. Please select a carb form the list.")
    elif carb_choice == "no":
        return None
    else:
        print("Sorry this is an invalid input. Please try again.")
    return carb

def veg():
    veg_choice = input("Do want vegetables in this meal?").lower()
    if veg_choice == "yes":
        return True
    elif veg_choice == "no":
        return None
    else:
        print("Sorry this is an invalid input. Please try again.")

def legume():
    legume_choice = input("Do want to a carb to this meal?").lower()
    if legume_choice == "yes":
        legume = input("What carb do would you like to add?\nLentils\nKindey Beans\nPinto Beans\nGreen Peas\nChanna\nDhal\nPigeon Peas").lower()
        legume_choices = ["lentils", "kindey beans", "pinto beans", "green peas", "channa", "Dhal", "pigeon peas"]
        if legume not in legume_choices:
            print("Sorry this is not a valid input. Please select a legume form the list.")
    elif legume_choice == "no":
        return None
    else:
        print("Sorry this is an invalid input. Please try again.")
    return legume
    

def sauce():
    pass