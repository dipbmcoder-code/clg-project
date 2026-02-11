# data_tags = {
#             "English Premier League": {
#                 "id":"3",
#                 "Manchester City":"8",
#                 "Liverpool":"11",
#                 "Arsenal":"22",
#                 "Aston Villa":"23",
#                 "Bournemouth":"24",
#                 "Brentford":"25",
#                 "Brighton & Hove Albion":"26",
#                 "Chelsea":"27",
#                 "Crystal Palace":"28",
#                 "Everton":"29",
#                 "Fulham":"30",
#                 "Leeds":'31',
#                 "Leicester City":'32',
#                 "Manchester United":"9",
#                 "Newcastle United":"33",
#                 "Nottingham Forest":"34",
#                 "Southampton":"35",
#                 "Tottenham Hotspur":"36",
#                 "West Ham United":"37",
#                 "Wolverhampton Wanderers":"38"
#                 },
#             "La Liga" : {
#                 "id":"4",
#                 "Barcelona":"12", 
#                 "Real Madrid":"13",
#                 "Almeria":"39",
#                 "Athletic Bilbao":"40",
#                 "Atletico Madrid":"41",
#                 "Cádiz":"42",
#                 "Celta Vigo":"43",
#                 "Elche":"44",
#                 "Espanyol":"45",
#                 "Getafe":"46",
#                 "Girona":"47",
#                 "Mallorca":"48",
#                 "Osasuna":"49",
#                 "Rayo Vallecano":"50",
#                 "Real Betis":"51",
#                 "Real Sociedad":"52",
#                 "Sevilla":"53",
#                 "Valencia":"54",
#                 "Valladolid":"55",
#                 "Villarreal":"56",
#                 "Athletic Club":"57"
#                 },
#             "Ligue 1" : {
#                 "id":"7",
#                 "PSG":"14", 
#                 "Marseille":"15",
#                 "Ajaccio":"58",
#                 "Angers":"59",
#                 "Auxerre":"60",
#                 "Brest":"61",
#                 "Clermont":"62",
#                 "Lens":"63",
#                 "Lille":"64",
#                 "Lorient":"65",
#                 "Lyon":"66",
#                 "Monaco":"67",
#                 "Montpellier":"68",
#                 "Nantes":"69",
#                 "Nice":"70",
#                 "Reims":"71",
#                 "Rennes":"72",
#                 "Strasbourg":"73",
#                 "Toulouse":"74",
#                 "Troyes":"75",
#                 },
#             "Serie A" :{
#                 "id":"5",
#                 "Napoli":"16", 
#                 "Atalanta":"17",
#                 "Bologna":"76",
#                 "Cremonese":"21",
#                 "Empoli":"77",
#                 "Fiorentina":"78",
#                 "Hellas Verona":"79",
#                 "Inter Milan":"80",
#                 "Juventus":"81",
#                 "Lazio":"82",
#                 "AC Milan":"83",
#                 "Monza":"84",
#                 "Roma":"85",
#                 "Salernitana":"86",
#                 "Sampdoria":"87",
#                 "Sassuolo":"88",
#                 "Spezia":"89",
#                 "Torino":"90",
#                 "Udinese":"91",

#                 },
#             "Bundesliga" : {
#                 "id":"6",
#                 "Union Berlin":"18", 
#                 "Eintracht Frankfurt":"92",
#                 "SC Freiburg":"19",  #TODO SC Freiburg
#                 "FC Augsburg":"94",
#                 "Hertha Berlin":"95",
#                 "VfL BOCHUM":"96",
#                 "Werder Bremen":"97",
#                 "Borussia Dortmund":"98",
#                 "1899 Hoffenheim":"99",
#                 "FC Koln":"100",  #TODO
#                 "RB Leipzig":"101",
#                 "Bayer Leverkusen":"102",
#                 "FSV Mainz 05":"103", #TODO Mainz 05
#                 "Borussia Monchengladbach":"104", #TODO Borussia Mönchengladbach
#                 "Bayern Munich":"105",
#                 "FC Schalke 04":"106",
#                 "VfB Stuttgart":"107", #TODO
#                 "VfL Wolfsburg":"108", #TODO

#                 }
#     }
    
# team1 = 's Wolfsburg'
# team2 = ''
# league_name = 'Bundesliga'


# if team1 in data_tags[league_name]:
#     print('123')
# l1=['{rank[0]}','{rank[1]}','{rank[2]}','{rank[3]}','{rank[4]}','{rank[5]}','{rank[6]}','{rank[7]}','{rank[8]}','{rank[9]}','{rank[10]}','{rank[11]}','{rank[12]}','{rank[13]}','{rank[14]}','{rank[15]}','{rank[16]}','{rank[17]}','{rank[18]}','{rank[19]}', '{all_games[0]}','{all_games[1]}','{all_games[2]}','{all_games[3]}','{all_games[4]}','{all_games[5]}','{all_games[6]}','{all_games[7]}','{all_games[8]}','{all_games[9]}','{all_games[10]}','{all_games[11]}','{all_games[12]}','{all_games[13]}','{all_games[14]}','{all_games[15]}','{all_games[16]}','{all_games[17]}','{all_games[18]}','{all_games[19]}','{win_games[0]}','{win_games[1]}','{win_games[2]}','{win_games[3]}','{win_games[4]}','{win_games[5]}','{win_games[6]}','{win_games[7]}','{win_games[8]}','{win_games[9]}','{win_games[10]}','{win_games[11]}','{win_games[12]}','{win_games[13]}','{win_games[14]}','{win_games[15]}','{win_games[16]}','{win_games[17]}','{win_games[18]}','{win_games[19]}' , '{draw_games[0]}','{draw_games[1]}','{draw_games[2]}','{draw_games[3]}','{draw_games[4]}','{draw_games[5]}','{draw_games[6]}','{draw_games[7]}','{draw_games[8]}','{draw_games[9]}','{draw_games[10]}','{draw_games[11]}','{draw_games[12]}','{draw_games[13]}','{draw_games[14]}','{draw_games[15]}','{draw_games[16]}','{draw_games[17]}','{draw_games[18]}','{draw_games[19]}', '{lose_games[0]}','{lose_games[1]}','{lose_games[2]}','{lose_games[3]}','{lose_games[4]}','{lose_games[5]}','{lose_games[6]}','{lose_games[7]}','{lose_games[8]}','{lose_games[9]}','{lose_games[10]}','{lose_games[11]}','{lose_games[12]}','{lose_games[13]}','{lose_games[14]}','{lose_games[15]}','{lose_games[16]}','{lose_games[17]}','{lose_games[18]}','{lose_games[19]}', '{goals_for[0]}','{goals_for[1]}','{goals_for[2]}','{goals_for[3]}','{goals_for[4]}','{goals_for[5]}','{goals_for[6]}','{goals_for[7]}','{goals_for[8]}','{goals_for[9]}','{goals_for[10]}','{goals_for[11]}','{goals_for[12]}','{goals_for[13]}','{goals_for[14]}','{goals_for[15]}','{goals_for[16]}','{goals_for[17]}','{goals_for[18]}','{goals_for[19]}', '{goals_missed[0]}','{goals_missed[1]}','{goals_missed[2]}','{goals_missed[3]}','{goals_missed[4]}','{goals_missed[5]}','{goals_missed[6]}','{goals_missed[7]}','{goals_missed[8]}','{goals_missed[9]}','{goals_missed[10]}','{goals_missed[11]}','{goals_missed[12]}','{goals_missed[13]}','{goals_missed[14]}','{goals_missed[15]}','{goals_missed[16]}','{goals_missed[17]}','{goals_missed[18]}','{goals_missed[19]}', '{goals_diff[0]}','{goals_diff[1]}','{goals_diff[2]}','{goals_diff[3]}','{goals_diff[4]}','{goals_diff[5]}','{goals_diff[6]}','{goals_diff[7]}','{goals_diff[8]}','{goals_diff[9]}','{goals_diff[10]}','{goals_diff[11]}','{goals_diff[12]}','{goals_diff[13]}','{goals_diff[14]}','{goals_diff[15]}','{goals_diff[16]}','{goals_diff[17]}','{goals_diff[18]}','{goals_diff[19]}', '{points[0]}','{points[1]}','{points[2]}','{points[3]}','{points[4]}','{points[5]}','{points[6]}','{points[7]}','{points[8]}','{points[9]}','{points[10]}','{points[11]}','{points[12]}','{points[13]}','{points[14]}','{points[15]}','{points[16]}','{points[17]}','{points[18]}','{points[19]}', '{name_teams[0]}','{name_teams[1]}','{name_teams[2]}','{name_teams[3]}','{name_teams[4]}','{name_teams[5]}','{name_teams[6]}','{name_teams[7]}','{name_teams[8]}','{name_teams[9]}','{name_teams[10]}','{name_teams[11]}','{name_teams[12]}','{name_teams[13]}','{name_teams[14]}','{name_teams[15]}','{name_teams[16]}','{name_teams[17]}','{name_teams[18]}','{name_teams[19]}', '{form_all[0]}','{form_all[1]}','{form_all[2]}','{form_all[3]}','{form_all[4]}','{form_all[5]}','{form_all[6]}','{form_all[7]}','{form_all[8]}','{form_all[9]}','{form_all[10]}','{form_all[11]}','{form_all[12]}','{form_all[13]}','{form_all[14]}','{form_all[15]}','{form_all[16]}','{form_all[17]}','{form_all[18]}','{form_all[19]}', '{logo_table[0]}','{logo_table[1]}','{logo_table[2]}','{logo_table[3]}','{logo_table[4]}','{logo_table[5]}','{logo_table[6]}','{logo_table[7]}','{logo_table[8]}','{logo_table[9]}','{logo_table[10]}','{logo_table[11]}','{logo_table[12]}','{logo_table[13]}','{logo_table[14]}','{logo_table[15]}','{logo_table[16]}','{logo_table[17]}','{logo_table[18]}','{logo_table[19]}']
# l2=[rank[0],rank[1],rank[2],rank[3],rank[4],rank[5],rank[6],rank[7],rank[8],rank[9],rank[10],rank[11],rank[12],rank[13],rank[14],rank[15],rank[16],rank[17],rank[18],rank[19], all_games[0],all_games[1],all_games[2],all_games[3],all_games[4],all_games[5],all_games[6],all_games[7],all_games[8],all_games[9],all_games[10],all_games[11],all_games[12],all_games[13],all_games[14],all_games[15],all_games[16],all_games[17],all_games[18],all_games[19],win_games[0],win_games[1],win_games[2],win_games[3],win_games[4],win_games[5],win_games[6],win_games[7],win_games[8],win_games[9],win_games[10],win_games[11],win_games[12],win_games[13],win_games[14],win_games[15],win_games[16],win_games[17],win_games[18],win_games[19] , draw_games[0],draw_games[1],draw_games[2],draw_games[3],draw_games[4],draw_games[5],draw_games[6],draw_games[7],draw_games[8],draw_games[9],draw_games[10],draw_games[11],draw_games[12],draw_games[13],draw_games[14],draw_games[15],draw_games[16],draw_games[17],draw_games[18],draw_games[19], lose_games[0],lose_games[1],lose_games[2],lose_games[3],lose_games[4],lose_games[5],lose_games[6],lose_games[7],lose_games[8],lose_games[9],lose_games[10],lose_games[11],lose_games[12],lose_games[13],lose_games[14],lose_games[15],lose_games[16],lose_games[17],lose_games[18],lose_games[19], goals_for[0],goals_for[1],goals_for[2],goals_for[3],goals_for[4],goals_for[5],goals_for[6],goals_for[7],goals_for[8],goals_for[9],goals_for[10],goals_for[11],goals_for[12],goals_for[13],goals_for[14],goals_for[15],goals_for[16],goals_for[17],goals_for[18],goals_for[19], goals_missed[0],goals_missed[1],goals_missed[2],goals_missed[3],goals_missed[4],goals_missed[5],goals_missed[6],goals_missed[7],goals_missed[8],goals_missed[9],goals_missed[10],goals_missed[11],goals_missed[12],goals_missed[13],goals_missed[14],goals_missed[15],goals_missed[16],goals_missed[17],goals_missed[18],goals_missed[19], goals_diff[0],goals_diff[1],goals_diff[2],goals_diff[3],goals_diff[4],goals_diff[5],goals_diff[6],goals_diff[7],goals_diff[8],goals_diff[9],goals_diff[10],goals_diff[11],goals_diff[12],goals_diff[13],goals_diff[14],goals_diff[15],goals_diff[16],goals_diff[17],goals_diff[18],goals_diff[19], points[0],points[1],points[2],points[3],points[4],points[5],points[6],points[7],points[8],points[9],points[10],points[11],points[12],points[13],points[14],points[15],points[16],points[17],points[18],points[19], name_teams[0],name_teams[1],name_teams[2],name_teams[3],name_teams[4],name_teams[5],name_teams[6],name_teams[7],name_teams[8],name_teams[9],name_teams[10],name_teams[11],name_teams[12],name_teams[13],name_teams[14],name_teams[15],name_teams[16],name_teams[17],name_teams[18],name_teams[19], form_all[0],form_all[1],form_all[2],form_all[3],form_all[4],form_all[5],form_all[6],form_all[7],form_all[8],form_all[9],form_all[10],form_all[11],form_all[12],form_all[13],form_all[14],form_all[15],form_all[16],form_all[17],form_all[18],form_all[19], logo_table[0],logo_table[1],logo_table[2],logo_table[3],logo_table[4],logo_table[5],logo_table[6],logo_table[7],logo_table[8],logo_table[9],logo_table[10],logo_table[11],logo_table[12],logo_table[13],logo_table[14],logo_table[15],logo_table[16],logo_table[17],logo_table[18],logo_table[19]]
# list_fixture_match = ['868044', '868041', '868037', '868045', '868040', '868038', '868042', '868039', '868043', '868036', '868031', '868030', '868033', '868035', '868032', '868026', '868028', '868029', '868034', '868027', '868019', '868020', '868021', '868017', '868024', '868018', '868022', '868025', '868023', '868016', '868010', '868008', '868015', '868007', '868013', '868014', '868012', '868011', '868006', '868009', '868001', '867998', '867996', '868005', '868004', '868003', '868002', '867999', '867997', '868000', '867990', '867994', '867991', '867986', '867995', '867987', '867989', '867993', '867988', '867992', '867983', '867985', '867977', '867976', '867982', '867981', '867980', '867979', '867978', '867984', '867972', '867973', '867970', '867975', '867966', '867971', '867969', '867968', '867967', '867974', '867961', '867960', '867963', '867958', '867959', '867956', '867962', '867964', '867965', '867957', '867955', '867954', '867950', '867953', '867952', '867951', '867949', '867948', '867947', '871243', '871244', '871240', '871236', '871242', '871241', '871238', '871237', '871239', '871234', '871233', '871235', '871232', '871231', '871230', '871229', '871228', '871227', '871224', '871223', '871221', '871219', '871226', '871218', '871220', '871225', '871222', '871211', '871212', '871216', '871215', '871214', '871213', '871210', '871209', '871217', '871203', '871207', '871204', '871202', '871205', '871206', '871201', '871208', '871200', '871199', '871194', '871191', '871198', '871197', '871196', '871195', '871192', '871193', '871188', '871186', '871184', '871189', '871187', '871183', '871182', '871190', '871185', '871173', '871177', '871180', '871179', '871178', '871181', '871175', '871174', '871176', '871167', '871172', '871165', '871170', '871169', '871168', '871171', '871166', '871164', '871562', '871568', '871567', '871564', '871561', '871560', '871563', '871569', '871566', '871565', '871556', '871552', '871558', '871550', '871551', '871559', '871554', '871555', '871557', '871553', '871546', '871542', '871541', '871548', '871545', '871547', '871549', '871543', '871544', '871540', '871531', '871538', '871530', '871539', '871532', '871533', '871537', '871534', '871535', '871536', '871483', '871525', '871529', '871522', '871527', '871528', '871520', '871524', '871523', '871526', '871521', '871518', '871519', '871516', '871515', '871512', '871517', '871510', '871511', '871513', '871514', '871505', '871508', '871509', '871507', '871504', '871502', '871503', '871506', '871501', '871500', '871493', '871498', '871494', '871499', '871492', '871491', '871497', '871496', '871490', '871495', '871487', '871485', '871489', '871488', '871481', '871480', '871486', '871482', '871484', '871478', '871471', '871479', '871477', '871476', '871475', '871473', '871472', '871470', '881862', '881865', '881861', '881869', '881866', '881864', '881868', '881860', '881863', '881867', '881852', '881854', '881850', '881859', '881858', '881856', '881855', '881851', '881853', '881857', '881843', '881845', '881841', '881842', '881844', '881849', '881848', '881847', '881840', '881846', '881832', '881834', '881835', '881836', '881839', '881831', '881830', '881838', '881833', '881837', '881829', '881828', '881827', '881826', '881825', '881824', '881823', '881822', '881821', '881820', '881819', '881818', '881817', '881816', '881814', '881813', '881815', '881812', '881811', '881810', '881809', '881808', '881807', '881806', '881805', '881804', '881803', '881802', '881801', '881800', '881799', '881798', '881797', '881796', '881795', '881794', '881793', '881792', '881791', '881790', '881789', '881788', '881787', '881786', '881785', '881784', '881783', '881782', '881780', '881781', '878014', '878013', '878018', '878016', '878021', '878015', '878020', '878012', '878019', '878017', '878009', '878010', '878005', '878008', '878004', '878007', '878006', '878002', '878003', '878011', '877993', '877995', '877999', '878000', '877997', '877992', '877996', '877994', '878001', '877998', '877987', '877983', '877984', '877989', '877991', '877982', '877990', '877985', '877986', '877988', '877980', '877978', '877977', '877972', '877973', '877975', '877974', '877976', '877981', '877979', '877969', '877968', '877966', '877962', '877965', '877967', '877971', '877964', '877963', '877970', '877959', '877961', '877957', '877953', '877952', '877954', '877958', '877960', '877956', '877955', '877944', '877949', '877942', '877948', '877951', '877946', '877943', '877950', '877945', '877947', '898684', '898683', '898679', '898682', '898678', '898681', '898677', '898680', '898676', '898667', '898674', '898672', '898670', '898673', '898675', '898669', '898671', '898668', '898665', '898663', '898661', '898666', '898664', '898658', '898662', '898659', '898660', '898649', '898655', '898657', '898650', '898653', '898652', '898651', '898654', '898656', '898644', '898645', '898642', '898647', '898641', '898640', '898646', '898643', '898648', '898630', '898632', '898635', '898633', '898639', '898638', '898634', '898637', '898636', '898631', '898623', '898624', '898627', '898622', '898626', '898628', '898625', '898629', '898619', '898621', '898616', '898613', '898614', '898618', '898615', '898620', '898617', '898607', '898611', '898606', '898609', '898610', '898612', '898608', '898604', '898605']
# print(len(list_fixture_match))



# l = [rounds_for_text,league_id,city_first_match,venue_first_match,first_date_round,home_first_match,away_first_match,all_home_teams,all_away_teams,team_name_max_injuries,max_injuries,team_max_goals_league,max_goals_league,team_min_conceded_league,min_conceded_top_saves,team_max_clean_sheet_league,max_cleen_sheet_league,team_max_conceded_league,max_conceded_saves_league,team_min_goals_attack_league,min_goals_attack_league,team_max_without_scored_league,max_without_scored_league,wins_without_scored,loses_without_scored,draws_without_scored,team_max_conceded_goals_league,max_conceded_goals_league,wins_conceded_goals,loses_conceded_goals,draws_conceded_goals,goals_top_league_1,name_top_goals_league_1,goals_top_league_2,name_top_goals_league_2,goals_top_league_3,name_top_goals_league_3,goals_top_league_4,name_top_goals_league_4,goals_top_league_5,name_top_goals_league_5,assists_top_league_1,name_top_assists_league_1,assists_top_league_2,name_top_assists_league_2,assists_top_league_3,name_top_assists_league_3,assists_top_league_4,name_top_assists_league_4,assists_top_league_5,name_top_assists_league_5,saves_top_league_1,name_top_saves_league_1,saves_top_league_2,name_top_saves_league_2,saves_top_league_3,name_top_saves_league_3,saves_top_league_4,name_top_saves_league_4,saves_top_league_5,name_top_saves_league_5]
# ll = ['{rounds_for_text}', '{league_id}', '{city_first_match}', '{venue_first_match}', '{first_date_round}', '{home_first_match}', '{away_first_match}', '{all_home_teams}', '{all_away_teams}', '{team_name_max_injuries}', '{max_injuries}', '{team_max_goals_league}','{max_goals_league}','{team_min_conceded_league}', '{min_conceded_top_saves}', '{team_max_clean_sheet_league}', '{max_cleen_sheet_league}','{team_max_conceded_league}','{max_conceded_saves_league}', '{team_min_goals_attack_league}', '{min_goals_attack_league}', '{team_max_without_scored_league}', '{max_without_scored_league}', '{wins_without_scored}', '{loses_without_scored}', '{draws_without_scored}', '{team_max_conceded_goals_league}', '{max_conceded_goals_league}','{wins_conceded_goals}','{loses_conceded_goals}','{draws_conceded_goals}','{goals_top_league_1}','{name_top_goals_league_1}','{goals_top_league_2}','{name_top_goals_league_2}','{goals_top_league_3}','{name_top_goals_league_3}','{goals_top_league_4}','{name_top_goals_league_4}','{goals_top_league_5}','{name_top_goals_league_5}','{assists_top_league_1}','{name_top_assists_league_1}','{assists_top_league_2}','{name_top_assists_league_2}','{assists_top_league_3}','{name_top_assists_league_3}','{assists_top_league_4}','{name_top_assists_league_4}','{assists_top_league_5}','{name_top_assists_league_5}','{saves_top_league_1}','{name_top_saves_league_1}','{saves_top_league_2}','{name_top_saves_league_2}','{saves_top_league_3}','{name_top_saves_league_3}','{saves_top_league_4}','{name_top_saves_league_4}','{saves_top_league_5}','{name_top_saves_league_5}']

# l1=['{rank[0]}','{rank[1]}','{rank[2]}','{rank[3]}','{rank[4]}','{rank[5]}','{rank[6]}','{rank[7]}','{rank[8]}','{rank[9]}','{rank[10]}','{rank[11]}','{rank[12]}','{rank[13]}','{rank[14]}','{rank[15]}','{rank[16]}','{rank[17]}','{rank[18]}','{rank[19]}', '{all_games[0]}','{all_games[1]}','{all_games[2]}','{all_games[3]}','{all_games[4]}','{all_games[5]}','{all_games[6]}','{all_games[7]}','{all_games[8]}','{all_games[9]}','{all_games[10]}','{all_games[11]}','{all_games[12]}','{all_games[13]}','{all_games[14]}','{all_games[15]}','{all_games[16]}','{all_games[17]}','{all_games[18]}','{all_games[19]}','{win_games[0]}','{win_games[1]}','{win_games[2]}','{win_games[3]}','{win_games[4]}','{win_games[5]}','{win_games[6]}','{win_games[7]}','{win_games[8]}','{win_games[9]}','{win_games[10]}','{win_games[11]}','{win_games[12]}','{win_games[13]}','{win_games[14]}','{win_games[15]}','{win_games[16]}','{win_games[17]}','{win_games[18]}','{win_games[19]}' , '{draw_games[0]}','{draw_games[1]}','{draw_games[2]}','{draw_games[3]}','{draw_games[4]}','{draw_games[5]}','{draw_games[6]}','{draw_games[7]}','{draw_games[8]}','{draw_games[9]}','{draw_games[10]}','{draw_games[11]}','{draw_games[12]}','{draw_games[13]}','{draw_games[14]}','{draw_games[15]}','{draw_games[16]}','{draw_games[17]}','{draw_games[18]}','{draw_games[19]}', '{lose_games[0]}','{lose_games[1]}','{lose_games[2]}','{lose_games[3]}','{lose_games[4]}','{lose_games[5]}','{lose_games[6]}','{lose_games[7]}','{lose_games[8]}','{lose_games[9]}','{lose_games[10]}','{lose_games[11]}','{lose_games[12]}','{lose_games[13]}','{lose_games[14]}','{lose_games[15]}','{lose_games[16]}','{lose_games[17]}','{lose_games[18]}','{lose_games[19]}', '{goals_for[0]}','{goals_for[1]}','{goals_for[2]}','{goals_for[3]}','{goals_for[4]}','{goals_for[5]}','{goals_for[6]}','{goals_for[7]}','{goals_for[8]}','{goals_for[9]}','{goals_for[10]}','{goals_for[11]}','{goals_for[12]}','{goals_for[13]}','{goals_for[14]}','{goals_for[15]}','{goals_for[16]}','{goals_for[17]}','{goals_for[18]}','{goals_for[19]}', '{goals_missed[0]}','{goals_missed[1]}','{goals_missed[2]}','{goals_missed[3]}','{goals_missed[4]}','{goals_missed[5]}','{goals_missed[6]}','{goals_missed[7]}','{goals_missed[8]}','{goals_missed[9]}','{goals_missed[10]}','{goals_missed[11]}','{goals_missed[12]}','{goals_missed[13]}','{goals_missed[14]}','{goals_missed[15]}','{goals_missed[16]}','{goals_missed[17]}','{goals_missed[18]}','{goals_missed[19]}', '{goals_diff[0]}','{goals_diff[1]}','{goals_diff[2]}','{goals_diff[3]}','{goals_diff[4]}','{goals_diff[5]}','{goals_diff[6]}','{goals_diff[7]}','{goals_diff[8]}','{goals_diff[9]}','{goals_diff[10]}','{goals_diff[11]}','{goals_diff[12]}','{goals_diff[13]}','{goals_diff[14]}','{goals_diff[15]}','{goals_diff[16]}','{goals_diff[17]}','{goals_diff[18]}','{goals_diff[19]}', '{points[0]}','{points[1]}','{points[2]}','{points[3]}','{points[4]}','{points[5]}','{points[6]}','{points[7]}','{points[8]}','{points[9]}','{points[10]}','{points[11]}','{points[12]}','{points[13]}','{points[14]}','{points[15]}','{points[16]}','{points[17]}','{points[18]}','{points[19]}', '{name_teams[0]}','{name_teams[1]}','{name_teams[2]}','{name_teams[3]}','{name_teams[4]}','{name_teams[5]}','{name_teams[6]}','{name_teams[7]}','{name_teams[8]}','{name_teams[9]}','{name_teams[10]}','{name_teams[11]}','{name_teams[12]}','{name_teams[13]}','{name_teams[14]}','{name_teams[15]}','{name_teams[16]}','{name_teams[17]}','{name_teams[18]}','{name_teams[19]}', '{form_all[0]}','{form_all[1]}','{form_all[2]}','{form_all[3]}','{form_all[4]}','{form_all[5]}','{form_all[6]}','{form_all[7]}','{form_all[8]}','{form_all[9]}','{form_all[10]}','{form_all[11]}','{form_all[12]}','{form_all[13]}','{form_all[14]}','{form_all[15]}','{form_all[16]}','{form_all[17]}','{form_all[18]}','{form_all[19]}', '{logo_table[0]}','{logo_table[1]}','{logo_table[2]}','{logo_table[3]}','{logo_table[4]}','{logo_table[5]}','{logo_table[6]}','{logo_table[7]}','{logo_table[8]}','{logo_table[9]}','{logo_table[10]}','{logo_table[11]}','{logo_table[12]}','{logo_table[13]}','{logo_table[14]}','{logo_table[15]}','{logo_table[16]}','{logo_table[17]}','{logo_table[18]}','{logo_table[19]}']
# l2=[rank[0],rank[1],rank[2],rank[3],rank[4],rank[5],rank[6],rank[7],rank[8],rank[9],rank[10],rank[11],rank[12],rank[13],rank[14],rank[15],rank[16],rank[17],rank[18],rank[19], all_games[0],all_games[1],all_games[2],all_games[3],all_games[4],all_games[5],all_games[6],all_games[7],all_games[8],all_games[9],all_games[10],all_games[11],all_games[12],all_games[13],all_games[14],all_games[15],all_games[16],all_games[17],all_games[18],all_games[19],win_games[0],win_games[1],win_games[2],win_games[3],win_games[4],win_games[5],win_games[6],win_games[7],win_games[8],win_games[9],win_games[10],win_games[11],win_games[12],win_games[13],win_games[14],win_games[15],win_games[16],win_games[17],win_games[18],win_games[19] , draw_games[0],draw_games[1],draw_games[2],draw_games[3],draw_games[4],draw_games[5],draw_games[6],draw_games[7],draw_games[8],draw_games[9],draw_games[10],draw_games[11],draw_games[12],draw_games[13],draw_games[14],draw_games[15],draw_games[16],draw_games[17],draw_games[18],draw_games[19], lose_games[0],lose_games[1],lose_games[2],lose_games[3],lose_games[4],lose_games[5],lose_games[6],lose_games[7],lose_games[8],lose_games[9],lose_games[10],lose_games[11],lose_games[12],lose_games[13],lose_games[14],lose_games[15],lose_games[16],lose_games[17],lose_games[18],lose_games[19], goals_for[0],goals_for[1],goals_for[2],goals_for[3],goals_for[4],goals_for[5],goals_for[6],goals_for[7],goals_for[8],goals_for[9],goals_for[10],goals_for[11],goals_for[12],goals_for[13],goals_for[14],goals_for[15],goals_for[16],goals_for[17],goals_for[18],goals_for[19], goals_missed[0],goals_missed[1],goals_missed[2],goals_missed[3],goals_missed[4],goals_missed[5],goals_missed[6],goals_missed[7],goals_missed[8],goals_missed[9],goals_missed[10],goals_missed[11],goals_missed[12],goals_missed[13],goals_missed[14],goals_missed[15],goals_missed[16],goals_missed[17],goals_missed[18],goals_missed[19], goals_diff[0],goals_diff[1],goals_diff[2],goals_diff[3],goals_diff[4],goals_diff[5],goals_diff[6],goals_diff[7],goals_diff[8],goals_diff[9],goals_diff[10],goals_diff[11],goals_diff[12],goals_diff[13],goals_diff[14],goals_diff[15],goals_diff[16],goals_diff[17],goals_diff[18],goals_diff[19], points[0],points[1],points[2],points[3],points[4],points[5],points[6],points[7],points[8],points[9],points[10],points[11],points[12],points[13],points[14],points[15],points[16],points[17],points[18],points[19], name_teams[0],name_teams[1],name_teams[2],name_teams[3],name_teams[4],name_teams[5],name_teams[6],name_teams[7],name_teams[8],name_teams[9],name_teams[10],name_teams[11],name_teams[12],name_teams[13],name_teams[14],name_teams[15],name_teams[16],name_teams[17],name_teams[18],name_teams[19], form_all[0],form_all[1],form_all[2],form_all[3],form_all[4],form_all[5],form_all[6],form_all[7],form_all[8],form_all[9],form_all[10],form_all[11],form_all[12],form_all[13],form_all[14],form_all[15],form_all[16],form_all[17],form_all[18],form_all[19], logo_table[0],logo_table[1],logo_table[2],logo_table[3],logo_table[4],logo_table[5],logo_table[6],logo_table[7],logo_table[8],logo_table[9],logo_table[10],logo_table[11],logo_table[12],logo_table[13],logo_table[14],logo_table[15],logo_table[16],logo_table[17],logo_table[18],logo_table[19]]

            # l = [rounds_for_text,league_id,city_first_match,venue_first_match,first_date_round,home_first_match,away_first_match,all_home_teams,all_away_teams,team_name_max_injuries,max_injuries,team_max_goals_league,max_goals_league,team_min_conceded_league,min_conceded_top_saves,team_max_clean_sheet_league,max_cleen_sheet_league,team_max_conceded_league,max_conceded_saves_league,team_min_goals_attack_league,min_goals_attack_league,team_max_without_scored_league,max_without_scored_league,wins_without_scored,loses_without_scored,draws_without_scored,team_max_conceded_goals_league,max_conceded_goals_league,wins_conceded_goals,loses_conceded_goals,draws_conceded_goals,goals_top_league_1,name_top_goals_league_1,goals_top_league_2,name_top_goals_league_2,goals_top_league_3,name_top_goals_league_3,goals_top_league_4,name_top_goals_league_4,goals_top_league_5,name_top_goals_league_5,assists_top_league_1,name_top_assists_league_1,assists_top_league_2,name_top_assists_league_2,assists_top_league_3,name_top_assists_league_3,assists_top_league_4,name_top_assists_league_4,assists_top_league_5,name_top_assists_league_5,saves_top_league_1,name_top_saves_league_1,saves_top_league_2,name_top_saves_league_2,saves_top_league_3,name_top_saves_league_3,saves_top_league_4,name_top_saves_league_4,saves_top_league_5,name_top_saves_league_5]
            # ll = ['{rounds_for_text}', '{league_id}', '{city_first_match}', '{venue_first_match}', '{first_date_round}', '{home_first_match}', '{away_first_match}', '{all_home_teams}', '{all_away_teams}', '{team_name_max_injuries}', '{max_injuries}', '{team_max_goals_league}','{max_goals_league}','{team_min_conceded_league}', '{min_conceded_top_saves}', '{team_max_clean_sheet_league}', '{max_cleen_sheet_league}','{team_max_conceded_league}','{max_conceded_saves_league}', '{team_min_goals_attack_league}', '{min_goals_attack_league}', '{team_max_without_scored_league}', '{max_without_scored_league}', '{wins_without_scored}', '{loses_without_scored}', '{draws_without_scored}', '{team_max_conceded_goals_league}', '{max_conceded_goals_league}','{wins_conceded_goals}','{loses_conceded_goals}','{draws_conceded_goals}','{goals_top_league_1}','{name_top_goals_league_1}','{goals_top_league_2}','{name_top_goals_league_2}','{goals_top_league_3}','{name_top_goals_league_3}','{goals_top_league_4}','{name_top_goals_league_4}','{goals_top_league_5}','{name_top_goals_league_5}','{assists_top_league_1}','{name_top_assists_league_1}','{assists_top_league_2}','{name_top_assists_league_2}','{assists_top_league_3}','{name_top_assists_league_3}','{assists_top_league_4}','{name_top_assists_league_4}','{assists_top_league_5}','{name_top_assists_league_5}','{saves_top_league_1}','{name_top_saves_league_1}','{saves_top_league_2}','{name_top_saves_league_2}','{saves_top_league_3}','{name_top_saves_league_3}','{saves_top_league_4}','{name_top_saves_league_4}','{saves_top_league_5}','{name_top_saves_league_5}']
            # '{rank[0]}','{rank[1]}','{rank[2]}','{rank[3]}','{rank[4]}','{rank[5]}','{rank[6]}','{rank[7]}','{rank[8]}','{rank[9]}','{rank[10]}','{rank[11]}','{rank[12]}','{rank[13]}','{rank[14]}','{rank[15]}','{rank[16]}','{rank[17]}','{rank[18]}','{rank[19]}', '{all_games[0]}','{all_games[1]}','{all_games[2]}','{all_games[3]}','{all_games[4]}','{all_games[5]}','{all_games[6]}','{all_games[7]}','{all_games[8]}','{all_games[9]}','{all_games[10]}','{all_games[11]}','{all_games[12]}','{all_games[13]}','{all_games[14]}','{all_games[15]}','{all_games[16]}','{all_games[17]}','{all_games[18]}','{all_games[19]}','{win_games[0]}','{win_games[1]}','{win_games[2]}','{win_games[3]}','{win_games[4]}','{win_games[5]}','{win_games[6]}','{win_games[7]}','{win_games[8]}','{win_games[9]}','{win_games[10]}','{win_games[11]}','{win_games[12]}','{win_games[13]}','{win_games[14]}','{win_games[15]}','{win_games[16]}','{win_games[17]}','{win_games[18]}','{win_games[19]}' , '{draw_games[0]}','{draw_games[1]}','{draw_games[2]}','{draw_games[3]}','{draw_games[4]}','{draw_games[5]}','{draw_games[6]}','{draw_games[7]}','{draw_games[8]}','{draw_games[9]}','{draw_games[10]}','{draw_games[11]}','{draw_games[12]}','{draw_games[13]}','{draw_games[14]}','{draw_games[15]}','{draw_games[16]}','{draw_games[17]}','{draw_games[18]}','{draw_games[19]}', '{lose_games[0]}','{lose_games[1]}','{lose_games[2]}','{lose_games[3]}','{lose_games[4]}','{lose_games[5]}','{lose_games[6]}','{lose_games[7]}','{lose_games[8]}','{lose_games[9]}','{lose_games[10]}','{lose_games[11]}','{lose_games[12]}','{lose_games[13]}','{lose_games[14]}','{lose_games[15]}','{lose_games[16]}','{lose_games[17]}','{lose_games[18]}','{lose_games[19]}', '{goals_for[0]}','{goals_for[1]}','{goals_for[2]}','{goals_for[3]}','{goals_for[4]}','{goals_for[5]}','{goals_for[6]}','{goals_for[7]}','{goals_for[8]}','{goals_for[9]}','{goals_for[10]}','{goals_for[11]}','{goals_for[12]}','{goals_for[13]}','{goals_for[14]}','{goals_for[15]}','{goals_for[16]}','{goals_for[17]}','{goals_for[18]}','{goals_for[19]}', '{goals_missed[0]}','{goals_missed[1]}','{goals_missed[2]}','{goals_missed[3]}','{goals_missed[4]}','{goals_missed[5]}','{goals_missed[6]}','{goals_missed[7]}','{goals_missed[8]}','{goals_missed[9]}','{goals_missed[10]}','{goals_missed[11]}','{goals_missed[12]}','{goals_missed[13]}','{goals_missed[14]}','{goals_missed[15]}','{goals_missed[16]}','{goals_missed[17]}','{goals_missed[18]}','{goals_missed[19]}', '{goals_diff[0]}','{goals_diff[1]}','{goals_diff[2]}','{goals_diff[3]}','{goals_diff[4]}','{goals_diff[5]}','{goals_diff[6]}','{goals_diff[7]}','{goals_diff[8]}','{goals_diff[9]}','{goals_diff[10]}','{goals_diff[11]}','{goals_diff[12]}','{goals_diff[13]}','{goals_diff[14]}','{goals_diff[15]}','{goals_diff[16]}','{goals_diff[17]}','{goals_diff[18]}','{goals_diff[19]}', '{points[0]}','{points[1]}','{points[2]}','{points[3]}','{points[4]}','{points[5]}','{points[6]}','{points[7]}','{points[8]}','{points[9]}','{points[10]}','{points[11]}','{points[12]}','{points[13]}','{points[14]}','{points[15]}','{points[16]}','{points[17]}','{points[18]}','{points[19]}', '{name_teams[0]}','{name_teams[1]}','{name_teams[2]}','{name_teams[3]}','{name_teams[4]}','{name_teams[5]}','{name_teams[6]}','{name_teams[7]}','{name_teams[8]}','{name_teams[9]}','{name_teams[10]}','{name_teams[11]}','{name_teams[12]}','{name_teams[13]}','{name_teams[14]}','{name_teams[15]}','{name_teams[16]}','{name_teams[17]}','{name_teams[18]}','{name_teams[19]}', '{form_all[0]}','{form_all[1]}','{form_all[2]}','{form_all[3]}','{form_all[4]}','{form_all[5]}','{form_all[6]}','{form_all[7]}','{form_all[8]}','{form_all[9]}','{form_all[10]}','{form_all[11]}','{form_all[12]}','{form_all[13]}','{form_all[14]}','{form_all[15]}','{form_all[16]}','{form_all[17]}','{form_all[18]}','{form_all[19]}', '{logo_table[0]}','{logo_table[1]}','{logo_table[2]}','{logo_table[3]}','{logo_table[4]}','{logo_table[5]}','{logo_table[6]}','{logo_table[7]}','{logo_table[8]}','{logo_table[9]}','{logo_table[10]}','{logo_table[11]}','{logo_table[12]}','{logo_table[13]}','{logo_table[14]}','{logo_table[15]}','{logo_table[16]}','{logo_table[17]}','{logo_table[18]}','{logo_table[19]}',
            # rank[0],rank[1],rank[2],rank[3],rank[4],rank[5],rank[6],rank[7],rank[8],rank[9],rank[10],rank[11],rank[12],rank[13],rank[14],rank[15],rank[16],rank[17],rank[18],rank[19], all_games[0],all_games[1],all_games[2],all_games[3],all_games[4],all_games[5],all_games[6],all_games[7],all_games[8],all_games[9],all_games[10],all_games[11],all_games[12],all_games[13],all_games[14],all_games[15],all_games[16],all_games[17],all_games[18],all_games[19],win_games[0],win_games[1],win_games[2],win_games[3],win_games[4],win_games[5],win_games[6],win_games[7],win_games[8],win_games[9],win_games[10],win_games[11],win_games[12],win_games[13],win_games[14],win_games[15],win_games[16],win_games[17],win_games[18],win_games[19] , draw_games[0],draw_games[1],draw_games[2],draw_games[3],draw_games[4],draw_games[5],draw_games[6],draw_games[7],draw_games[8],draw_games[9],draw_games[10],draw_games[11],draw_games[12],draw_games[13],draw_games[14],draw_games[15],draw_games[16],draw_games[17],draw_games[18],draw_games[19], lose_games[0],lose_games[1],lose_games[2],lose_games[3],lose_games[4],lose_games[5],lose_games[6],lose_games[7],lose_games[8],lose_games[9],lose_games[10],lose_games[11],lose_games[12],lose_games[13],lose_games[14],lose_games[15],lose_games[16],lose_games[17],lose_games[18],lose_games[19], goals_for[0],goals_for[1],goals_for[2],goals_for[3],goals_for[4],goals_for[5],goals_for[6],goals_for[7],goals_for[8],goals_for[9],goals_for[10],goals_for[11],goals_for[12],goals_for[13],goals_for[14],goals_for[15],goals_for[16],goals_for[17],goals_for[18],goals_for[19], goals_missed[0],goals_missed[1],goals_missed[2],goals_missed[3],goals_missed[4],goals_missed[5],goals_missed[6],goals_missed[7],goals_missed[8],goals_missed[9],goals_missed[10],goals_missed[11],goals_missed[12],goals_missed[13],goals_missed[14],goals_missed[15],goals_missed[16],goals_missed[17],goals_missed[18],goals_missed[19], goals_diff[0],goals_diff[1],goals_diff[2],goals_diff[3],goals_diff[4],goals_diff[5],goals_diff[6],goals_diff[7],goals_diff[8],goals_diff[9],goals_diff[10],goals_diff[11],goals_diff[12],goals_diff[13],goals_diff[14],goals_diff[15],goals_diff[16],goals_diff[17],goals_diff[18],goals_diff[19], points[0],points[1],points[2],points[3],points[4],points[5],points[6],points[7],points[8],points[9],points[10],points[11],points[12],points[13],points[14],points[15],points[16],points[17],points[18],points[19], name_teams[0],name_teams[1],name_teams[2],name_teams[3],name_teams[4],name_teams[5],name_teams[6],name_teams[7],name_teams[8],name_teams[9],name_teams[10],name_teams[11],name_teams[12],name_teams[13],name_teams[14],name_teams[15],name_teams[16],name_teams[17],name_teams[18],name_teams[19], form_all[0],form_all[1],form_all[2],form_all[3],form_all[4],form_all[5],form_all[6],form_all[7],form_all[8],form_all[9],form_all[10],form_all[11],form_all[12],form_all[13],form_all[14],form_all[15],form_all[16],form_all[17],form_all[18],form_all[19], logo_table[0],logo_table[1],logo_table[2],logo_table[3],logo_table[4],logo_table[5],logo_table[6],logo_table[7],logo_table[8],logo_table[9],logo_table[10],logo_table[11],logo_table[12],logo_table[13],logo_table[14],logo_table[15],logo_table[16],logo_table[17],logo_table[18],logo_table[19],
# l = ['867946', '867947',  '867948', '867949', '867950', '867951', '867952', '867953', '867954', '867955', '867956', '867957', '867958', '867959', '867960', '867961', '867962', '86795563', '867964', '867965', '867966','867967','867968','867969','867970','867971','867972','867973','867974','867975','867976','867977','867978','867979','867980','867981','867982','867983','867984','867985', '877942','877943','877944','877945','877946','877947','877948','877949','877950','877951',]
# l1 = ['881780', '881781', '881782', '881783', '881784','881785', '881786','881787','881788', '881789', '871470', '871471', '871472', '871473','871474','871475','871476','871477','871478','871479','871480','871481','871482','871484','871485','871486','871487','871488','871489','877942','877943','877944','877945','877946','877947','877948','877949','877950','877950','877951', '867947', '867948', '867949', '867950', '867951', '867952', '867953', '867954', '867955', '867956', '867957', '867958', '867959', '867960', '867961', '867962', '867963', '867964', '867965', '867966', '867967', '867968', '867969', '867970', '867971', '867972', '867973', '867974', '867975', '867984']
# print(l + l1)

list_d = ['1', '2', '3']
h3_leader = ''
h3_another = ''

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


def review_round_text(rounds, league_id):
    from db import get_data_round

    # Запрос в БД
    insert_query = (
        f"SELECT * FROM round_review WHERE rounds={rounds} AND league_id={league_id}"
    )

    index_text_review_round = get_data_round(insert_query)

    index_text_review_round = index_text_review_round[0]


    idd, rounds, season, league_id, league_name, team_home_leader, team_away_rival, goal_leader, goal_rival, name_home_review, name_away_review, goals_home, goals_away, count_home, count_away, count_draw, h3_amounts_list, h3_names_list, h3_team_names_list, h3_fixture_match_list, name_top_goals_league_1, goals_top_league_1, team_top_goals_league1_1, name_top_goals_league_2, goals_top_league_2, team_top_goals_league2_1, name_top_goals_league_3, goals_top_league_3, team_top_goals_league3_1, name_top_goals_league_4, goals_top_league_4, team_top_goals_league4_1, name_top_goals_league_5, goals_top_league_5, team_top_goals_league5_1, all_goals_round, all_penalty_round, all_goals_previous_round, total_percent_round, average_goals_in_season, average_penalty_in_season, time_fast_goal, team_name_fast_goal, name_fast_goal, team_away_fast_goal, scrore_fast_goal, team_top_destroyer, destroyer_interceptions, destroyer_blocks, destroyer_tackles, destroyer_saves, amount_max_destroyer, team_main_destroyer, team_rival_destroyer, goals_main_destroyer, goals_rival_destroyer, max_destroyer_of_season_name, max_destroyer_of_season_amount, team_top_creator, creator_duels, creator_shots_on_target, creator_shots_off_target, team_main_creator, team_rival_creator, goals_main_creator, goals_rival_creator, amount_max_creator, max_creator_of_season_name, max_creator_of_season_amount, name_max_accurate_in_round, max_accurate_in_round, max_total_passes_with_accurate_in_round, name_min_accurate_in_round, min_accurate_in_round, min_total_passes_with_accurate_in_round, name_max_accuracy_in_season, percent_max_accuracy_in_season, name_min_accuracy_in_season, percent_min_accuracy_in_season, name_max_saves_of_round, main_team_max_saves, round_max_saves_of_round, rival_team_max_saves, amount_max_saves_of_round, top_fouls_total_yel_card, top_fouls_total_red_card, top_fouls_team_name_home, top_fouls_team_name_away, top_fouls_goals_home, top_fouls_goals_away, name_top3_fouls_of_season, ycards_top3_fouls_of_season, rcards_top3_fouls_of_season, name_teams_cards_top3_fouls_of_season, round_injuries, average_injuries_in_round, top_round_injuries_name_team, top_round_injuries_amount, name_top_assists_league_1, assists_top_league_1, team_top_assists_league1, name_top_assists_league_2, assists_top_league_2, team_top_assists_league2, name_top_assists_league_3, assists_top_league_3, team_top_assists_league3, name_top_assists_league_4, assists_top_league_4, team_top_assists_league4, name_top_assists_league_5, assists_top_league_5, team_top_assists_league5, name_top_saves_league_1, saves_top_league_1, team_top_saves_league1, name_top_saves_league_2, saves_top_league_2, team_top_saves_league2, name_top_saves_league_3, saves_top_league_3, team_top_saves_league3, name_top_saves_league_4, saves_top_league_4, team_top_saves_league4, name_top_saves_league_5, saves_top_league_5, team_top_saves_league5, rank_for_table, name_table_team, logo_for_table, form_table, all_matches_table, win_matches_table, draw_matches_table, lose_matches_table, goals_scored_for_table, goals_missed_for_table, goals_diff_table, points_for_table, date_next_round, arena_next_round, first_team_home_next_round, first_team_away_next_round, sum_accuracy_name, all_rounds = index_text_review_round[0], index_text_review_round[1], index_text_review_round[2], index_text_review_round[3], index_text_review_round[4], index_text_review_round[5], index_text_review_round[6], index_text_review_round[7], index_text_review_round[8], index_text_review_round[9], index_text_review_round[10], index_text_review_round[11], index_text_review_round[12], index_text_review_round[13], index_text_review_round[14], index_text_review_round[15], index_text_review_round[16], index_text_review_round[17] ,index_text_review_round[18] , index_text_review_round[19], index_text_review_round[20] ,index_text_review_round[21],index_text_review_round[22], index_text_review_round[23] ,index_text_review_round[24],index_text_review_round[25], index_text_review_round[26], index_text_review_round[27], index_text_review_round[28], index_text_review_round[29], index_text_review_round[30], index_text_review_round[31], index_text_review_round[32], index_text_review_round[33],index_text_review_round[34],index_text_review_round[35],index_text_review_round[36],index_text_review_round[37],index_text_review_round[38],index_text_review_round[39],index_text_review_round[40],index_text_review_round[41],index_text_review_round[42],index_text_review_round[43],index_text_review_round[44],index_text_review_round[45],index_text_review_round[46],index_text_review_round[47],index_text_review_round[48],index_text_review_round[49],index_text_review_round[50],index_text_review_round[51],index_text_review_round[52],index_text_review_round[53],index_text_review_round[54],index_text_review_round[55],index_text_review_round[56],index_text_review_round[57],index_text_review_round[58],index_text_review_round[59],index_text_review_round[60],index_text_review_round[61],index_text_review_round[62],index_text_review_round[63],index_text_review_round[64],index_text_review_round[65],index_text_review_round[66],index_text_review_round[67],index_text_review_round[68],index_text_review_round[69],index_text_review_round[70],index_text_review_round[71],index_text_review_round[72],index_text_review_round[73],index_text_review_round[74],index_text_review_round[75],index_text_review_round[76],index_text_review_round[77],index_text_review_round[78],index_text_review_round[79],index_text_review_round[80],index_text_review_round[81],index_text_review_round[82],index_text_review_round[83],index_text_review_round[84],index_text_review_round[85],index_text_review_round[86],index_text_review_round[87],index_text_review_round[88],index_text_review_round[89],index_text_review_round[90],index_text_review_round[91],index_text_review_round[92],index_text_review_round[93],index_text_review_round[94],index_text_review_round[95],index_text_review_round[96],index_text_review_round[97],index_text_review_round[98],index_text_review_round[99],index_text_review_round[100],index_text_review_round[101],index_text_review_round[102],index_text_review_round[103],index_text_review_round[104],index_text_review_round[105],index_text_review_round[106],index_text_review_round[107],index_text_review_round[108],index_text_review_round[109],index_text_review_round[110],index_text_review_round[111],index_text_review_round[112],index_text_review_round[113],index_text_review_round[114],index_text_review_round[115],index_text_review_round[116],index_text_review_round[117],index_text_review_round[118],index_text_review_round[119],index_text_review_round[120],index_text_review_round[121],index_text_review_round[122],index_text_review_round[123],index_text_review_round[124],index_text_review_round[125],index_text_review_round[126],index_text_review_round[127],index_text_review_round[128],index_text_review_round[129],index_text_review_round[130],index_text_review_round[131],index_text_review_round[132],index_text_review_round[133],index_text_review_round[134],index_text_review_round[135],index_text_review_round[136],index_text_review_round[137],index_text_review_round[138],index_text_review_round[139],index_text_review_round[140],index_text_review_round[141],index_text_review_round[142],index_text_review_round[143],index_text_review_round[144], index_text_review_round[145]

    rank_for_table = rank_for_table.split()
    all_matches_table = all_matches_table.split()
    win_matches_table = win_matches_table.split()
    draw_matches_table = draw_matches_table.split()
    lose_matches_table = lose_matches_table.split()
    goals_scored_for_table = goals_scored_for_table.split()
    goals_missed_for_table = goals_missed_for_table.split()
    goals_diff_table = goals_diff_table.split()
    points_for_table = points_for_table.split()
    name_table_team = str(name_table_team).replace("+", " ").split()
    form_table = str(form_table).replace("+", " ").split()
    logo_for_table = str(logo_for_table).replace("+", " ").split()

    name_home_review = str(name_home_review).replace("+", " ").split()
    name_away_review = str(name_away_review).replace("+", " ").split()
    who_scored_home = str(who_scored_home).replace("+", " ").split()
    who_scored_away = str(who_scored_away).replace("+", " ").split()
    name_top3_fouls_of_season = str(name_top3_fouls_of_season).replace("+", " ").split()
    ycards_top3_fouls_of_season = str(ycards_top3_fouls_of_season).split()
    rcards_top3_fouls_of_season = str(rcards_top3_fouls_of_season).split()
    sum_accuracy = str(sum_accuracy).split()
    name_teams_cards_top3_fouls_of_season = str(name_teams_cards_top3_fouls_of_season).replace("+", " ").split()
    sum_accuracy_name = str(sum_accuracy_name).replace("+", " ").split()

    h3_amounts_list = str(h3_amounts_list).split()
    
    name_home_review = replace_new_list(name_home_review)
    name_away_review = replace_new_list(name_away_review)
    who_scored_home = replace_new_list(who_scored_home)
    who_scored_away = replace_new_list(who_scored_away)
    name_top3_fouls_of_season = replace_new_list(name_top3_fouls_of_season)
    name_teams_cards_top3_fouls_of_season = replace_new_list(name_teams_cards_top3_fouls_of_season)
    name_table_team = replace_new_list(name_table_team)
    h3_names_list = h3_names_list.replace("+", " ").split()
    h3_team_names_list = h3_team_names_list.replace("+", " ").split()
    h3_names_list = replace_new_list(h3_names_list)
    h3_team_names_list = replace_new_list(h3_team_names_list)   
    


    h3_leader = ''
    h3_another = ''

    for i in range(len(h3_team_names_list)):
        if i == 0:
            
            h3_fixture = get_data_fix(h3_fixture_match_list[i])
            team_away = h3_fixture[0]
            goals_home = h3_fixture[1]
            goals_away = h3_fixture[2]
            if goals_home > goals_away:
                result = 'won'
            if goals_home < goals_away:
                result = 'lost'
            if goals_home == goals_away:
                result = 'make it a draw'


            h3_leader = f'{h3_names_list[i]} ({h3_team_names_list[i]}) scored {h3_amounts_list[i]} in the match with {team_away}. His team {result} with the final score {goals_home} - {goals_away}.'
        if i != 0:
            h3_another = h3_another + f'{h3_names_list[i]} ({h3_team_names_list[i]}) scored {h3_amounts_list[i]}, '
    f = ''
    for table in range(len(rank_for_table)):
        f = f + f"<tr align='centre' valign='top'><td>{rank_for_table[table]}</td><td><img src='{logo_for_table[table]}' alt=''></td><td>{name_table_team[table]}</td><td>{form_table[table]}</td><td>{all_matches_table[table]}</td><td>{win_matches_table[table]}</td><td>{draw_matches_table[table]}</td><td>{lose_matches_table[table]}</td><td>{goals_scored_for_table[table]}</td><td>{goals_missed_for_table[table]}</td><td>{goals_diff_table[table]}</td><td>{points_for_table[table]}</td></tr>"
    

    tr_1 = (f'<tr align="center" valign="top" style= "background-color: #aedbea;">'
            f'<td>#</td>'
            f'<td></td>'
            f'<td><b>Team</b></td>'
            f'<td><b>Form</b></td>'
            f'<td>PL</td>'
            f'<td style= "background-color: #4a9460;">W</td>'
            f'<td>D</td>' #style= "background-color: #9f9c98;"
            f'<td style= "background-color: #a13c3c;">L</td>'
            f'<td>GF</td>'  
            f'<td>GA</td>'
            f'<td>GD</td>' 
            f'<td>Pts</td>'
            f'</tr>')

    table = f"<table><tbody>{tr_1}{f}</tbody></table>"

    tr_1_games = (f'<tr align="center" valign="top" style= "background-color: #aedbea;">'
            f'<td>Teams</td>'
            f'<td>Result</td>'
            f'</tr>')

    all_matches_round = ''
    for all_matches in range(len(name_home_review)):
        all_matches_round = all_matches_round + f"<tr align='centre' valign='top'><td>{name_home_review[all_matches]} - {name_away_review[all_matches]}</td><td>{goals_home[all_matches]} - {goals_away[all_matches]}</td></tr>"

    table_all_matches_round = f"<table><tbody>{tr_1_games}{all_matches_round}</tbody></table>"
    
    
    data = {
        "title":{
            "rounds":f"{rounds}",
            "league_name":f"{league_name}", 
            "all_rounds":f"{all_rounds}"
        },
        "matches":{
            "team_home_leader":f"{team_home_leader}",
            "team_away_rival":f"{team_away_rival}",
            "goal_leader":f"{goal_leader}",
            "goal_rival":f"{goal_rival}",
            "table_all_matches_round":f"{table_all_matches_round}",
            "count_home":f"{count_home}",
            "count_away":f"{count_away}",
            "count_draw":f"{count_draw}",
            "h3_leader":f"{h3_leader}",
            "h3_another":f"{h3_another}"
        },
        "stats":{
            "name_top_goals_league_1":f"{name_top_goals_league_1}",
            "name_top_goals_league_2":f"{name_top_goals_league_2}",
            "name_top_goals_league_3":f"{name_top_goals_league_3}",
            "name_top_goals_league_4":f"{name_top_goals_league_2}",
            "name_top_goals_league_5":f"{name_top_goals_league_5}",
            "total_name_top_goals_league_1_round":f"{total_name_top_goals_league_1_round}",
            "total_name_top_goals_league_2_round":f"{total_name_top_goals_league_2_round}",
            "total_name_top_goals_league_3_round":f"{total_name_top_goals_league_3_round}",
            "total_name_top_goals_league_4_round":f"{total_name_top_goals_league_4_round}",
            "total_name_top_goals_league_5_round":f"{total_name_top_goals_league_5_round}",
            "all_goals_round":f"{all_goals_round}",
            "all_penalty_round":f"{all_penalty_round}",
            "precent_of_last_round":f"{precent_of_last_round}",
            "average_goals_in_season":f"{average_goals_in_season}",
            "all_penalty_round":f"{all_penalty_round}",
            "average_penalty_in_season":f"{average_penalty_in_season}",
            "time_fast_goal":f"{time_fast_goal}",
            "name_fast_goal":f"{name_fast_goal}",
            "team_name_fast_goal":f"{team_name_fast_goal}",
            "team_away_fast_goal":f"{team_away_fast_goal}",
            "scrore_fixture_fast_goal":f"{scrore_fixture_fast_goal}"
        },
        "team_efficiency":{
            "team_top_destroyer":f"{team_top_destroyer}",
            "destroyer_interceptions":f"{destroyer_interceptions}",
            "destroyer_blocks":f"{destroyer_blocks}",
            "destroyer_tackles":f"{destroyer_tackles}",
            "destroyer_saves":f"{destroyer_saves}",
            "amount_max_destroyer":f"{amount_max_destroyer}",
            "team_main_destroyer":f"{team_main_destroyer}",
            "team_rival_destroyer":f"{team_rival_destroyer}",
            "goals_main_destroyer":f"{goals_main_destroyer}",
            "goals_rival_destroyer":f"{goals_rival_destroyer}",
            "max_destroyer_of_season_name":f"{max_destroyer_of_season_name}",
            "max_destroyer_of_season_amount":f"{goals_main_destroyer}",

            "team_top_creator":f"{team_top_creator}",
            "creator_duels":f"{creator_duels}",
            "creator_shots_on_target":f"{creator_shots_on_target}",
            "creator_shots_off_target":f"{creator_shots_off_target}",
            "amount_max_creator":f"{amount_max_creator}",
            "team_rival_creator":f"{team_rival_creator}",
            "goals_main_creator":f"{goals_main_creator}",
            "goals_rival_creator":f"{goals_rival_creator}",
            "max_creator_of_season_name":f"{max_creator_of_season_name}",
            "max_creator_of_season_amount":f"{max_creator_of_season_amount}",

            "name_max_accurate_in_round":f"{name_max_accurate_in_round}",
            "max_accurate_in_round":f"{max_accurate_in_round}",
            "max_total_passes_with_accurate_in_round":f"{max_total_passes_with_accurate_in_round}",
            "name_max_accuracy_in_season":f"{name_max_accuracy_in_season}",
            "percent_max_accuracy_in_season":f"{percent_max_accuracy_in_season}",
            "name_min_accurate_in_round":f"{name_min_accurate_in_round}",
            "min_accurate_in_round":f"{min_accurate_in_round}",
            "name_min_accuracy_in_season":f"{name_min_accuracy_in_season}",
        },
        "players_stats":{
            "name_max_saves_of_round":f"{name_max_saves_of_round}",
            "main_team_max_saves":f"{main_team_max_saves}",
            "amount_max_saves_of_round":f"{amount_max_saves_of_round}",
            "rival_team_max_saves":f"{rival_team_max_saves}",
            "top_fouls_total_yel_card":f"{top_fouls_total_yel_card}",
            "top_fouls_total_red_card":f"{top_fouls_total_red_card}",
            "top_fouls_team_name_home":f"{top_fouls_team_name_home}",
            "top_fouls_team_name_away":f"{top_fouls_team_name_away}",
            "top_fouls_goals_home":f"{top_fouls_goals_home}",
            "top_fouls_goals_away":f"{top_fouls_goals_away}",
            "name_top3_fouls_of_season":f"{name_top3_fouls_of_season}",
            "ycards_top3_fouls_of_season":f"{ycards_top3_fouls_of_season}",
            "rcards_top3_fouls_of_season":f"{rcards_top3_fouls_of_season}",
            "name_teams_cards_top3_fouls_of_season":f"{name_teams_cards_top3_fouls_of_season}",

        }
    }


from datetime import datetime, timedelta
s = '2022-11-05T15:00:00'
date_match1 = datetime.strptime(s[:15], "%Y-%m-%dT%H:%M").strftime('%B %d %Y')
print(date_match1)