import json
# from pprint import pprint
import sys
import requests
import pprint


def movie_info(movies_list):
    result = []
    
    genre_list = [{"pk": 28, "name": "액션"}, {"pk": 12, "name": "모험"}, {"pk": 16, "name": "애니메이션"}, {"pk": 35, "name": "코미디"}, {"pk": 80, "name": "범죄"}, { "pk": 99, "name": "다큐멘터리"}, { "pk": 18, "name": "드라마"}, { "pk": 10751, "name": "가족"}, { "pk": 14, "name": "판타지"}, { "pk": 36, "name": "역사"}, { "pk": 27, "name": "공포"}, { "pk": 10402, "name": "음악"}, { "pk": 9648, "name": "미스터리"}, { "pk": 10749, "name": "로맨스"}, { "pk": 878, "name": "SF"}, { "pk": 10770, "name": "TV 영화"}, { "pk": 53, "name": "스릴러"}, {"pk": 10752, "name": "전쟁"}, {"pk": 37, "name": "서부"}]

    # 내가 원하는 정보의 key값
    key_list = ['poster_path', 'release_date', 'id', 'title','overview', 'releadse_date', 'vote_average', 'backdrop_path', 'adult']
    # for 문을 이용하여 key가 key_list 내부에 있으면 info ditionary에 추가
    i = 1
    for movie in movies_list:
        fields = {}
        # print(movie)
        for key in key_list:
            try:
                fields[key] = movie[key]
            except:
                continue
            # 장르 리스트 순회 1           
            for genres in genre_list:
                try:
                    if movie['genre_ids'][0] == genres["pk"]:
                    # 장르 아이디와 일치한다면
                        genre_name = genres["name"]
                        fields['genre'] = genre_name
                except:
                    continue
        # print(fields)
        info = { 
            "model": "movies.movie",
            "pk": i,
        }
        info["fields"] = fields
        result.append(info)
        i += 1
        # result.append(fields)
        # id -> 주소에 입력해서 -> 영상을 가져와서 -> 할당을 하여 저장한다.
    return result
        

BASE_URL='https://api.themoviedb.org/3'
path = '/movie/popular?'
params = {
    'api_key' : 'b423b9f62c2dcbbc988e246c89249738',
    'language' : 'ko-KR',
}
response = requests.get(BASE_URL + path, params = params).json()

movie = response['results']
# pprint.pprint(movie)

BASE_URL='https://api.themoviedb.org/3/movie/'
path = '/credits?'
params = {
    'api_key' : 'b423b9f62c2dcbbc988e246c89249738',
    'language' : 'ko-KR',
}
for idx in range(len(movie)):
    # print(movie[idx]['id'])
    response = requests.get(BASE_URL + str(movie[idx]['id']) + path, params = params).json()
    
    
    # 출연진 가져오기 !!!!!!!!!!!!!!!!!!!!!!!!
    
    # pprint.pprint(response['cast'])
    for idx2 in range(len(response['cast'])):
        if response['cast'][idx2]['order'] <= 5:
            # pprint.pprint(response['cast'][idx2])
    # https://api.themoviedb.org/3/movie/22/credits?api_key=b423b9f62c2dcbbc988e246c89249738&language=en-US
            response['cast'][idx2]['id']
            BASE_URL='https://api.themoviedb.org/3/person/'
            # path = '/credits?'
            params = {
                'api_key' : 'b423b9f62c2dcbbc988e246c89249738',
                'language' : 'ko-KR',
            }
            for idx3 in range(len(response['cast'][idx2])):
                # print(movie[idx]['id'])
                res = requests.get(BASE_URL + str(response['cast'][idx2][idx3]['id']), params = params).json()
                pprint.pprint(res)
            # with open(f'movie.json', 'w', encoding="utf-8") as f:
            #     json.dump(movies, f, ensure_ascii=False, indent="\t")
# movies = movie_info(movie)

# pprint.pprint(movies)

# with open(f'movie.json', 'w', encoding="utf-8") as f:
#     json.dump(movies, f, ensure_ascii=False, indent="\t")



'''
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
'''