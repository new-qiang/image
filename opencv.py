import cv2
import numpy as np
import math
face_cascade = cv2.CascadeClassifier('D:\opencv\opencv\sources\data\haarcascades\haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier('D:\opencv\opencv\sources\data\haarcascades\haarcascade_eye_tree_eyeglasses.xml')
nose_cascade = cv2.CascadeClassifier('D:\opencv\opencv\sources\data\haarcascades\haarcascade_mcs_nose.xml')
def findface(img, gray):
    # 1.3  5
    faces = face_cascade.detectMultiScale(gray, 1.2, 5)
    face_n =len(faces)
    if face_n == 1:
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = img[y:y + h//2, x:x +w]
            # 1.1  4   #1.2 4    1.2 2 !
            k = 5
            for i in range(4):
                eyes = eye_cascade.detectMultiScale(roi_gray, 1.2, k)
                n_eyes = len(eyes)
                if k == 2:
                    print("请睁开双眼")
                    break
                elif n_eyes > 2:
                    k = k + i
                    continue
                elif n_eyes < 2:
                    k = k - i
                    continue
                elif n_eyes == 2 :
                    findeyes(eyes, roi_gray, x, y, w, h)
                    print(k)
                #print('发现%s只眼睛,请正对相机:' % (len(eyes)))

    elif  face_n>1:
        print('发现%s张脸,正在识别最前方的脸:' % (len(faces)))
    else:
        print('发现%s张脸,请正面对相机:' % (len(faces)))
        return 0
def findeyes(eyes, roi_gray,x, y, w, h):
    for (ex, ey, ew, eh) in eyes:
        cv2.circle(roi_gray, (int(ex + ew / 2), int(ey + eh / 2)), 8, (0, 0, 255), -1)
    eye_l = (eyes[0][0] + eyes[0][2] // 2, eyes[0][1] + eyes[0][3] // 2)
    eye_r = (eyes[1][0] + eyes[1][2] // 2, eyes[1][1] + eyes[1][3] // 2)
    p_x = int(x + (eyes[0][0] + eyes[0][2] / 2 + eyes[1][0] + eyes[1][2] / 2) / 2)
    p_y = int(y + (eyes[0][1] + eyes[0][3] / 2 + eyes[1][1] + eyes[1][3] / 2) / 2)
    cv2.circle(img, (p_x, p_y), 5, (0, 0, 255), -1)
    cv2.line(roi_gray, eye_l, eye_r, (0, 0, 255), 1)
    tan_eye = (eye_r[1] - eye_l[1]) / (eye_r[0] - eye_l[0])
    angle_eye = math.degrees(math.atan(tan_eye))
    if angle_eye > 4.5:
        print("右眼高%s" % (angle_eye))
    elif angle_eye < -4.5:
        print("左眼高%s" % (abs(angle_eye)))
    roi_gray = img[p_y:y + h, x:x + w]
    nose = nose_cascade.detectMultiScale(roi_gray, 1.3, 9)
    for (nx, ny, nw, nh) in nose:
        cv2.circle(roi_gray, (int(nx + nw / 2), int(ny + nh / 2)), 10, (0, 0, 255), 1)
    #print('发现%s个鼻子,请正对相机:' % (len(nose)))
    return (x, y, w, h, p_x, p_y)
if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    # img = cv2.imdecode(np.fromfile('C:\\Users\\75687\\Desktop\\QQ图片20170512201206.jpg', dtype=np.uint8), -1)
    while 1:
        res, img = cap.read()
        res, img = cap.read()
        res, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # cv2.equalizeHist(gray, gray)
        findface(img, gray)
        cv2.imshow("me", img)
        cv2.waitKey(100)
