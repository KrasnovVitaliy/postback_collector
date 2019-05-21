import smtplib
from config import Config
import logging

config = Config()
logger = logging.getLogger(__name__)


def send_email(receiver, subject, text):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(config.EMAIL_USERNAME, config.EMAIL_PASSWORD)

    body = '\r\n'.join(['To: {}'.format(receiver),
                        'From: {}'.format(config.EMAIL_USERNAME),
                        'Subject: {}'.format(subject),
                        '', text])

    try:
        server.sendmail(config.EMAIL_USERNAME, [receiver], body)
        logger.debug("Email to {} with subject: {} sent".format(receiver, subject))
    except Exception as e:
        logger.error("Coul not send email. Error: {}".format(e))

    server.quit()
