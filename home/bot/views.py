from django.shortcuts import render
import json,datetime
import numpy as np
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
import wikipedia
from django.http import JsonResponse
import colorama
from django.views.decorators.csrf import csrf_exempt
colorama.init()


import random
import pickle
# Create your views here.
def index(request):
    return render(request,'index.html')

@csrf_exempt
def get(request):
    try:
        from bs4 import BeautifulSoup
        url = 'https://www.narveersingh.com/contact-me/'
        from urllib.request import Request, urlopen

        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

        web_byte = urlopen(req).read()

        webpage = web_byte.decode('utf-8')
        # print(webpage)
        soup = BeautifulSoup(webpage, "html.parser")
        div = soup.find_all("p", {"class": "elementor-image-box-description"})
        phone = div[0].text
        city = div[1].text
        email = div[2].text

    except:
        pass
    with open(r"C:\Users\ag612\PycharmProjects\AIChatbot\intent.json") as file:
        data = json.load(file)

    model = keras.models.load_model(r'C:\Users\ag612\PycharmProjects\AIChatbot\home\bot\chat_model')

    # load tokenizer object
    with open(r'C:\Users\ag612\PycharmProjects\AIChatbot\home\bot\tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    # load label encoder object
    with open(r'C:\Users\ag612\PycharmProjects\AIChatbot\home\bot\label_encoder.pickle', 'rb') as enc:
        lbl_encoder = pickle.load(enc)

    if request.method == 'POST':
        inp=request.POST['msg']

        max_len = 20

        result = model.predict(keras.preprocessing.sequence.pad_sequences(tokenizer.texts_to_sequences([inp]),
                                                                              truncating='post', maxlen=max_len))
        tag = lbl_encoder.inverse_transform([np.argmax(result)])

        for i in data['intents']:
            if i['tag'] == tag:
                ch= np.random.choice(i['responses'])
                if ch == "appoint":
                    out=f" Narveer Singh will help you to boost your business:), Contact No:{phone}, email id: {email}"
                elif ch == "time":
                    out = datetime.datetime.now()
                elif ch == "contact":
                    out = phone
                elif ch == "email":
                    out = email
                elif ch == "search":
                    out = wikipedia.summary(inp, sentences=2)
                else:
                    out = np.random.choice(i['responses'])

                return JsonResponse({'status':'save','dataset':out})
    else:
        return JsonResponse({'status': 0})