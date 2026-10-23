from dotenv import load_dotenv
import httpx
import os
from pydantic import BaseModel, ValidationError
from asyncio import run, gather, create_task, sleep, TimeoutError, wait_for, Semaphore
import time


load_dotenv()

api_token = os.getenv("EPC_BEARER_TOKEN")

base_url = "https://api.get-energy-performance-data.communities.gov.uk"

postcode = "M21 9BG"  # Example postcode

class Model(BaseModel):
    data: list[dict[str, str | int | None]]
    pagination: dict[str, int | None]
    postcode: str | None = None
    postcode_country: str | None = None
    postcode_region: str | None = None
    postcode_admin_district: str | None = None
    postcode_longitude: float | None = None
    postcode_latitude: float | None = None


# dict_keys(['data', 'pagination'])
# data dict_keys(['certificateNumber', 'addressLine1', 'addressLine2', 'addressLine3', 'addressLine4', 'postcode', 'postTown', 'council', 'constituency', 'currentEnergyEfficiencyBand', 'registrationDate', 'uprn', 'schemaType'])
# data types - string, None
# pagination dict_keys(['totalRecords', 'currentPage', 'totalPages', 'nextPage', 'prevPage', 'pageSize'])
# pagination types - int, None


def get_random_postcode_data():
    random_postcode = httpx.get("https://api.postcodes.io/random/postcodes").json()
    postcode_data = {
        "postcode": random_postcode["result"]["postcode"],
        "postcode_country": random_postcode["result"]["country"],
        "postcode_region": random_postcode["result"]["region"],
        "postcode_admin_district": random_postcode["result"]["admin_district"],
        "postcode_longitude": random_postcode["result"]["longitude"],
        "postcode_latitude": random_postcode["result"]["latitude"]
    }
    print(postcode_data)
    return postcode_data

def get_epc_domestic_certificate(postcode: str):
    return httpx.get(
                base_url + "/api/domestic/search" + postcode,
                headers={"Authorization": f"Bearer {api_token}", "Accept": "application/json"}
            )

def get_epc_domestic_certificate_by_postcode(postcode: str):
    search_criteria = {
    "domestic_certificate": "/api/domestic/search",
    "domestic_certificate_postcode": "/api/domestic/search?postcode="
    }
    try:
        response = Model.model_validate(httpx.get(
            base_url + search_criteria["domestic_certificate_postcode"] + postcode,
            headers={"Authorization": f"Bearer {api_token}", "Accept": "application/json"}
        ).json())
    except httpx.RequestError as e:
        print(f"An error occurred while requesting {e.request.url!r}.")
    except httpx.HTTPStatusError as e:
        print(f"Error response {e.response.status_code} while requesting {e.request.url!r}.")
    except ValidationError as e:
        print(f"Validation error: {e}")
    finally:
        response_dict = response.model_dump()
    return response_dict




async def async_fetch_postcode_data():
    async with httpx.AsyncClient() as client:
        random_postcode = await client.get("https://api.postcodes.io/random/postcodes")
        random_postcode = random_postcode.json()
        postcode_data = {
            "postcode": random_postcode["result"]["postcode"],
            "postcode_country": random_postcode["result"]["country"],
            "postcode_region": random_postcode["result"]["region"],
            "postcode_admin_district": random_postcode["result"]["admin_district"],
            "postcode_longitude": random_postcode["result"]["longitude"],
            "postcode_latitude": random_postcode["result"]["latitude"]
        }
        print(f"{postcode_data['postcode']} - {random_postcode['result']['admin_district']}")
    return postcode_data

in_flight = 0
pc = []
for p in range(20):
    pc.append(get_random_postcode_data()["postcode"])
    #  + "-" + str(get_random_postcode_data()["postcode_admin_district"]
print(pc)

def sync_fetch_epc_data(postcodes: list):
    pn = 1
    for post in pc:
        get_epc_domestic_certificate(post)
        print(f"Processed postcode: {post} ({pn}/{len(postcodes)})")
        pn += 1

count = 0

async def async_fetch_epc_data(postcode: str, semaphore: Semaphore, aclient: httpx.AsyncClient):
    global in_flight
    global count
    async with semaphore:
        try:
            in_flight += 1
            print(f"Currently in flight: {in_flight}")
            response = await aclient.get(base_url + "/api/domestic/search?postcode=" + postcode, headers={"Authorization": f"Bearer {api_token}", "Accept": "application/json"})
            count += 1
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            print(f"Processed postcode: {postcode} ({count}/20) - {data['data'][0]['council']}" if isinstance(data["data"], list) else "Error: No data found")
        except httpx.RequestError as e:
            print(f"An error occurred while requesting {e.request.url!r}.")
        except httpx.HTTPStatusError as e:
            print(f"Error response {e.response.status_code} while requesting {e.request.url!r}.")
        finally:
            print(f"Postcode {count}/20")
            in_flight -= 1
            print(f"Currently in flight again: {in_flight}")

async def async_for_loop_fetch_epc_data(postcodes: list):
    n = 1
    for post in postcodes:
        print(f"Processing postcode: {post} ({n}/{len(postcodes)})")
        n += 1
        await async_fetch_epc_data(post)
    # tasks = [create_task(async_fetch_epc_data(postcode)) for _ in range(4)]
    # await gather(*tasks)

async def async_tasks_semaphore_fetch_epc_data(postcodes: list, concurrency: int):
    semaphore = Semaphore(concurrency)
    async with httpx.AsyncClient() as httpx_client:
        tasks = [create_task(async_fetch_epc_data(postcode, semaphore, httpx_client)) for postcode in postcodes]
        await gather(*tasks)
    # global in_flight
    # in_flight += 1
    # print(f"Currently in flight: {in_flight}")
    # await gather(*tasks)
    # in_flight -= 1
    # print(f"Currently in flight again: {in_flight}")


async def async_semaphore_fetch_epc_data(postcodes: list, concurrency: int):
    n = 1
    for post in postcodes:
        async with Semaphore(concurrency):
            print(f"Processing postcode: {post} ({n}/{len(postcodes)})")
            n += 1
            await async_fetch_epc_data(post)

def classify_staus_code(status_code: int) -> str:
    if status_code == 400:
        return "Bad Request"
    elif status_code == 401:
        return "Unauthorized"
    elif status_code == "connection_timeout":
        return "Connection Timeout - Retry"
    elif status_code == "read_timeout":
        return "Read Timeout - "
    elif status_code == 404:
        return "Not Found"
    elif status_code == 429:
        return "Too Many Requests - Retry"
    elif status_code == 500:
        return "Internal Server Error - Restrained"
    elif status_code == 502:
        return "Bad Gateway - Retry"
    elif status_code == 503:
        return "Service Unavailable - Retry"
    elif status_code == 504:
        return "Gateway Timeout - Restrained"
    elif 100 <= status_code < 200:
        return "Informational"
    elif 200 <= status_code < 300:
        return "Success"
    elif 300 <= status_code < 400:
        return "Redirection"
    elif 400 <= status_code < 500:
        return "Client Error"
    elif 500 <= status_code < 600:
        return "Server Error"
    else:
        return "Unknown Status Code"
    
atsis_time = time.time()
run(async_tasks_semaphore_fetch_epc_data(pc, 4))
atsie_time = time.time() - atsis_time

# nis_time = time.time()
# sync_fetch_epc_data(pc)
# nie_time = time.time() - nis_time

# ais_time = time.time()
# run(async_for_loop_fetch_epc_data(pc))
# aie_time = time.time() - ais_time

# asis_time = time.time()
# run(async_semaphore_fetch_epc_data(pc, 4))
# asie_time = time.time() - asis_time

# print(f"Time taken for synchronous requests: {nie_time:.2f} seconds")
# print(f"Time taken for asynchronous for loop requests: {aie_time:.2f} seconds")
print(f"Time taken for asynchronous tasks semaphore requests: {atsie_time:.2f} seconds")
# print(f"Time taken for asynchronous semaphore requests: {asie_time:.2f} seconds")
# get_random_postcode_data()