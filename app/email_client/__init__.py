from email.mime.text import MIMEText
import smtplib


class EmailClient(object):

    def __init__(self):
        pass

    def set_host(self, host, port):
        self.host = host
        self.port = port

    def set_auth(self, username, password):
        self.username = username
        self.password = password

    def set_sender(self, sender):
        self.sender = sender

    def set_recipients(self, recipients):
        """
        set MIME-friendly email recipients
        'recipients' is either:
         - a single email address as string
         - a list of email addresses as list
        """
        if isinstance(recipients, str):
            self.recipients = recipients
        elif isinstance(recipients, list):
            COMMASPACE = ', '
            self.recipients = COMMASPACE.join(recipients)
        else:
            raise TypeError("recipients must be string or list of strings, " + str(type(recipients)) + " was given")

    def write_message(self, body="", subject=""):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = self.recipients
        self.message = msg

    def sendmail(self):
        server = smtplib.SMTP(self.host, self.port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(self.username, self.password)
        text = self.message.as_string()
        server.sendmail(self.sender, self.recipients, text)
        server.quit()


if __name__ == '__main__':
    
    # python 2 support
    try:
        import configparser # (python 3)
    except ImportError:
        import ConfigParser as configparser # (python 2)

    print("testing")

    config_file = 'config.ini'
    config = configparser.ConfigParser()
    config.read(config_file)

    print("sender: " + config.get('email', 'sender'))
    print("recipient: " + config.get('email', 'recipient'))
    print("username: " + config.get('email', 'username'))
    print("password: " + config.get('email', 'password'))
    print("host: " + config.get('email', 'host'))
    print("port: " + config.get('email', 'port'))

    message_body = "this is a test"
    subject = "test email"

    client = EmailClient()
    client.set_host(config.get('email', 'host'), config.get('email', 'port'))
    client.set_auth(config.get('email', 'username'), config.get('email', 'password'))
    client.set_sender(config.get('email', 'sender'))
    client.set_recipients(config.get('email', 'recipient'))
    client.write_message(message_body, subject)
    client.sendmail()
