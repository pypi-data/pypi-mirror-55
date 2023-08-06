#!/usr/bin/env python3
import os
import subprocess
from tkinter import *
from tkinter import messagebox
import crypt

tk = Tk()
tk.title('Test')
tk.geometry('600x400')

print("hello")
print('hello "g"')

os.system("l"+"s")
adminPassword = ""
haveListAcc = "nothave"

def setAdminpassword(passwd):
	global adminPassword
	adminPassword = passwd
	print(adminPassword)

def forSetAdminpassword():
	global adminPassword
	popupp = Toplevel()
	popupp.wm_title("ListAccounts")
	popupp.geometry("300x200")

	labelPassAd = Label(popupp, text="Please assign [sudo] password")
	labelPassAd.config(font=("Courier", 10))
	entryPassAd = Entry(popupp, width=29)

	buttonConList = Button(popupp, text="OK", width=10, command=lambda: setAdminpassword(entryPassAd.get()))
	butonnCalcelList = Button(popupp, text="CANCEL", width=10)

	labelPassAd.place(x=37, y=10)
	entryPassAd.place(x=37, y=40)
	buttonConList.place(x=10, y=80)
	butonnCalcelList.place(x=180, y=80)
	if adminPassword != "":
		entryPassAd.insert(0, adminPassword)

def mand():
	global adminPassword
	global haveListAcc
	if adminPassword == "":
		popupp = Toplevel()
		popupp.wm_title("ListAccounts")
		popupp.geometry("300x200")

		labelPassAd = Label(popupp, text="Please assign [sudo] password")
		labelPassAd.config(font=("Courier", 10))
		entryPassAd = Entry(popupp, width=29)

		buttonConList = Button(popupp, text="OK", width=10, command=lambda: setAdminpassword(entryPassAd.get()))
		butonnCalcelList = Button(popupp, text="CANCEL", width=10)

		labelPassAd.place(x=37, y=10)
		entryPassAd.place(x=37, y=40)
		buttonConList.place(x=10, y=80)
		butonnCalcelList.place(x=180, y=80)
	else:
		un = entry1.get()
		pw = entry2.get()
		en = crypt.crypt(pw,"sha256")
		stat = messagebox.askyesno(title='Add User', message='do you sure add?')
		if stat > 0:
			os.system("echo %s | sudo -S %s"%(adminPassword,"adduser --disabled-password --gecos "+'""'+" "+un))
			os.system("(echo %s ;echo %s) | sudo -S %s"%(pw,pw,"passwd "+un))
			entry1.delete(0, END)
			entry2.delete(0, END)
			if haveListAcc == "nothave":
				Listbox.delete(0, END)
				outt = os.popen("echo %s | sudo -S %s"%(adminPassword,"awk -F':' '$2 ~ "+'"\$"'+" {print $1}' /etc/shadow")).read()
				out2 = outt.split("\n")
				print(out2)
				for p in out2:
					if p != '':
						Listbox.insert(END, p)
				haveListAcc = "have"
	#os.system("$echo "+a+" | sudo -S sleep 1 && sudo -S useradd -p "+en+" -m "+a)
	
def listUser():
	#pw=123456
	global adminPassword
	global haveListAcc

	if adminPassword == "":
		popupp = Toplevel()
		popupp.wm_title("ListAccounts")
		popupp.geometry("300x200")

		labelPassAd = Label(popupp, text="Please assign [sudo] password")
		labelPassAd.config(font=("Courier", 10))
		entryPassAd = Entry(popupp, width=29)

		buttonConList = Button(popupp, text="OK", width=10, command=lambda: setAdminpassword(entryPassAd.get()))
		butonnCalcelList = Button(popupp, text="CANCEL", width=10)

		labelPassAd.place(x=37, y=10)
		entryPassAd.place(x=37, y=40)
		buttonConList.place(x=10, y=80)
		butonnCalcelList.place(x=180, y=80)
	else:
		outt = os.popen("echo %s | sudo -S %s"%(adminPassword,"awk -F':' '$2 ~ "+'"\$"'+" {print $1}' /etc/shadow")).read()
		#outt = os.popen("echo %s | sudo -S %s"%(pw,"awk -F':' '$2 ~ "+'"\$"'+" {print $1}' /etc/shadow")).read()
		out2 = outt.split("\n")
		print(out2)
		haveListAcc="have"
		putAccountToList(out2)

def putAccountToList(ary):
	global haveListAcc
	if haveListAcc=="nothave":
		for i in ary:
			if i != "":
				Listbox.insert(END, i)
	else:
		Listbox.delete(0,END)
		for i in ary:
			if i != "":
				Listbox.insert(END, i)

def setChangepassword(pw, un):
	os.system("(echo %s ;echo %s) | sudo -S %s"%(pw,pw,"passwd "+un))

def changePassPop():
	global adminPassword
	current_selected = Listbox.curselection()
	nameUpdate = Listbox.get(current_selected, None)
	print(nameUpdate)

	popupp = Toplevel()
	popupp.wm_title("ListAccounts")
	popupp.geometry("300x200")

	labelPassChange = Label(popupp, text="Change "+nameUpdate+" password")
	labelPassChange.config(font=("Courier", 10))
	entryPassChange = Entry(popupp, width=29)

	buttonConChange = Button(popupp, text="OK", width=10, command=lambda: setChangepassword(entryPassChange.get(),nameUpdate))
	butonnCalcelChange = Button(popupp, text="CANCEL", width=10)

	labelPassChange.place(x=37, y=10)
	entryPassChange.place(x=37, y=40)
	buttonConChange.place(x=10, y=80)
	butonnCalcelChange.place(x=180, y=80)

def delAccount(pw, un):
	os.system("echo %s | sudo -S %s"%(pw,"userdel "+un))
	outt = os.popen("echo %s | sudo -S %s"%(adminPassword,"awk -F':' '$2 ~ "+'"\$"'+" {print $1}' /etc/shadow")).read()
	out2 = outt.split("\n")
	for o in out2:
		if o != '':
			Listbox.insert(END, o)

def getdelAccount():
	global adminPassword
	#sudo userdel Username
	stat = messagebox.askyesno(title='Add User', message='do you sure to delete?')
	if stat > 0:
		current_selected = Listbox.curselection()
		nameDelete = Listbox.get(current_selected, None)
		print(nameDelete)
		Listbox.delete(0, END)
		delAccount(adminPassword, nameDelete)
	#os.system("echo %s | sudo -S %s"%(adminPassword,"userdel "+name))

label1 =Label(tk, text="Username : ")
entry1 = Entry(tk, width=25)
label1.place(x=100,y=50)
entry1.place(x=185,y=50)

label2 =Label(tk, text="Password  : ")
entry2 = Entry(tk, width=25)
label2.place(x=100,y=80)
entry2.place(x=185,y=80)

Addbutton = Button(tk, text='ADD', width=5, command=mand, bg="gray")
Addbutton.place(x=420, y=50)



button2 = Button(tk, text='ListUser', width=5, command=listUser, bg="gray")
button2.place(x=420, y=80)


Listbox = Listbox(width=50, height=10, bg="white", fg="black", selectbackground="gray")
Listbox.place(x=100,y=120)

button3 = Button(tk, text='Delete', width=12, bg="gray", command=lambda: getdelAccount())
button3.place(x=410, y=315)

button2 = Button(tk, text='Change Password', width=12, bg="gray", command=lambda: changePassPop())
button2.place(x=70, y=315)

buttonSetAdpas = Button(tk, text='Set Admin Password', width=20, bg="gray", command=lambda: forSetAdminpassword())
buttonSetAdpas.place(x=208, y=315)

tk.mainloop()
