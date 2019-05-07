import smtplib, ssl
import cv2
from imageio import imread
import io
import os
import base64
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Email_services():

    def __init__(self, sender_email="vaicoworksreportes@gmail.com", password="vaicoworks"):
        self.sender_email = sender_email
        self.password = password
        self.smtp_server = "smtp.gmail.com"
        self.port = 587  # For starttls
        self.context = ssl.create_default_context()

    def get_sender(self):
        return self.sender_email

    def get_image_from_base64(self,base64_str, out_name='b64img'):
        out_name = out_name+'.jpg'
        out_name = "static/img/" + out_name
        #b64_string = base64_str.decode()
        img_temp = imread(io.BytesIO(base64.b64decode(base64_str)))
        cv2_img = cv2.cvtColor(img_temp, cv2.COLOR_RGB2BGR)
        cv2.imwrite(out_name, cv2_img)

    def clear_temp_imgs(self):
        os.remove('static/img/reporte_de_obra.jpg')

    """+ Recipients must be a list with the email addresses that you want to send the message.
    + Attachment parameter must be a string with the path of the image."""
    def send_email(self,recipients,subject='Reporte de la obra',
                        message="Vaico Works email service is working",
                        attachment=None):

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = 'vaicoworksreportes@gmail.com'
        msg['To'] = ', '.join(recipients)
        body = MIMEText(message) # convert the body to a MIME compatible string
        msg.attach(body)
        msg.preamble = 'Vaico Works'

        if attachment is not None:
            filename = attachment.split('/')[-1]
            with open(attachment,'rb') as _file:
                img = MIMEImage(_file.read())
                img.add_header('Content-Disposition', "attachment; filename= {0}".format(filename))
            msg.attach(img)

        server = smtplib.SMTP(self.smtp_server,self.port)

        try:
            server.ehlo()
            server.starttls(context=self.context) # Secure the connection
            server.ehlo()
            server.login(self.get_sender(), self.password)
            server.send_message(msg)

        except Exception as e:
            # Print any error messages to stdout
            print('Error',e)
        finally:
            if (attachment is not None):
                self.clear_temp_imgs()
            server.quit()
        print('Message sent')


#x = Email_services()
#x.send_email(['p4rsek@gmail.com','camilovilla699@gmail.com'],attachment='/home/josh/MEGA/Keras/test_vaico/person6.jpg')#
