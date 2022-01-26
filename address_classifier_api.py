import re
import requests
import json
from fuzzywuzzy import fuzz

ROOT_URL = 'https://ukrposhta.ua/address-classifier'

REGION_ID = 8 # Запорізька
DISTRICT_ID = 950 # Мелітопольський
CITY_ID = 4633 # Мелітополь

API_methods = {
    'get_region': {
        'method': 'get_regions_by_region_ua',
        'params': ['region_name']
    },
    'get_districts': {
        'method': 'get_districts_by_region_id_and_district_ua',
        'params': ['region_id', 'district_ua']
    },
    'get_city': {
        'method': 'get_city_by_region_id_and_district_id_and_city_ua',
        'params': ['region_id', 'district_id', 'city_ua']
    },
    'get_street': {
        'method': 'get_street_by_region_id_and_district_id_and_city_id_and_street_ua',
        'params': ['region_id', 'district_id', 'city_id', 'street_ua']
    },
    'get_house_number': {
        'method': 'get_addr_house_by_street_id',
        'params': ['street_id', 'housenumber']
    },
    '': {
        'method': '',
        'params': ['']
    },
}

def search_by_fuzz(
        what_search='', 
        where_search_j={}, 
        key_params={'key_s': '', 'key_r': ''}, 
        r=50
    ):
    '''
    EN: Using the FuzzyWuzzy library for fuzzy comparison in Python.
    Levenshtein distance (editor distance)
    RU: Применение библиотеки FuzzyWuzzy для нечёткого сравнения в Python. 
    Расстояние Левенштейна (редакционное расстояние).
    '''
    if what_search:
        list_result = []
        for item in where_search_j:
            Ratio = fuzz.ratio(
                what_search.lower(),
                item[key_params['key_s']].lower()
            )
            if Ratio>=r:
                list_result.append(
                    {
                        item[key_params['key_s']]:item[key_params['key_r']]
                    }
                )
        return list_result
    return None


def call_api(api_function=None, fuzzy=False, parameters={}):
    '''
    Call requests GET to ukrpost API. Adress classifiacator
    '''
    if api_function:
        method = API_methods[api_function]['method']
        query = parameters
        if fuzzy:
            query['fuzzy']=1
        headers = {
            'Accept': 'application/json'
        }
        
        try:
            req = requests.get(ROOT_URL+'/'+method, params=query, timeout=5, headers=headers)
        except requests.exceptions.Timeout:
            # Maybe set up for a retry, or continue in a retry loop
            print(f'Time out to - {ROOT_URL+"/"+method}')
            print(f'status_code - {requests.status_code}')
            return None
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            return None
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            raise SystemExit(e)
        
        if req.status_code==200:
            return req.json()
        else:
            print(f'status_code:\n{req.status_code}')

    else:
        return None
