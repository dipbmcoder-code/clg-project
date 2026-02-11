

# import math


# g_home = ['name minutes (total)','name2 minutes2 (total2','name3 minutes3 (total3)','name4 minutes4 (total4)']
# g_away = ['name minutes (total)','name2 minutes2 (total2']

# text_home = ''
# text_away = ''
# for i in range(len(g_home)):
#     text_home += f'<td>{g_home[i]}</tb>'
# for i in range(len(g_away)):
#     text_away += f'<td>{g_away[i]}</tb>'

# print(text_home)
# print(text_away)


# l = ['871221', 'Union Berlin', 'VfL Wolfsburg', 'F._Rønnow+C._Trimmel+N._Gießelmann+R._Knoche+T._Baumgartl+Diogo_Leite+R._Khedira+J._Haberer+A._Schäfer+S._Becker+J._Siebatcheu', 'K._Casteels+Paulo_Otávio+M._Lacroix+M._van_de_Ven+M._Arnold+J._Brekalo+M._Svanberg+R._Baku+B._Franjić+L._Waldschmidt+L._Nmecha', 'T._Baumgartl+J._Haberer+A._Schäfer+S._Becker+J._Siebatcheu', 'L._Waldschmidt+M._Svanberg+Paulo_Otávio+B._Franjić+J._Brekalo', 'P._Jaeckel+M._Thorsby+P._Seguin+S._Michel+K._Behrens', 'Omar_Marmoush+F._Nmecha+Y._Gerhardt+K._Paredes+J._Kamiński', '62 62 76 87 87', '60 60 69 79 79', '54 77', 'J._Siebatcheu+S._Becker', '', '', '', '', '', '', '', '', '', '', 'Jordan Siebatcheu', 'Maximilian Arnold', 'Jordan Siebatcheu', 'Micky van de Ven', 'Diogo Leite', 'Ridle Baku', '48%', '52%', 'András Schäfer', 'Ridle Baku', 'Eintracht Frankfurt', '2022-10-01', 'Deutsche Bank Park', 'VfB Stuttgart', '2022-10-01', 'VOLKSWAGEN ARENA', 'S. Becker', 'N. Füllkrug', 'D. Kamada', '6', '5', '4', 'Union Berlin', 'Werder Bremen', 'Eintracht Frankfurt', 871221, 2, 0, 4, 10, 4, None, None, 1, 2, 0, 16, 5, 4, 12, 2, 2, 3, 1, 6, 2, 5, 1, 6, 9, 0, 2]
# # print(len(l))

# predictions_goals_home = '-2.5'

# predictions_goals_home = predictions_goals_home.replace("-", "")
# predictions_goals_home = math.ceil(float(predictions_goals_home))
# predictions_goals_home = round(float(predictions_goals_home)+ 0.1)

# print(predictions_goals_home)


# from datetime import datetime, timedelta

# date = datetime.now().strftime("%Y-%m-%dT%H:%M")
# # date1 = datetime.strptime(date, "%Y-%m-%dT%H:%M")
# date2 = date - timedelta(minutes=5)


# print(date2)
# team_a = 'name1'
# team_b = 'name2'
# fouls_yel_team1 = '2'
# fouls_yel_team2 = '0'
# fouls_red_team1 = '0'
# fouls_red_team2 = '2'


# yellow_home = f"<p>{team_a} *жёлтую* карточку получил(и): </p><p>{fouls_yel_team1}</p>"
# yellow_away = f"<p>{team_b} *жёлтую* карточку получил(и): </p><p>{fouls_yel_team2}</p>"
# red_home = f"<p>{team_a} *красную* карточку получил(и): </p><p>{fouls_red_team1}</p>"
# red_away = f"<p>{team_b} *красную* карточку получил(и): </p><p>{fouls_red_team2}</p>"

# if fouls_yel_team1 != [] or fouls_yel_team2 != [] or fouls_red_team1 != [] or fouls_red_team2 != []:
#     title = f"<h3>Наказания:</h3>"
    
#     if fouls_yel_team1 != []:
#         fouls_y_home = f'{yellow_home}'
#     elif fouls_yel_team1 == []:
#         fouls_y_home = ''

#     if fouls_yel_team2 != []:
#         fouls_y_away = f"{yellow_away}"
#     elif fouls_yel_team2 == []:
#         fouls_y_away = ''

#     if fouls_red_team1 != []:
#         fouls_r_home = f"{red_home}"
#     elif fouls_red_team1 == []:
#         fouls_r_home = ''

#     if fouls_red_team2 != []:
#         fouls_r_away = f"{red_away}"
#     elif fouls_red_team2 == []:
#         fouls_r_away = ''
    
#     fouls = (
#         f"{title}{fouls_y_home}{fouls_y_away}{fouls_r_home}{fouls_r_away}"
#     )
# else:
#     fouls = f"<h3>Наказания:</h3><p>В этом матче фолов нет</p>"


# all_scorers= []

# if all_scorers != []:
#     title = f"<p><b>Авторы голов:</b></p>"
#     if all_scorers != []:
#         scorers = f"{all_scorers}"
#     elif all_scorers == []:
#         scorers = ''


#     goals = f"{title}<p>{all_scorers}<br></p>"
# else:
#     goals = ''


import base64
import hashlib
import os

# import boto3
# access_key = 'KEY'
# secret_access_key = 'KEYu'


# contents = "hello world!"
# md = hashlib.md5(contents.encode('utf-8')).digest()
# contents_md5 = base64.b64encode(md).decode('utf-8')

# client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)

# client.upload_file('/root/result/img_preview/878003_preview.png', 'botbot-buckets-football', 'preview/878003_preview.png', ExtraArgs={'ACL':'public-read'})
# res = client.put_object_acl(ACL='public-read', bucket='2', key='1')

# r = client.put_object(ACL='public-read', Body='/root/result/img_preview/868034_preview.png', Bucket='botbot-buckets-football', Key='preview/868034_preview.png', ContentMD5='AKIAXNURKQRLLY3CBDVL:7zrCnXvcAWGrjoWV/5Ap0Cz1/pHtYYUBHdPnSTau', ContentType='image/png')





# client.meta.upload_file('/root/result/img_preview/871550_preview.png', 'botbot-buckets-football', 'preview/871550_preview.png')
# s3 = boto3.resource('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)
# s3.meta.client.upload_file('/root/result/img_preview/871550_preview.png', 'botbot-buckets-football', 'preview/871550_preview.png')
