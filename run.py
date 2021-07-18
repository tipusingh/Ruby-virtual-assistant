from PyQt5 import QtWidgets, QtGui,QtCore
from PyQt5.QtGui import QMovie
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import pyttsx3
import speech_recognition as sr
import os
import time
import webbrowser
import datetime
from pyowm import OWM
from rake_nltk import Rake
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import random


flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)
engine.setProperty('rate',180)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wish():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour <12:
        speak("Good morning Tipu")
    elif hour>=12 and hour<18:
        speak("Good Afternoon Tipu")
    else:
        speak("Good night Tipu")

class mainT(QThread):
    def __init__(self):
        super(mainT,self).__init__()
    
    def run(self):
        self.JARVIS()
    
    def STT(self):
        R = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listning...........")
            audio = R.listen(source)
        try:
            print("Recog......")
            text = R.recognize_google(audio,language='en-in')
            print(">> ",text)
        except Exception:
            speak("Sorry Speak Again")
            return "None"
        text = text.lower()
        return text

    def JARVIS(self):
        wish()
        while True:
            self.query = self.STT()
            if 'good bye' in self.query:
                sys.exit()
            elif 'open google' in self.query:
                speak("opening google")
                webbrowser.open('www.google.co.in')
            elif 'open youtube' in self.query:
                webbrowser.open("www.youtube.com")
            elif 'play music' in self.query:
                music_dir = "D:\music"
                songs = os.listdir(music_dir)
                random = os.startfile(os.path.join(music_dir, songs[1]))

            elif "mak how are you" in self.query:
                speak("i am good")
            elif "macc how are you" in self.query:
                speak("i am good")
            elif "mack are you" in self.query:
                speak("i am good")
            elif "macc are you" in self.query:
                speak("i am good")
            elif "mac are you" in self.query:
                speak("i am good")        
            elif "how are you" in self.query:
                speak("i am good")            
                
            elif 'search'  in self.query:
                speak("Searching web for you")
                self.query = self.query.replace("search", "")
                webbrowser.open_new_tab(self.query)
                time.sleep(5)

            elif 'what is today task'  in self.query or "what i have to do today" in self.query:
                speak("first you have to complete you blockchain project")
                speak("and watch agents of shield in the night")

                

            elif 'play music' in self.query or "play song" in self.query:
                speak("Here you go with music")
                # music_dir = "G:\\Song"
                music_dir = "D:\music"
                songs = os.listdir(music_dir)
                print(songs)
                random = os.startfile(os.path.join(music_dir, songs[1]))
        
                
                    


            elif "suggest me a movie" in self.query or "recommend me a movie" in self.query or "recommend movie" in self.query:
    
            
                Eng= pd.read_csv('IMDB_Top250Engmovies2_OMDB_Detailed(1).csv')
                Hindi = pd.read_csv('IMDB_Top250Indianmovies2_OMDB_Detailed.csv')
                frames=[Eng,Hindi]
                df=pd.concat(frames)
                df = df[['Title','Genre','Director','Writer','Actors','Plot']]


                df['Key_words'] = ""
                r = Rake()
                for index, row in df.iterrows():
                    r.extract_keywords_from_text(row['Plot'])
                    key_words_dict_scores = r.get_word_degrees()
                    row['Key_words'] = list(key_words_dict_scores.keys())


                df['Genre'] = df['Genre'].map(lambda x: x.split(','))
                df['Actors'] = df['Actors'].map(lambda x: x.split(',')[:3])
                df['Director'] = df['Director'].map(lambda x: x.split(','))
                for index, row in df.iterrows():
                    row['Genre'] = [x.lower().replace(' ','') for x in row['Genre']]
                    row['Actors'] = [x.lower().replace(' ','') for x in row['Actors']]
                    row['Director'] = [x.lower().replace(' ','') for x in row['Director']]



                df['Bag_of_words'] = ''
                columns = ['Genre', 'Director', 'Actors', 'Key_words']
                for index, row in df.iterrows():
                    words = ''
                    for col in columns:
                        words += ' '.join(row[col]) + ' '
                    row['Bag_of_words'] = words

                df = df[['Title','Bag_of_words']]



                count = CountVectorizer()
                count_matrix = count.fit_transform(df['Bag_of_words'])
                cosine_sim = cosine_similarity(count_matrix, count_matrix)


                indices = pd.Series(df['Title'])
                def recommend(title, cosine_sim = cosine_sim):
                    recommended_movies = []
                    idx = indices[indices == title].index[0]
                    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)
                    top_10_indices = list(score_series.iloc[1:11].index)
    
                    for i in top_10_indices:
                        recommended_movies.append(list(df['Title'])[i])
                        k=random.choice(recommended_movies)
        
                    return recommended_movies
                
                speak("Which movie do you watch last?")
                self.query=self.STT()
                self.query=self.query.title() 
                j=[]
                for i in recommend(self.query):
                    j.append(i)
                movie=random.choice(j)
            
                
                speak("Recommended movie is")
            
                
                speak(movie)    
    

FROM_MAIN,_ = loadUiType(os.path.join(os.path.dirname(__file__),"./scifi.ui"))

class Main(QMainWindow,FROM_MAIN):
    def __init__(self,parent=None):
        super(Main,self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(1920,1080)
        self.label_7 = QLabel
        self.exitB.setStyleSheet("background-image:url(./lib/exit - Copy.png);\n"
        "border:none;")
        self.exitB.clicked.connect(self.close)
        self.setWindowFlags(flags)
        Dspeak = mainT()
        self.label_7 = QMovie("./lib/gifloader.gif", QByteArray(), self)
        self.label_7.setCacheMode(QMovie.CacheAll)
        self.label_4.setMovie(self.label_7)
        self.label_7.start()

        self.ts = time.strftime("%A, %d %B")

        Dspeak.start()
        self.label.setPixmap(QPixmap("./lib/tuse.png"))
        self.label_5.setText("<font size=8 color=#00d7f9>"+self.ts+"</font>")
        self.label_5.setFont(QFont(QFont('Acens',8)))
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setXOffset(-1)
        self.shadow.setYOffset(-1)
        self.shadow.setBlurRadius(20)
        self.shadow.setColor(QColor(0, 191, 255))

        self.label_5.setGraphicsEffect(self.shadow)

    



app = QtWidgets.QApplication(sys.argv)
main = Main()
main.show()
exit(app.exec_())