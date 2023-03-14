# TTS (Google Text To Speech)
# pip install gTTS
# pip install playsound
from gtts import gTTS
from playsound import playsound

text = '안녕하세요, 이수진입니다.'

tts = gTTS(text=text, lang='ko', slow=False)
tts.save('./StudyPython/output/hi.mp3')
print('생성 완료!')

playsound('./StudyPython/output/hi.mp3')
print('음성출력 완료!')