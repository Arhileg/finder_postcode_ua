import json
import address_classifier_api as ac_api
from models import Address
from  pprint import pprint


REGION_ID = 8 # Запорізька
DISTRICT_ID = 950 # Мелітопольський

address = [
    'м. Мелітополь, вул. ПІЩАНСЬКА, буд.103',
    'м. Мелітополь, вул. МОТОРНА, буд.11',
    'м. Мелітополь, вул. ЛЮТНЕВА, буд.181а',
    'м. Мелітополь, вул. ІНТЕРКУЛЬТУРНА, буд.317',
    'м. Мелітополь, пл. ПЕРЕМОГИ, буд.1, кв.27',
    'м. Мелітополь, вул. ОСИПЕНКО, буд.90, кв.115'
]

def read_citys():
    with open('citys.json', 'r', encoding='utf-8') as f:
        citys_data =  json.load(f)
        # json.dump(city_list, f, ensure_ascii=False, indent=4)
    return citys_data['Entries']['Entry']
    citys = {}
    for city in citys_data:
        citys[city['CITY_UA']] = city['CITY_ID']
    return citys

def read_streets(city_id):
    with open('streets_'+str(city_id)+'.json', 'r', encoding='utf-8') as f:
        streets_data =  json.load(f)
    streets = streets_data['Entries']['Entry']
    return streets

def parse_adress(address_list):
    address_objects_list = []
    for ad in address_list:
        address_objects_list.append(Address(ad))
    return address_objects_list

def find_city(item, call_api=False):
    if call_api:
        params = {
            'region_id': REGION_ID,
            'district_id': DISTRICT_ID,
            'city_ua': item.city
        }
        json_result = ac_api.call_api(
            api_function='get_city', 
            # fuzzy=True, 
            parameters=params)
        return json_result
    else:
        citys_json = read_citys()
        clear_search = False # flag - find element eqals to search if True else
        
        city_id = ac_api.search_by_fuzz(
            what_search=item.city,
            where_search_j=citys_json,
            key_params={'key_s': 'CITY_UA', 'key_r': 'CITY_ID'},
            r=80
        )
        return city_id

def find_street(city_id='', item={}, call_api=False):
    if call_api:
        params = {
            'region_id': REGION_ID,
            'district_id': DISTRICT_ID,
            'city_id': city_id,
            'street_ua': item['street']
        }
        json_result = ac_api.call_api(
            api_function='get_street', 
            parameters=params)
        return json_result
    else:
        streets_json = read_streets(city_id)
        clear_search = False # flag - find element eqals to search if True else
        
        city_id = ac_api.search_by_fuzz(
            what_search=item.city,
            where_search_j=streets_json,
            key_params={'key_search': 'STREET_UA', 'key_return': 'STREET_ID'},
            r=80
        )
        return city_id

def main():
    address_objects_list = parse_adress(address)
    for item in address_objects_list:
        city_id = find_city(item)
        if city_id:
            street_id = find_street(city_id=city_id, item=item)
            pprint(item['street'])
            pprint(street_id)
        # pprint(city_id)
    
if __name__=='__main__':
    main()
