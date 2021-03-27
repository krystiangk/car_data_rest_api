import requests


# Function that checks if the car data sent with POST method through POST /cars endpoint exists in the nhtsa db
# Returns car data with first letter capitalized if exists, otherwise None.
def check_if_car_exists(posted_car_data):
    posted_car_data = dict((k, v.title()) for k, v in posted_car_data.items())
    nhtsa_response = requests. \
        get(f"https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{posted_car_data['make']}?format=json").json()
    make_models = [car['Model_Name'].title() for car in nhtsa_response['Results']]
    for model in make_models:
        if model == posted_car_data['model']:
            return posted_car_data
    return
