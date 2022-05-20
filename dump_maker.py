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
    return result
        
    #       genre_list_temp = []
    #       for genres in genre_list:       
    #         # 장르 리스트 순회 2
    #             try:
    #                 for idx in range(len(movie['genre_ids'])):
    #                     if movie['genre_ids'][idx] == genres["pk"]:
    #                     # 장르 아이디와 일치한다면
    #                         genre_name = genres["name"]
    #                         genre_list_temp.append(genre_name)
    #             except:
    #                 continue
    #         fields['genre'] = genre_list_temp
    #     result.append(fields)
    # return result


# if __name__ == '__main__':
#     movies_json = open('movies.json', encoding='UTF8')
#     movies_list = json.load(movies_json)

    movies = movie_info(movies_list)
    with open('movie.json', 'w', encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent="\t")

for i in range(3, 11):
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
    # pprint.pprint(movies)

    with open(f'movie{i}.json', 'w', encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent="\t")