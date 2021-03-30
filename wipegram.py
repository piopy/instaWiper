import instagrapi, time, random, os, wget,json
from instagrapi import Client
from datetime import datetime

user_name=''
password=''
path_file = 'cookie_thumper'
api=None

with open("config.json") as f:
    data = json.loads(f.read())
    user_name = data["user_name"]
    password = data["password"]

print("Login con",user_name)
### LOGIN ###

def savecookie(data):
    with open(path_file, 'w', encoding='utf8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=True)#, default=default)

def readcookie(data):
    with open(data, 'r', encoding='utf8') as json_file:
        return json.load(json_file)#, object_hook=object_hook)

if os.path.exists(path_file):
    api = Client(readcookie(path_file))
else:
    api = Client()
    api.uuid="99f90278-174d-420c-9b07-47677e09ab20"
    api.phone_id="51224ec5-943d-4ea8-b71d-bd3249c0d588"
    api.device_id="android-ef688bb0d352317c"
    api.user_agent="Instagram 135.0.0.1.1 Android (28/9.0; 420dpi; 1080x1920; OnePlus; ONEPLUS A3003; OnePlus3; qcom; en_US; 180322800)"
    api.client_session_id="dfc8810b-633d-4048-b396-e170f2037832"
    api.login(user_name, password,relogin=True)
    savecookie(api.get_settings())

### CORE ###
def cancella_p():
    while len(api.user_medias_v1(api.user_id_from_username(user_name),amount=50))!=0:
        medias=api.user_medias_v1(api.user_id_from_username(user_name),amount=50)
        if len(medias) >0:
            for m in medias:
                api.media_delete(m.id)
                time.sleep(random.randint(1,60)/10)
    print("All posts are deleted!")
def cancella_s():
    while len(api.user_stories_v1(api.user_id_from_username(user_name)))!=0:
        medias=api.user_stories_v1(api.user_id_from_username(user_name))
        if len(medias)>0:
            for m in medias:
                api.story_delete(m.id)
                time.sleep(random.randint(1,60)/10)
    print("All stories are deleted!")

def upload_storia(url='https://i.pinimg.com/originals/79/1f/ca/791fca6132c5c51e1bac62a78dfac848.jpg',frase=''):
    path='./'
    foto=path+'cat.jpg'
    wget.download(url,foto)
    api.photo_upload_to_story(foto,'')

if __name__ == '__main__':
    time.sleep(5)
    print("Are you sure deleting ALL your photos? It cannot be undone!")
    choice=input("(y/n): ")
    if choice.lower()=='y': 
        try:
            cancella_p()
            time.sleep(5)
            cancella_s()
            time.sleep(5)
        except Exception as e:
            if str(e)=="'NoneType' object is not subscriptable" : print("All stories are deleted!")
            else: 
                print(e)
                exit(0)
        wget.download('https://i.pinimg.com/736x/69/7a/aa/697aaa89a67342ff6e115bb7f312d988.jpg','./snap.jpg')
        api.account_change_picture('snap.jpg')
    else: exit(0)
