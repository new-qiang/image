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
def cut_pic():

    res = cv2.resize(img_jianjie, (354, 472), interpolation=cv2.INTER_AREA)
    cv2.putText(res, 'Beta 1.01', (5, 460), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
    imageVar = cv2.Laplacian(res, cv2.CV_64F).var()
    if imageVar< 250:
        print("提示:图片模糊")
        cv2.imencode('.jpg', res)[1].tofile('%ss裁剪.jpg' % (images))
    else:
        cv2.imencode('.jpg', res)[1].tofile('%ss裁剪.jpg' % (images))
input_1 = sys.argv
if len(input_1) > 1:
    im = glob.glob(sys.argv[1])
    for images in im:
        #print(images)
        img = cv2.imdecode(np.fromfile(images, dtype=np.uint8), -1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)
        face_n = len(faces)
        face_n_b = False
        if face_n == 1:
            for (x, y, w, h) in faces:
                face_n_b = True
        elif face_n > 1:
            print('正在判断正前方的脸:')
            face_nw = []
            for face_1 in faces:
                face_nw.append(face_1[2])
            face_nw2 = face_nw.copy()
            face_nw.sort(reverse=True)
            nw = face_nw2.index(face_nw[0])
            # 得到最大的脸
            faces_true = [faces[nw]]
            for (x, y, w, h) in faces_true:
                face_n_b = True
        if face_n_b:
            # 带头顶的区域
            #高_起点
            a =int(y - h/3)
            #终点
            b= int(a + 472.0* w/250.0)
            #宽起点
            c =int(x+w/2 - (354.0 * w /250.0)/2)
            #终点
            d =int(c + w/250.0*354.0)

            if a <0   :
                a = 0
                print("头顶太接近顶部")
            if b> img.shape[0]:
                b = img.shape[0]
                a = b - int(472.0* w/250.0)
            if c <0 :
                print("头顶太接近顶部")
                c = 0
            if d>img.shape[1]:
                d = img.shape[1]
                c = d - int(354.0* w/250.0)
            img_jianjie = img[a:b, c:d]
            cv2.imwrite("D:\\123.jpg", img_jianjie)
            roi_gray_all = gray[y:y+h,x:x+w]
            roi_gray_e = gray[y:y + h // 2, x:x + w]
            k = 5
            for i in range(5):
                eyes = eye_cascade.detectMultiScale(roi_gray_e, 1.2, k)
                n_eyes = len(eyes)

                if n_eyes == 2:
                    if k >5:
                        k = 4
                    yanjing = True
                    eye_l = (eyes[0][0] + eyes[0][2] // 2, eyes[0][1] + eyes[0][3] // 2)
                    eye_r = (eyes[1][0] + eyes[1][2] // 2, eyes[1][1] + eyes[1][3] // 2)
                    tan_eye = (eye_r[1] - eye_l[1]) / (eye_r[0] - eye_l[0])
                    angle_eye = math.degrees(math.atan(tan_eye))
                    if angle_eye > 3.9:
                        #print("双眼不平:%s°" % round(abs(angle_eye)))
                        # print("图片不通过")
                        yanjing = False
                    elif angle_eye < -4.5:
                        #print("双眼不平:%s°" % round(abs(angle_eye)))
                        # print("图片不通过")
                        yanjing = False
                    roi_gray_nose  =  roi_gray_all[h//2:h+1,0:w]
                    nose = nose_cascade.detectMultiScale(roi_gray_all, 1.3, 9)
                    n_nose = len(nose)

                    if n_nose == 1:
                        for (nx, ny, nw, nh) in nose:
                            nose_center = (int(nx + nw / 2 ), int(ny + nh / 2))
                            tan_nose1 = (nose_center[1] - eye_l[1]) / (nose_center[0] - eye_l[0])
                            tan_nose2 = (nose_center[1] - eye_r[1]) / (nose_center[0] - eye_r[0])
                            angle_nose1 = math.degrees(math.atan(tan_nose1))
                            angle_nose2 = math.degrees(math.atan(tan_nose2))
                            angle_nose = abs(abs(angle_nose2) - abs(angle_nose1))
                            bili = abs(nose_center[1]-h/2)
                            bili = bili / w
                            # print(angle_nose1,angle_nose2, angle_eye ,bili)
                            if angle_nose > 7:
                                fenshu = round(k / 5 * 60  + ((0.15 - bili ) / 0.15) * 20 ,2)
                                print("提示:鼻子左右倾斜，分数:%s" % fenshu)
                            elif not yanjing:
                                fenshu = round(k / 10 * 60 +  ((7 - angle_nose) / 7) * 20 + ((0.15 - bili ) / 0.15) * 20,2)
                                print("提示:双眼不平，分数:%s" % fenshu)
                            else:
                                if bili < 0.08:
                                    #print(k, angle_nose)
                                    fenshu = round(k / 5 * 60 + ((7 - angle_nose) / 7) * 20 ,2)
                                    print("提示:请勿头仰，分数:%s" % fenshu)
                                else:
                                    #print(k / 5 * 60, angle_nose, bili)
                                    fenshu = round(k/5 * 60 + ((7 - angle_nose) / 7) * 20 + ((0.15 - bili ) / 0.15) * 20,2)
                                    print("图片通过，分数:%s" % fenshu)
                            cut_pic()
                    elif n_nose>1:
                        nose_nw = []
                        for nose_1 in nose:
                            nose_nw.append(nose_1[2])
                        nose_nw2 = nose_nw.copy()
                        nose_nw.sort(reverse=True)
                        nw = nose_nw2.index(nose_nw[0])
                        # 得到最大的脸
                        nose_true = [nose[nw]]
                        for (nx, ny, nw, nh) in nose_true:
                            face_n_b = True
                            nose_center = (int(nx + nw / 2), int(ny + nh / 2))
                            tan_nose1 = (nose_center[1] - eye_l[1]) / (nose_center[0] - eye_l[0])
                            tan_nose2 = (nose_center[1] - eye_r[1]) / (nose_center[0] - eye_r[0])
                            angle_nose1 = math.degrees(math.atan(tan_nose1))
                            angle_nose2 = math.degrees(math.atan(tan_nose2))
                            angle_nose = abs(abs(angle_nose2) - abs(angle_nose1))
                            bili = abs(nose_center[1] - h / 2)
                            bili = bili / w
                            # print(angle_nose1,angle_nose2, angle_eye ,bili)
                            if angle_nose > 7:
                                fenshu = round(k / 5 * 60 + ((0.15 - bili) / 0.15) * 20, 2)
                                print("提示:鼻子左右倾斜，分数:%s" % fenshu)
                            elif not yanjing:
                                fenshu = round(k / 10 * 60 + ((7 - angle_nose) / 7) * 20 + ((0.15 - bili) / 0.15) * 20,
                                               2)
                                print("提示:双眼不平，分数:%s" % fenshu)
                            else:
                                if bili < 0.08:
                                    # print(k, angle_nose)
                                    fenshu = round(k / 5 * 60 + ((7 - angle_nose) / 7) * 20, 2)
                                    print("提示:请勿头仰，分数:%s" % fenshu)
                                else:
                                    # print(k / 5 * 60, angle_nose, bili)
                                    fenshu = round(
                                        k / 5 * 60 + ((7 - angle_nose) / 7) * 20 + ((0.15 - bili) / 0.15) * 20-30, 2)
                                    print("图片通过2，分数:%s" % fenshu)
                            cut_pic()
                    else:
                        fenshu = round(k / 5 * 60)
                        print("提示:图像质量差 , 分数:%s"%fenshu)
                        cut_pic()
                    break
                elif k == 2:

                    fenshu = round(k / 5 * 60)
                    print("提示:注意眼睛_%s , 分数:%s" % (n_eyes,fenshu))
                    cut_pic()
                    break
                elif n_eyes < 2:
                    k = k - 1
                    continue
                elif k == 9:
                    fenshu = round(k / 20 * 60)
                    print("提示:注意眼睛 , 分数:%s" % fenshu)
                    cut_pic()
                elif 2<n_eyes <9:
                    k = k + 1
                    continue
        else:
             print('脸部过分倾斜,请正对相机,眼睛不要被镜框遮挡:')

