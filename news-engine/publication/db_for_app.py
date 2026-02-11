import psycopg2
import requests, json
host = 'localhost'
user = 'db_user',
password = 'pass',
database = 'db_match'

def writesonic(title):
    url = "https://api.writesonic.com/v2/business/content/chatsonic?engine=premium"


    payload = {
        "enable_google_results": "true",
        "enable_memory": False,
        "input_text": title
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-KEY": "YOUR_KEY"
    }

    response = requests.post(url, json=payload, headers=headers).json()
    return response['message']



def check_stat_preview(insert_query):
    try:
        connection = psycopg2.connect(
            host='localhost',
            user = 'db_user',
            password = 'PASS',
            database = 'db_match'
        )
        with connection.cursor() as cursor:
            cursor.execute(insert_query)
            result = cursor.fetchall()
            connection.commit()
            return result


    except Exception as _ex:
        print('[INFO] ERROR', _ex)

    finally:
        if connection:
            connection.close()

def replace_new_list(list_old):
    new_list = []
    for i in range(len(list_old)):
        if " " in list_old[i]:
            new_list.append(list_old[i].replace("_", " "))
        else:
            new_list.append(list_old[i])
    return new_list


def get_data_fix(fixture_match, team_name_home):
    insert_query = (
        f"SELECT name_home_review, name_away_review, goals_home, goals_away FROM match_review WHERE fixture_match_for_check = {fixture_match}"
    )
    index = check_stat_preview(insert_query)
    print(index)
    index = index[0]
    name_home_review = index[0]
    name_away_review = index[1]
    goals_home = index[2]
    goals_away = index[3]

    if name_home_review == team_name_home:
        team_away = name_away_review
        goals_home_new = goals_home
        goals_away_new = goals_away
    else:
        team_away = name_home_review
        goals_away_new = goals_home
        goals_home_new = goals_away

    return team_away, goals_home_new, goals_away_new
def get_data(insert_query):
    try:
        connection = psycopg2.connect (
            host='localhost',
            user = 'db_user',
            password = 'PASS',
            database = 'db_match'
        )
        with connection.cursor() as cursor:

            cursor.execute(insert_query)
            result = cursor.fetchall()
            return result
            connection.commit()

    except Exception as _ex:
        print('[INFO] ERROR', _ex)

    finally:
        if connection:
            connection.close()
# print(get_data(f"SELECT * FROM players WHERE name LIKE 'Hakim Ziyech';"))
def get_user_id_main(type_subscribe):
    try: 
        # Подключаемся
        connection = psycopg2.connect( 
            host='localhost',
            user='db_user',
            password='PASS',
            database='main'
        )
        # Создаем курсор
        with connection.cursor() as cursor:
            insert_query = (
                f"SELECT user_id FROM subscribe WHERE type_subscribe LIKE '{type_subscribe}';"
            )
            cursor.execute(insert_query)
            result = cursor.fetchall()
            l=[]
            for i in range(len(result)):
                l.append(result[i][0])
            return l
   
    except Exception as _ex:
        print('[INFO] ERROR', _ex)
    # Финал
    finally:
        if connection:
            # Отключаемся
            connection.close()
import json
import base64
# l_version, fixture_match, types, url

# user = 'botbot.news'
# password = 'vAcM BwHH Dqhq Eicv 54xt 0EOu'
# credentials = user + ':' + password
#
# token = base64.b64encode(credentials.encode())
# header = {'Authorization': 'Basic ' + token.decode('utf-8')}
# platform_url = "https://malanka.media/wp-json/wp/v2/media"
from time import sleep

def upload_image_to_wordpress(file_path, url, header_json, fixture_match, types=None):
    try: 
        print("header", header_json, fixture_match)
        print(file_path)
        media = {'file': open(file_path, "rb"), 'caption': f'{fixture_match}'}
        responce = requests.post(url, headers=header_json, files=media)
        print("image response",responce)
        responce = responce.json()
        img_id = responce['id']

        # Track successful WordPress upload
        if types:
            from publication.message_tracker import add_message, MessageStage, MessageStatus
            add_message(
                types,
                MessageStage.IMAGE_WORDPRESS_UPLOAD,
                MessageStatus.SUCCESS,
                f"Image uploaded to WordPress successfully (ID: {img_id})"
            )

        print(f"[INFO] Image uploaded to WordPress with ID: {img_id}")
        return img_id
    except Exception as _ex:
        error_msg = f"Failed upload image {_ex}"
        print(error_msg)

        # Track WordPress upload error
        if types:
            from publication.message_tracker import add_message, MessageStage, MessageStatus
            add_message(
                types,
                MessageStage.IMAGE_WORDPRESS_UPLOAD,
                MessageStatus.ERROR,
                "WordPress image upload failed",
                error_details=str(_ex)
            )

        return 0
# upload_image_to_wordpress('/Applications/BotBot/work_rep/new/footballBot/result/img_match/140_12_round_review.png', platform_url, header, '1')


# platform_name = "wordpress"
# platform_url = "https://botbot.news/wp-json/wp/v2/posts"
# platform_user = "botbot"
# platform_password = "cGvj MT0x lqRl cEuY tddX huHk"
#
# credentials = platform_user + ':' + platform_password
# token = base64.b64encode(credentials.encode())
# header = {'Authorization': 'Basic ' + token.decode('utf-8')}
# post = {
#     'title': 'test',
#     'status': 'publish',  # тип
#     'content': 'test',
#     'categories': '', # category ID
#     'tags': '',
#     # 'date'   : f'{date}',   # время публикации --  {время матча - один день}
#     'meta': {'_knawatfibu_url': featured_image}
# }
# responce = requests.post(platform_url, headers=header, json=post)
# responce = responce.json()
# print(responce['link'])

def bot_send_message_tg(featured_image, token, channel, text):

    responce = requests.post(
        url = f'https://api.telegram.org/bot{token}/sendPhoto',
        data = {
            'chat_id':f"{channel}",
            'photo': f"{featured_image}"
        }
    ).json
    sleep(2)
    responce = requests.post(
        url = f'https://api.telegram.org/bot{token}/sendMessage',
        data = {
            'chat_id':f"{channel}",
            'text': f"{text}",
            'parse_mode':"Markdown"
        }
    ).json
    # print(responce.text)
# bot_sendtext('test', 'test', 'test', 'test.com')


# import tweepy
# def bot_send_twitter(title, text_publ, league_name, url_publ, featured_image, team_home, team_away, list_data):
#     text = f"{title}\n\nLeague: #{league_name.replace(' ','')}2022\nTeams: #{team_home.replace(' ','')} #{team_away.replace(' ','')}\n\nMore details: {url_publ}"
#     # api_key, api_secrets, access_token, access_secret = list_data


#     consumer_key = "5PIDwNuLfysS7jzN2nf1KLLCs"
#     consumer_secret = "ZCHB2YT79qxc2NpcxIJ0Sj2RX0kkzUwZrawRiqY4lzc6Nhz889"
#     access_token = "1597182488887140352-Lt7hE74ors0JhvgO0cOZ5awFQm8vii"
#     access_token_secret = "78QfEBdG2fxSceIuPfaM2ZPqXbsRIf1KW3KVhAVOBULvB"

    # client = tweepy.Client("AAAAAAAAAAAAAAAAAAAAAE1PjwEAAAAAPFwuhTfb6RvAYTZ4AC5LxLWdP6g%3DfXCwa5HvCSH7BIWjGgSpPtDuLVYkizs1ZDSxHL5tQrF1pnrC3L")
    # Authenticate to Twitter
    # auth = tweepy.OAuthHandler(api_key, api_secrets)
    # auth.set_access_token(access_token, access_secret)

    # api = tweepy.API(client)
    # print(api)

    # Authenticate to Twitter
    # auth = tweepy.OAuthHandler(api_key, api_secrets)
    # auth.set_access_token(access_token, access_secret)

    # api = tweepy.Client(
    #     consumer_key="vJ12V3Uq87lujXQJ5q9rYWSOZ",
    #     consumer_secret="aSiHiy6RyGaHYqUxE0HoVcjOQyYCTMdMGOtrkTvOo5FUi7wnm5",
    #     access_token="1597182488887140352-MLOOvyaTXEaMl2lxEPknxXC2h6NlxX",
    #     access_token_secret="GV8kuM9do3IT7n3wAzgaQKuiThhOSi96Xr1KXKc0kHdBa"
    # )
    #
    # from twython import Twython
    #
    # APP_KEY = consumer_key  # Customer Key here
    # APP_SECRET = consumer_secret  # Customer secret here
    # OAUTH_TOKEN =  access_token # Access Token here
    # OAUTH_TOKEN_SECRET = access_token_secret # Access Token Secret here
    #
    # twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    #
    # twitter.update_status(status="Hello from Python! :D")
    # api = tweepy.Client(bearer_token="AAAAAAAAAAAAAAAAAAAAAE1PjwEAAAAAPFwuhTfb6RvAYTZ4AC5LxLWdP6g%3DfXCwa5HvCSH7BIWjGgSpPtDuLVYkizs1ZDSxHL5tQrF1pnrC3L", consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)
    # api.create_tweet(text = "hello", media_ids=[featured_image])
    # client = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token,
    #                        access_token_secret=access_token_secret)
    # query = 'news'
    # tweets = client.search_recent_tweets(query=query, max_results=10)
    # api = tweepy.API(oauth1_user_handler)
    # status = "This is my first post to Twitter using the API"
    # api.update_status(status=status)
    # for tweet in tweets.data:
    #     print(tweet.text)
    # print(oauth1_user_handler.get_authorization_url())
    # api = tweepy.API(auth)
    # print(api)
    # api = tweepy.API(auth, wait_on_rate_limit=True)

    # api.update_with_media(featured_image, text)
# bot_send_twitter('test', 'test', 'test', 'test.com', 'https://buckets-botbot-football.s3.eu-central-1.amazonaws.com/match/eng_855765_review.png', 'test', 'test', ["85qcANNHPeb40D8FrEDsKtPzR", "aSiHiy6RyGaHYqUxE0HoVcjOQyYCTMdMGOtrkTvOo5FUi7wnm5", '1597182488887140352-KWCa1dJWwn0loGf8LLHU3Qg0Y1QOTw', 'GV8kuM9do3IT7n3wAzgaQKuiThhOSi96Xr1KXKc0kHdBa'])
