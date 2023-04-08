from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

import math
import pandas as pd
import cv2
import imageio
from django.http.response import HttpResponse
import mimetypes
import os
from PIL import Image
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
from datetime import date
from datetime import datetime


import base64

def home(request):
    return render(request, 'todo/home.html')

def qr_c(request):
    return render(request, 'todo/profile.html')




def download_file(request):
    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    filename = 'test.txt'
    # Define the full file path
    filepath = BASE_DIR + '/downloadapp/Files/' + filename
    # Open the file for reading content
    path = open(filepath, 'r')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response


    response = HttpResponse(content_type='image/png')
    image.save(response, 'png')
    response['Content-Disposition'] = 'attachment; filename={0}'.format("Export.png")

    return response




def getlocation(request,PM_site,PM_floor,PM_piller):

    piller_information = pd.read_excel('Korum_data_5.xlsx')
    piller_info_name = pd.read_excel('Korum_data_pillers.xlsx')

    piller_name = []
    piller_replacement = []
    locations = []
    for i in range(len(piller_info_name)):
        piller_name.append(piller_info_name["piller name"][i])
        locations.append(piller_info_name["piller name"][i].replace(' ','_'))

        piller_replacement.append(piller_info_name["replacement name"][i])

    Piller_names = dict(zip(piller_name, piller_replacement))


    PM_site = PM_site.replace('_',' ')
    PM_floor = PM_floor.replace('_',' ')
    PM_piller = PM_piller.replace('_',' ')

    if request.method == 'POST':


        location2find = request.POST['location2find'] 
        location2find = location2find.replace('_',' ')
        PM_piller = PM_piller.replace('_',' ')

        print('PM site = ' + PM_site)
        print('PM floor = ' + PM_floor)
        print('PM piller = ' + PM_piller)
        print('location2find = ' + location2find)
# 

        firstnode = PM_piller
        secondnode = location2find

        firstnode = Piller_names[firstnode]
        secondnode = Piller_names[secondnode]

        import time
        start_time = time.time()

        nodes=[]
        Dict={}

        ##print('*****************************************')
        ##print('PARKOMATE ROUTE FINDING SIMULATOR - BEGIN')
        ##print('*****************************************')
        ##print()

        neigDict={}
        piller2piller_max_distance = 100
        piller2piller_max_distance_x = 150
        piller2piller_max_distance_y = 150

        def route(dict,x,y,routes=None):
            if routes is None:
                routes = [x]
            if x == y:
                c=0
                for a in range(1,len(routes),1):
                    distxx=(Dict[routes[a-1]])[0]
                    distyx=(Dict[routes[a-1]])[1]
                    distxnext=(Dict[routes[a]])[0]
                    distynext=(Dict[routes[a]])[1]
                    dist = math.sqrt(((float(distxnext)-float(distxx))**2)+((float(distynext)-float(distyx))**2))
                    cost=dist
                    c=c+cost
                Costs.append(c)
                yield routes
            for next in dict[x] - set(routes):
                yield from route(dict,next,y,routes+[next])



        def repeat():
            length = len(sorted(list(route(neigDict,firstnode,secondnode))))
            print("\t"+ str(length) +' ROUTE(S) FOUND:')
            
            R =list(route(neigDict,firstnode,secondnode))
            c=0
            selectednumb=0
            selectedpath=[]
            if len(R)==0:
                return None
            number_of_iterations = 0
            for i in R:
                c+=1
                if Costs[c-1] == min(Costs):
                    selectednumb=str(c)
                    selectedpath.append(i)

            print("\tSELECTED ROUTE (ROUTE " + str(selectednumb) + "): " + " -> ".join(min(selectedpath)))
            return min(selectedpath)
            """print("\tPACKET " + + " HAS BEEN SENT")"""



        neighborhood = []

        for i in range(len(piller_information)):
            L = []
            L.append(piller_information["Piller name"][i])
            L.append([piller_information["x_cor"][i],piller_information["y_cor"][i]])
            nodes.append(L)
            Dict[L[0]]=[L[1][0],L[1][1]]
            NH = []
            NH.append(piller_information["Piller name"][i])
            for k in piller_information["neighborhood"][i].split(','):
                NH.append(k)
            neighborhood.append(NH)
            for i in neighborhood:
                neigDict[i[0]]=i[1:]
            for i in neigDict.keys():
                neigDict[i]=set(neigDict[i])

            for i in neigDict.keys():
                g=""
                for a in neigDict[i]:
                    g=g+a+", "

        path = 'KORUM_MALL.png'
        image = cv2.imread(path)
        window_name = 'KORUM_MALL'


        x=1
        Costs=[]
        Final_path = repeat()

        color = (255,0, 0)
        thickness = 2
        radius = 5
        color2 = (5, 0, 200)
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 0.5
        image = cv2.circle(image, (Dict[Final_path[0]][0],Dict[Final_path[0]][1]), radius, color, thickness)
        image = cv2.putText(image, "You are Here",(Dict[Final_path[0]][0]-45,Dict[Final_path[0]][1]-10), font, fontScale, color2, 1, cv2.LINE_AA)


        image = cv2.circle(image, (Dict[Final_path[len(Final_path)-1]][0],Dict[Final_path[len(Final_path)-1]][1]), radius, color, thickness)
        image = cv2.putText(image, "You are Here",(Dict[Final_path[0]][0]-45,Dict[Final_path[0]][1]-10), font, fontScale, color2, 1, cv2.LINE_AA)


        color = (5,250, 0)


        for i in range(len(Final_path)-1):
            
            image = cv2.line(image, Dict[Final_path[i]], Dict[Final_path[i+1]], color, thickness)
            image = cv2.circle(image, (Dict[Final_path[i]][0],Dict[Final_path[i]][1]), radius, color, thickness)
            # cv2.waitKey(1)
            # cv2.imshow(window_name, image)

        print("Time taken to get result %s seconds " % round((time.time() - start_time),3))

        # cv2.imshow(window_name, image)
        # cv2.waitKey(500)
        # cv2.destroyWindow(window_name)


        Final_path_str = 'Shortest path : \n'
        for f in Final_path:
            Final_path_str += f + ' => '
        
        Final_path_str = Final_path_str[0:len(Final_path_str)-3]

        now = datetime.now()

        now = str(now)
        now = now.replace('-','_')
        now = now.replace(' ','_')
        now = now.replace(':','_')
        now = now.replace('.','_')
        print(now)
        # cv2.imwrite("static/videos/"+ now  +".png",image)

        cv2.imwrite("todo/static/videos/"+ now  +".png",image)

        path1= '/videos/'+ now  +'.png'
        print(path1)

        return render(request, 'todo/viewtodo.html',{"Final_path_str":Final_path_str,'path1': path1})

    else:
        return render(request, 'todo/getlocation.html',{'PM_site':PM_site,'PM_floor':PM_floor,'PM_piller':PM_piller,'locations':locations})


