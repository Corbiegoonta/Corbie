def summary(result):

    """Provides textual summary for the results of the collatz_algorithm function
    Args: 
        result: the tuple returned by the collatz_algorithm function
    """
    
    number_of_steps = result[0]
    list_of_hailstone_numbers = result[1]
    starting_number = result[3]

    print(f"With a starting number of {starting_number}, the Collatz Conjecture iterated through {number_of_steps} steps producing the following hailstone numbers: \n {list_of_hailstone_numbers}")