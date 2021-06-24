import sys

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from django.db.models import Q
# from .serializers import *
# from .models import *
import requests
import json
import os
from rest_framework import status
from decouple import config, UndefinedValueError
import random
from datetime import datetime
import matplotlib.pyplot as plt
import requests
import time
import json
import pandas as pd
import numpy as np


class LanguageAnaliseView(APIView):
    """
    Analise profile's languages by username
    """

    def post(self, request):
        username = request.data['username']

        try:
            github_token = os.environ['github_token']
        except KeyError:
            try:
                github_token = config('github_token')
            except UndefinedValueError:
                print('ERROR: github_token is not defined ! ! !')
                sys.exit()

        # f = open('token.txt')
        # git_token = f.readline()
        # f.close()

        headers = {
            'content-type': 'application/json',
            'Authorization': f'Bearer {github_token}'
        }

        repos = requests.get(url=f'https://api.github.com/users/{username}/repos', headers=headers).json()
        print(f"Number of open repos: {len(repos)}")

        with open('data.json', 'w') as fp:
            json.dump(repos, fp)
        languages = dict()

        i = 0
        for repo in repos:
            if i > 4:
                break
            i += 1
            # print(repo['name'])
            time.sleep(0)
            repo_languages = requests.get(f"https://api.github.com/repos/{username}/{repo['name']}/languages",
                                          headers=headers).json()
            # print(repo_languages)
            for repo_language, value in repo_languages.items():
                # print(repo_language, value)
                if repo_language not in languages:
                    languages[repo_language] = value
                else:
                    languages[repo_language] += value
            # print()

        # preparing data for pie chart
        value_sum = 0
        for value in languages.values():
            value_sum += value

        chart_languages = dict()
        for language, value in languages.items():
            print(value / value_sum, end=' ')
            if value / value_sum < 0.01:
                print(language, 'true')
                if 'Other' not in chart_languages:
                    chart_languages['Other'] = value
                else:
                    chart_languages['Other'] += value
            else:
                print(language, 'false')
                if language not in chart_languages:
                    chart_languages[language] = value
                else:
                    chart_languages[language] += value
        print(chart_languages)

        for language, value in languages.items():
            print(f"{value}\t- {language}")
        print()

        # labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
        # sizes = [15, 30, 45, 10]
        # explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

        # labels = tuple(languages.keys())
        # sizes = tuple(languages.values())
        # plt.barh(labels, sizes)
        # plt.title('title name')
        # plt.ylabel('y axis name')
        # plt.xlabel('x axis name')
        # plt.show()

        # labels = tuple(languages.keys())
        # sizes = tuple(languages.values())
        # explode = tuple()
        # for el in labels:
        #     explode += (0.1,)
        # print(len(labels), labels)
        # fig1, ax1 = plt.subplots()
        # ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        #         shadow=True, startangle=90, radius=.9)
        # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        # plt.show()

        # # Import
        # df_raw = pd.read_csv("https://github.com/selva86/datasets/raw/master/mpg_ggplot2.csv")
        # # Prepare Data
        # df = df_raw.groupby('class').size().reset_index(name='counts')
        # # Draw Plot
        fig, ax = plt.subplots(figsize=(12, 7), subplot_kw=dict(aspect="equal"), dpi=80)

        # data = df['counts']
        # categories = df['class']
        # explode = [0, 0, 0, 0, 0, 0.1, 0]

        sizes = tuple(chart_languages.keys())
        labels = tuple(chart_languages.values())

        explode = tuple()
        for el in labels:
            explode += (0.0,)

        def func(pct, allvals):
            # absolute = int(pct / 100. * np.sum(allvals))
            # return "{:.1f}% ({:d} )".format(pct, absolute)
            return "{:.1f}%".format(pct, )

        wedges, texts, autotexts = ax.pie(x=labels,
                                          autopct=lambda pct: func(pct, labels),
                                          textprops=dict(color="w"),
                                          colors=plt.cm.Dark2.colors,
                                          startangle=140,
                                          explode=explode)

        # print(autotexts)
        # Decoration
        ax.legend(wedges, sizes, title="Languages", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        plt.setp(autotexts, size=10, weight=700)
        ax.set_title("Class of Languages (bytes): Pie Chart")
        # plt.show()
        path = f'media/language_analyzes/{username}.png'
        plt.savefig(path)
        return Response({
            'username': username,
            'pie_chart': path
        })

# class MainView(APIView):
#     """
#     Validates service
#     """
#
#     def get_current_weather(self, city_name):
#         try:
#             owm_token = os.environ['OWM_TOKEN']
#         except:
#             try:
#                 owm_token = config('OWM_TOKEN')
#             except:
#                 raise FileNotFoundError
#         data = requests.get(
#             f'https://api.openweathermap.org/data/2.5/weather?units=metric&q={city_name}&appid={owm_token}').json()
#
#         result = f'''
# ☀ Current weather: {data['weather'][0]['main']}
# 🌡️ Current temperature: {round(float(data['main']['temp']), 2)}°С ({int(data['main']['temp_min'])} - {int(data['main']['temp_max'])})
# ☁ Cloudiness: {data['clouds']['all']}%
# 💨 Current wind: {data['wind']['speed']} m/s
# 🌅 Sunrise and sunset: {datetime.utcfromtimestamp(int(data['sys']['sunrise']) + 10800).strftime('%H:%M')} - {datetime.utcfromtimestamp(int(data['sys']['sunset']) + 10800).strftime('%H:%M')}
# '''
#         return result
#
#     def post(self, request):
#         event = request.data
#         if event['type'] == 'message_new':
#             print(f"Message: {event['object']['message']['text']}")
#
#             try:
#                 token = os.environ['VK_TOKEN']
#             except:
#                 try:
#                     token = config('VK_TOKEN')
#                 except:
#                     raise FileNotFoundError
#
#             # self.get_current_weather('Moscow')
#
#             session = vk.Session()
#             api = vk.API(session, v='5.126')
#
#             # keyboard_data = {
#             #     "one_time": False,
#             #     "buttons": [
#             #         [
#             #             {
#             #                 "action": {
#             #                     "type": "text",
#             #                     "payload": "{\"button\": \"1\"}",
#             #                     "label": "Weather (Moscow)"
#             #                 },
#             #                 "color": "primary"
#             #             },
#             #         ],
#             #         [
#             #             {
#             #                 "action": {
#             #                     "type": "text",
#             #                     "payload": "{\"button\": \"2\"}",
#             #                     "label": "Birthdays"
#             #                 },
#             #                 "color": "positive"
#             #             },
#             #         ],
#             #         [
#             #             {
#             #                 "action": {
#             #                     "type": "text",
#             #                     "payload": "{\"button\": \"3\"}",
#             #                     "label": "Email"
#             #                 },
#             #                 "color": "negative"
#             #             },
#             #         ],
#             #     ]
#             # }
#
#             if event['object']['message']['text'] == 'Weather (Moscow)':
#                 print('Weather')
#                 random_id = random.randrange(1, 100000, 1)
#                 with open('keyboard.json') as json_file:
#                     keyboard_data = json.load(json_file)
#                 api.messages.send(
#                     keyboard=json.dumps(keyboard_data),
#                     # keyboard=keyboard_data,
#                     access_token=token,
#                     user_id=event['object']['message']['from_id'],
#                     message=self.get_current_weather('Moscow'),
#                     random_id=random_id
#                 )
#             elif event['object']['message']['text'] == 'Birthdays':
#                 print('Birthdays')
#                 random_id = random.randrange(1, 100000, 1)
#                 api.messages.send(
#                     keyboard=json.dumps(keyboard_data),
#                     access_token=token,
#                     user_id=event['object']['message']['from_id'],
#                     message='Birthdays !',
#                     random_id=random_id
#                 )
#             elif event['object']['message']['text'] == 'Email':
#                 print('Email')
#                 random_id = random.randrange(1, 100000, 1)
#                 api.messages.send(
#                     keyboard=json.dumps(keyboard_data),
#                     access_token=token,
#                     user_id=event['object']['message']['from_id'],
#                     message='Email !',
#                     random_id=random_id
#                 )
#             return HttpResponse('ok')
#
#
#
#
# class TestView(APIView):
#     """
#     Tests service
#     """
#
#     def get_current_weather(self, city_name):
#         try:
#             owm_token = os.environ['OWM_TOKEN']
#         except:
#             try:
#                 owm_token = config('OWM_TOKEN')
#             except:
#                 raise FileNotFoundError
#         data = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={owm_token}').json()
#
#         print((float(data['main']['temp']) - 273))
#         result = f'''Current weather: {data['weather'][0]['main']}
# Current temperature: {float(data['main']['temp']) - 273}
# '''
#         return result
#
#     def get(self, request):
#         data = self.get_current_weather('Moscow')
#         return HttpResponse(data)
