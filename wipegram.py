import instagrapi, time, random, os, wget,json
from instagrapi import Client
from instagrapi.types import Media, DirectThread,DirectMessage,UserShort
from datetime import datetime

user_name=''
password=''
path_file = 'cookie_thumper'
api=None

with open("config.json") as f:
    data = json.loads(f.read())
    user_name = data["user_name"]
    password = data["password"]

### LOGIN ###

def savecookie(data):
    with open(path_file, 'w', encoding='utf8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=True)#, default=default)

def readcookie(data):
    with open(data, 'r', encoding='utf8') as json_file:
        return json.load(json_file)#, object_hook=object_hook)

def login():
    global api
    print("Login con",user_name)
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
        time.sleep(3)
        medias=api.user_medias_v1(api.user_id_from_username(user_name),amount=50)
        if len(medias) >0:
            for m in medias:
                api.media_delete(m.id)
                time.sleep(random.randint(1,60)/10)
    print("All posts are deleted!")

def archivia_p():
    while len(api.user_medias_v1(api.user_id_from_username(user_name),amount=50))!=0:
        time.sleep(3)
        medias=api.user_medias_v1(api.user_id_from_username(user_name),amount=50)
        if len(medias) >0:
            for m in medias:
                api.media_archive(m.id)
                time.sleep(random.randint(1,60)/10)
    print("All posts are archived!")

def cancella_s():
    while len(api.user_stories_v1(api.user_id_from_username(user_name)))!=0:
        medias=api.user_stories_v1(api.user_id_from_username(user_name))
        if len(medias)>0:
            for m in medias:
                api.story_delete(m.id)
                time.sleep(random.randint(1,60)/10)
    print("All stories are deleted!")

def direct_eraser():
    time.sleep(2)
    while len(api.direct_threads(50))!=0:
        time.sleep(3)
        threads=api.direct_threads(50)
        if len(threads)>0:
            for t in threads:
                api.direct_thread_hide(t.id)
                time.sleep(random.randint(1,60)/10)
    print("All threads are deleted!")
    return

# def deep_direct_eraser(thread_id): #TODO
#     global user_name
#     id=thread_id
#     thread=api.direct_thread(id)
#     messages=thread.messages
#     for m in messages:
#         if m.user_id==api.user_id_from_username(user_name):
#             print("ancora non esiste questa funzione")
#     return

def blip():
    wget.download('https://i.pinimg.com/736x/69/7a/aa/697aaa89a67342ff6e115bb7f312d988.jpg','./snap.jpg')
    api.account_change_picture('snap.jpg')

def thanos():
    time.sleep(5)
    print("Select 'd' to DELETE all posts, 'a' to archive them. \nWARNING: Deleting cannot be undone")
    choice=input("(d/a): ")
    if choice.lower()=='d': 
        try:
            cancella_p()
            time.sleep(5)
            cancella_s()
            time.sleep(3)
        except Exception as e:
            if str(e)=="'NoneType' object is not subscriptable" : print("All stories are deleted!")
            else: 
                print(e)
                exit(0)
        blip()
    elif choice.lower()=='a': 
        try:
            archivia_p()
            time.sleep(5)
            cancella_s()
            time.sleep(3)
        except Exception as e:
            if str(e)=="'NoneType' object is not subscriptable" : print("All stories are deleted!")
            else: 
                print(e)
                exit(0)
        blip()
    else: exit(0)

def unfollow_all():
    following=api.user_following(api.user_id_from_username(user_name))
    for i in following: 
        api.user_unfollow(i) 
        time.sleep(random.randint(1,60)/10)
        print("Removed ",api.username_from_user_id(f))

def unfollow_infami():
    followers=api.user_followers(api.user_id_from_username(user_name))
    following=api.user_following(api.user_id_from_username(user_name))
    for f in following: 
        print("Scanning",api.username_from_user_id(f))
        if f not in followers: 
            api.user_unfollow(f)
            print("Removed ",api.username_from_user_id(f))
        time.sleep(random.randint(1,60)/10)
        

def menu():
    print("Selezionare l' opzione desiderata")
    print("1. Cancella/archivia storie e posts")
    print("2. Rimuovi chi non ti segue (inclusa chiara ferragni)")
    print("3. Rimuovi tutti i following")
    print("4. Cancella tutti i direct")
    
    return input("Inserisci numero: ")

if __name__ == '__main__':
    login()
    choice=menu()
    if choice=='1': thanos()
    elif choice=='2': unfollow_infami()
    elif choice=='3': unfollow_all()
    elif choice=='4': direct_eraser()
    else: exit(0)