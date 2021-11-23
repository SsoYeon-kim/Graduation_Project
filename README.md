개인화 TTS를 이용한 루게릭 환자 지원 의사 소통 시스템

# 목차

## 1. 시스템 소개
1-1. 주제 선정이유   

## 2. 기능 구현
#### [아이트래킹]   
2-1. 눈 영역 검출   
2-2. 시선추적, 모션인식   
  
#### [한글 자판]   
2-3. 자모 결합   
2-4. 화면 구성   

#### [개인화 TTS]   
2-5. Glow-TTS   
2-6. Multi-band MelGAN   
2-7. 음성 결과   

## 3. 동작 영상   

<hr>

# 1. 시스템 소개
 
## 주제 선정 이유   
   
* 근위축성 측색경화증(ASL)은 퇴행성 신경 질환으로, 원인이 정확히 밝혀지지 않은 희귀질환인다. 대뇌 및 척수의 운동신경원이 선택적으로 파괴되기에 '운동신경원 질환'이라고 하며, '루게릭병'이라고도 불린다. 루게릭병의 초기증상은 식별하기 어려울 정도로 매우 미미하여 초기진단이 어렵다. 그리고 점진적으로 팔과 다리에 경련이 발생하고 힘이 빠져 자주 넘어지는 현상이 발생된다. 뿐만 아니라, 목소리를 낼 때 사용되는 근육에도 마비가 오기에 목소리가 잘 나오지 않아 의사소통이 이뤄지지 않는 현상까지 발생하게 된다.   
   
<img src="https://user-images.githubusercontent.com/62587484/139672279-8d8f7751-622c-4105-8e98-cdfb5fb5446d.png" width="45%">     

* 위에 표에서 알 수 있듯이 루게릭병 환자 발생 현황은 2013과 비교하여 2016년에는 400명 이상 증가하였으며 매년 증가하고 있는 추세다.    

<img src="https://user-images.githubusercontent.com/62587484/139671587-7c75bae7-58f1-4f31-93b6-41641fd3e5f4.png" width="55%">   

* 위 그림은 루게릭병에 대한 임상 점수이다. 사지의 근력 약화와 근 위축, 사지 마비, 언어 장애, 호흡 기능의 저하 등 일반적으로 병의 진행이 빠르다고 알려져 있다. 근위축성 측색경화증(루게릭병)의 증상이 나타난 후 평균적으로, 약 50%가 3-5년 이내에 사망에 이르게 되며 10년 안의 사망률이 90%가량이다. 약 10%의 경우, 10년 이상 장기 투병하는 사례도 있다. 특히, 의사소통의 문제로 인해서 환자들과 보호자 사이의 육체적·정신적인 어려움이 존재한다. 그렇기에 이 시스템은 의사소통의 필요성을 충족시키기 위한 아이디어로 시작되었다.      

기존에 루게릭병 환자를 위한 보조기구로 눈의 선을 추적하는 안구 마우스, 훈련용 소프트웨워, 게이밍용 안구 마우스가 있다. 기존 안구 마우스는 게이밍용 안구 마우스를 포함하여 수십-수천만원대의 가격으로 수십만 원인 훈련용 소프트웨어까지 합친다면 매우 비싼 가격이다. 때문에 환자용 안구 마우스가 아닌 게이밍용 안구 마우스를 쓰는 사람들도 있다.    
   
앞선 보조기구들은 오직 마우스의 기능만 존재하며 키보드 또한 기존 윈도우 키보드를 사용한다. 이러한 단점들을 개선하여 웹캠을 이용해 비용을 절감하고 한글 특성에 맞는 직관적 키보드를 구성하였으며 마우스의 기능에 더불어 잃어버린 환자의 목소리를 개인화 TTS를 사용하여 복원하는 기능을 추가하였다. 결과적으로 환자는 눈을 이용하여 원하는 텍스트를 입력하고 복원한 환자의 목소리로 텍스트를 재생하여 실제로 대화하는 듯한 시스템을 개발하였다.

# 2. 기능 구현   

* 아이트래킹은 다음과 같은 순서로 진행된다.   
openCV -> 눈 영역 검출 -> 시선추적 -> 모션 인식 -> 문자 추출 -> 사용자   
   
## 눈 영역 검출   

환자의 시선을 추적하기 위해 openCV를 사용하였다. 웹캠을 통해 얼굴을 인식한 후 눈 영역을 검출하게 된다. 이후 시선 추적을 통해 환자가 키보드의 어느 글자를 응시하거나 깜빡이는지를 판별하여 문자를 추출하게 된다. 눈 영역 검출은 DLIB68 안면 랜드마크 예측 알고리즘을 사용하여 68개의 점을 얼굴에 나타내고 눈에 해당되는 인덱스를 가져와 검출한다.    
<img src="https://user-images.githubusercontent.com/62587484/139681170-6d68cae6-7e56-4238-9bf5-38ff9980e6b8.png" width="35%">       

<pre><code>
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
</code></pre>
   
## 시선추적, 모션인식   
   
검출 이후 임계값 지정, 외곽 검출 등을 거쳐 흰자와 검은자를 구별한다. 좌, 우 응시를 판별하기 위해 흰자의 비율을 사용한다.
<pre><code>
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
</code></pre>
상, 하 시선을 구분하기 위해서는 위를 볼 때 눈커풀이 열리고 아래를 볼 때 눈꺼풀이 닫히는 특징을 이용한다. 눈 위치의 점 인덱스 중 눈 위 중앙과 아래 중앙의 거리를 계산하여 일정 비율 이상일 시 위를 응시, 이하일 시 아래를 응시하는 것으로 판별한다.
<pre><code>
def get_EyeTopDownLooking(eye_points, facial_landmarks):
    center_top = midpoint(facial_landmarks.part(eye_points[0]), facial_landmarks.part(eye_points[1]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[2]), facial_landmarks.part(eye_points[3]))

    return hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))
</code></pre>
깜빡임은 눈의 수직, 수평 비율로 판별한다. 상하를 판별할 때 사용한 수직길이와 눈의 수평길이를 계산하여 두 길이의 비율을 사용한다.
<pre><code>
def get_blinking_ratio(eye_points, facial_landmarks):
    left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
    right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
    center_top = midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
    center_bottom = midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

    hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
    ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

    ratio = hor_line_lenght / ver_line_lenght
    return ratio
</code></pre>
##  자모 결합   
      
영어의 경우 자음과 모음의 구분이 없어 글자를 결합하지 않는다. 하지만 한글의 경우 초성, 중성, 종성으로 이루어져 눈으로 글자를 입력할 시 모든 글자가 각각 입력되는 문제가 생긴다. 따라서 자음자와 모음자를 합쳐 음절 단위로 모아쓰게 하였으며 한글의 특성에 맞춰 키보드를 제작하였다.   
다음은 자모 결합을 할 때 진행 순서이다.   
첫 번째 글자는 자음을 선택하고 중성에는 무조건 모음이 들어가며 종성에서는 받침의 유무로 판단해 받침이 있다면 자음을 선택하고 모아쓰기를 하고 받침이 없다면 다음 단어의 초성을 선택한다. 그 후 각각 선택한 단어들을 리스트를 생성해 append시켜주고 리스트의 음소들을 하나의 문자열로 만들어준다.

<pre><code>
    #출력창에 한글 출력(자모결합)
    eye_list = list()
    eye_list.append(text)
    result = join_jamos(''.join(eye_list))
    b.lineEE.setText(result)
</code></pre>
   
..이 외 관련 코드는 unicode.py파일과 시선추적 코드를 참고..

## 화면 구성   
화면 구성은 다음 사진과 같다.   
<img src="https://user-images.githubusercontent.com/62587484/142987507-15a05d5f-7cc7-474f-8178-2ff5305f41ed.png" width="45%"><img src="https://user-images.githubusercontent.com/62587484/142987579-87a82149-0c03-477b-b978-9740e083a6fb.png" width="50%">    

## Glow-TTS   

## Multi-band MelGAN   

## 음성 결과   

# 3. 동작 영상   


