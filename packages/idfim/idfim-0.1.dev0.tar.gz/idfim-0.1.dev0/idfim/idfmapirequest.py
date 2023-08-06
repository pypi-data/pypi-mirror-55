import requests

def get_isochrone_polygon(api_token, starting_point, max_duration, datetime=None):
    '''
    starting_point_str:
    str gps position
    
    datetime_str:
    str 20191104T080000',    # AAAAMMJJTHHMMSS
    default: now
    
    max_duration
    int
    minutes
    '''
    #Paramètres de la requête (URL?)
    url = 'https://traffic.api.iledefrance-mobilites.fr/v1/mri-isochrones/isochrones'

    starting_point_lat_long_tuple = starting_point.split(",")
    starting_point_long_lat_str = starting_point_lat_long_tuple[1] + ";" + starting_point_lat_long_tuple[0]

    params = {
        'from': starting_point_long_lat_str,    # {long;lat}. Ex : '2.335547;48.876076'
        'datetime': datetime,                   # Format: YYYYMMDDTHHMMSS
        'max_duration': str(max_duration * 60)  # In seconds. Ex: 1800
    }

    headers = {
        'Accept-Encoding': 'gzip',
        'Authorization': 'Bearer ' + api_token
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        raise Exception('Status:', response.status_code, 'Erreur sur la requête; fin de programme')

    response_dict = response.json()
    
    polygon_list = [isochrone['geojson'] for isochrone in response_dict['isochrones']]
    
    return polygon_list

