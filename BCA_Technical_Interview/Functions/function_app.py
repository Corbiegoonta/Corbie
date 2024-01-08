import azure.functions as func
import logging
from collatz_conjecture import collatz_algorithm

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="big_trig")
def big_trig(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    name = req.params.get('name')

    try: 
        start = req.params.get('start')
        starting_number = int(start)
        results = collatz_algorithm(starting_number)
        number_of_steps = results[0]
        list_of_hailstone_numbers = results[1]
        starting_number = results[3]
    except TypeError as e:
        if start is None and name is not None:
            return func.HttpResponse(
                f"Hi {name}, This HTTP triggered function executed successfully.",
                status_code=200
            )
        elif start is None and name is None:
            return func.HttpResponse(
                    f"This HTTP triggered function executed successfully. Pass in a name and starting number in the parameters for a full response",
                    status_code=200
                )
        else:
            print(e)
            print("Please input an integer into the start parameter.")
    if name and starting_number:    
        return func.HttpResponse(
            f"Hello, {name}. \nThis HTTP triggered function executed successfully. \nWith a starting number of {starting_number}, the Collatz Conjecture iterated through {number_of_steps} steps producing the following hailstone numbers: \n{list_of_hailstone_numbers}",
            status_code=200
            )   
    else:
        if name is None:
            return func.HttpResponse(
                f"This HTTP triggered function executed successfully. \nWith a starting number of {starting_number}, the Collatz Conjecture iterated through {number_of_steps} steps producing the following hailstone numbers: \n{list_of_hailstone_numbers}",
                status_code=200
            )
        
            
    
