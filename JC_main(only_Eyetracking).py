import sys

import cv2
import numpy as np
import dlib
from math import hypot
import pyglet

from unicode import join_jamos

from PIL import ImageFont, ImageDraw, Image

from PyQt5.QtWidgets import QDialog, QApplication
from qtpy import uic
from PyQt5.QtCore import Qt


#opencv 응시 확인용 글씨, 지울거임
font = cv2.FONT_HERSHEY_PLAIN

#출력창 상단바 없애기
class Popup:
    pass

#출력창 UI
main = uic.loadUiType("board.ui")[0]

#출력창 UI
class lb(QDialog, main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

# Load sounds
sound = pyglet.media.load("sound.wav", streaming=False)

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

width = 1900
height = 910

#배경 RGB
c_back = (143,163,138)
#버튼 RGB
c_btn_org = (220,240,245)
#버튼 깜빡 RGB
c_btn_b = (154,217,240)

# 4개 고르는 창(JA1~JA7, MO1~MO6 공통으로 사용, 위에 글자만 바뀌는거임)
keyboard = np.zeros((height, width, 3), np.uint8)
keyboard[:] = c_back

fontpath = "hy강b-yoond1004.ttf"
#응시창 글씨
imageFont_G = ImageFont.truetype(fontpath, 200)
#메인창 글씨
imageFont = ImageFont.truetype(fontpath, 50)

keys_set_ja1 = {0: "ㄱ", 1: "ㄷ", 2: "ㄲ", 3: "ㄸ"}
keys_set_ja2 = {0: "ㄴ", 1: "ㄹ", 2: "ㅁ", 3: "ㅇ"}
keys_set_ja3 = {0: "ㅂ", 1: "ㅅ", 2: "ㅃ", 3: "ㅆ"}
keys_set_ja4 = {0: "ㅈ", 1: "ㅊ", 2: "ㅉ", 3: "ㅋ"}
keys_set_ja5 = {0: "ㅌ", 1: "ㅍ", 2: "ㅎ", 3: "ㄺ"}
keys_set_ja6 = {0: "ㄻ", 1: "ㄼ", 2: "ㄾ", 3: "ㅀ"}
keys_set_ja7 = {0: "ㄳ", 1: "ㅄ", 2: "ㄵ", 3: "ㄶ"}

keys_set_mo1 = {0: "ㅏ", 1: "ㅑ", 2: "ㅓ", 3: "ㅕ"}
keys_set_mo2 = {0: "ㅗ", 1: "ㅛ", 2: "ㅜ", 3: "ㅠ"}
keys_set_mo3 = {0: "ㅡ", 1: "ㅣ", 2: "ㅐ", 3: "ㅒ"}
keys_set_mo4 = {0: "ㅔ", 1: "ㅖ", 2: "ㅢ", 3: "ㅙ"}
keys_set_mo5 = {0: "ㅚ", 1: "ㅘ", 2: "ㅟ", 3: "ㅝ"}

keys_set_jamain = {0: "ㄱ ㄷ\nㄲ ㄸ",
                   1: "ㄴ ㄹ\nㅁ ㅇ",
                   2: "ㅂ ㅅ\nㅃ ㅆ",
                   3: "ㅈ ㅊ\nㅉ ㅋ",
                   4: "ㅌ ㅍ\nㅎ ㄺ",
                   5: "ㄻ ㄼ\nㄾ ㅀ",
                   6: "ㄳ ㅄ\nㄵ ㄶ",
                   7: "자동\n완성",
                   8: "취소",
                   9: "TTS"}

keys_set_momain = {0: "ㅏ ㅑ\nㅓ ㅕ",
                   1: "ㅗ ㅛ\nㅜ ㅠ",
                   2: "ㅡ ㅣ\nㅐ ㅒ",
                   3: "ㅔ ㅖ\nㅢ ㅙ",
                   4: "ㅚ ㅘ\nㅟ ㅝ",
                   5: "완료"}

keys_set_auto = {0: "아파요",
                 1: "아니요",
                 2: "물",
                 3: "가려워",
                 4: "네",
                 5: "이전"}

#응시 창 그리기
def draw_letter_G(letter_index, text):
    global gaze_pil, draw

    # Keys
    if letter_index == 0:
        x = 10
        y = 10
    elif letter_index == 1:
        x = int(width / 2) + 10
        y = 10
    elif letter_index == 2:
        x = 10
        y = int(height / 2) + 10
    elif letter_index == 3:
        x = int(width / 2) + 10
        y = int(height / 2) + 10

    f_width = int(width / 2) - 20
    f_height = int(height / 2) - 20

    text_x = int(f_width / 2 + x - 100)
    text_y = int(f_height / 2 + y - 100)

    cv2.rectangle(keyboard, (x, y), (x + f_width, y + f_height), c_btn_org, -1)

    gaze_pil = Image.fromarray(keyboard)
    draw = ImageDraw.Draw(gaze_pil)
    draw.text((text_x,text_y),text, font=imageFont_G, fill=(51,51,51))

#jamain창(깜빡임)
def draw_letter_B_jamain(letter_index, text, letter_light):
    global gaze_pil, draw

    if letter_index == 0:
        x = 920
        y = 130
    elif letter_index == 1:
        x = 1500
        y = 260
    elif letter_index == 2:
        x = 1500
        y = 600
    elif letter_index == 3:
        x = 1200
        y = 790
    elif letter_index == 4:
        x = 700
        y = 790
    elif letter_index == 5:
        x = 370
        y = 600
    elif letter_index == 6:
        x = 370
        y = 260
    elif letter_index == 7:
        x = 700
        y = 500
    elif letter_index == 8:
        x = 950
        y = 500
    elif letter_index == 9:
        x = 1200
        y = 500

    # 빛 들어올 때
    if letter_light is True:
        cv2.circle(keyboard, (x, y), 110, c_btn_b, -1)

        gaze_pil = Image.fromarray(keyboard)
        draw = ImageDraw.Draw(gaze_pil)
        draw.text((x-50, y-30), text, font=imageFont, fill=(51, 51, 51))
    # 원래 버튼
    else:
        cv2.circle(keyboard, (x, y), 110, c_btn_org, -1)

        gaze_pil = Image.fromarray(keyboard)
        draw = ImageDraw.Draw(gaze_pil)
        draw.text((x-50, y-30), text, font=imageFont, fill=(51, 51, 51))

#momain창(깜빡임)
def draw_letter_B_momain(letter_index, text,letter_light):
    global gaze_pil, draw

    if letter_index == 0:
        x = 920
        y = 200
    elif letter_index == 1:
        x = 1300
        y = 400
    elif letter_index == 2:
        x = 1100
        y = 700
    elif letter_index == 3:
        x = 700
        y = 700
    elif letter_index == 4:
        x = 500
        y = 400
    elif letter_index == 5:
        x = 920
        y = 500

    # 빛 들어올 때
    if letter_light is True:
        cv2.circle(keyboard, (x, y), 110, c_btn_b, -1)

        gaze_pil = Image.fromarray(keyboard)
        draw = ImageDraw.Draw(gaze_pil)
        draw.text((x-50, y-30), text, font=imageFont, fill=(51, 51, 51))
    #원래 버튼
    else:
        cv2.circle(keyboard, (x, y), 110, c_btn_org, -1)

        gaze_pil = Image.fromarray(keyboard)
        draw = ImageDraw.Draw(gaze_pil)
        draw.text((x-50, y-30), text, font=imageFont, fill=(51, 51, 51))

#자동완성창(깜빡임)
def draw_letter_B_auto(letter_index, text,letter_light):
    global gaze_pil, draw

    if letter_index == 0:
        x = 920
        y = 200
    elif letter_index == 1:
        x = 1300
        y = 400
    elif letter_index == 2:
        x = 1100
        y = 700
    elif letter_index == 3:
        x = 700
        y = 700
    elif letter_index == 4:
        x = 500
        y = 400
    elif letter_index == 5:
        x = 920
        y = 500

    # 빛 들어올 때
    if letter_light is True:
        cv2.circle(keyboard, (x, y), 110, c_btn_b, -1)

        gaze_pil = Image.fromarray(keyboard)
        draw = ImageDraw.Draw(gaze_pil)
        draw.text((x-50, y-30), text, font=imageFont, fill=(51, 51, 51))

    # 원래버튼
    else:
        cv2.circle(keyboard, (x, y), 110, c_btn_org, -1)

        gaze_pil = Image.fromarray(keyboard)
        draw = ImageDraw.Draw(gaze_pil)
        draw.text((x-50, y-30), text, font=imageFont, fill=(51, 51, 51))

#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

#눈 함수들
def midpoint(p1 ,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

def get_blinking_ratio(eye_points, facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

    hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

    ratio = hor_line_lenght / ver_line_lenght
    return ratio

def get_EyeTopDownLooking(eye_points, facial_landmarks):
    center_top = midpoint(facial_landmarks.part(eye_points[0]), facial_landmarks.part(eye_points[1]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[2]), facial_landmarks.part(eye_points[3]))

    return hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

def eyes_contour_points(facial_landmarks):
    left_eye = []
    right_eye = []
    for n in range(36, 42):
        x = facial_landmarks.part(n).x
        y = facial_landmarks.part(n).y
        left_eye.append([x, y])
    for n in range(42, 48):
        x = facial_landmarks.part(n).x
        y = facial_landmarks.part(n).y
        right_eye.append([x, y])
    left_eye = np.array(left_eye, np.int32)
    right_eye = np.array(right_eye, np.int32)
    return left_eye, right_eye

def get_gaze_ratio(eye_points, facial_landmarks):
    left_eye_region = np.array([(facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y),
                                (facial_landmarks.part(eye_points[1]).x, facial_landmarks.part(eye_points[1]).y),
                                (facial_landmarks.part(eye_points[2]).x, facial_landmarks.part(eye_points[2]).y),
                                (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y),
                                (facial_landmarks.part(eye_points[4]).x, facial_landmarks.part(eye_points[4]).y),
                                (facial_landmarks.part(eye_points[5]).x, facial_landmarks.part(eye_points[5]).y)], np.int32)
    # cv2.polylines(frame, [left_eye_region], True, (0, 0, 255), 2)

    height, width, _ = frame.shape
    mask = np.zeros((height, width), np.uint8)
    cv2.polylines(mask, [left_eye_region], True, 255, 2)
    cv2.fillPoly(mask, [left_eye_region], 255)
    eye = cv2.bitwise_and(gray, gray, mask=mask)

    min_x = np.min(left_eye_region[:, 0])
    max_x = np.max(left_eye_region[:, 0])
    min_y = np.min(left_eye_region[:, 1])
    max_y = np.max(left_eye_region[:, 1])

    gray_eye = eye[min_y: max_y, min_x: max_x]
    _, threshold_eye = cv2.threshold(gray_eye, 70, 255, cv2.THRESH_BINARY)
    height, width = threshold_eye.shape
    left_side_threshold = threshold_eye[0: height, 0: int(width / 2)]
    left_side_white = cv2.countNonZero(left_side_threshold)

    right_side_threshold = threshold_eye[0: height, int(width / 2): width]
    right_side_white = cv2.countNonZero(right_side_threshold)

    if left_side_white == 0:
        gaze_ratio = 1
    elif right_side_white == 0:
        gaze_ratio = 5
    else:
        gaze_ratio = left_side_white / right_side_white
    return gaze_ratio

#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

frames = 0

#글자 인덱스
letter_index = 0
#깜빡임 프레임
blinking_frames = 0
#응시 프레임
gaze_frame = 0

#키보드에 출력할 text
text = ""

#창 전환을 위한 text
ch = ""

# #키보드 선택 변수
keyboard_selected = "jamain"

select_keyboard_jamain = True
select_keyboard_momain = False
select_keyboard_auto = False

select_keyboard_G_JA = False
select_keyboard_G_MO = False
#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
#출력창
app = QApplication(sys.argv)
b = lb()
b.setGeometry(0,0,1920,150)
b.setWindowFlags(Qt.FramelessWindowHint)
b.show()
#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

while True:
    _, frame = cap.read()

    # rows, cols, _ = frame.shape

    frames += 1
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Draw a white space for loading bar
    # frame[rows - 50: rows, 0: cols] = (255, 255, 255)

# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    #키보드 선택
    if keyboard_selected == "jamain":
        keys_set = keys_set_jamain
    elif keyboard_selected == "momain":
        keys_set = keys_set_momain
    elif keyboard_selected == "auto":
        keys_set = keys_set_auto
    elif keyboard_selected == "ja1":
        keys_set = keys_set_ja1
    elif keyboard_selected == "ja2":
        keys_set = keys_set_ja2
    elif keyboard_selected == "ja3":
        keys_set = keys_set_ja3
    elif keyboard_selected == "ja4":
        keys_set = keys_set_ja4
    elif keyboard_selected == "ja5":
        keys_set = keys_set_ja5
    elif keyboard_selected == "ja6":
        keys_set = keys_set_ja6
    elif keyboard_selected == "ja7":
        keys_set = keys_set_ja7
    elif keyboard_selected == "mo1":
        keys_set = keys_set_mo1
    elif keyboard_selected == "mo2":
        keys_set = keys_set_mo2
    elif keyboard_selected == "mo3":
        keys_set = keys_set_mo3
    elif keyboard_selected == "mo4":
        keys_set = keys_set_mo4
    elif keyboard_selected == "mo5":
        keys_set = keys_set_mo5
    active_letter = keys_set[letter_index]

    # 아래에서 그림을 그릴 때 letter_index를 증가시킴(7프레임당 1증가)

# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
# 깜빡이는 창 그리기

    # jamain이 true일 때 그리기 (버튼 불빛)
    if select_keyboard_jamain is True:
        cv2.rectangle(keyboard, (0, 0), (width, height), c_back, -1)

        if frames == 7:
            letter_index += 1
            frames = 0
        if letter_index == 10:
            letter_index = 0

        for i in range(10):
            if i == letter_index:
                light = True
            else:
                light = False

            draw_letter_B_jamain(i, keys_set[i], light)
            keyboard = np.array(gaze_pil)
    # momain이 true일 때 그리기 (버튼 불빛)
    elif select_keyboard_momain is True:

        cv2.rectangle(keyboard, (0, 0), (width, height), c_back, -1)

        if frames == 7:
            letter_index += 1
            frames = 0
        if letter_index == 6:
            letter_index = 0

        for i in range(6):
            if i == letter_index:
                light = True
            else:
                light = False

            draw_letter_B_momain(i, keys_set[i], light)
            keyboard = np.array(gaze_pil)
    # auto가 true일 때 그리기 (버튼 불빛)
    elif select_keyboard_auto is True:
        cv2.rectangle(keyboard, (0, 0), (width, height), c_back, -1)

        if frames == 7:
            letter_index += 1
            frames = 0
        if letter_index == 6:
            letter_index = 0

        for i in range(6):
            if i == letter_index:
                light = True
            else:
                light = False

            draw_letter_B_momain(i, keys_set[i], light)
            keyboard = np.array(gaze_pil)
    # 자음응시창이 true일 때 그리기(불빛 X)
    elif select_keyboard_G_JA is True:
        cv2.rectangle(keyboard,(0,0), (width, height), c_back, -1)

        for i in range(4):
            draw_letter_G(i, keys_set[i])
            keyboard = np.array(gaze_pil)
    # 모음응시창이 true일 때 그리기(불빛 X)
    elif select_keyboard_G_MO is True:
        cv2.rectangle(keyboard,(0,0), (width, height), c_back, -1)

        for i in range(4):
            draw_letter_G(i, keys_set[i])
            keyboard = np.array(gaze_pil)

# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

    # 얼굴이 인식된 동안
    faces = detector(gray)
    for face in faces:
        landmarks = predictor(gray, face)

        left_eye, right_eye = eyes_contour_points(landmarks)

        # Detect blinking
        left_eye_ratio = get_blinking_ratio([36, 37, 38, 39, 40, 41], landmarks)
        right_eye_ratio = get_blinking_ratio([42, 43, 44, 45, 46, 47], landmarks)
        blinking_ratio = (left_eye_ratio + right_eye_ratio) / 2

        gaze_ratio_left_eye = get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks)
        gaze_ratio_right_eye = get_gaze_ratio([42, 43, 44, 45, 46, 47], landmarks)
        gaze_ratio = (gaze_ratio_right_eye + gaze_ratio_left_eye) / 2

        gaze_ratio_top_L_eye = get_EyeTopDownLooking([37, 38, 39, 40], landmarks)
        gaze_ratio_top_R_eye = get_EyeTopDownLooking([43, 44, 45, 46], landmarks)
        gaze_ratio_Top = (gaze_ratio_top_L_eye + gaze_ratio_top_R_eye) / 2

        # Eyes color
        cv2.polylines(frame, [left_eye], True, (0, 255, 0), 2)
        cv2.polylines(frame, [right_eye], True, (0, 255, 0), 2)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        #응시 비율 확인용 나중에 지울거임

        # T,D 응시 비율
        cv2.putText(frame, str(gaze_ratio_Top), (100, 100), font, 2, (255, 0, 0), 3)
        # L,C,R 응시 비율
        cv2.putText(frame, str(gaze_ratio), (100, 300), font, 2, (255, 0, 0), 3)

        # 오른쪽 위
        if gaze_ratio <= 0.9 and gaze_ratio_Top > 16.3:
            cv2.putText(frame, "R T", (300, 400), font, 2, (0, 255, 0), 3)
        # 오른쪽 아래
        elif gaze_ratio <= 0.9 and gaze_ratio_Top <= 16.3:
            cv2.putText(frame, "R B", (300, 400), font, 2, (0, 255, 0), 3)
        # 왼쪽 위
        elif gaze_ratio > 0.9 and gaze_ratio_Top > 16.3:
            cv2.putText(frame, "L T", (300, 400), font, 2, (0, 255, 0), 3)
        # 왼쪽 아래
        elif gaze_ratio > 0.9 and gaze_ratio_Top <= 16.3:
            cv2.putText(frame, "L B", (300, 400), font, 2, (0, 255, 0), 3)

        #~~~~~~~~~~~~~~~~~~~~~~~~~

        #자음 메인화면 (깜빡임으로 클릭)
        if select_keyboard_jamain is True:

            #깜빡일 때
            if blinking_ratio > 5:
                blinking_frames += 1
                frames -= 1
                #일정시간(6)동안 깜빡일 때
                if blinking_frames == 5:
                    ch += active_letter
                    sound.play()

                    if ch == "ㄱ ㄷ\nㄲ ㄸ":
                        select_keyboard_jamain = False
                        frames = 0
                        print("ㄱ ㄷ ㄲ ㄸ 깜빡")
                        select_keyboard_G_JA = True
                        keyboard_selected = "ja1"
                        letter_index = 0
                        ch = ""
                    elif ch == "ㄴ ㄹ\nㅁ ㅇ":
                        select_keyboard_jamain = False
                        frames = 0
                        print("ㄴ ㄹ ㅁ ㅇ 깜빡")
                        select_keyboard_G_JA = True
                        keyboard_selected = "ja2"
                        letter_index = 0
                        ch = ""
                    elif ch == "ㅂ ㅅ\nㅃ ㅆ":
                        select_keyboard_jamain = False
                        frames = 0
                        print("ㅂ ㅅ ㅃ ㅆ 깜빡")
                        select_keyboard_G_JA = True
                        keyboard_selected = "ja3"
                        letter_index = 0
                        ch = ""
                    elif ch == "ㅈ ㅊ\nㅉ ㅋ":
                        select_keyboard_jamain = False
                        frames = 0
                        print("ㅈ ㅊ ㅉ ㅋ 깜빡")
                        select_keyboard_G_JA = True
                        keyboard_selected = "ja4"
                        letter_index = 0
                        ch = ""
                    elif ch == "ㅌ ㅍ\nㅎ ㄺ":
                        select_keyboard_jamain = False
                        frames = 0
                        print("ㅌ ㅍ ㅎ ㄺ 깜빡")
                        select_keyboard_G_JA = True
                        keyboard_selected = "ja5"
                        letter_index = 0
                        ch = ""
                    elif ch == "ㄻ ㄼ\nㄾ ㅀ":
                        select_keyboard_jamain = False
                        frames = 0
                        print("ㄻ ㄼ ㄾ ㅀ 깜빡")
                        select_keyboard_G_JA = True
                        keyboard_selected = "ja6"
                        letter_index = 0
                        ch = ""
                    elif ch == "ㄳ ㅄ\nㄵ ㄶ":
                        select_keyboard_jamain = False
                        frames = 0
                        print("ㄳ ㅄ ㄵ ㄶ 깜빡")
                        select_keyboard_G_JA = True
                        keyboard_selected = "ja7"
                        letter_index = 0
                        ch = ""
                    elif ch == "자동\n완성":
                        select_keyboard_jamain = False
                        frames = 0
                        print("자동완성 깜빡")
                        select_keyboard_auto = True
                        keyboard_selected = "auto"
                        letter_index = 0
                        ch = ""
                    elif ch == "취소":
                        print("취소 깜빡")
                        letter_index = 0
                        ch = ""
                        text = ""
                    elif ch == "TTS":
                        print("TTS 깜빡")
                        text += "."
                        letter_index = 0
                        ch = ""
            # 안깜빡일 때
            else:
                blinking_frames = 0
        # 모음 메인화면 (깜빡임으로 클릭)
        elif select_keyboard_momain is True:
            # 깜빡일 때
            if blinking_ratio > 5:
                blinking_frames += 1
                frames -= 1
                # 일정시간(6)동안 깜빡일 때
                if blinking_frames == 5:
                    frames = 0
                    ch += active_letter
                    sound.play()

                    select_keyboard_momain = False

                    print(ch)

                    if ch == "ㅏ ㅑ\nㅓ ㅕ":
                        print("ㅏ ㅑ ㅓ ㅕ 깜빡")
                        select_keyboard_G_MO = True
                        keyboard_selected = "mo1"
                        ja1 = True
                        letter_index = 0
                        ch = ""
                    elif ch == "ㅗ ㅛ\nㅜ ㅠ":
                        print("ㅗ ㅛ ㅜ ㅠ 깜빡")
                        select_keyboard_G_MO = True
                        keyboard_selected = "mo2"
                        letter_index = 0
                        ch = ""
                    elif ch == "ㅡ ㅣ\nㅐ ㅒ":
                        print("ㅡ ㅣ ㅐ ㅒ 깜빡")
                        select_keyboard_G_MO = True
                        keyboard_selected = "mo3"
                        letter_index = 0
                        ch = ""
                    elif ch == "ㅔ ㅖ\nㅢ ㅙ":
                        print("ㅔ ㅖ ㅢ ㅙ 깜빡")
                        select_keyboard_G_MO = True
                        keyboard_selected = "mo4"
                        letter_index = 0
                        ch = ""
                    elif ch == "ㅚ ㅘ\nㅟ ㅝ":
                        print("ㅚ ㅘ ㅟ ㅝ 깜빡")
                        select_keyboard_G_MO = True
                        keyboard_selected = "mo5"
                        letter_index = 0
                        ch = ""
                    elif ch == "완료":
                        print("완료 깜빡")
                        select_keyboard_jamain = True
                        keyboard_selected = "jamain"
                        letter_index = 0
                        ch = ""
            # 안깜빡일 때
            else:
                blinking_frames = 0
        # 자동완성 메인화면 (깜빡임으로 클릭)
        elif select_keyboard_auto is True:
            # 깜빡일 때
            if blinking_ratio > 5:
                blinking_frames += 1
                frames -= 1

                # 일정시간(6)동안 깜빡일 때
                if blinking_frames == 5:
                    frames = 0
                    ch += active_letter

                    print(ch)
                    sound.play()

                    select_keyboard_auto = False

                    if ch == "물":
                        text += "목말라요 물주세요."
                        ch = ""
                        select_keyboard_jamain = True
                        keyboard_selected = "jamain"
                        letter_index = 0
                    elif ch == "가려워":
                        text += "가려워요 긁어주세요."
                        ch = ""
                        select_keyboard_jamain = True
                        keyboard_selected = "jamain"
                        letter_index = 0
                    elif ch == "네":
                        text += "네 알겠습니다."
                        ch = ""
                        select_keyboard_jamain = True
                        keyboard_selected = "jamain"
                        letter_index = 0
                    elif ch == "아니요":
                        text += "아니요 괜찮습니다."
                        ch = ""
                        select_keyboard_jamain = True
                        keyboard_selected = "jamain"
                        letter_index = 0
                    elif ch == "아파요":
                        text += "아파요 도와주세요."
                        ch = ""
                    elif ch == "이전":
                        ch = ""
                        select_keyboard_jamain = True
                        keyboard_selected = "jamain"
                        letter_index = 0
            #안깜빡일 때
            else:
                blinking_frames = 0
        #자음 응시 창일 때 (4개 영역 중 한 영역 응시로 선택, 선택하면 momain으로)
        elif select_keyboard_G_JA is True:
            #오른쪽 위
            if gaze_ratio <= 0.9 and gaze_ratio_Top > 16.3:
                print("2번 자리 응시중")
                gaze_frame += 1

                #일정시간(15) 응시
                if gaze_frame == 15:
                    frames = 0
                    gaze_frame = 0
                    text += keys_set[1]
                    print(text)
                    sound.play()
                    select_keyboard_G_JA = False
                    keyboard_selected = "momain"
                    select_keyboard_momain = True
                    letter_index = 0

            # 오른쪽 아래
            elif gaze_ratio <= 0.9 and gaze_ratio_Top <= 16.3:
                print("4번 자리 응시중")
                gaze_frame += 1

                # 일정시간(15) 응시
                if gaze_frame == 15:
                    frames = 0
                    gaze_frame = 0
                    text += keys_set[3]
                    print(text)
                    sound.play()
                    select_keyboard_G_JA = False
                    keyboard_selected = "momain"
                    select_keyboard_momain = True
                    letter_index = 0

            # 왼쪽 위
            elif gaze_ratio > 0.9 and gaze_ratio_Top > 16.3:
                print("1번 자리 응시중")
                gaze_frame += 1

                # 일정시간(15) 응시
                if gaze_frame == 15:
                    frames = 0
                    gaze_frame = 0
                    text += keys_set[0]
                    print(text)
                    sound.play()
                    select_keyboard_G_JA = False
                    keyboard_selected = "momain"
                    select_keyboard_momain = True
                    letter_index = 0

            # 왼쪽 아래
            elif gaze_ratio > 0.9 and gaze_ratio_Top <= 16.3:
                print("3번 자리 응시중")
                gaze_frame += 1

                # 일정시간(15) 응시
                if gaze_frame == 15:
                    frames = 0
                    gaze_frame = 0
                    text += keys_set[2]
                    print(text)
                    sound.play()
                    select_keyboard_G_JA = False
                    keyboard_selected = "momain"
                    select_keyboard_momain = True
                    letter_index = 0
        # 모음 응시 창일 때 (4개 영역 중 한 영역 응시로 선택, 선택하면 jamain으로)
        elif select_keyboard_G_MO is True:
            # 오른쪽 위
            if gaze_ratio <= 0.9 and gaze_ratio_Top > 16.3:
                print("2번 자리 응시중")
                gaze_frame += 1

                # 일정시간(15) 응시
                if gaze_frame == 15:
                    frames = 0
                    gaze_frame = 0
                    text += keys_set[1]
                    print(text)
                    sound.play()
                    select_keyboard_G_MO = False
                    keyboard_selected = "jamain"
                    select_keyboard_jamain = True
                    letter_index = 0

            # 오른쪽 아래
            elif gaze_ratio <= 0.9 and gaze_ratio_Top <= 16.3:
                print("4번 자리 응시중")
                gaze_frame += 1

                # 일정시간(15) 응시
                if gaze_frame == 15:
                    frames = 0
                    gaze_frame = 0
                    text += keys_set[3]
                    print(text)
                    sound.play()
                    select_keyboard_G_MO = False
                    keyboard_selected = "jamain"
                    select_keyboard_jamain = True
                    letter_index = 0

            # 왼쪽 위
            elif gaze_ratio > 0.9 and gaze_ratio_Top > 16.3:
                print("1번 자리 응시중")
                gaze_frame += 1

                # 일정시간(15) 응시
                if gaze_frame == 15:
                    frames = 0
                    gaze_frame = 0
                    text += keys_set[0]
                    print(text)
                    sound.play()
                    select_keyboard_G_MO = False
                    keyboard_selected = "jamain"
                    select_keyboard_jamain = True
                    letter_index = 0

            # 왼쪽 아래
            elif gaze_ratio > 0.9 and gaze_ratio_Top <= 16.3:
                print("3번 자리 응시중")
                gaze_frame += 1

                # 일정시간(15) 응시
                if gaze_frame == 15:
                    frames = 0
                    gaze_frame = 0
                    text += keys_set[2]
                    print(text)
                    sound.play()
                    select_keyboard_G_MO = False
                    keyboard_selected = "jamain"
                    select_keyboard_jamain = True
                    letter_index = 0


    cv2.imshow("Frame", frame)

    cv2.imshow("Virtual keyboard", keyboard)

    #출력창에 한글 출력(자모결합)
    eye_list = list()
    eye_list.append(text)
    result = join_jamos(''.join(eye_list))
    b.lineEE.setText(result)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
app.exec_()