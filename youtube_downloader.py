#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 09:29:46 2019

@author: ezhang
take Youtube playlist URL and download every video in the list
"""

import pandas as pd
import math
import datetime
import os
import pytube
import time
import subprocess

#袁视角playlist
playlist_url = 'https://www.youtube.com/playlist?list=PLnzvH6pAJKSrGZP9Z75wfc_CHJn9wTWR7'
download_fp = 'F:/Youtube/export/raw/'

pl = pytube.Playlist(playlist_url)
pl.populate_video_urls()

start_time = time.time()

for url in pl.video_urls:
#   get video info based on supplied video url
    try:
    #download the progressive version of mp4 file, pick the lowest res 
        pytube.YouTube(url).streams.filter(progressive = True, file_extension = 'mp4').order_by('resolution').first().download(download_fp)
    #report unavailable files and move on 
    except pytube.exceptions.VideoUnavailable:
        print('video not available: ' + url)
elapsed_time = time.time() - start_time
print('Runtime: '+ str(math.floor(elapsed_time))+ 's')

#convert mp4 to aac
foldername_raw = 'F:/Youtube/export/raw/'
foldername_convert = 'F:/Youtube/export/convert/'
ext_raw = '.mp4'
ext_convert = '.mp3'
# get the list of files in the directory, remove any subfolders, only keep actual files
filename_no_ext = [".".join(f.split(".")[:-1]) for f in os.listdir(foldername_raw) if os.path.isfile(foldername_raw + f)]

for f in filename_no_ext:
    command= 'G:/ffmpeg-4.2.1-win64-static/bin/ffmpeg.exe -i "' + foldername_raw + f + ext_raw + '" -f mp3 -ab 192000 -vn "' + foldername_convert + f + ext_convert + '"'
    subprocess.call(command)
    