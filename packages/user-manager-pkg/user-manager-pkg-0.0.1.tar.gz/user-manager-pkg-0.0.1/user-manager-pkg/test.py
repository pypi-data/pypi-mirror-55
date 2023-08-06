#!/usr/bin/env python3
import os
import subprocess
from tkinter import *
import crypt

tk = Tk()
tk.title('Test')
tk.geometry('600x400')

print("hello")
print('hello "g"')

os.system("l"+"s")

def mand():
	print("hello Mand")
	a = entry1.get()
	print(a)
	pw = entry2.get()
	en = crypt.crypt(pw,"sha256")
	os.system("echo %s | sudo -S %s"%(pw,"adduser --disabled-password --gecos "+'""'+" "+a))
	os.system("(echo %s ;echo %s) | sudo -S %s"%(pw,pw,"passwd "+a))
	#os.system("echo %s | sudo -S %s"%(pw,"passwd "+a)
	#os.system("echo "+a+":"+pw+" | chpasswd ")
	#os.system("$echo "+a+" | sudo -S sleep 1 && sudo -S useradd -p "+en+" -m "+a)
	
def listUser():
	pw=123456
	os.system("echo %s | sudo -S %s"%(pw,"awk -F':' '$2 ~ "+'"\$"'+" {print $1}' /etc/shadow"))

label1 =Label(tk, text="Username")
entry1 = Entry(tk, width=25)
label1.pack()
entry1.pack()

label2 =Label(tk, text="Password")
entry2 = Entry(tk, width=25)
label2.pack()
entry2.pack()

button1 = Button(tk, text='Test', width=25, command=mand)
button1.pack()

button2 = Button(tk, text='ListUser', width=25, command=listUser)
button2.pack()

tk.mainloop()
