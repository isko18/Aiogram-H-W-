import smtplib
from config import smtp_sender,smpt_sender_password
from email.message import EmailMessage
from email.mime.image import MIMEImage

def send_email(to_email,subject,message,image_path = None):
    sender = smtp_sender
    password = smpt_sender_password
    
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    
    try:
        server.login(sender,password)
        msg = EmailMessage()
        msg["subject"] = subject 
        msg["From"] = sender
        msg["To"] = to_email
        msg.set_content(message)
        if image_path:
            with open(image_path, "rb") as img:
                img_d = img.read()
                msg.add_attachment(img_d, maintyoe= 'image', subtype= 'jng',filename=image_path)
        server.send_message(msg)
        
        
        return"200 ok"
    except Exception as error:
        return f"Error{error}"
    finally:
        server.quit()
print(send_email("toksonbaevislam2004@gmail.com","Demo day","Здравствуйте вы приглашены на Demo day",r"C:\Users\Amin_stors\OneDrive\Рабочий стол\Aiogram-H-W-\Happy Halloween 1920x1280.jpg"))