import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def enviar_correo(correo_admin, pass_admin, subject,body):
    email = correo_admin
    if correo_admin.find('gmail') != -1:
        s = smtplib.SMTP('smtp.gmail.com', 587)
    if correo_admin.find('hotmail') != -1:
        s = smtplib.SMTP('pod51000.outlook.com', 587)
    s.starttls()
    s.login(correo_admin,pass_admin)
    msg = MIMEMultipart()
    msg['From']=correo_admin
    msg['To']=email
    msg['Subject']=subject
    msg.attach(MIMEText(body,'plain'))
    s.send_message(msg)
    del msg
    s.quit()