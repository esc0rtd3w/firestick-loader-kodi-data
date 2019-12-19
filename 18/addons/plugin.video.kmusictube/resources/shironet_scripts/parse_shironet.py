#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import requests
import re
import time

base_url = 'http://shironet.mako.co.il'
driver = webdriver.Chrome("c:/chromedriver.exe")
driver.set_page_load_timeout(10)
total_artists = 0
json_header = '{\n"artists":[\n'

def open_protected_url(url, word):
    global driver
    while (True):
        try:
            driver.get(url)
            break
        except TimeoutException:
            print ("got timeout!!!!")
            try:
                driver.refresh()
                break
            except TimeoutException:
                print ("got  refresh timeout!!!!")
                continue
    try:
        return (driver.page_source)
    except TimeoutException:
        return open_protected_url(url, word)

def extract_artist_disks(url, fh):
    link = open_protected_url(base_url+url,"דיסקוגרפיה")
    disks_img = re.compile('<a href="(.+?)">\s*<img src="(.+?)"\s*title="(.+?)"\s*class="artist_disk_pic"').findall(link)
    disks_data = re.compile('<a href="(.+?)"\s*class="artist_more_link">(.+?)<\/a>').findall(link)

    i=0
    k=1
    for url,name in disks_data:
        try:
            fh.write('{\n"disk_name":"'+name.replace('\"','')+'",\n')
        except UnicodeEncodeError:
            fh.write('{\n"disk_name":"null_name",\n')
        try:
            fh.write('"disk_img":"'+disks_img[i][1]+'",\n')
        except IndexError:
            fh.write('"disk_img":"/jsp/images/275x315.gif",\n')
        link = open_protected_url(base_url+url.replace("amp;",""),"מילים")
        disk_songs = re.compile('<a class="artist_normal_link_clean"\s*href=".+?">\s*(.+?)\s*<\/a>').findall(link)
        disk_songs = disk_songs + re.compile('class="artist_normal_txt">\s*[0-9]+\s*.\s*(.+?)<\/td>').findall(link)

        fh.write('"tracks": [\n')
        j=1
        for song in disk_songs:
            if (j == len(disk_songs)):
                try:
                    fh.write('"'+song.replace('\"','')+'"\n')
                except UnicodeEncodeError:
                    fh.write('"null_song"\n')
            else:
                try:
                    fh.write('"'+song.replace('\"','')+'",\n')
                except UnicodeEncodeError:
                    fh.write('"null_song",\n')
            j += 1
        i += 1

        fh.write(']\n')
        if (k == len(disks_data)):
            fh.write('}\n')
        else:
            fh.write('},\n')
        k += 1


def extract_artist_songs(url, fh):
    link = open_protected_url(base_url+url,"שירים")
    pages_url = re.compile('<a href="(.+?)"\s*class="artist_nav_bar">\s*[0-9]+\s*<\/a>').findall(link)
    songs_names = re.compile('<span class="artist_normal_txt">\s*.+?<\/span>\s*<a href=".+?"\s*class="artist_player_songlist">\s*(.+?)<\/a>').findall(link)

    if pages_url:
        for url in pages_url:
            link = open_protected_url(base_url+url.replace("amp;","")+"&sort=popular","שירים")
            songs_names = songs_names + re.compile('<span class="artist_normal_txt">\s*.+?<\/span>\s*<a href=".+?"\s*class="artist_player_songlist">\s*(.+?)<\/a>').findall(link)
    i=1
    for song in songs_names:
        if (i == len(songs_names)):
            try:
                fh.write('"'+song.replace('\"','')+'"\n')
            except UnicodeEncodeError:
                fh.write('"null_song"\n')
        else:
            try:
                fh.write('"'+song.replace('\"','')+'",\n')
            except UnicodeEncodeError:
                fh.write('"null_song",\n')
        i += 1

def extract_artist_matedata(url, fh):
    link = open_protected_url(base_url+url,"מילים")
    songs_url = url+"&type=works"
    discs_url = re.compile('<a href="(.+?)">דיסקוגרפיה</a>').findall(link)
    artist_img = re.compile('<img src=\s*"(.+?)"\s*.+?class="artist_main_pic_frame"\s*\/>').findall(link)
    try:
        fh.write('"artist_img":"'+artist_img[0]+'",\n')
    except IndexError:
        fh.write('"artist_img":"/jsp/images/275x315.gif",\n')
    fh.write('"all_songs": [\n')
    if songs_url:
        extract_artist_songs(songs_url.replace("amp;","")+"&sort=popular", fh)
    fh.write('],\n')
    fh.write('"disks": [\n')
    if discs_url:
        extract_artist_disks(discs_url[0].replace("amp;","") , fh)
    fh.write(']\n')


def get_char_artist(url, fh, index):
    global total_artists
    page_id = 1
    link = requests.get(url+str(page_id))
    artists_data = re.compile('<a class="index_link" href="(.+?)">\s*(.+?)\s*<\/a>\s*<br>').findall(link.text)

    while (("הבא") in link.text):
        page_id = page_id + 1
        link = requests.get(url+str(page_id))
        artists_data = artists_data + re.compile('<a class="index_link" href="(.+?)">\s*(.+?)\s*<\/a>\s*<br>').findall(link.text)

    data_len = len(artists_data)
    total_artists = total_artists + len(artists_data)

    print ("new Char:")
    i=1
    for url, artist in artists_data:
        print (str(i) + " out of " + str(data_len))
        fh.write('{\n')
        try:
            fh.write('"artist":"'+artist.replace('\"','')+'",\n')
        except UnicodeEncodeError:
            fh.write('"artist":"null_artist",\n')
        extract_artist_matedata(url,fh)

        if (index == len(artists_data)):
            fh.write('}\n')
        else:
            fh.write('},\n')
        index += 1
        i += 1

def israeli_artists():
    #heb_chars = ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ז', 'ח', 'ט', 'י', 'כ', 'ל', 'מ', 'נ', 'ס', 'ע', 'פ', 'צ', 'ק', 'ר', 'ש', 'ת']
    heb_chars = ['ע', 'פ', 'צ', 'ק', 'ר', 'ש', 'ת']
    #heb_chars.reverse()

    index = 16
    for heb_char in heb_chars:
        start = time.time()
        fh = open("c:/json_files/"+str(index)+".json",'w')
        fh.write(json_header)
        get_char_artist('http://shironet.mako.co.il/servlet/com.dic.shironet.site.index.servletGetPerformersIndexPrefix?lang=1&prefix=' + heb_char + '&sort=popular&page=', fh, 1)
        fh.write(']\n}\n')
        fh.close()
        end = time.time()
        print ("run time for char "+ str(index)+ " is "+str(end - start)+" seconds.")
        index += 1

def main():
    global driver
    israeli_artists()
    driver.quit()

if __name__ == '__main__':
    main()
