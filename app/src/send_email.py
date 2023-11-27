import os
import smtplib, ssl

def send_email(sender_email, receiver_email, message):
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    password = os.environ.get('EMAIL_PASSWORD')
    # Create a secure SSL context
    context = ssl.create_default_context()  

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.starttls(context=context) # Secure the connection
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()