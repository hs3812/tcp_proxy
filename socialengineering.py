import smtplib
from email.mime.text import MIMEText
def sendmail(user,pwd,to,subject,text):
    msg = MIMEText(text)
    msg['From']=user
    msg['To']=to
    msg['Subject']=subject
    try:
        smtp = smtplib.SMTP('smtp.gmail.com',587)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(user,pwd)
        smtp.sendmail(user,to,msg.as_string())
        smtp.close()
    except:
        print('failed')
        
user = 'cs6903party1@gmail.com'
pwd = 'asdadsdasd'
sendmain(user,pwd,'rayray@gmail.com','mi','mimi')