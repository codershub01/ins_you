from django.shortcuts import render
from .serializer import you_serial , igtv_serial
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from pytube import YouTube
from moviepy.editor import *
import os , time
from selenium import webdriver
# Create your views here.
#


@api_view(['POST'])
def Resolution(request):
    if request.method == "POST":
        s = igtv_serial(data=request.data)
        if s.is_valid():
            url = s.data['url']
            youtube = YouTube(url)
            reso_ = []
            stream = youtube.streams
            for i in stream:
                stream_data = str(i)
                if 'mime_type="video/mp4"' in stream_data:
                    for j in stream_data.split(" "):
                        if j.startswith("res"):
                            reso_.append(j)
            resolution = {
                "mime_type":'video/mp4',
                'res':reso_
            }
            return Response(resolution,status=status.HTTP_200_OK)
        return Response(s.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def you(request):
    if request.method == 'POST':
        s = you_serial(data=request.data)
        if s.is_valid():
            u = s.data['url']
            pix = s.data['pixel']
            youtube = YouTube(u)
            thumb_ = u  .split('v=')[1]
            if pix == '360p' :
                video = youtube.streams.filter(res="360p").first()
                thumbnail_link = "https://i.ytimg.com/vi/"+thumb_+"/mqdefault.jpg"
            elif pix == '480p' :
                video = youtube.streams.filter(res="480p").first()
                thumbnail_link = "https://i.ytimg.com/vi/"+thumb_+"/sddefault.jpg"
            elif pix == '720p' :
                video = youtube.streams.filter(res="720p").first()
                thumbnail_link = "https://i.ytimg.com/vi/"+thumb_+"/hqdefault.jpg"
            elif pix == '1080p':
                video = youtube.streams.filter(res="1080p").first()
                thumbnail_link = "https://i.ytimg.com/vi/"+thumb_+"/maxresdefault.jpg"
            ytb = video.download()
            res = {
                "video": ytb,
                "title": youtube.title,
                "length": youtube.length,
                "thumbnail": thumbnail_link
            }
            return Response(res, status=status.HTTP_200_OK)

        return Response(s.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def mp3(request):
    if request.method == 'POST':
        print(12)
        s = you_serial(data=request.data)

        if s.is_valid():
            u = s.data['url']
            youtube = YouTube(u)
            v = youtube.streams.filter(only_audio=True).first()
            ytb = v.download()
            videoclip = AudioFileClip(ytb)
            mp3  = videoclip.write_audiofile(ytb[0:len(ytb)-3]+'mp3')
            os.remove(ytb)
            res = {
                "video": mp3,
                "title":youtube.title,
                "length": youtube.length,
                "thumbnail":youtube.thumbnail_url
            }

            return Response(res,status=status.HTTP_200_OK)
        return Response(s.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def igtv(request):

    if request.method == 'POST':
        serializer = igtv_serial(data=request.data)
        if serializer.is_valid():
            url = serializer.data['url']

            driver = webdriver.Firefox(executable_path='/home/nr/Desktop/youinsta/yi/geckodriver')
            # driver.headless =True
            driver.get('https://instasave.website/')
            x = driver.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/form/input")
            x.send_keys(url)
            driver.find_element_by_id("submit").click()
            igtv_ref = driver.find_element_by_xpath("/html/body/div[2]/div/div/div[1]/a").click()
            driver.close()
            res= {
                'igtv_url':url,
                'web_platform': "https://instasave.website/",
                "download_url" : igtv_ref
            }
            return Response(res,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)