import json
import sys
import requests
import pprint


def director_info(movie_list):
    result = []
    for movie in movie_list:
        BASE_URL2='https://api.themoviedb.org/3/movie/'
        path2 = '/credits?'
        params = {
            'api_key' : 'b423b9f62c2dcbbc988e246c89249738',
            'language' : 'ko-KR',
        }
        response = requests.get(BASE_URL2 + str(movie['id']) + path2, params = params).json()
        for idx2 in range(len(response['crew'])):
            if response['crew'][idx2]['job'] == "Director":
                fields = {}
                BASE_URL3='https://api.themoviedb.org/3/person/'
                params = {
                    'api_key' : 'b423b9f62c2dcbbc988e246c89249738',
                    'language' : 'ko-KR',
                }
                res = requests.get(BASE_URL3 + str(response['crew'][idx2]['id']), params = params).json()
                fields['name'] = res['name']
                fields['profile_path'] = res['profile_path']

                info = { 
                    "model": "movies.director",
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
    'page' : 26
}
response = requests.get(BASE_URL1 + path1, params = params).json()
movie_list = response['results']
directors = director_info(movie_list)

with open('director26.json', 'w', encoding="utf-8") as f:
    json.dump(directors, f, ensure_ascii=False, indent="\t")