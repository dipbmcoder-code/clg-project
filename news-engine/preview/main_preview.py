#!/opt/envs/venv_310/bin/python3

# Запуск:
# Переходим в папку visual
# пишем команду: python3 ../main_preview.py

# ФУНКЦИЯ ДЛЯ ПРЕВЬЮ МАТЧА
# Импорт для АПИ
import requests
import sys
import os
from dotenv import load_dotenv
import ast
import json
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
# Импорт для даты
from datetime import datetime, timezone, timedelta

# Импорт функции запроса в БД
from preview.graph_old_prev import insert_preview_match_api
from preview.db_preview import check_fixture_match, insert_db, check_fixture_match_preview_post
from preview.text_preview import preview_match_text
from preview.text_visual_preview import output_visual_text, output_visual_gemini_text

from publication.app_test import main_publication
from publication.cms_db import get_leagues_id, get_websites, filter_websites_by_leagues, filter_websites_by_enable, get_max_hours
from publication.rapidapi import get_fixtures_by_league, get_league_by_id

from publication.save_img_aws import save_aws, delete_img
from publication.cms_logs import insert_news_log
import publication.message_tracker as message_tracker
import publication.module_failure_tracker as module_failure_tracker
from publication.utils import check_api_quota, send_quota_alert_email
load_dotenv()

print("🕓 Cron job started for: preview")

# Check API quota before processing
quota_available, quota_error = check_api_quota()
if not quota_available:
    print(f"🚨 API Quota Exceeded: {quota_error}")
    send_quota_alert_email(quota_error)
    print("📧 Alert email sent to administrators")
    print("⛔ Exiting cron job - quota must be resolved before processing")
    sys.exit(0)  # Exit gracefully

types = 'preview'
websites = get_websites()
websites = filter_websites_by_enable(websites, types)
#raise ValueError("Age cannot be negative!")
list_league_id = get_leagues_id(websites)
list_league_id = list_league_id if list_league_id else []

# list_league_id = ['12', '20', '973', '186', '1164', '233', '570', '276', '200', '399', '288', '202', '567', '585', '400']
# list_league_id = ['570']
# print(list_league_id)
# exit()
def check_matches_date(list_dates):
    raw_fixture = []

    for league_id, date_str in list_dates:
        # получение сезона по Лиге
        
        season = get_league_by_id(league_id)['seasons'][-1]['year']
        
        # цикл по определенным дням
        # for date_element in list_date:
            # получение данных по матчу
        raw_fixture.extend(
            [[element['fixture']['id'], element['fixture']['date'][:16],league_id] for element in get_fixtures_by_league(league_id, season, date_str)]
        )
   
    return raw_fixture

# Ближайшие матчи-
def check_match():
    global list_league_id
    global get_league_by_id
    global get_fixtures_by_league
    raw_fixture = []
   
    for league_id in list_league_id:
        # получение сезона по Лиге
        season = get_league_by_id(league_id)['seasons'][-1]['year']
        # print(season)
        raw_fixture.extend(
            [
                [element['fixture']['id'], element['fixture']['date'][:16],league_id] for element in get_fixtures_by_league(league_id, season)]
        )

    return raw_fixture


#['868122', '868123', '868117', '868116', '868118', '868120', '868121', '868125', '868119', '868124']
# Сохранение результаты в переменные


search_method = os.getenv('PREVIEW_SEARCH_METHOD') #! 'future'

# search all day long
current_date = datetime.now()

# Add 48 hours (2 days)
# new_date = current_date + timedelta(hours=int(get_max_hours(websites, types) or 0))

new_dates = {(league['id'], (current_date + timedelta(hours=int(website.get('match_previews_time')) or 0)).strftime("%Y-%m-%d")) for website in websites if website.get('website_leagues') for league in website.get('website_leagues')}
# Format the new date as "YYYY-MM-DD"
# formatted_date = new_date.strftime("%Y-%m-%d")
# list_days = formatted_date
# list_days = '2025-04-01'
# print(count)
# exit()
# l_fixture = api
l_fixture = check_matches_date(new_dates) if search_method == 'all_day' else check_match()

# print(list_days)
# print(l_fixture)
# exit()
# Цикл по ближайшим матчам + проверка + запуск генерации запросов в АПИ
print("cron job started")
for fixture, fixture_date, league_id in l_fixture:

    # exit()
        
    # 1 Проверка есть ли в БД данный fixture_match
    if not check_fixture_match(fixture):
        
        # 1.1 Запуск запросов данных с АПИ + сохранение в БД
        insert_preview_match_api(fixture_match=fixture)
        
        
    if check_fixture_match(fixture):
        # print('1111111111111111111111111')
        # exit()

        # 2 Текст 
        preview_match_text(fixture)
        website_ids = []
        for website in filter_websites_by_leagues(websites, league_id):
            # Дата ближайших матчей
            time_match = datetime.strptime(fixture_date, "%Y-%m-%dT%H:%M")
            formatted_time_utc = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            current_time_gmt_parsed = datetime.strptime(formatted_time_utc, '%Y-%m-%d %H:%M:%S')
            # print(formatted_time_utc)
            # print(time_match - timedelta(hours=int(os.getenv('HOURS')), minutes=int(os.getenv('MINUTES'))))
            # exit()
            # Проверка по дате
            if current_time_gmt_parsed >= time_match - timedelta(hours=int(website.get('match_previews_time') or 0)):
                l_version = website.get('l_version') if website.get('l_version') else 'eng'
                website_ids.append(website["documentId"])
                if not check_fixture_match_preview_post(fixture, website['documentId']):
                    
                    # Add initial log message
                    message_tracker.add_message(
                        types,
                        message_tracker.MessageStage.RECORD_INSERTION,
                        message_tracker.MessageStatus.SUCCESS,
                        f"Log perform for fixture - {fixture}"
                    )
                    
                    title = ""
                    workflow_success = False
                    try:
                        # 3 Визуализация
                        #output_visual_text(fixture) # пример поиска файла :
                        
                        output_visual_gemini_text(fixture, l_version, types, website) # {fixture_match}_away.png
                        # start_preview_graph(fixture_m[check_time]) #Проблема, цикл останавливается здесь

                        # сохранение файла aws
                        save_aws(fixture, l_version, types)
                        # Публикация на сайт
                        # try:
                        published = main_publication(fixture, types, league_id, website)
                        if published:
                            title = published.get('title', '')
                            workflow_success = True
                        else:
                            website_ids.pop()
                        # except Exception:
                        #     continue
                    except Exception as e:
                        print(f"❌ Error in preview workflow: {e}")
                        message_tracker.add_message(
                            types,
                            message_tracker.MessageStage.PUBLICATION,
                            message_tracker.MessageStatus.ERROR,
                            f"Workflow error: {str(e)}"
                        )
                    finally:
                        delete_img(fixture, l_version, types)
                        
                        messages_json = message_tracker.get_messages_json(types)
                        overall_status = message_tracker.get_overall_status(types)
                        image_generated = message_tracker.was_image_generated(types)

                        insert_news_log(
                            news_type=types,
                            news_title=f"{title}",
                            website_name=website.get('platform_name', 'Unknown Website'),
                            image_generated=image_generated,
                            news_status=overall_status,
                            message=messages_json
                        )
                        
                        # Track failure/success for module deactivation
                        # Failure if: overall status is Failed OR workflow had exception
                        if overall_status == 'Failed' or not workflow_success:
                            module_disabled = module_failure_tracker.increment_failure(types)
                            if module_disabled:
                                print(f"🛑 Module '{types}' has been disabled. Exiting workflow...")
                                sys.exit(1)  # Exit immediately when module is disabled
                        else:
                            module_failure_tracker.reset_failure(types)

                        # Clear messages for this key
                        message_tracker.clear_messages(types)
        if len(website_ids) > 0:
            website_ids = f"'{json.dumps(website_ids)}'::jsonb"
            update_query = (
                f"UPDATE match_preview "
                f"SET is_posted = TRUE, "
                f"posted_datetime = NOW(), "
                f"website_ids = {website_ids} "
                f"WHERE fixture_match = {fixture} ;"
            )
            insert_db(update_query, 'post_preview')
        
print("cron job finished")

