import threading
import urllib
import getpass

import vk
import os


class Audio():
    """object with information about track"""

    def __init__(self):
        self.login()
        self.get_audio()
        self.count = len(self.list_audio) - 1

    def login(self):
        while True:
            login = input("input your login: ")
            password = getpass.getpass("input your password: ")
            try:
                session = vk.AuthSession(app_id='3697615', user_login=login,
                                         user_password=password)
                self.api = vk.API(session)
            except vk.exceptions.VkAuthError:
                print("you made mistake, try again")
            else:
                break

    def get_audio(self):
        self.list_audio = self.api.audio.get()

    def download(self, count=0):
        name = self.get_name(count)
        if not os.path.exists('{0}.mp3'.format(name)):
            print('start to write: "{0}"'.format(name))
            try:
                down_file = urllib.request.urlopen(self.list_audio[count]['url']).read()  # download file from network
                f = open('{0}.mp3'.format(name), 'wb')
                f.write(down_file)
                f.close()
                print('"{0}"  was loaded successfully'.format(name))
            # if track doesn't exist on server (was deleted and some else)
            except urllib.error.HTTPError:
                print('track "{0}" does not exist'.format(name))
            except KeyError:
                print('track "{0}" is not accessible'.format(name))
        else:
            print('track "{0}" was load before'.format(name))

    def download_all(self, quantity=4):
        quantity += 1
        while True:
            if self.count < 0: return
            if threading.active_count() < quantity:
                for i in range(quantity - threading.active_count()):
                    threading.Thread(target=self.download, args=(self.count,)).start()
                    self.count -= 1

    def get_name(self, count=0):
        name = '{0} - {1}'.format(self.list_audio[count]['artist'], self.list_audio[count]['title'])
        for char in '/:?|"':
            name = name.replace(char, '')
        return name


if __name__ == '__main__':
    Audio().download_all()
