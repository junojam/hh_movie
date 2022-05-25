import json
import sys
import requests
import pprint


def actor_info(movie_list):
    result = []
    for movie in movie_list:
        BASE_URL2='https://api.themoviedb.org/3/movie/'
        path2 = '/credits?'
        params = {
            'api_key' : 'b423b9f62c2dcbbc988e246c89249738',
            'language' : 'ko-KR',
        }

        response = requests.get(BASE_URL2 + str(movie['id']) + path2, params = params).json()
        for idx2 in range(len(response['cast'])):
            if response['cast'][idx2]['order'] < 5:
                fields = {}
                BASE_URL3='https://api.themoviedb.org/3/person/'
                params = {
                    'api_key' : 'b423b9f62c2dcbbc988e246c89249738',
                    'language' : 'ko-KR',
                }
                
                res = requests.get(BASE_URL3 + str(response['cast'][idx2]['id']), params = params).json()
                fields['name'] = res['name']
                fields['profile_path'] = res['profile_path']

                info = { 
                    "model": "movies.actor",
                    "pk": res['id'],
                }
                info["fields"] = fields
                result.append(info)
    return result
        
# ------------------------------------------------------
BASE_URL1='https://api.themoviedb.org/3'
path1 = '/movie/popular?'
params = {
    'api_key' : 'b423b9f62c2dcbbc988e246c89249738',
    'language' : 'ko-KR',
    'page' : 10
}
response = requests.get(BASE_URL1 + path1, params = params).json()
movie_list = response['results']
actors = actor_info(movie_list)

with open('actor10.json', 'w', encoding="utf-8") as f:
    json.dump(actors, f, ensure_ascii=False, indent="\t")