from textual_summary import summary

def collatz_algorithm(starting_number: int) -> int|list:

    """Implements the collatz conjecture algorithm
    Args: 
        starting_number: the number that the algoritm starts with
    Returns:
        number_of_steps: number of steps taken by the algorithm to get to the last hailstone number
        list_of_hailstone_numbers: a list of all the hailstone numbers produced by the algorithm
        final_hailstone_number: the final hailstone number produced by the algorithm (1, -1, -5 or -17 if the collatz conjecture remains unproven)
        starting_number: the starting number used by the algorithm
    """

    hailstone_number = starting_number
    number_of_steps = 0
    list_of_hailstone_numbers = []
    infinite_loop = False

    try:
        if hailstone_number > 0:
            while hailstone_number != 1:
                number_of_steps += 1
                if hailstone_number % 2 == 0:
                    hailstone_number /= 2
                else:
                    hailstone_number = (hailstone_number * 3) + 1
                list_of_hailstone_numbers.append(hailstone_number)
        elif hailstone_number < 0:
            while infinite_loop is False:
                number_of_steps += 1
                if hailstone_number % 2 == 0:
                    hailstone_number /= 2
                    # print(hailstone_number)
                    if hailstone_number == -10 or hailstone_number == -2 or hailstone_number == -34:
                        infinite_loop = True
                else:
                    hailstone_number = (hailstone_number * 3) + 1
                    # print(hailstone_number)
                    if hailstone_number == -10 or hailstone_number == -2 or hailstone_number == -34:
                        infinite_loop = True
                list_of_hailstone_numbers.append(hailstone_number)
        else:
            print("The starting number needs to be either more than or less than 0")
    except Exception as e:
        print(f"The following error has occurred: \n {e}")
    
    final_hailstone_number = hailstone_number

    return number_of_steps, list_of_hailstone_numbers, final_hailstone_number, starting_number

if __name__ == "__main__":
    summary(collatz_algorithm(-1))