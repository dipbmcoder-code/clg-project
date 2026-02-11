import json
import random
from pathlib import Path
root_folder = Path(__file__).resolve().parents[1]

def main_change_text(l_version, types, view, custom):

    """
    l_version - язык текста: ру, анлг и тд
    types - тип: матч, тур
    view - вид публикации: превью/ревью
    """

    """ Загружаем файл с данными блоков текста """
    if custom == False:
        file_path = root_folder / 'parameters' / 'football' / 'users' / 'text' / f'{l_version}_{view}_{types}_new.json'
        # print(file_path)
        with open(file_path) as file:
            file = json.load(file)
    elif custom == True:
        pass


    """ Главная строка текста (общая) """
    main_string = ''

    """ Главная строка заголовка 
        Авто выбор заголовка """
    if len(file['title']) > 1: main_title = file["title"][f"{random.randint(1, len(file['title']))}"]
    else: main_title = file["title"][f"1"]

    """
    Сделать систему для title в тексте  в конце title + текст)
    Создать возврат строки html 
    """
    """ Цикл по созданию блоков текста """
    for i_main in range(len(file) - 1):
        """ Делаем цикл по всем блокам текста с файла (у него может быть сколько угодно блоков и сколько угодно предложний и вариантов этих самых предложений)"""

        
        """ Получаем список предложений """
        sentence = file[f"{i_main}"]["sentence"]
        """ Получаем список заголовков"""

        title = file[f"{i_main}"]["title"]

        """Создаем интервальные переменные"""
        interval_string_for_sentence = ' '
        interval_string_for_title = ' '

        """ Цикл по всем предложений """
        for i_sentence in range(len(sentence)):

            i_sentence = f"{i_sentence}"

            if len(sentence[i_sentence]) != '0':
                """ Проверка, если один вариант предложения то берем его """
                if len(sentence[i_sentence]) == '1': interval_string_for_sentence = interval_string_for_sentence + sentence[i_sentence]["1"]
                else: interval_string_for_sentence = interval_string_for_sentence + sentence[i_sentence][f"{random.randint(1, len(sentence[i_sentence]))}"]
                """ Если больше одного то берем рандомный вариант (выставляем от 1 до n) и потом добавляем это к предыдущим предложениям"""


        """ Проверяем есть ли заголовок"""
        if title != "":
            """ Делаем цикл по вариантам заголовка """
            for i_title in range(len(title)):
                """ И делаем все то же как с предложениями """
                if len(title) == 1: interval_string_for_title = title["1"]
                else: interval_string_for_title = title[f"{random.randint(1, len(title))}"]

        """ Соединяем предложение с заголовком и добавляем это к общей строке (к остальным блокам)"""
        main_string = main_string + interval_string_for_title + interval_string_for_sentence

    """ Возвращаем общую строку """
    return [main_title, main_string]


# title, main_text = main_change_text('en', 'match', 'review')
# print(title)