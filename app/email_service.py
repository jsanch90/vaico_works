import smtplib, ssl
from email.message import EmailMessage

class Email_services():

    def __init__(self, sender_email="vaicoworksreportes@gmail.com", password="vaicoworks"):
        self.sender_email = sender_email
        self.password = password
        self.smtp_server = "smtp.gmail.com"
        self.port = 587  # For starttls
        self.context = ssl.create_default_context()
    
    def get_sender(self):
        return self.sender_email

    
    """Recipients must be a list with the email addresses that you want to send the message"""
    def send_email(self,recipients,subject='Reporte de la obra',message="""Vaico Works email service is working"""):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.get_sender()
        msg['To'] = ', '.join(recipients)
        msg.set_content(message)

        server = smtplib.SMTP(self.smtp_server,self.port)

        try:
            server.ehlo() 
            server.starttls(context=self.context) # Secure the connection
            server.ehlo() # Can be omitted
            server.login(self.get_sender(), self.password)
            server.send_message(msg)

        except Exception as e:
            # Print any error messages to stdout
            print('Error',e)
        finally:
            server.quit()
        print('Message sent')

# x = Email_services()
# x.send_email(['este991@gmail.com','p4rsek@gmail.com'])