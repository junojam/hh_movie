import json
import requests

BASE_URL='https://api.themoviedb.org/3'
path = '/movie/popular?'
params = {
    'api_key' : 'b423b9f62c2dcbbc988e246c89249738',
    'language' : 'ko-KR'
}
response = requests.get(BASE_URL + path, params = params).json()

for idx in range(len(response['results'])):
    response['results'][idx]['title']


# https://api.themoviedb.org/3/movie/popular?api_key=b423b9f62c2dcbbc988e246c89249738&language=ko-KR&page=1
    
# with open('popularMovie.json', 'w') as f:
#     json_string = json.dump(response, f, indent=2)
    
    