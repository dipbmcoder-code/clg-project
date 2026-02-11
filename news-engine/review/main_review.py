#!/opt/envs/venv_310/bin/python3



# #Сделать запрос к db - fixture match
# #Условие 1, если дата матча = дата сейчас - 105 минут
# #Условие 2, Делаем запрос к апи и смотрим статус 

# from review_text import check_review_match
from datetime import datetime, timezone, timedelta
import os
import sys
from time import sleep
import json
from dotenv import load_dotenv
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
load_dotenv()
from review.db import get_data, get_date, get_fixture_match,get_league, check_fixture_match, check_fixture_match_review_post,insert_db
from review.text_review import start_review_text
from review.insert_review_api import insert_review_match_api
from review.pillow2_football_review import start_review_image, start_gemini_review_image
from review.save_review_img_aws import save_review_aws, delete_review_img
from review.graph_review import start_review_graph
from review.img_lineups import start_img_review_lineups

from publication.app_test import main_publication
from publication.cms_db import get_websites, filter_websites_by_leagues, check_enable_for, filter_websites_by_enable, get_min_minutes
from publication.rapidapi import get_fixture_by_id
from publication.cms_logs import insert_news_log
import publication.message_tracker as message_tracker
import publication.module_failure_tracker as module_failure_tracker
from publication.utils import check_api_quota, send_quota_alert_email

print("🕓 Cron job started for: review")

# Check API quota before processing
quota_available, quota_error = check_api_quota()
if not quota_available:
    print(f"🚨 API Quota Exceeded: {quota_error}")
    send_quota_alert_email(quota_error)
    print("📧 Alert email sent to administrators")
    print("⛔ Exiting cron job - quota must be resolved before processing")
    sys.exit(0)  # Exit gracefully

def check_status(fixture_match):
    global get_fixture_by_id
    data_check = get_fixture_by_id(fixture_match)
    return data_check['fixture']['status']['long'] if data_check else None
    


# Получение fixture_match. Все матчи которые будут проводиться сегодня
websites = get_websites()
types = "review"
website = filter_websites_by_enable(websites, types)
if check_enable_for(websites, types):
    types_search = os.getenv('REVIEW_SEARCH_METHOD')
    list_date = ['2025-04-01']
    list_fixture_match = get_fixture_match('list' if types_search == 'list' else 'all_day', list_date if types_search == 'list' else [])
    # print(list_fixture_match)
    # exit()
    # list_fixture_match = ['868076', '868077', '868078', '868079', '868080', '868081', '868082', '868083', '868084', '868085']
    # date_m =['2022-10-29T14:00', '2022-10-30T14:00', '2022-10-29T14:00', '2022-10-29T14:00', '2022-10-29T14:00', '2022-10-29T16:30', '2022-10-29T11:30','2022-10-29T18:45','2022-10-30T16:15','2022-10-29T14:00']
    # list_fixture_match = ['878028', '878014', '878013', '878018', '878016', '878021', '878015', '878020', '878012', '878019', '878017', '878009', '878010', '878005', '878008', '878004', '878007', '878006', '878002', '878003', '878011', '877993', '877999', '877995', '878000', '877997', '877992', '877996', '877994', '878001', '877998', '877987', '877983', '877984', '877989', '877991', '877982', '877990', '877985', '877986', '877988', '877980', '877978', '877977', '877972', '877973', '877975', '877974', '877976', '877981', '877979', '877969', '877968', '877966', '877962', '877965', '877967', '877971', '877964', '877963', '877970', '877959', '877961', '877957', '877953', '877952', '877954', '877958', '877960', '877956', '877955', '877944', '877949', '877942', '877948', '877951', '877946', '877943', '877950', '877945', '877947']
    # list_fixture_match = ['868122', '868123', '868117', '868116', '868118', '868120', '868121', '868125', '868119', '868124']
    # list_fixture_match = ['898731', '898734','898735']   
    #Full
    # list_fixture_match = ['868044', '868041', '868037', '868045', '868040', '868038', '868042', '868039', '868043', '868036', '868031', '868030', '868033', '868035', '868032', '868026', '868028', '868029', '868034', '868027', '868019', '868020', '868021', '868017', '868024', '868018', '868022', '868025', '868023', '868016', '868010', '868008', '868015', '868007', '868013', '868014', '868012', '868011', '868006', '868009', '868001', '867998', '867996', '868005', '868004', '868003', '868002', '867999', '867997', '868000', '867990', '867994', '867991', '867986', '867995', '867987', '867989', '867993', '867988', '867992', '867983', '867985', '867977', '867976', '867982', '867981', '867980', '867979', '867978', '867984', '867972', '867973', '867970', '867975', '867966', '867971', '867969', '867968', '867967', '867974', '867961', '867960', '867963', '867958', '867959', '867956', '867962', '867964', '867965', '867957', '867955', '867954', '867950', '867953', '867952', '867951', '867949', '867948', '867947', '871243', '871244', '871240', '871236', '871242', '871241', '871238', '871237', '871239', '871234', '871233', '871235', '871232', '871231', '871230', '871229', '871228', '871227', '871224', '871223', '871221', '871219', '871226', '871218', '871220', '871225', '871222', '871211', '871212', '871216', '871215', '871214', '871213', '871210', '871209', '871217', '871203', '871207', '871204', '871202', '871205', '871206', '871201', '871208', '871200', '871199', '871194', '871191', '871198', '871197', '871196', '871195', '871192', '871193', '871188', '871186', '871184', '871189', '871187', '871183', '871182', '871190', '871185', '871173', '871177', '871180', '871179', '871178', '871181', '871175', '871174', '871176', '871167', '871172', '871165', '871170', '871169', '871168', '871171', '871166', '871164', '871562', '871568', '871567', '871564', '871561', '871560', '871563', '871569', '871566', '871565', '871556', '871552', '871558', '871550', '871551', '871559', '871554', '871555', '871557', '871553', '871546', '871542', '871541', '871548', '871545', '871547', '871549', '871543', '871544', '871540', '871531', '871538', '871530', '871539', '871532', '871533', '871537', '871534', '871535', '871536', '871483', '871525', '871529', '871522', '871527', '871528', '871520', '871524', '871523', '871526', '871521', '871518', '871519', '871516', '871515', '871512', '871517', '871510', '871511', '871513', '871514', '871505', '871508', '871509', '871507', '871504', '871502', '871503', '871506', '871501', '871500', '871493', '871498', '871494', '871499', '871492', '871491', '871497', '871496', '871490', '871495', '871487', '871485', '871489', '871488', '871481', '871480', '871486', '871482', '871484', '871478', '871471', '871479', '871477', '871476', '871475', '871473', '871472', '871470', '881862', '881865', '881861', '881869', '881866', '881864', '881868', '881860', '881863', '881867', '881852', '881854', '881850', '881859', '881858', '881856', '881855', '881851', '881853', '881857', '881843', '881845', '881841', '881842', '881844', '881849', '881848', '881847', '881840', '881846', '881832', '881834', '881835', '881836', '881839', '881831', '881830', '881838', '881833', '881837', '881829', '881828', '881827', '881826', '881825', '881824', '881823', '881822', '881821', '881820', '881819', '881818', '881817', '881816', '881814', '881813', '881815', '881812', '881811', '881810', '881809', '881808', '881807', '881806', '881805', '881804', '881803', '881802', '881801', '881800', '881799', '881798', '881797', '881796', '881795', '881794', '881793', '881792', '881791', '881790', '881789', '881788', '881787', '881786', '881785', '881784', '881783', '881782', '881780', '881781', '878014', '878013', '878018', '878016', '878021', '878015', '878020', '878012', '878019', '878017', '878009', '878010', '878005', '878008', '878004', '878007', '878006', '878002', '878003', '878011', '877993', '877995', '877999', '878000', '877997', '877992', '877996', '877994', '878001', '877998', '877987', '877983', '877984', '877989', '877991', '877982', '877990', '877985', '877986', '877988', '877980', '877978', '877977', '877972', '877973', '877975', '877974', '877976', '877981', '877979', '877969', '877968', '877966', '877962', '877965', '877967', '877971', '877964', '877963', '877970', '877959', '877961', '877957', '877953', '877952', '877954', '877958', '877960', '877956', '877955', '877944', '877949', '877942', '877948', '877951', '877946', '877943', '877950', '877945', '877947', '898684', '898683', '898679', '898682', '898678', '898681', '898677', '898680', '898676', '898667', '898674', '898672', '898670', '898673', '898675', '898669', '898671', '898668', '898665', '898663', '898661', '898666', '898664', '898658', '898662', '898659', '898660', '898649', '898655', '898657', '898650', '898653', '898652', '898651', '898654', '898656', '898644', '898645', '898642', '898647', '898641', '898640', '898646', '898643', '898648', '898630', '898632', '898635', '898633', '898639', '898638', '898634', '898637', '898636', '898631', '898623', '898624', '898627', '898622', '898626', '898628', '898625', '898629', '898619', '898621', '898616', '898613', '898614', '898618', '898615', '898620', '898617', '898607', '898611', '898606', '898609', '898610', '898612', '898608', '898604', '898605']

    print("cron job started")
    # current_datetime = datetime.now()
    # current_gmt_datetime = datetime.now(timezone.utc)
    # print("Server Time",current_datetime)
    # print("GTM Time",current_gmt_datetime)
    if list_fixture_match != False:
        
        for check_time_for_review in range(len(list_fixture_match)):
            
            league = get_league(list_fixture_match[check_time_for_review])
            

            # Получение даты и времени матча по fixture_match
            # print(list_fixture_match[check_time_for_review])
            time_match = datetime.strptime(get_date(list_fixture_match[check_time_for_review]), "%Y-%m-%dT%H:%M") 
            current_datetime = datetime.now()
            # print(current_datetime)
            # exit()
# Format it in the desired format
            # formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            # formatted_datetime = datetime.strptime(formatted_datetime, "%Y-%m-%d %H:%M:%S")

            
            # print(check_status(fixture_match=list_fixture_match[check_time_for_review]))
            # print(datetime.now())
            # print(time_match + timedelta(minutes=105))

            # Проверка по дате
            formatted_time_utc = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            current_time_gmt_parsed = datetime.strptime(formatted_time_utc, '%Y-%m-%d %H:%M:%S')
            # print(formatted_time_utc)
            # print(current_time_gmt_parsed)
            # print(time_match + timedelta(minutes=105))
            # exit()
            if current_time_gmt_parsed >= time_match + timedelta(minutes=get_min_minutes(websites, types)):
                # print(time_match + timedelta(minutes=105))
                # exit()
                    
                #Проверяю статус матча
                if check_status(fixture_match=list_fixture_match[check_time_for_review]) == 'Match Finished':
                    if check_fixture_match(list_fixture_match[check_time_for_review]) == False:
                        # Сохранение
                        insert_review_match_api(fixture_match=list_fixture_match[check_time_for_review])
                        sleep(5)

                    # Создание json
                    start_review_text(list_fixture_match[check_time_for_review])
                    website_ids = []
                    for website in filter_websites_by_leagues(websites, league[0]):
                        website_ids.append(website["documentId"])
                        if check_fixture_match_review_post(list_fixture_match[check_time_for_review], website["documentId"]) == False:
                            
                            # Add initial log message
                            message_tracker.add_message(
                                types,
                                message_tracker.MessageStage.RECORD_INSERTION,
                                message_tracker.MessageStatus.SUCCESS,
                                f"Log perform for fixture - {list_fixture_match[check_time_for_review]}"
                            )
                            
                            title = ""
                            workflow_success = False
                            try:
                                #start_review_image(fixture_match=list_fixture_match[check_time_for_review])
                                
                                start_gemini_review_image(fixture_match=list_fixture_match[check_time_for_review], website=website)
                                start_review_graph(fixture_match=list_fixture_match[check_time_for_review])
                                start_img_review_lineups(fixture_match=list_fixture_match[check_time_for_review])
                                # Сохранение файла в aws
                                save_review_aws(list_fixture_match[check_time_for_review], types)
                                # Создание и публикация поста
                                # try:
                                published = main_publication(list_fixture_match[check_time_for_review], types,league[0], website)
                                if published:
                                    title = published.get('title', '')
                                    workflow_success = True
                                else:
                                    website_ids.pop()
                                # except Exception:
                                #     continue
                            except Exception as e:
                                print(f"❌ Error in review workflow: {e}")
                                message_tracker.add_message(
                                    types,
                                    message_tracker.MessageStage.PUBLICATION,
                                    message_tracker.MessageStatus.ERROR,
                                    f"Workflow error: {str(e)}"
                                )
                            finally:
                                # Удаление изображений
                                delete_review_img(list_fixture_match[check_time_for_review], types)
                                
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
                            f"UPDATE match_review "
                            f"SET is_posted = TRUE, "
                            f"posted_datetime = NOW(), "
                            f"website_ids = {website_ids} "
                            f"WHERE fixture_match = '{list_fixture_match[check_time_for_review]}' ;"
                        )
                        insert_db(update_query, 'post_review')
    print("cron job finished")
