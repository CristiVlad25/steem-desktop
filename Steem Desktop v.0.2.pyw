#!/usr/bin/env python3.5

from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from threading import Thread
from steem.post import Post as ps
from steem.account import Account as act
import piston
import steem

# The Main Window

root = Tk()
root.title('Steem Desktop')
root.iconbitmap('stm.ico')

# Style and Logo

style = ttk.Style()
style.theme_use('winnative')
imglogo = PhotoImage(file='stm.png').subsample(2,2)

# Notebook for the Tabs

noteb = ttk.Notebook()
f1 = Text(height=20, width=50, font='comic-sans 10', fg='green')
f2 = scrolledtext.ScrolledText(height=20, width=50, wrap=WORD, font='comic-sans 10', fg='green')
f3 = scrolledtext.ScrolledText(height=20, width=90, wrap=WORD, font='comic-sans 10', fg='green')
noteb.add(f1, text='User Account')
noteb.add(f2, text='Last Post')
noteb.add(f3, text='Votes Given')
noteb.grid(row=1, column=1, pady=10)
f1.tag_config('gr', foreground='green') # just in case some specific text needs to be colored
f2.tag_config('gr', foreground='green') # just in case some specific text needs to be colored
f2.tag_config('bl', foreground='blue') # just in case some specific text needs to be colored

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

    if f3.get('1.0', END) != '':
        f3.delete('1.0', END)
        
    if entry1.get() != '':
        acnt = piston.account.Account(entry1.get())
        post = piston.post.Post(acnt.steem.get_blog(entry1.get())[0])
        actl = act(entry1.get())
        perml = actl.steemd.get_blog_entries(entry1.get(), -1, 1)[0]['permlink']
        rebl = actl.steemd.get_reblogged_by(entry1.get(), perml)
        items = acnt.steem.get_blog(entry1.get())[0].items()

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
        
        f2.insert(INSERT, post.title+'\n\n', 'bl')
        f2.insert(INSERT, 'Resteemed by: '+str(rebl)+'\n')
        f2.insert(INSERT, 'Replies: '+str(post.children)+'\n')
        f2.insert(INSERT,'Current Vote Count: '+str(len(post.active_votes))+'\n')
        f2.insert(INSERT, 'Current Payout: '+str(ps(post).reward)+'\n\n')
        f2.insert(INSERT,'Voter\t\t\tPercentage\n\n')

        # Votes Given

        f3.insert(INSERT, 'The Last 100 Votes Given by the User'+'\n\n', 'bl')
        f3.insert(INSERT,'Post Author\tPercentage\tPermlink\n\n')

    # Managing/Populating the Vote List   

    list_one = list() # Creating a list for Vote Management

    for item in items:
        
        if 'active_votes' in item[0]:
            for i in item[1]:
                i_time = i['time']
                i_voter = i['voter']
                i_percent = i['percent']/100
                list_one.append((i_time, i_voter, i_percent))

    for i in sorted(list_one, reverse=True):
        time, voter, percent = i
        f2.insert(INSERT,voter+'\t\t\t'+str(percent)+'\n')

    # Managing/Populating the 'Votes Given' List - last 100 votes

    list_two = list() # Creating a list for Vote Management

    for itm in acnt.history2():
        
        if itm['type'] == 'vote' and itm['voter'] == 'cristi':
            itm_time = itm['timestamp']
            itm_link = str(itm['permlink'])
            itm_author = itm['author']
            itm_percent = str(itm['weight']/100)
            list_two.append((itm_time, itm_author, itm_percent, itm_link))

    list_two = list_two[-100:]

    for itmd in sorted(list_two, reverse=True):
        time, author, percentt, link = itmd
        f3.insert(INSERT, author+'\t\t'+percentt+'\t\t'+link+'\n')            

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

# The Checkbutton

var_one = IntVar()
checkb_one = Checkbutton(root, text='Auto-Refresh', onvalue=1, offvalue=0, variable=var_one)
checkb_one.grid(row=0, column=1, sticky=E)

# Automate the Retrieve if Checkbutton is 'checked'

def chckb(*args):
       
    if var_one.get():
        thr()
        
    else:
        pass

    root.after(30000, chckb) #refreshes after 1 minute

# Running the mainloop

entry1.bind('<Return>', get) # for the 'get' function
entry1.focus()
root.resizable(width=False, height=False)
chckb()
root.mainloop()
