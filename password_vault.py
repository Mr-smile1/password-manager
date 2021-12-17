# youtube link #
# https://www.youtube.com/watch?v=UrH2WCoYEVo&list=PLWZqQRbyQ4y__1Yi-zZhX06zw32WrwxCZ&index=3


from array import array
import sqlite3, hashlib       #database and hashing password
from tkinter import *         # GUI liberary
from tkinter import simpledialog
from functools import partial

# Database Code

with sqlite3.connect("password_Vault.db") as db:          #name is database in parathesis 
    cursor = db.cursor()                                           # cursor is the variable with is connected to db
   
#SQL command   
cursor.execute("""                                        
CREATE TABLE IF NOT EXISTS masterpassword(
    id INTEGER PRIMARY KEY,
    password TEXT NOT NULL
);
""")   

cursor.execute("""                                        
CREATE TABLE IF NOT EXISTS vault(
    id INTEGER PRIMARY KEY,
    website TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
""")   

#add new details to database
def popUp(text):
    answer = simpledialog.askstring("input string", text)

    return answer


# GUI and running code

window = Tk()                 # variable

window.title("Valut2000")     # name 


#User defined function for new user screen-----------------------
def hashPassword(input):
    hash = hashlib.md5(input)        #call hashlib turn input to md5 hash
    hash = hash.hexdigest()          #turn to hexadecimal hash ?

    return hash 


#User defined function for new user screen-----------------------
def firstScreen():
    window.geometry("300x150")

    lbl = Label(window, text="create master password")    
    lbl.config(anchor=CENTER)               
    lbl.pack()                              

    txt = Entry(window, width=10)           
    txt.pack()                              
    txt.focus()

    lbl2 = Label(window, text="Re-enter Password")                  
    lbl2.pack() 

    txt2 = Entry(window, width=10)           
    txt2.pack()                              
    txt2.focus()

    lbl3 = Label(window)                  
    lbl3.pack() 

    def savePassword():
        if txt.get() == txt2.get():                                     # if match
            hashedPassword = hashPassword(txt.get().encode('utf-8'))    # it will give some random values from utf-8 to hash                              # hashedPassword - variable
            
            #SQL command
            insert_password = """ INSERT INTO masterpassword(password) 
            VALUES(?) """
            
            cursor.execute(insert_password, [(hashedPassword)] )                      # calling function
           
            # ? is because we are passing a variable and pass it in [(hashedPassword)]
            
            db.commit()                                                 # actually add to database
            passwordVault()                                             # open the vault

        else:                                                           # if password don not match
            lbl3.config(text="Password do not match")                   

    btn = Button(window, text="Submit", command=savePassword)     
    btn.pack(pady=5)


#User defined function for login screen-----------------------
def loginScreen():
    window.geometry("250x100")

#text that appear on the GUI
    lbl = Label(window, text="enter master password")    # lbl is variable
    lbl.config(anchor=CENTER)               #anther way to center with padding and all
    lbl.pack()                              # no idea

#asks user to enter value
    txt = Entry(window, width=10)           # add - (show="*") :- to not show what is typed
    txt.pack()                              # some how it take properties from upper code and center the enter form
    txt.focus()

#text that appear on the GUI
    lbl2 = Label(window)                    # lbl2 is variable            
    lbl2.pack() 

    def getMasterPassword():
        checkMasterPassword = hashPassword(txt.get().encode('utf-8'))
        cursor.execute("SELECT * FROM masterpassword WHERE id = 1 AND password = ?", [(checkMasterPassword)])
        # id = 1 , as there will only be one master password so just check at id 1 
        
        #print(checkMasterPassword)

        return cursor.fetchall()

    def checkPassword():                    # the authentication function
        match = getMasterPassword()

        #print(match)

        if match:
            passwordVault()                 # function calling
            #lbl2.config(text="you are in..!!")    # print on GUI
            #print("you are in..!!")          # print on terminal
        else:
            txt.delete(0, 'end')             # it automatically delete the password when entered wrong
            lbl2.config(text="Wrong Password") 

    btn = Button(window, text="Submit", command=checkPassword)     # button to click, on click it will call checkPassword()
    btn.pack(pady=5)


#User defined function for Password Vault screen-----------------------
def passwordVault():
    for widget in window.winfo_children():                         # this basically delete the text enetered after we login froom login screen to vault
        widget.destroy()

    def addEntry():
        text = "Website Name"
        text2 = "Username"
        text3 = "Password"

        website = popUp(text)
        username = popUp(text2)
        password = popUp(text3)

        insert_fields = """ INSERT INTO vault(website,username,password)
        VALUES(?, ?, ?) """

        cursor.execute(insert_fields, (website, username, password))
        db.commit()

        passwordVault()

    def removeEntry(input):
        cursor.execute("DELETE FROM vault WHERE id = ?", (input,))
        db.commit()

        passwordVault()

    window.geometry("700x350")

    lbl3 = Label(window, text="Password Vault")                     # althought he scope of lbl is till the prev function but i used lbl3 just remove any connection and is for understanding basis only lbl variable can also be used insted
    lbl3.grid(column=1)

    btn = Button(window, text="Add Entry", command=addEntry)
    btn.grid(column=1, pady=10)

    lbl4 = Label(window, text="Website")
    lbl4.grid(row=2, column=0, padx=80)
    lbl4 = Label(window, text="Username")
    lbl4.grid(row=2, column=1, padx=80)
    lbl4 = Label(window, text="Password")
    lbl4.grid(row=2, column=2, padx=80)

    cursor.execute("SELECT * FROM VAULT")
    if(cursor.fetchall() != None):
        i=0
        while True:
            cursor.execute("SELECT * FROM VAULT")
            array = cursor.fetchall()

            lbl5 = Label(window, text=(array[i][1]), font=("Helvetica", 12))
            lbl5.grid(column=0, row=i+3)
            lbl5 = Label(window, text=(array[i][2]), font=("Helvetica", 12))
            lbl5.grid(column=1, row=i+3)
            lbl5 = Label(window, text=(array[i][3]), font=("Helvetica", 12))
            lbl5.grid(column=2, row=i+3)

            btn = Button(window, text="DELETE", command=partial(removeEntry, array[i][0]))
            btn.grid(column=3, row=i+3, pady=10)

            i=i+1

            cursor.execute("SELECT * FROM vault")
            if(len(cursor.fetchall()) <= i):
                break

cursor.execute("SELECT * FROM masterpassword")
if cursor.fetchall():
    loginScreen() 
else:
    firstScreen()              # function calling

window.mainloop()              # to open the GUI 