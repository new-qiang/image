import cv2
import numpy as np
import math
import
face_cascade = cv2.CascadeClassifier('C:\haarcascades\haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier('C:\haarcascades\haarcascade_eye_tree_eyeglasses.xml')
nose_cascade = cv2.CascadeClassifier('C:\haarcascades\haarcascade_mcs_nose.xml')

def findface(img, gray):
    # 1.3  5    1.2 5
    faces = face_cascade.detectMultiScale(gray, 1.2, 5)
    face_n = len(faces)
    if face_n == 1:
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = img[y:y + h // 2, x:x + w]
            # 1.1  4   #1.2 4    1.2 2 !
            k = 5
            for i in range(5):
                eyes = eye_cascade.detectMultiScale(roi_gray, 1.2, k)
                n_eyes = len(eyes)
                print(k, "eyes:", n_eyes)

                if n_eyes == 2:
                    findeyes(eyes, roi_gray, x, y, w, h)
                    break
                elif k == 2:
                    print("请睁开双眼")
                    break
                elif n_eyes > 2:
                    k = k + 1
                    continue
                elif n_eyes < 2:
                    k = k - 1
                    continue
                    # print('发现%s只眼睛,请正对相机:' % (len(eyes)))
    elif face_n > 1:
        print('发现%s张脸,正在判断正前方的脸:' % (len(faces)))
        # 所有脸的宽度列表
        print(faces)
        face_nw = []
        for face_1 in faces:
            face_nw.append(face_1[2])
        face_nw2 = face_nw.copy()
        # print(face_nw,"-----")
        face_nw.sort(reverse=True)
        nw = face_nw2.index(face_nw[0])
        # print(nw)
        faces_true = [faces[nw]]
        # print(faces_true)
        for (x, y, w, h) in faces_true:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = img[y:y + h // 2, x:x + w]
            # 1.1  4   #1.2 4    1.2 2 !
            k = 5
            for i in range(5):
                eyes = eye_cascade.detectMultiScale(roi_gray, 1.2, k)
                n_eyes = len(eyes)
                print(k, "eyes:", n_eyes)
                if n_eyes == 2:
                    findeyes(eyes, roi_gray, x, y, w, h)
                    break
                elif k == 2:
                    print("请睁开双眼")
                    break
                elif n_eyes > 2:
                    k = k + 1
                    continue
                elif n_eyes < 2:
                    k = k - 1
                    continue
    else:
        print('脸部过分倾斜,请正对相机:' % (len(faces)))
        return 0
def findeyes(eyes, roi_gray, x, y, w, h):
    for (ex, ey, ew, eh) in eyes:
        cv2.circle(roi_gray, (int(ex + ew / 2), int(ey + eh / 2)), 8, (0, 0, 255), -1)
    face_center = (w // 2, h // 2)
    eye_l = (eyes[0][0] + eyes[0][2] // 2, eyes[0][1] + eyes[0][3] // 2)
    eye_r = (eyes[1][0] + eyes[1][2] // 2, eyes[1][1] + eyes[1][3] // 2)
    p_x = int(x + (eyes[0][0] + eyes[0][2] / 2 + eyes[1][0] + eyes[1][2] / 2) / 2)
    p_y = int(y + (eyes[0][1] + eyes[0][3] / 2 + eyes[1][1] + eyes[1][3] / 2) / 2)
    cv2.circle(img, (p_x, p_y), 5, (0, 0, 255), -1)
    cv2.line(roi_gray, eye_l, eye_r, (0, 0, 255), 1)
    tan_eye = (eye_r[1] - eye_l[1]) / (eye_r[0] - eye_l[0])
    angle_eye = math.degrees(math.atan(tan_eye))
    if angle_eye > 4.5:
        print("左眼高%s" % (angle_eye))
    elif angle_eye < -4.5:
        print("右眼高%s" % (abs(angle_eye)))
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
            cv2.circle(roi_gray, (int(nx + nw / 2), int(ny + nh / 2)), 10, (0, 0, 255), 1)
            # print ((nose_center[1] , eye_l[1] ) , (nose_center[0] , eye_l[0]))
            bili = abs(nose_center[1])
            print(nose_center, w, bili)
            bili = bili / w
            if angle_nose > 6.3:
                print("鼻子左右倾斜:%s" % (angle_nose))
            else:
                if bili < 0.185:
                    print("请勿仰头")
    else:
        print("鼻子???")
    # print('发现%s个鼻子,请正对相机:' % (len(nose)))
    return (x, y, w, h, p_x, p_y)
    # cap = cv2.VideoCapture(1)
try:
    image = input('请输入图片名(绝对路径): ')
        # print(kkk)
    img = cv2.imdecode(np.fromfile(image, dtype=np.uint8), -1)
    # while 1:
    # res, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.equalizeHist(gray, gray)
    findface(img, gray)
except FileNotFoundError:
    print("文件路径不正确")
finally:
    print("请重新调用")
