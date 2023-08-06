# -*- coding:utf-8 -*-
# Author : tangxi
# Data : $2019/11/05 $11:31
import os
import cv2
import numpy as np
import dlib
import math
import argparse
import time
import matplotlib
from imutils import face_utils
from scipy.spatial import distance
import urllib.request
from urllib.request import urlretrieve
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"}
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def get_images(path):
    return [os.path.join(path,each) for each in os.listdir(path) if each.endswith(".jpg") or each.endswith(".jpeg")]

def eye_aspect_ratio(eye):
    '''
        计算眼睛部位的横纵比
    '''
    A = distance.euclidean(eye[1],eye[5])
    B = distance.euclidean(eye[2],eye[4])
    C = distance.euclidean(eye[0],eye[3])
    return (A+B)/(2.0*C)

def relight(img, light=1, bias=0):
    h = img.shape[0]
    w = img.shape[1]
    if len(img.shape)==2:
        for i in range(0,w):
            for j in range(0,h):
                tmp = int(img[j,i]*light + bias)
                if tmp > 255:
                    tmp = 255
                elif tmp < 0:
                    tmp = 0
                img[j,i] = tmp
    else:
        c = 3
        for i in range(0,w):
            for j in range(0,h):
                for ci in range(c):
                    tmp = int(img[j,i,ci]*light + bias)
                    if tmp > 255:
                        tmp = 255
                    elif tmp < 0:
                        tmp = 0
                    img[j,i,ci] = tmp
    return img

def calculate_region_sum(img,x,y,w,h):
    sum = 0
    for i in range(w):
        for j in range(h):
            for c in range(3):
                sum=sum+img[x+i,y+j,c]           
    return sum

def get_distance(pt1,pt2):
    return math.sqrt((pt1[0] - pt2[0])*(pt1[0]-pt2[0]) + (pt1[1]-pt2[1])*(pt1[1]-pt2[1]))

import sys
def get_face_landmarks(img):
    h_img,w_img = img.shape[0:2]

    img = relight(img,1.2,0.5)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #使用默认人脸识别的模型
    detector = dlib.get_frontal_face_detector()
    # 获取人脸关键点预训练模型
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    #获取眼睛的位置
    (lStart,lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
    (rStart,rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]
    dets = detector(gray, 1)
    flag = False   #是否有人脸,无人脸返回True
    is_fake = False 
    for i,d in enumerate(dets):
        flag = True
        ##获取人脸区域
        x1 = d.top() if d.top() > 0 else 0
        y1 = d.bottom() if d.bottom() > 0 else 0
        x2 = d.left() if d.left() > 0 else 0
        y2 = d.right() if d.right() > 0 else 0
        face = img[x1:y1,x2:y2]
        face_ratio = (y1-x1)*(y2-x2) / (h_img*w_img)
        print(face_ratio)
        if  face_ratio< 0.1:
            break
        ##先判断图像是否大致正常    
        chans = cv2.split(img)
        hist_res = 0
        for chan in chans:
            hist = cv2.calcHist([chan],[0],None,[256],[0,256])
            max_min= cal_max_min(hist)
            if max_min >8000:
                print(max_min)
                hist_res+=1
        if hist_res>2:
            is_fake=True
            
        shape = predictor(img, d)  # 寻找人脸的68个标定点
        shape_np = face_utils.shape_to_np(shape)
        
        all_points = []
        for j,pt in enumerate(shape.parts()):
            pt_pos = (pt.x, pt.y)
            all_points.append(pt_pos)
            cv2.circle(img,pt_pos,1,(0,255,0),-1)
        ##------------------看眼睛部分特征-----------------------------------------#
        leftEye = shape_np[lStart:lEnd]
        rightEye = shape_np[rStart:rEnd]
        rightEAR = eye_aspect_ratio(rightEye)
        leftEAR = eye_aspect_ratio(leftEye)
        ear = (leftEAR+rightEAR)/2
        print(ear)
        try:
            dis_eye_left1 = get_distance(all_points[19],all_points[37])/get_distance(all_points[37],all_points[41])
            dis_eye_left2 = get_distance(all_points[19],all_points[38])/get_distance(all_points[37],all_points[41])        
            dis_eye_right1 = get_distance(all_points[24],all_points[43])/get_distance(all_points[37],all_points[41])
            dis_eye_right2 = get_distance(all_points[24],all_points[44])/get_distance(all_points[37],all_points[41])
            eye_res = 0
            print(dis_eye_left1)
            print(dis_eye_left2)
            print(dis_eye_right1)
            print(dis_eye_right2)
            if dis_eye_left1>8:eye_res+=1
            if dis_eye_left2>8:eye_res+=1
            if dis_eye_right1>8:eye_res+=1
            if dis_eye_right2>8:eye_res+=1
            if ear >= 0.19 and eye_res > 2:
                is_fake = True
#                 print("fake face")
        except ZeroDivisionError as e:
            pass

        ##----------------------下面看嘴巴部分特征------------------------------------#
        # 遍历所有脸部特征点
        left=all_points[48];right= all_points[54];up=all_points[51];down=all_points[57];middle =all_points[66]
        mouth=[]
        mouth.append(shape.parts()[48]);mouth.append(shape.parts()[54]);mouth.append(shape.parts()[66]);mouth.append(shape.parts()[51])
        mouth_width = get_distance(right,left)
        if mouth_width<1:
            is_fake=True
            break
        mouth_height = get_distance(up,middle)
        mouth_ratio = mouth_height/mouth_width
        print(mouth_ratio)
        if mouth_ratio > 0.35:
#             print("张嘴")
            c = np.zeros((len(mouth),2))
            c = c.astype(np.float32)
            for i,p in enumerate(mouth):
                c[i,0] = float(p.x)
                c[i,1] = float(p.y)
            x, y, w, h = cv2.boundingRect(c)
            x_1 = x+int(w*0.3)
            y_1 = y+int(h*0.3)
            x_2 = x+int(w*0.8)
            y_2 = y+int(h*0.8)
            mouth_center = (int(x_1 + (x_2-x_1)/2),int(y_1+(y_2-y_1)/2))
            c=gray[mouth_center[1],mouth_center[0]]
            l=gray[left[1],left[0]]
            r=gray[right[1],right[0]]
            u=gray[up[1],up[0]]
            d=gray[down[1],down[0]]
            mouth_res = 0
            diff_l = c-l if c>l else l-c
            diff_r = c-r if c>r else r-c
            diff_u = c-u if c>u else u-c
            diff_d = c-d if c>d else d-c
            print(diff_l)
            print(diff_r)
            print(diff_u)
            print(diff_d)
            if diff_l >110:mouth_res=mouth_res+1
            if diff_r>110:mouth_res=mouth_res+1
            if diff_u>110:mouth_res=mouth_res+1
            if diff_d>110:mouth_res=mouth_res+1
            if mouth_res >=2:
                is_fake=True
    if flag == False:
        is_fake = False
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    plt.imshow(img)
    plt.show()
    return is_fake

def cal_max_min(hist):
    diff_max = -sys.maxsize-1
    for i in range(hist.shape[0]-1):
        if (hist[i+1][0] - hist[i][0]) >diff_max:
            diff_max = hist[i+1][0] - hist[i][0]
    return diff_max

def judge(imgname):
    is_fake = False
    try:
        img = cv2.imread(imgname)
        is_fake = get_face_landmarks(img)
        if is_fake==True:
            print(imgname," :fake faces")
        else:
            print(imgname," :pass")
    except Exception as e:
        pass
    return is_fake

def down_pic(url,path):
    """[用urlopen来把请求的数据写进路径，文件流的形式]
    
    Arguments:
        url {[string]} -- [待下载图像url]
        path {[string]} -- [图像下载后存放路径]
    """
    try:
        req = urllib.request.Request(url, headers=headers)
        data = urllib.request.urlopen(req).read()
        with open(path, 'wb') as f:
            f.write(data)
            f.close()
            print("download success")
    except Exception as e:
        print(str(e))
        
if __name__=="__main__":
    
    argparser = argparse.ArgumentParser(description="fake face detect")
    argparser.add_argument("--image_path",help="the path of image on disk")
    argparser.add_argument("--image_url",help="the url of image which can be downloaded")
    args = argparser.parse_args()
    if args.image_path:
        res = judge(args.image_path)
        if res:
            print("fake face")
        else:
            print("pass")
    elif args.image_url:
        path = str(int(time.time()))+".jpg"
        down_pic(args.image_url,path)
        res = judge(path)
        if res:
            print("fake face")
        else:
            print("pass")
#     imgs = get_images("huotijiance_real/")
#     imgs.sort()
#     fake_count=0
#     for each in imgs:
#         print(each,end='  :')
#         img = cv2.imread(each)
#         res = get_face_landmarks(img)
#         if res:
#             fake_count+=1
#         print("fake face" if res else "can not find problems")
#     print(fake_count) 
    
#     imgs = get_images("fake2/")
#     imgs.sort()
#     fake_count=0
#     for each in imgs:
#         print(each,end='  :')
#         img = cv2.imread(each)
#         res = get_face_landmarks(img)
#         if res:
#             fake_count+=1
#         print("fake face" if res else "can not find problems")
#     print(fake_count)  