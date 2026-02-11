import requests

# Функция получения ближайших матчей 
def check_match():  
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    headers = {
        "X-RapidAPI-Key": "YOUR_KEY",
        "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
    }
    req_gen = requests.get(url, headers=headers, params={
        "league": "39", 
        "season": "2022",
        "next": "7"
    })
    req_gen2 = requests.get(url, headers=headers, params={
        "league": "78", 
        "season": "2022",
        "next": "7"
    })
    req_gen3 = requests.get(url, headers=headers, params={
        "league": "61", 
        "season": "2022",
        "next": "7"
    })
    req_gen4 = requests.get(url, headers=headers, params={
        "league": "135", 
        "season": "2022",
        "next": "7"
    })
    req_gen5 = requests.get(url, headers=headers, params={
        "league": "140", 
        "season": "2022",
        "next": "7"
    })
    data_gen = req_gen.json()
    data_gen2 = req_gen2.json()
    data_gen3 = req_gen3.json()
    data_gen4 = req_gen4.json()
    data_gen5 = req_gen5.json()
    
    fixture_m = []
    date_m = []

    #Цикл добавления списков даты и айди матча в списки  
    for num in range(len(data_gen['response'])):
        fixture_match = data_gen['response'][num]['fixture']['id']
        date_match = data_gen['response'][num]['fixture']['date'][:16]
        fixture_m.append(fixture_match)
        date_m.append(date_match)
    
    for num in range(len(data_gen2['response'])):
        fixture_match2 = data_gen2['response'][num]['fixture']['id']
        date_match2 = data_gen2['response'][num]['fixture']['date'][:16]
        fixture_m.append(fixture_match2)
        date_m.append(date_match2)
    
    for num in range(len(data_gen3['response'])):
        fixture_match3 = data_gen3['response'][num]['fixture']['id']
        date_match3 = data_gen3['response'][num]['fixture']['date'][:16]
        fixture_m.append(fixture_match3)
        date_m.append(date_match3)

    for num in range(len(data_gen4['response'])):
        fixture_match4 = data_gen4['response'][num]['fixture']['id']
        date_match4 = data_gen4['response'][num]['fixture']['date'][:16]
        fixture_m.append(fixture_match4)
        date_m.append(date_match4)

    for num in range(len(data_gen5['response'])):
        fixture_match5 = data_gen5['response'][num]['fixture']['id']
        date_match5 = data_gen5['response'][num]['fixture']['date'][:16]
        fixture_m.append(fixture_match5)
        date_m.append(date_match5)



    # Возвращаем данные по индексу 0 и 1
    return fixture_m, date_m
