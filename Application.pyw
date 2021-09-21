from hexAndString import *
from DES import *
import mysql.connector as SQL
from tkinter import *
from RSA import *
import smtplib
import time
import random
from twilio.rest import Client

cursor=""
db_password=""
file_location="Info.TXT"
From=""
ePass=""
con=""
account_sid=""
auth_token=""
link="www.google.com"
twilio_number = '+15873155539'

def infoExtraction(key):
    
    # Converting The Password guard enters to 64-bit DES-key
    key=string2hex(key)

    # Opening the encrypted file stored in memory and copying first 16 char to msg
    a=open(file_location)
    text=a.read()
    a.close()
    text=text.split("\n")
    msg=text[:-1]

    # Decrypting the msg using key(in a cyclic way)
    len_msg=len(msg)
    len_key=len(key)-1
    password=[]
    for i in range(len_msg):
        password.append(DESAlgorithm(key[i%len_key],msg[i],ch=2))

    # Converting The Password from 64-bit DES-Decryption to String
    password=hex2string(password)
    global From,ePass,db_password,account_sid,auth_token
    try:
        db_password,From,ePass,account_sid,auth_token=password.split("\n")
    except:
        pass
    return None

def changePasswordWindow():

    def changePassword(new):
        msg=string2hex(db_password+"\n"+From+"\n"+ePass+"\n"+account_sid+"\n"+auth_token)
        new=string2hex(new)
        len_msg=len(msg)
        len_new=len(new)-1
        password=[]
        for i in range(len_msg):
            password.append(DESAlgorithm(new[i%len_new],msg[i],ch=1))

        a=open(file_location)
        temp=a.read()
        temp=temp.split("\n")
        temp=temp[-1]

        # Replace the currently existing Info
        a=open(file_location,"w")
        for i in password:
            a.write(i+"\n")
        a.write(temp)
        a.close()
        return None

    def changePasswordCall():
        changePassword(newPasswordEntry.get())
        window3.destroy()
    window3 = Tk()
    window3.geometry("400x250")
    window3.title("Change Password")
    Label(window3, text = "New Password").place(x = 30,y = 50)
    newPasswordEntry=Entry(window3)
    newPasswordEntry.place(x = 30, y = 70)
    Button(window3,text = "Change",activebackground = "pink",activeforeground = "blue",command=changePasswordCall).place(x = 30, y = 100)
    window3.mainloop()

def homePageWindow():

    def visitorAuthenticationWindow():
        
        def visitorAuthentication():
            name=visitorNameEntry.get()
            query="SELECT phoneNo, publicKey_e, publicKey_n FROM Details WHERE flatNo="+flatNoEntry.get()+";"
            cursor.execute(query)
            data=cursor.fetchall()
            OTP=random.randint(100000,999999)
            OTPSent=pow(OTP,data[0][1],data[0][2])
            client=Client(account_sid, auth_token)
            msg=visitorNameEntry.get()+" is here to visit kindly copy the Code\n"+str(OTPSent)+"\n and Visit The website: "+link
            client.messages.create(to='+91'+data[0][0], from_= twilio_number, body=msg)

            def verify():
                
                def verificationDone():
                    verifiedWindow.destroy()
                    OTPWindow.destroy()
                    window3.destroy()
                    return None

                if OTP==int(OTPEntered.get()):
                    verifiedWindow=Tk()
                    verifiedWindow.geometry("250x100")
                    verifiedWindow.title("Verified")
                    Label(verifiedWindow, text="Verified!!!").place(x=90,y=20)
                    Button(verifiedWindow, text="Ok",activebackground="pink", activeforeground="blue",command=verificationDone).place(x=100,y=50)
                    verifiedWindow.mainloop()
                return None

            OTPWindow=Tk()
            OTPWindow.geometry("300x200")
            OTPWindow.title("OTP Verification")
            Label(OTPWindow, text="OTP").place(x=130,y=50)
            OTPEntered=Entry(OTPWindow)
            OTPEntered.place(x=85,y=70)
            Button(OTPWindow, text = "Verify",activebackground = "pink", activeforeground = "blue",command=verify).place(x=125,y=100)
            OTPWindow.mainloop()
            pass
        
        window3=Tk()
        window3.geometry("400x250")
        window3.title("Visitor Authentication")
        Label(window3, text = "Visitor Name").place(x = 30,y = 50)
        Label(window3, text = "Flat Number").place(x = 30,y = 110)
        visitorNameEntry=Entry(window3)
        visitorNameEntry.place(x = 30, y = 70)
        flatNoEntry=Entry(window3)
        flatNoEntry.place(x = 30, y = 130)
        Button(window3, text = "Send SMS",activebackground = "pink", activeforeground = "blue", command=visitorAuthentication).place(x = 30, y = 170)
        window3.mainloop()
        pass

    def monthlyRoutineWindow():

        def monthlyRoutine():
            global cursor
            cursor.execute("SELECT flatNo,email FROM Details;")
            data=cursor.fetchall()
            primeNo=primeNoGenerator(10000)
            try:
                server=smtplib.SMTP_SSL("smtp.gmail.com",465)
                server.login(From,ePass)
                for flatNo,To in data:
                    e,d,n=RSAKeyGen(primeNo)
                    query="UPDATE Details SET publicKey_e="+ str(e) +",publicKey_n="+ str(n) +" WHERE flatNo="+ str(flatNo) +";"
                    cursor.execute(query)
                    time.sleep(5)
                    Msg=f"Subject:This Month's Key\nHey flat {flatNo} Owner, your Private Key For This Month is\n{d}-{n}"
                    server.sendmail(From,To,Msg)
                cursor.execute("SELECT publickey_e,publickey_n FROM Details WHERE flatNo= (SELECT * FROM Variable);")
                e=cursor.fetchall()
                e,n=e[0]
                a=open(file_location)
                text=a.read()
                a.close()
                text=text.split("\n")
                text=text[0:-1]
                text.append(RSAEncryption(e,n,db_password+"\n"+From+"\n"+ePass+"\n"+account_sid+"\n"+auth_token))
                text="\n".join(text)
                a=open(file_location,'w')
                a.write(text)
                a.close()
            finally:
                server.quit()
                wait.destroy()
            return None
        wait=Tk()
        wait.geometry("300x100")
        wait.title("Monthly Routine")
        Label(wait,text="Run The Monthly Routene?").pack()
        Button(wait,text="yes",activebackground = "pink", activeforeground = "blue",command=monthlyRoutine).pack()
        wait.mainloop()
    
    try:
        window.destroy()
    except:
        pass
    window2 = Tk()
    window2.title("Home Page")
    window2.geometry("400x250")
    Button(window2, text = "Monthly Routine",activebackground = "pink", activeforeground = "blue", command=monthlyRoutineWindow).place(x = 120, y = 50)
    Button(window2, text = "Visitor Authentication",activebackground = "pink", activeforeground = "blue", command=visitorAuthenticationWindow).place(x = 120, y = 100)
    Button(window2, text = "Change Password",activebackground = "pink", activeforeground = "blue", command=changePasswordWindow).place(x = 120, y = 150)
    window2.mainloop()

def Login():
    try:
        global cursor,con
        con=SQL.connect(host='localhost', user='root', password=db_password, database='alpha',auth_plugin='mysql_native_password',autocommit=True)
        cursor=con.cursor()
        return True
    except SQL.errors.ProgrammingError:
        return False

def directLogin():
    infoExtraction(passwordValue.get())
    if Login()==True:
        homePageWindow()
    return None

def forgotPasswordWindow():
    
    def forgotPassword():
        d,n=map(int,(key.get()).split("-"))
        a=open(file_location)
        temp=a.read()
        temp=temp.split("\n")
        temp=temp[-1]
        try:
            temp=RSADecryption(d,n,temp)
        except:
            return None
        global From,ePass,db_password,account_sid,auth_token
        db_password,From,ePass,account_sid,auth_token=temp.split("\n")
        if Login()==True:
            window5.destroy()
            changePasswordWindow()
            homePageWindow()
        return None

    window5=Tk()
    window5.geometry("300x150")
    window5.title("Password Recovery")
    Label(window5, text="Secretarie's Private Key").place(x=90, y=20)
    key=Entry(window5)
    key.place(x=85, y=50)
    Button(window5, text = "Submit",activebackground = "pink", activeforeground = "blue",command=forgotPassword).place(x=125, y=90)
    window5.mainloop()
    return None

window=Tk()
window.geometry("400x250")
window.title("Login")
Label(window, text="Password").place(x = 165,y = 50)
passwordValue=Entry(window)
passwordValue.place(x = 130, y = 70)
Button(window, text = "Login",activebackground = "pink", activeforeground = "blue", command=directLogin).place(x = 165, y = 110)
Button(window, text = "Forgot Password",activebackground = "pink", activeforeground = "blue", command=forgotPasswordWindow).place(x = 140, y = 170)
window.mainloop()
