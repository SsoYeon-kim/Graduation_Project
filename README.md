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
2-4.  구성   

#### [개인화 TTS]   
2-5. 구성도   
2-6. Glow-TTS   
2-7. Multi-band MelGAN   
2-8. 음성 결과   

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

##  키보드 구성   
   
다음은 기존 윈도우 키보드의 사진이다.   
<img src="https://user-images.githubusercontent.com/62587484/142987745-5d6dc06a-5ad8-4097-bb1a-43264b2880db.png" width="45%">   
   
눈으로 기존 윈도우 키보드를 사용하여 글자를 입력할 경우 자음과 모음의 거리가 멀어 눈의 이동범위가 넓어지고 이에 따라 눈에 피로도가 증가하게 된다. 따라서 다음과 같은 키보드를 구성하였다. 화면 구성은 다음 사진과 같다.   
   
<img src="https://user-images.githubusercontent.com/62587484/142987507-15a05d5f-7cc7-474f-8178-2ff5305f41ed.png" width="45%">   
   
위 사진은 자음 메인 페이지(깜빡임)와 자음 선택 페이지(응시)화면이다. 자음 메인 페이지에서 불빛이 순서대로 깜빡이는 버튼에서 눈을 약 1초 정도 깜빡일 시 선택이 된다. 이후 4개의 자음 중 선택하는 페이지로 넘어가게 되고 해당 페이지에서는 약 1초 정도 선택할 자음을 응시하면 된다. 이와 같은 방식으로 모음 메인 페이지와 모음 선택 페이지로 구성된다. 페이지의 순서는 한글의 특성에 맞춰 자음-모음-자음 순으로 초성, 중성, 종성을 선택할 수 있게 한다.    
   
<img src="https://user-images.githubusercontent.com/62587484/142987579-87a82149-0c03-477b-b978-9740e083a6fb.png" width="50%">    
   
위 사진은 자동완성 페이지로 환자가 글자를 입력하는 시간을 단축해준다. 일상생활에서 자주 사용하는 네, 아니요, 아파요 등 한 번의 클릭으로 간편하게 입력할 수 있다. 자동완성 페이지와 자동완성 단어를 선택하는 페이지로 구성된다.   
따라서 직관적이고 누구나 쉽게 사용 가능하며 한국어에 맞추어 편리성을 확보한 키보드를 구성하였다.   

## 구성도   
   
TTS는 미리 녹음된 육성을 이용하는 음성 서비스와 달리 문자를 바로 음성으로 변환시켜주는 음성 합성 기술을 뜻한다. 사전에 미리 정해진 문장을 녹음하여 재생하는 것이 아닌 환자가 하고 싶은 말을 환자의 목소리로 만들어내는 것이다. 음성합성을 위해 end to end시스템을 사용하는데 이는 입력부터 출력까지 하나의 모듈로 이루어진 시스템으로 텍스트와 음성과 같이 쌍에 해당하는 데이터를 가지고 텍스트 문자열은 입력으로 음성 신호를 출력으로 하는 심층 신경망 모델에 대한 학습을 자동으로 해내게 된다.   
본 시스템은 환자가 목소리를 잃기 전 환자의 목소리를 녹음 하는 것을 전제로 한다. 이 외에 경우 환자의 구강구조 특성과 동성 가족 목소리를 활용하여 목소리를 만들 수 있다.    

다음은 개인화 TTS 구성도이다.  
   
<img src="https://user-images.githubusercontent.com/62587484/142988684-ee5b8778-5e45-4671-b444-19e7210d8d43.png" width="50%">  
   
Text2Mel 모델로 Glow-TTS, Vocoder 모델로 Multi-band MelGAN을 사용한다. 입력한 텍스는 Glow-TTS를 거쳐 Mel-Spectrogram으로 만들어지고 이는 Multi-band melGAN을 거쳐 음성으로 만들어지게 된다. 

## Glow-TTS   
   
Glow-TTS는 기존에 많이 사용하던 타코트론2보다 15.7배 빠르게 mel-spectrogram을 만들 수 있다. 이는 흐름 및 동적 프로그래밍의 속성을 활용하여 텍스트와 음성을 정렬하는 방법을 내부적으로 학습하는 독립형 병렬 TTS모델이다. 
   
[Glow-TTS](https://proceedings.neurips.cc/paper/2020/file/5c3b99e8f92532e5ad1556e53ceea00c-Paper.pdf)
   
## Multi-band MelGAN   
   
Multi-band melGAN은 melGAN을 개선한 것으로 다중대역을 사용한다. 수용 영역을 확장하여 음성 생성에 도움이 되며 더 빠른 파형 생성과 고품질로 음성을 생성하게 된다.
   
[Multi-band melGAN](https://arxiv.org/pdf/2005.05106.pdf)
   
다음의 코드로 TTS를 test해볼 수 있다.
   
<pre><code>
text = '○○○ tts입니다. 오늘은 20○○년 ○월 ○일 ○시 ○분 입니다.'
URL = f'http://localhost:5000/tts-server/api/infer-glowtts?text={requests.utils.quote(text)}'
response = requests.get(URL)
with open('input.wav', 'wb') as fd:
  for chunk in response.iter_content(chunk_size=128):
    fd.write(chunk)

samplerate, data = wavfile.read('input.wav')
data = data*32767
wavfile.write('convert.wav', samplerate, data.astype(np.int16))

wave_obj = sa.WaveObject.from_wave_file('convert.wav')
play_obj = wave_obj.play()
play_obj.wait_done()
</code></pre>

## 음성 결과   
   
음성 데이터는 두 명이 직접 녹음에 참여하였고(Mimic Recording Studio) 약 3000개 이상의 문장으로 3시간 가량의 음성 데이터를 사용한다. 원본 음성 파형과 생성된 음성 파형을 비교했을 때 다음과 같은 결과를 보여준다.   
   
<img src="https://user-images.githubusercontent.com/62587484/142990475-6a595167-e224-4544-b951-8fe2d628d10f.png" width="50%">   
<img src="https://user-images.githubusercontent.com/62587484/142990514-7a9fc8a2-5ceb-4dd9-8057-3fd994403db6.png" width="50%"><img src="https://user-images.githubusercontent.com/62587484/142990552-e868027f-80be-4e23-ade5-95e4c46a317b.png" width="50%">  
   <img src="https://user-images.githubusercontent.com/62587484/142990514-7a9fc8a2-5ceb-4dd9-8057-3fd994403db6.png" width="50%"><img src="https://user-images.githubusercontent.com/62587484/142990552-e868027f-80be-4e23-ade5-95e4c46a317b.png" width="50%">  
   
이 외에도 녹음에 참여한 A(표준어 사용), B(사투리 사용)의 억양을 살려 음성 학습이 가능하였고, 물음표와 점의 구분 또한 가능하였다. 
   
# 3. 동작 영상   
   
다음은 "감사합니다" 입력, 자동완성 페이지 시연영상이다.   
   
<img src="https://user-images.githubusercontent.com/62587484/143851062-dd4a48a4-9741-47c3-a75b-90a32e246757.gif" width="50%"><img src="https://user-images.githubusercontent.com/62587484/143851069-df6d8699-d4e3-4b33-b1be-32526c5711a2.gif" width="50%">  
