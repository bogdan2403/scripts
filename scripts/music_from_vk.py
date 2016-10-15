import vk
import urllib.request
import time
import os


class Audio_info():
    """object with information about track"""

    def __init__(self, track):
        self.title = track['title']
        self.artist = track['artist']
        self.url = track['url']

    def __str__(self):
        """"return name track (str)"""
        return '{0} - {1}'.format(self.artist, self.title)


# initialization session
while True:
    login = input("input your login: ")
    password = input("input your password: ")
    try:
        session = vk.AuthSession(app_id='3697615', user_login=login, user_password=password)
        api = vk.API(session)
    except vk.exceptions.VkAuthError:
        print("you made mistake, try again")
    else:
        break


def repl(track):
    track_name = str(track)

    # check name on symbol '/', ':' and '?'"
    # return index if is symbol
    def check(track):
        flag0 = track.find("/")
        flag1 = track.find(":")
        flag2 = track.find("?")
        flag3 = track.find("|")
        flag4 = track.find('"')
        if flag0 != -1:
            return flag0
        if flag1 != -1:
            return flag1
        if flag2 != -1:
            return flag2
        if flag3 != -1:
            return flag3
        if flag4 != -1:
            return flag4

    flag = check(track_name)
    if flag or flag == 0:
        while flag or flag == 0:
            # we can't change symbol in string, so we use list
            track_name = list(track_name)
            track_name[flag] = ""
            # i don't know why doesn't work str(), it returns list
            s = ''
            for i in track_name:
                s = s + i
            # for check need
            flag = check(s)
            track_name = s
    # return track_name without symbol '/', ':' and '?'
    return track_name


list_audio = api.audio.get()
i = len(list_audio) - 1
if not os.path.exists('music/'):
    os.makedirs('music')
for i, track in enumerate(reversed(list_audio)):
    track = Audio_info(track)
    track_name = repl(track)
    if not os.path.exists('music/{0}.mp3'.format(track_name)):
        print(ascii('start to write: {0}'.format(track_name)))
        try:
            t1 = time.time()
            down_file = urllib.request.urlopen(track.url).read()
            f = open('music/{0}.mp3'.format(track_name), 'wb')
            f.write(down_file)
            f.close()
            t2 = time.time() - t1
            mass = os.path.getsize('music/{0}.mp3'.format(track_name)) / 1024 / 1024
            print(ascii('{0}  {1} Mb/s'.format(track_name, round(mass / t2, 1))))
            # if track doesn't exist on server (was deleted and some else)
        except urllib.request.URLError:
            print(ascii('track does no\'t exist'))
    else:
        print(ascii('track {0} was load before'.format(track_name)))
    i -= 1
