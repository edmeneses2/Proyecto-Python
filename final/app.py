from flask import Flask, render_template, request
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob

from datetime import datetime
import matplotlib.pyplot as plt 



app = Flask(__name__)

@app.route('/')
def main():
    return render_template("app.html")


@app.route("/PREDECIR SENTIMIENTOS", methods=['POST'])
def predecir():
    
    palabra= request.form['palabra']

    consumer_key = 'BYsJJWz9Phgnwl1uoXkpOUds2'
    consumer_secret = 'Ij2USkdlaujZ5MZyslsDatQJuoogEJNrJeFoQWzAzHiMMXUsWK'
    access_token = '358533318-zqqhEgLMRieZKwbsd7YV86mCoj7VVQ42GhxBRYYx'
    access_token_secret = 'diO2GrprFbXOEDjaluQTuB5hKvGe8eb4mbYRaTYNe01HD'

    #Se autentica en twitter
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)
    
  
    #Se define las listas que capturan la popularidad

    numero_de_Tweets = 100
    lenguaje = 'es'


    popularidad_list = []
    numeros_list = []
    numero = 1
    for tweet in tweepy.Cursor(api.search, palabra, lang=lenguaje).items(numero_de_Tweets):
        analisis = TextBlob(tweet.text)
        analisis = analisis.sentiment
        popularidad = analisis.polarity
        popularidad_list.append(popularidad)
        numeros_list.append(numero)
        numero = numero + 1

        axes = plt.gca()
    axes.set_ylim([-1, 2])
    
    plt.scatter(numeros_list, popularidad_list)
    Promedio = (sum(popularidad_list))/(len(popularidad_list))
    Promedio = "{0:.0f}%".format(Promedio * 100)
    time  = datetime.now().strftime("Hora actual : %H:%M\n fecha: %m-%d-%y")
    plt.text(0, 1.25, 
             "Promedio de sentimientos en Twitter:  " + str(Promedio) + "\n" + time, 
             fontsize=12, 
             bbox = dict(facecolor='none', 
                         edgecolor='black', 
                         boxstyle='square, pad = 1'))
    
    plt.title("Análisis de sentimientos sobre " + palabra + " en twitter")
    plt.xlabel("Número de tweets")
    plt.ylabel("Sentimiento")
    plt.show()
    
    return render_template('app.html', Promedio=Promedio)


