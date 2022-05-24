import json
# from pprint import pprint
import sys
import requests
import pprint


def actor_info(movie_list):
    result = []
    # key_list = ['id', ]
    i = 1
    for movie in movie_list:
        # print(movie['id'])
        # https://api.themoviedb.org/3/movie/22/credits?api_key=b423b9f62c2dcbbc988e246c89249738&language=en-US
        BASE_URL2='https://api.themoviedb.org/3/movie/'
        path2 = '/credits?'
        params = {
            'api_key' : 'b423b9f62c2dcbbc988e246c89249738',
            'language' : 'ko-KR',
        }
        # print(movie['title'])
        # print(movie['id'])
        response = requests.get(BASE_URL2 + str(movie['id']) + path2, params = params).json()
        # pprint.pprint(response)
        for idx2 in range(len(response['cast'])):
            if response['cast'][idx2]['order'] < 5:
                fields = {}
                # pprint.pprint(response['cast'][idx])
                BASE_URL3='https://api.themoviedb.org/3/person/'
                params = {
                    'api_key' : 'b423b9f62c2dcbbc988e246c89249738',
                    'language' : 'ko-KR',
                }
                
                res = requests.get(BASE_URL3 + str(response['cast'][idx2]['id']), params = params).json()
                # print(movie['title'])
                # pprint.pprint(res['name'])
                # pprint.pprint(res['profile_path'])
                # pprint.pprint(response['cast'][idx2]['character'])
                # pprint.pprint(response['cast'][idx2]['known_for_department'])
                
                fields['movie_id'] = movie['id']
                fields['name'] = res['name']
                fields['profile_path'] = res['profile_path']
                fields['department'] = response['cast'][idx2]['known_for_department']
                fields['character'] = response['cast'][idx2]['character']
        
                # for key in key_list:
                #     try:
                #         fields[key] = movie[key]
                #     except:
                #         continue    

                info = { 
                    "model": "movies.actor",
                    "pk": i,
                }
                info["fields"] = fields
                result.append(info)
                i += 1
        # result.append(fields)
        # id -> 주소에 입력해서 -> 영상을 가져와서 -> 할당을 하여 저장한다.
    return result
        
# ------------------------------------------------------
BASE_URL1='https://api.themoviedb.org/3'
path1 = '/movie/popular?'
params = {
    'api_key' : 'b423b9f62c2dcbbc988e246c89249738',
    'language' : 'ko-KR',
}
response = requests.get(BASE_URL1 + path1, params = params).json()
movie_list = response['results']
actors = actor_info(movie_list)

pprint.pprint(actors)

with open('actor1.json', 'w', encoding="utf-8") as f:
    json.dump(actors, f, ensure_ascii=False, indent="\t")