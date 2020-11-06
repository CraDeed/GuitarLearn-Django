import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from urllib import parse
from os.path import abspath, dirname, join

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings.dev")

import django
django.setup()

from guitarlearn.models import YoutubeTutorial

def youtube_craw(artist="", song=""):

    BASE_DIR = dirname(dirname(abspath(__file__)))

    options = webdriver.ChromeOptions()
    options.headless = True

    parse_artist = parse.quote_plus(artist)
    parse_song = parse.quote_plus(song)
    guitar = parse.quote_plus("기타 레슨 강좌")

    url = f"https://www.youtube.com/results?search_query={parse_artist}+{parse_song}+{guitar}"

    driver = webdriver.Chrome('backend/static/chromedriver.exe', options=options)
    driver.get(url)

    driver.implicitly_wait(2)

    SCROLL_PAUSE_TIME = 0.5
    # 한번 스크롤 하고 멈출 시간 설정

    from selenium.webdriver.common.keys import Keys

    body = driver.find_element_by_tag_name('body')
    # body태그를 선택하여 body에 넣음

    last_height = driver.execute_script('return document.documentElement.scrollHeight')
    # 현재 화면의 길이를 리턴 받아 last_height에 넣음
    for _ in range(3):
        body.send_keys(Keys.END)
        # body 본문에 END키를 입력(스크롤내림)
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script('return document.documentElement.scrollHeight')

    page = driver.page_source

    driver.quit()

    soup = BeautifulSoup(page, 'lxml')

    all_videos = soup.find_all(id='dismissable')

    video_list = []

    for video in all_videos:
        title_link = video.find(id='video-title')
        artist_link = video.find('a',{"class":"yt-simple-endpoint style-scope yt-formatted-string"})
        img_link = video.find(id="thumbnail")

        lower_title = title_link['title'].lower().strip()

        if song == "":
            if ('기타' in lower_title) or ('guitar' in lower_title) or ('acoustic' in lower_title):
                if ('커버' in lower_title) or ('cover' in lower_title) or ('lesson' in lower_title) or ('tab' in lower_title) or ('코드' in lower_title) or ('chords' in lower_title) or ('강좌' in lower_title):
                    title = title_link['title']
                    link = 'https://www.youtube.com/' + title_link['href']
                    youtuber = artist_link.get_text()
                    thumbnail = "https://i.ytimg.com/vi/" + img_link.get("href").replace("/watch?v=","") + "/mqdefault.jpg"
                    key = img_link.get("href").replace("/watch?v=","")

                    video_list.append({'title': title, "link": link, 'youtuber': youtuber, 'thumbnail' : thumbnail, 'key': key})
        else:
            if song in lower_title:
                if ('기타' in lower_title) or ('guitar' in lower_title) or ('acoustic' in lower_title):
                    if ('커버' in lower_title) or ('cover' in lower_title) or ('lesson' in lower_title) or ('tab' in lower_title) or ('코드' in lower_title) or ('chords' in lower_title) or ('강좌' in lower_title):
                        title = title_link['title']
                        link = 'https://www.youtube.com/' + title_link['href']
                        youtuber = artist_link.get_text()
                        thumbnail = "https://i.ytimg.com/vi/" + img_link.get("href").replace("/watch?v=","") + "/mqdefault.jpg"
                        key = img_link.get("href").replace("/watch?v=","")

                        video_list.append({'title': title, "link": link, 'youtuber': youtuber, 'thumbnail' : thumbnail, 'key': key})

    return video_list

if __name__=='__main__':
    YoutubeTutorial.objects.all().delete()
    data = youtube_craw(artist="아이유")
    for item in data:
        YoutubeTutorial(title = item['title'], link = item['link'], youtuber = item['youtuber'],thumbnail = item['thumbnail'], key = item['key']).save()