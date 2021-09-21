from hexAndString import *
from DES import *

db_password=input("Enter the Database Password: ")
gmail_id=input("Enter Your Gmail-ID: ")
gmail_password=input("Enter Your Gmail-Password: ")
twilio_sid=input("Enter Twilio Account SID: ")
twilio_auth_token=input("Enter Twilio Account Authentication Token: ")
password=input("Enter the Application Password: ")

msg=string2hex(db_password+"\n"+gmail_id+"\n"+gmail_password+"\n"+twilio_sid+"\n"+twilio_auth_token)
key=string2hex(password)

len_msg=len(msg)
len_key=len(key)-1
content=[]
for i in range(len_msg):
    content.append(DESAlgorithm(key[i%len_key],msg[i],ch=1))

content.append("ffffffffffffffff")
content="\n".join(content)
print("\n\n"+content)

ch=input("\n\nDo you want to create the Info.txt file:\n\t1: Yes\n\t2: No\nChoice: ")
if ch=="1":
    a=open("Info.txt","w")
    a.write(content)
    a.close()
