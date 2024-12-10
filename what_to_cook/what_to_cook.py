import random


print(

    '''

                                                        _--"-.
                                            .-"      "-.
                                            |""--..      '-.
                                            |      ""--..   '-.
                                            |.-. .-".    ""--..".
                                            |'./  -_'  .-.      |
                                            |      .-. '.-'   .-'
                                            '--..  '.'    .-  -.
                                                ""--..   '_'   :
                                                    ""--..   |
                                                            ""-' 
                 
                 
  _____                 _                   __  __            _    _____                           _             
 |  __ \               | |                 |  \/  |          | |  / ____|                         | |            
 | |__) |__ _ _ __   __| | ___  _ __ ___   | \  / | ___  __ _| | | |  __  ___ _ __   ___ _ __ __ _| |_ ___  _ __ 
 |  _  // _` | '_ \ / _` |/ _ \| '_ ` _ \  | |\/| |/ _ \/ _` | | | | |_ |/ _ \ '_ \ / _ \ '__/ _` | __/ _ \| '__|
 | | \ \ (_| | | | | (_| | (_) | | | | | | | |  | |  __/ (_| | | | |__| |  __/ | | |  __/ | | (_| | || (_) | |   
 |_|  \_\__,_|_| |_|\__,_|\___/|_| |_| |_| |_|  |_|\___|\__,_|_|  \_____|\___|_| |_|\___|_|  \__,_|\__\___/|_|   
                                                                                                                 
                                                                                                                 
                                        Welcome to the Random Meal Generator!'''
)


input_check = True

while input_check is True:
    try:
        action = int(input("What would you like to do today?\n1. Choose a random meal to prepare.\n2. Add a meal to the meal repository.\n3. See the meal repository.\n4. Remove a meal\n5. Exit.\n"))
        if action >= 1 and action <= 5:
            if action == 1:
                with open("./meal_list.txt", "r") as file:
                    content = file.read()
                split_content = content.split("\n")
                for item in split_content:
                    if "" in split_content:
                        split_content.remove("")
                meal_choice_check = True
                while meal_choice_check is True:
                    randomly_chosen_meal = random.choice(split_content)
                    if randomly_chosen_meal == "\n" or randomly_chosen_meal == "\n":
                        continue
                    else:
                        print(f"\nToday's meal to cook is {randomly_chosen_meal}!\n")
                        try:
                            meal_acceptance = input("Are you happy with your choice? (Yes/No)\n").lower()
                            if meal_acceptance == "yes":
                                meal_choice_check = False
                            elif meal_acceptance == "no":
                                choose_meal_again = input("\nWould you like to choose another meal? (Yes/No)\n").lower()
                                if choose_meal_again == "yes":
                                    ("\nChoosing next meal....\n")
                                elif choose_meal_again == "no":
                                    meal_choice_check = False
                            else:
                                print("\nThis is an invalid choice. Please answer Yes or No.\n")
                        except Exception as e:
                            if e == AttributeError:
                                print("\nThis input is invalid. Please answer Yes or No.\n")
                            else:
                                print(e)
            elif action == 2:
                meal_to_add = input("What meal would you like to add?\n")
                with open("./meal_list.txt", "a+") as file:
                    file.write("\n" + meal_to_add)
                    new_meal_list = file.read()
                    print("This is the new meal list.")
                    print(new_meal_list)
                print(f"{meal_to_add} has been added to the list. The new meal list is...\n")
                with open("./meal_list.txt", "r") as file:
                    meals = file.read()
                    print(meals + "\n")
            elif action == 3:
                with open("./meal_list.txt", "r") as file:
                    meal_list = file.read()
                print(f"{meal_list}\n")
            elif action == 4:
                meal_to_be_removed = input("What meal do you want to remove?\n")
                with open("./meal_list.txt", "r") as file:
                    loaded_meal_list = file.read()
                if meal_to_be_removed not in loaded_meal_list:
                    print("Sorry this meal is not in the meal list.")
                else:
                    with open("./meal_list.txt", "r") as files:
                        lines = files.readlines()
                        for line in lines:
                            if meal_to_be_removed in line:
                                lines.remove(line)
                                print(f"{meal_to_be_removed} has been deleted from the meal list.")
                    with open("./meal_list.txt", "w+") as file1:
                        for meal in lines:
                            file1.write(meal)
                    with open("./meal_list.txt", "r") as file2:
                        new_meal_list_after_deletion = file2.read()
                    print(f"\nYour new meal list is...\n{new_meal_list_after_deletion}")
            else:
                input_check = False
                print("\nHave a great day and Happy Cooking!\n")
        else:
            print(f"\n{action} is an invalid input. Please choose a number from the list above.\n")
    except Exception as e:
        if e == ValueError:
            print(f"\nThis is an invalid input. Please input a number form the list above to continue.\n")
        else:
            print(e)
            print(f"\nThis is an invalid input. Please try again.\n")

