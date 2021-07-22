import requests
import simpleaudio as sa
import wave

from scipy.io import wavfile
import scipy.io
import numpy as np

text = '김소연 tts입니다. 오늘은 2021년 6월 15일 10시 50분 입니다.'
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