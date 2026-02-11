from publication.utils import generate_openai_content
from datetime import datetime

def generate_content(data, l_version, id, types):
    if types == 'preview':
        if l_version == 'eng':
            league_name = data['league'].name
            match_date = data.get('match_date')
            dt = datetime.fromisoformat(match_date.replace("Z", "+00:00"))
            formatted_date = dt.strftime("%d %B %Y")
            venue_name = data['venue'] if data.get('venue') else "the stadium"
            home_team = data.get('home_team')
            away_team = data.get('away_team')
            home_position = data.get('home_position')
            away_position = data.get('away_position')
            players_to_watch = data.get('players_to_watch',[])
            summary = data.get('summary','')
            
            article_template = f"The article must be written in the BBC style of writing articles which is the pyramid style of writing. Do not use fluff at the start of the paragraph or article or sentence. Go straight to the point like the BBC does in its articles. \nExample: {home_team} vs {away_team}, {formatted_date}. please do not generate any dummy text in []"
            
            if home_position and away_position:
                article_template += f"\n{home_team} — on the {home_position} place in {league_name}, {away_team} — {away_position} in {league_name}. please do not generate any dummy text in []"
                print(f"player to watch: {players_to_watch}")
            if players_to_watch:
                for player in players_to_watch:
                    for p in player:
                        article_template += f"\n{p.player_name} scored {p.session_goals} goals this season for {p.team}."
            
            article_template += "\nArticle Must be long, SEO-friendly, with natural language to pass AI content detection. please do not generate any dummy text in []"

            title_prompt = f"Write a Headline using this example: \n{home_team} vs {away_team}, {formatted_date} The format of the headline must be structured for SEO and AI search discovery and must be this: [{home_team}] vs [{away_team}]: Preview - Team News, Line-ups, Prediction and Tips | [{formatted_date}]"
            
            list_text = [
                article_template,
                "Using data from the respective match, write a BBC pyramid style of writing football match preview article. The data must also take into consideration that it is writing the preview in a football league system when that is the case. It must take into consideration the league table and any associated information for the competition. Must be SEO-friendly, with natural language to pass AI content detection.",
                "Using data from the respective match, write a BBC pyramid style of writing football match preview article. The data must also take into consideration that it is writing the preview in a football league system when that is the case. It must take into consideration the league table and any associated information for the competition. Must be SEO-friendly, with natural language to pass AI content detection.",
                "Using data from the respective match, write a BBC pyramid style of writing football match preview article. The data must also take into consideration that it is writing the preview in a football league system when that is the case. It must take into consideration the league table and any associated information for the competition. Must be SEO-friendly, with natural language to pass AI content detection. please do not generate any dummy text in []"
            ]
            
            if summary:
                list_text.append(f"Additional context: {summary}")

            content_prompt = "\n\n".join(list_text)
            list_prompt = [title_prompt,content_prompt]
            i = 0
            main_title = ""
            main_content = ""
            main_text_list = []
            for p in list_prompt:
                result = generate_openai_content(p)
                if i == 0:
                    main_title = result
                else:
                    main_content = result
                i += 1
            for i in ['"', "'"]:
                main_title = main_title.replace(i, "") if i in main_title else main_title
            
            for paragraph in main_content.split("\n\n"):
                    main_text_list.append(f"<p>{paragraph}</p>\n")

            article_html = f"""
            <article>
            {''.join(main_text_list)}
            </article>
            """
            return main_title, article_html
    
    if types == 'review':
        if l_version == 'eng':
            league_name = data['league']['name'] if 'name' in data.get('league') else "Football League"
            match_date = data.get('match_date')
            dt = datetime.fromisoformat(match_date.replace("Z", "+00:00"))
            formatted_date = dt.strftime("%d %B %Y")
            venue_name = data['venue'] if data.get('venue') else "the stadium"
            home_team = data.get('home_team')
            away_team = data.get('away_team')
            home_score = data.get('home_score')
            away_score = data.get('away_score')
            goalscorers = data.get('goalscorers',[])
            summary = data.get('summary','')

            goals_for_openai = []
            if goalscorers:
                #for scoreres in goalscorers:
                goals_for_openai = ", ".join([
                    f"{goal.player_name} ({goal.team}) - {goal.minute}'"
                    for goal in goalscorers
                ])
            title_prompt = f"Write a headline for a football match report. The headline must be structured for SEO and AI search discovery: '{home_team} vs {away_team} {home_score}:{away_score}, {formatted_date}, {league_name}'."
            list_text = [
                f"Using the information and data from the just-ended match, write a comprehensive football match report suitable for publication on a football news website {home_team} vs {away_team} {home_score}:{away_score} in {league_name}. {goals_for_openai}. The writing must adhere to high BBC standards of writing match reports, which is the BBC pyramid style of writing, and be optimized for search engines to ensure good ranking. Write the content in a natural, human-like style, ensuring it passes AI content detection tools.",
                "Write a match report that includes ball possession and shooting statistics. The writing must adhere to high BBC standards of writing match reports, which is the BBC pyramid style of writing, and be optimized for search engines to ensure good ranking.",
                "Write a match report using the provided data about passing accuracy. The writing must adhere to high BBC standards of writing match reports, which is the BBC pyramid style of writing, and be optimized for search engines to ensure good ranking.",
                "Write a match report with a focus on defensive actions, including interceptions and blocks. The writing must adhere to high BBC standards of writing match reports, which is the BBC pyramid style of writing, and be optimized for search engines to ensure good ranking.",
                "Write a match report using the data about face-to-face duels for the ball. The writing must adhere to high BBC standards of writing match reports, which is the BBC pyramid style of writing, and be optimized for search engines to ensure good ranking."
            ]
            
            if summary:
                list_text.append(f"Additional match context: {summary}")

            content_prompt = "\n\n".join(list_text)
            list_prompt = [title_prompt,content_prompt]
            i = 0
            main_title = ""
            main_content = ""
            main_text_list = []
            for p in list_prompt:
                result = generate_openai_content(p)
                if i == 0:
                    main_title = result
                else:
                    main_content = result
                i += 1
            for i in ['"', "'"]:
                main_title = main_title.replace(i, "") if i in main_title else main_title
            
            for paragraph in main_content.split("\n\n"):
                    main_text_list.append(f"<p>{paragraph}</p>\n")

            article_html = f"""
            <article>
            {''.join(main_text_list)}
            </article>
            """
            return main_title, article_html