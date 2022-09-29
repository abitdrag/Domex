import smtplib, ssl

smtp_server = "smtp.gmail.com"
port = 587 # for starttls
sender_email = "domaindomex@gmail.com"
password = "domaindomex@12"
context = ssl.create_default_context()

def send_email(to, message):
    print("sending email!!")
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, to, message)
    except Exception as e:
        print(e)
    finally:
        server.quit()

