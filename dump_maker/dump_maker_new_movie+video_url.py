import json
# from pprint import pprint
import sys
import requests
import pprint


def movie_info(movies_list):
    result = []
    genre_list = [{"pk": 28, "name": "액션"}, {"pk": 12, "name": "모험"}, {"pk": 16, "name": "애니메이션"}, {"pk": 35, "name": "코미디"}, {"pk": 80, "name": "범죄"}, { "pk": 99, "name": "다큐멘터리"}, { "pk": 18, "name": "드라마"}, { "pk": 10751, "name": "가족"}, { "pk": 14, "name": "판타지"}, { "pk": 36, "name": "역사"}, { "pk": 27, "name": "공포"}, { "pk": 10402, "name": "음악"}, { "pk": 9648, "name": "미스터리"}, { "pk": 10749, "name": "로맨스"}, { "pk": 878, "name": "SF"}, { "pk": 10770, "name": "TV 영화"}, { "pk": 53, "name": "스릴러"}, {"pk": 10752, "name": "전쟁"}, {"pk": 37, "name": "서부"}]
    key_list = ['poster_path', 'release_date', 'title','overview', 'releadse_date', 'vote_average', 'backdrop_path', 'adult']
    for movie in movies_list:
        fields = {}
        actors_lst = []
        directors_lst = []
        BASE_URL99='https://api.themoviedb.org/3/movie/'
        path99 = '/credits?'
        params = {
            'api_key' : 'b423b9f62c2dcbbc988e246c89249738',
            'language' : 'ko-KR',
        }
        response = requests.get(BASE_URL99 + str(movie['id']) + path99, params = params).json()
        
        # actors 추가
        for idx2 in range(len(response['cast'])):
            if response['cast'][idx2]['order'] < 5:
                actors_lst.append(response['cast'][idx2]['id'])

        # directors 추가
        for idx3 in range(len(response['crew'])):
            if response['crew'][idx3]['job'] == "Director":
                directors_lst.append(response['crew'][idx3]['id'])

        tmp = movie['id']
        path = f'/movie/{tmp}/videos?'
        params1 = {
            'api_key' : 'b423b9f62c2dcbbc988e246c89249738',
            'language' : 'ko-KR',
        }
        params2 = {
            'api_key' : 'b423b9f62c2dcbbc988e246c89249738',
        }
        response1 = requests.get(BASE_URL + path, params = params1).json()
        response2 = requests.get(BASE_URL + path, params = params2).json()
        # pprint.pprint(response1)
        # pprint.pprint(response2)
        if response1['results'] or response2['results']:
            try:
                if response1['results'][0]['key']:
                    video_url = 'https://www.youtube.com/embed/' + response1['results'][0]['key'] + '?autoplay=1&mute=1'
            except:
                if response2['results'][0]['key']:
                    video_url = 'https://www.youtube.com/embed/' + response2['results'][0]['key'] + '?autoplay=1&mute=1'
            fields['video_url'] = video_url
        
        # movie credit 조회 url
        # https://api.themoviedb.org/3/movie/606402/credits?api_key=b423b9f62c2dcbbc988e246c89249738&language=ko-KR

        for key in key_list:
            try:
                fields[key] = movie[key]
            except:
                continue    
            for genres in genre_list:
                try:
                    if movie['genre_ids'][0] == genres["pk"]:
                        genre_name = genres["name"]
                        fields['genre'] = genre_name
                except:
                    continue
        fields['actors'] = actors_lst
        fields['directors'] = directors_lst
        info = { 
            "model": "movies.movie",
            "pk": movie['id'],
        }
        info["fields"] = fields
        result.append(info)
    return result
        

for i in range(6, 11):
    if i == 10:
        BASE_URL='https://api.themoviedb.org/3'
        path = '/movie/popular?'
        params = {
            'api_key' : 'b423b9f62c2dcbbc988e246c89249738',
            'language' : 'ko-KR',
            'page' : i
        }
        response = requests.get(BASE_URL + path, params = params).json()
        movie = response['results']
        movies = movie_info(movie)

        with open(f'movie{i}.json', 'w', encoding="utf-8") as f:
            json.dump(movies, f, ensure_ascii=False, indent="\t")
        
'''
dumpdata 기본 모델
https://api.themoviedb.org/3/movie/popular?api_key=b423b9f62c2dcbbc988e246c89249738&language=en-US

영화 id로 출연진 가져오기
https://api.themoviedb.org/3/movie/22/credits?api_key=b423b9f62c2dcbbc988e246c89249738&language=en-US

출연진 id로 정보 가져오기
https://api.themoviedb.org/3/person/85?api_key=b423b9f62c2dcbbc988e246c89249738&language=en-US
프로필 사진
https://www.themoviedb.org/t/p/w300_and_h450_bestv2/ilPBHd3r3ahlipNQtjr4E3G04jJ.jpg

출연진 id로 유명 영화 가져오기
https://api.themoviedb.org/3/person/85/movie_credits?api_key=b423b9f62c2dcbbc988e246c89249738&language=en-US

backdrop_path 확인
https://www.themoviedb.org/t/p/w300_and_h450_bestv2/8zfRLCgKrLAc5SSnACz8ZqmeKAP.jpg
backdrop_path는 TMDB의 배경사진

poster_path 확인
https://www.themoviedb.org/t/p/w300_and_h450_bestv2/uXEqmloGyP7UXAiphJUu2v2pcuE.jpg

영화 id로 영화의 정보 가져오기(동영상URL을 위한 key가 있음)
https://api.themoviedb.org/3/movie/22/videos?api_key=b423b9f62c2dcbbc988e246c89249738

key를 확인한다.
naQr0uTrH_s

key를 youtube에 주소 기입하면 영상을 볼 수 있음
https://www.youtube.com/watch?v=naQr0uTrH_s

embed 방식으로 하려면 아래와 같이할 것.
https://www.themoviedb.org/video/play?key=naQr0uTrH_s

​

'''