# -*- coding: <utf-8> -*-
import cv2
import numpy as np
import math
import glob
import time
import sys
import os
face_cascade = cv2.CascadeClassifier('C:\haarcascades\haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier('C:\haarcascades\haarcascade_eye_tree_eyeglasses.xml')
nose_cascade = cv2.CascadeClassifier('C:\haarcascades\haarcascade_mcs_nose.xml')
def finhead(img, gray, x, y, w, h, p_x, p_y):
    face_data = (x, y, w, h, p_x, p_y)
    ph = gray[int(face_data[1] - face_data[3] / 2):face_data[1], face_data[0]:face_data[0] + face_data[2]]
    blur = cv2.GaussianBlur(ph, (5, 5), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    mage, contours, hierarchy = cv2.findContours(th3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    min_point = []
    for i in contours:
        min_point.append(i[0][:1][0][-1])
    min_point.sort()
    min_P = face_data[1] - face_data[3] / 2 + min_point[0]
    min_P = int(min_P)
    k = face_data[2] / 250 * 472
    b = face_data[2] / 250 * 177
    min_P = min_P - face_data[2] / 250 * 15
    data_all = (face_data, min_P, b, k)
    pic_h = (data_all[-3], data_all[-3] + data_all[-1])
    pic_w = (data_all[0][-2] - data_all[-2], data_all[0][-2] + data_all[-2])
    one_pic = img[int(pic_h[0]):int(pic_h[1]), int(pic_w[0]):int(pic_w[1])]
    res = cv2.resize(one_pic, (354, 472), interpolation=cv2.INTER_AREA)
    cv2.imencode('.jpg', res)[1].tofile('%ss裁剪.jpg' % (kkk))
def findface(img, gray):
    faces = face_cascade.detectMultiScale(gray, 1.2, 5)
    face_n = len(faces)
    if face_n == 1:
        for (x, y, w, h) in faces:
            roi_gray = img[y:y + h // 2, x:x + w]
            k = 5
            for i in range(5):
                eyes = eye_cascade.detectMultiScale(roi_gray, 1.2, k)
                n_eyes = len(eyes)
                if n_eyes == 2:
                    findeyes(eyes, roi_gray, x, y, w, h, k)
                    break
                elif k == 2:
                   # print("请睁开双眼")
                    print("图片不通过")
                    break
                elif n_eyes > 2:
                    k = k + 1
                    continue
                elif n_eyes < 2:
                    k = k - 1
                    continue
    elif face_n > 1:
        print('正在判断正前方的脸:')
        face_nw = []
        for face_1 in faces:
            face_nw.append(face_1[2])
        face_nw2 = face_nw.copy()
        face_nw.sort(reverse=True)
        nw = face_nw2.index(face_nw[0])
        faces_true = [faces[nw]]
        for (x, y, w, h) in faces_true:
            roi_gray = img[y:y + h // 2, x:x + w]
            k = 5
            for i in range(5):
                eyes = eye_cascade.detectMultiScale(roi_gray, 1.2, k)
                n_eyes = len(eyes)
                if n_eyes == 2:
                    findeyes(eyes, roi_gray, x, y, w, h, k)
                    break
                elif k == 2:
                    #print("请睁开双眼")
                    print("图片不通过")
                    break
                elif n_eyes > 2:
                    k = k + 1
                    continue
                elif n_eyes < 2:
                    k = k - 1
                    continue
    else:
        #print('脸部过分倾斜,请正对相机:')
        print("图片不通过")
        return 0
def findeyes(eyes, roi_gray, x, y, w, h, k):
    yanjing = True
    face_center = (w // 2, h // 2)
    eye_l = (eyes[0][0] + eyes[0][2] // 2, eyes[0][1] + eyes[0][3] // 2)
    eye_r = (eyes[1][0] + eyes[1][2] // 2, eyes[1][1] + eyes[1][3] // 2)
    p_x = int(x + (eyes[0][0] + eyes[0][2] / 2 + eyes[1][0] + eyes[1][2] / 2) / 2)
    p_y = int(y + (eyes[0][1] + eyes[0][3] / 2 + eyes[1][1] + eyes[1][3] / 2) / 2)
    tan_eye = (eye_r[1] - eye_l[1]) / (eye_r[0] - eye_l[0])
    angle_eye = math.degrees(math.atan(tan_eye))
    if angle_eye > 3.9:
        #print("双眼不平:%s°" % round(abs(angle_eye)))
        #print("图片不通过")
        yanjing = False
    elif angle_eye < -4.5:
        #print("双眼不平:%s°" % round(abs(angle_eye)))
        #print("图片不通过")
        yanjing = False
    roi_gray = img[p_y:y + h + 1, x:x + w + 1]
    nose = nose_cascade.detectMultiScale(roi_gray, 1.2, 9)
    n_nose = len(nose)
    if n_nose == 1:
        for (nx, ny, nw, nh) in nose:
            nose_center = (int(nx + nw / 2), int(ny + nh / 2))
            tan_nose1 = (nose_center[1] - eye_l[1]) / (nose_center[0] - eye_l[0])
            tan_nose2 = (nose_center[1] - eye_r[1]) / (nose_center[0] - eye_r[0])
            angle_nose1 = math.degrees(math.atan(tan_nose1))
            angle_nose2 = math.degrees(math.atan(tan_nose2))
            angle_nose = abs(abs(angle_nose2) - abs(angle_nose1))
            bili = abs(nose_center[1])
            bili = bili / w
            if angle_nose > 6.3 :
                #print("鼻子左右倾斜:%s" % round(angle_nose, 2))
                fenshu = round(k / 5 * 60 + ((6.3 - angle_nose) / 6.3) * 20 + ((bili - 0.185) / 0.25) * 20, 2)
                print("图片不通过，分数:%s,鼻子左右倾斜" % fenshu)
            elif not yanjing:
                fenshu = round(k / 5 * 60 + ((6.3 - angle_nose) / 6.3) * 20 + ((bili - 0.185) / 0.25) * 20, 2)
                print("图片不通过，分数:%s,双眼不平" % fenshu)
            else:
                if bili < 0.185 :
                    #print("请勿仰头")
                    fenshu = round(k / 5 * 60 + ((6.3 - angle_nose) / 6.3) * 20 + ((bili - 0.185) / 0.25) * 20, 2)
                    print("图片不通过，分数:%s,请勿仰头" % fenshu)
                else:
                    fenshu = round(k / 5 * 60 + ((6.3 - angle_nose) / 6.3) * 20 + ((bili - 0.185) / 0.25) * 20, 2)

                    print("图片通过，分数:%s" % fenshu)
        finhead(img, gray, x, y, w, h, p_x, p_y)
    else:
        print("图片不通过")
input_1 = sys.argv
if len(input_1) > 1:
    images = glob.glob(sys.argv[1])
    for kkk in images:
        filename_1 = os.path.dirname(kkk)
        img = cv2.imdecode(np.fromfile(kkk, dtype=np.uint8), -1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        findface(img, gray)
else:
    print("请输入路径")