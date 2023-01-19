import requests
import json
import os
from tkinter import *
from tkinter import messagebox as mb
from tkinter import Tk, Frame, BOTH


class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")
        self.parent = parent
        self.parent.title("Window on the screen center")
        self.pack(fill=BOTH, expand=1)
        self.centerWindow()

    def centerWindow(self):
        w = 290
        h = 150

        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))


def main():
    url = 'https://api.worldoftanks.ru/wot/account/list/?application_id=e06efe55259bb20b5357450f1f75e0bc&search=' + fld_name.get() + '&fields=nickname%2C+account_id&limit=1'

    get_user_id(url)


def get_user_id(url):
    responce = requests.get(url)
    responce_json_data = responce.json()

    write_json_file(responce_json_data)


def write_json_file(responce_json_data):
    if (responce_json_data['meta']['count'] == 1):
        account_id = responce_json_data['data'][0]['account_id']
        account_nickname = responce_json_data['data'][0]['nickname']

        if os.path.isfile('players.json'):
            if (check_is_account_added(responce_json_data) == False):
                with open('players.json', 'r') as file:
                    file_json_data = json.load(file)
                    file_json_data['players'].append({str(account_nickname): account_id})
                    with open('players.json', 'w') as file:
                        json.dump(file_json_data, file, indent=4, ensure_ascii=False)
                    mb.showinfo(
                        "WG player id checker",
                        "Данные добавлены в файл players.json")
        else:
            file_json_data = {'players': [{str(account_nickname): account_id}]}
            with open('players.json', 'w') as file:
                json.dump(file_json_data, file, indent=4, ensure_ascii=False)
            mb.showinfo(
                "WG player id checker",
                "Данные добавлены в файл players.json")
    else:
        mb.showwarning(
            'WG player id checker',
            'Аккаунта с таким именем не существует!')


def check_is_account_added(responce_json_data):
    with open('players.json', 'r') as file:
        account_id = responce_json_data['data'][0]['account_id']
        account_nickname = responce_json_data['data'][0]['nickname']
        file_json_data = json.load(file)
        for i in range(len(file_json_data['players'])):
            if (file_json_data['players'][i] == {str(account_nickname): account_id}):
                mb.showwarning(
                    'WG player id checker',
                    'Аккаунт с таким именем уже есть в файле players.json')
                return (True)
        return (False)


window = Tk()
ex = Example(window)

window.title('WG player id checker')
window.geometry('300x200')
window.resizable(False, False)

fld_name = Entry(window, font=40, justify=CENTER)
fld_name.pack(pady=40)

btn_get_id = Button(window, text='Получить данные', font=40, command=main)
btn_get_id.pack(side=BOTTOM, pady=30)

def doProcessOnEnterKey(e):
    main()

window.bind('<Return>', doProcessOnEnterKey)

window.mainloop()