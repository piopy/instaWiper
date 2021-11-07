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
def randomsleep():
    '''Sleeps from 0.1 to 6 seconds, is commented but you can uncomment it to enable it. Current API sleeps themself so there's no longer need of this'''
    time.sleep(0)   # time.sleep(random.randint(1,60)/10)
    return

def cancella_p():
    while len(api.user_medias_v1(api.user_id_from_username(user_name),amount=50))!=0:
        time.sleep(3)
        medias=api.user_medias_v1(api.user_id_from_username(user_name),amount=50)
        if len(medias) >0:
            for m in medias:
                api.media_delete(m.id) #may fail with albums/videos, need more testing
                randomsleep()   
    print("All posts are deleted!")

def archivia_p():
    while len(api.user_medias_v1(api.user_id_from_username(user_name),amount=50))!=0:
        time.sleep(3)
        medias=api.user_medias_v1(api.user_id_from_username(user_name),amount=50)
        if len(medias) >0:
            for m in medias:
                api.media_archive(m.id)
                randomsleep()   #time.sleep(random.randint(1,60)/10)
    print("All posts are archived!")

def cancella_s():
    while len(api.user_stories_v1(api.user_id_from_username(user_name)))!=0:
        medias=api.user_stories_v1(api.user_id_from_username(user_name))
        if len(medias)>0:
            for m in medias:
                api.story_delete(m.id)
                randomsleep()   #time.sleep(random.randint(1,60)/10)
    print("All stories are deleted!")

def remove_followers():
    followers=api.user_followers(api.user_id_from_username(user_name))
    for f in followers:
        api.user_remove_follower(f)
        randomsleep()

def direct_eraser():
    time.sleep(2)
    while len(api.direct_threads(50))!=0:
        time.sleep(3)
        threads=api.direct_threads(50)
        if len(threads)>0:
            choice=input("Do you want to enable the manual mode? (Y for yes)").lower()
            if choice=='y':
                for t in threads:
                    print("Deleting {} thread".format(t.thread_title))
                    risp=input("Delete this thread? (Y for yes)").lower()
                    if risp == 'y':
                        deep_direct_eraser(t.id)
                        api.direct_thread_hide(t.id)
                        randomsleep()   #time.sleep(random.randint(1,60)/10)
                    else: print(t.thread_title,"thread not deleted")
            else:
                for t in threads:
                    print("Deleting {} thread".format(t.thread_title))
                    deep_direct_eraser(t.id)
                    api.direct_thread_hide(t.id)
                    randomsleep()   #time.sleep(random.randint(1,60)/10)
    print("All threads are deleted!")
    return

def deep_direct_eraser(thread_id): #TODO
    global user_name
    id=thread_id
    thread=api.direct_thread(id)
    messages=thread.messages
    for m in messages:
        if m.user_id==api.user_id_from_username(user_name):
            api.direct_message_delete(id,m.id)
    return

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
            time.sleep(2)
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
            time.sleep(2)
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
        randomsleep()   #time.sleep(random.randint(1,60)/10)
        print("Removed ",api.username_from_user_id(f))

def unfollow_infami():
    followers=api.user_followers(api.user_id_from_username(user_name))
    following=api.user_following(api.user_id_from_username(user_name))
    choice=input("Enable Manual mode? (Y for yes)").lower()
    if choice == 'y':
        for f in following: 
            print("Scanning",api.username_from_user_id(f))
            if f not in followers: 
                un=input("This user don't follow you, unfollow him? (Y for yes)").lower()
                if un== 'y':
                    api.user_unfollow(f)
                    print("Removed ",api.username_from_user_id(f))
                else:
                    print("Skipped ",api.username_from_user_id(f))
            randomsleep()   #time.sleep(random.randint(1,60)/10)
    else:
        for f in following: 
            print("Scanning",api.username_from_user_id(f))
            if f not in followers: 
                api.user_unfollow(f)
                print("Removed ",api.username_from_user_id(f))
            randomsleep()   #time.sleep(random.randint(1,60)/10)

def backup():
    if not os.path.exists('./backup'): os.mkdir("./backup")
    medias=api.user_medias_v1(api.user_id_from_username(user_name),0)
    if len(medias)==0:
        print("You have 0 posts")
        return
    else:
        print("You have {} posts".format(len(medias)))
        medias=[m.id for m in medias]
        res=save_medias(medias)
        if res == True: 
            print("Completed!")

def edit_account():
    api.account_edit(
        biography='',
        is_business=False,
        is_private=True,
        is_verified=True, #ce provo
        username='wipegram'+str(random.randint(0,5000)),
        external_url='',
        full_name='wipegram_piopy'

    )

def nuke():
    choice=input("Wanna nuke [1], partial nuke [2] or cancel [3]? ")
    if not choice == '1' or not choice=='2': exit()
    print("Unfollowing all your contacts")
    unfollow_all()
    input("Press ENTER to continue")
    print("Removing all your contacts")
    remove_followers()
    input("Press ENTER to continue")
    print("Removing all your posts and stories")
    cancella_s()
    if choice=='1':cancella_p()
    else: archivia_p()
    input("Press ENTER to continue")
    print("Deleting all your messages")
    direct_eraser()
    input("Press ENTER to continue")
    print("Deleting all your messages")
    edit_account()
    input("All done")

def save_medias(media_ids):                         
    if len(media_ids)==0: return False
    if not os.path.exists('./backup'): os.mkdir("./backup")
    for m in media_ids:
        randomsleep()
        path=(api.media_user(m)).username
        if not os.path.exists('./backup/'+path): os.mkdir("./backup/"+path)
        try:api.album_download(m,'./backup/'+path)
        except: pass
        try:api.photo_download(m,'./backup/'+path)
        except: pass
        try:api.video_download(m,'./backup/'+path)
        except: pass
        try:api.clip_download((m,'./backup/'+path))
        except: pass
        try:api.igtv_download(m,'./backup/'+path)
        except: pass
    return True


############################################################################################################################      

def menu():
    print("Select what to do")
    print("1. Delete/archive stories and posts")
    print("2. Unfollow who doesn't follow you back (including Chiara Ferragni)(Manual mode can be selected)")
    print("3. Unfollow all")
    print("4. Deep erase of all your Directs")
    print("5. Backup ALL your post")
    print("6. Nuclear Explosion")
    
    return input("Choice (1-6): ")

if __name__ == '__main__':
    login()
    choice=menu()
    if choice=='1': thanos()
    elif choice=='2': unfollow_infami()
    elif choice=='3': unfollow_all()
    elif choice=='4': direct_eraser()
    elif choice=='5': backup()
    elif choice=='6': nuke()
    else: exit(0)
    input("Press ENTER to exit")