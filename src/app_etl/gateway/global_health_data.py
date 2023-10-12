import requests


# TODO: add error handling for failure to invoke WHO GHO API
def retrieve_indicator_data(indicator_code):
    url = f"https://ghoapi.azureedge.net/api/{indicator_code}"
    request = requests.get(url)
    return request.json()["value"]
