import azure.functions as func
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="corbfunc")
def corbfunc(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req.params.get('name')

    starting_number = 10
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
    

    return func.HttpResponse(
            f"With a starting number of {starting_number}, the Collatz Conjecture iterated through {number_of_steps} steps producing the following hailstone numbers: \n {list_of_hailstone_numbers}",
            status_code=200
        )