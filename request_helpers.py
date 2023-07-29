import requests

def get_dict_from_url(url):
    return (
        requests
        .get(url,headers={'User-Agent': 'Mozilla/5.0'})
        .json()
    )
