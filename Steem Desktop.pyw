#!/usr/bin/env python3.4

from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from threading import Thread
import piston

# The Main Window

root = Tk()
root.title('Steemit Desktop')
root.iconbitmap('stm.ico')

# Creating a Dictionary for Vote Management

dict1 = {}

# Style and Logo

style = ttk.Style()
style.theme_use('winnative')
imglogo = PhotoImage(file='stm.png').subsample(2,2)

# Notebook for the Tabs

noteb = ttk.Notebook()
f1 = Text(height=20, width=50, font='comic-sans 10', fg='green')
f2 = scrolledtext.ScrolledText(height=20, width=50, wrap=WORD, font='comic-sans 10', fg='green')
noteb.add(f1, text='User Account')
noteb.add(f2, text='Last Post')
noteb.grid(row=1, column=1, pady=10)
f1.tag_config('gr', foreground='green') # just in case some specific text needs to be colored
f2.tag_config('gr', foreground='green') # just in case some specific text needs to be colored

# Creating the Label, Entry widgets

label1 = ttk.Label(root, text='Username:')
label1.grid(row=0, column=0)
entry1 = ttk.Entry(root, width=30)
entry1.grid(row=0, column=1, columnspan=4, sticky=W)
label2=ttk.Label(root, image=imglogo)
label2.grid(row=1, column=6)

# The Callback Function for the 'Retrieve' button

def callback():

    # clearing the text windows when refreshing (using the Retrieve button for multiple times)
    
    if f1.get('1.0', END) != '':
        f1.delete('1.0', END)

    if f2.get('1.0', END) != '':
        f2.delete('1.0', END)
        
    if entry1.get() != '':
        acnt = piston.account.Account(entry1.get())
        post = piston.post.Post(acnt.steem.get_blog(entry1.get())[0])

        # User Account
        
        f1.insert(INSERT,'Followers: '+str(len(acnt.get_followers())))
        f1.insert(INSERT, '\nAccount Reputation: '+str(acnt.rep))
        f1.insert(INSERT, '\nVoting Power: '+str(acnt.voting_power()))
        f1.insert(INSERT, '\n\nBalances:\n')
        f1.insert(INSERT, '\nSteem: '+str(acnt.balances['STEEM']))
        f1.insert(INSERT, '\nSteem Power: '+str(acnt.sp))
        f1.insert(INSERT, '\nSBD: '+str(acnt.balances['SBD']))
        f1.insert(INSERT, '\nVests: '+str(acnt.balances['VESTS']))

        # Last Post
        
        f2.insert(INSERT, post.title+'\n\n')
        f2.insert(INSERT,'Current Vote Count: '+str(len(post.active_votes))+'\n\n')
        f2.insert(INSERT,'Voter\t\t\tPercentage\n\n')

    # Managing/Populating the Vote List

    for item in acnt.steem.get_blog('cristi')[0].items():
        if 'active_votes' in item:
            for item1 in item[1]:
                dict1[item1['time']]={item1['voter'], item1['percent']/100}
            for k,(v1,v2) in sorted(dict1.items(), reverse=True):
                if type(v1)==float:
                    f2.insert(INSERT, v2+'\t\t\t'+str(v1)+'\n')
                else:
                    f2.insert(INSERT, v1+'\t\t\t'+str(v2)+'\n')

# Function to use the 'Return' key and 'Retrieve' button interchangeably

def get(event):
    thr()

# Using threading for smoother functionality

def thr():
    t1 = Thread(target=callback, daemon=True)
    t1.start()

# The Retrieve Button (needs to be defined after the 'callback' and 'thr' functions

MyButton1 = ttk.Button(root, text='Retrieve', width=10, command=thr)
MyButton1.grid(row=0, column=6)

# Running the mainloop

entry1.bind('<Return>', get) # for the 'get' function
entry1.focus()
root.resizable(width=False, height=False)
root.mainloop()
