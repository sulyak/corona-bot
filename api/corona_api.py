import json
import requests

URL = "https://corona.lmao.ninja/"

def counter_from_region(region: str=""):
    """Get the counter from specific regeion.
    `param region`: the specif region as str\n
    `Return Value`: A Json Response Content with data from the requested region

    If no param were given, the worldwide data will be returned.\n
    An exception will be raise if the given region does not exist
    """

    # check if region was given as argument
    if region:
        region_url = URL + "countries/" + region
    else:
        region_url = URL + "all/"

    # get request data as dict
    response = requests.get(region_url).json()

    # assert that region exist
    if 'message' in response:
        raise NameError(response['message'])

    return response

def does_region_exist(region: str):
    region_url = URL + "countries/" + region
    response = requests.get(region_url).json()
    
    return 'message' not in response

def main():
    print(counter_from_region())

if __name__ == "__main__": main()
