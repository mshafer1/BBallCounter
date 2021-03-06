import json
import smtplib
import datetime
from os import path

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

EMAIL_LIST_FILE = 'PrimaryList.json'
EMAIL_CONFIG_FILE = 'emailConfig.json'

if __name__ == '__main__':
    # me == my email address
    # you == recipient's email address
    me = "matthew.shafer@ni.com"

    config_file = path.join(path.dirname(path.realpath(__file__)),EMAIL_CONFIG_FILE)
    with open(config_file, 'r') as configFile:
        config = json.load(configFile)

    me = config['SENDER_EMAIL']

    file = path.join(path.dirname(path.realpath(__file__)),EMAIL_LIST_FILE)
    with open(file, 'r') as addresses_file:
        recipients = json.load(addresses_file)
    if len(recipients) == 0:
        raise Exception("Can't send to nobody")
    you = ', '.join(recipients)

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Basketball {0} (if court is dry)?".format('@ 4:30' if datetime.datetime.today().weekday() not in [4] else 'Saturday ({:%m/%d}) at 10:00'.format((datetime.date.today() + datetime.timedelta(days=1))))
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    text = "Can you make it?\n https://goo.gl/forms/k4jnCc879HfuSfeA3"
    html = """
    <html>
      <head></head>
      <body>
        <h1>Can you make it?</h1>
        <ul>
            <li><a href="https://docs.google.com/forms/d/e/1FAIpQLSf1ZzOoMllQlGFaQzSGWyv5VXUpKrUa8DRKp_XRNZCaBAQfsQ/formResponse?entry.164115360=Email+Responder&entry.462227184=Yes&submit=Submit">Yes</a></li>
            <li><a href="https://docs.google.com/forms/d/e/1FAIpQLSf1ZzOoMllQlGFaQzSGWyv5VXUpKrUa8DRKp_XRNZCaBAQfsQ/formResponse?entry.164115360=Email+Responder&entry.462227184=Yes+-+late&submit=Submit">Yes - Late</a></li>
            <li><a href="https://docs.google.com/forms/d/e/1FAIpQLSf1ZzOoMllQlGFaQzSGWyv5VXUpKrUa8DRKp_XRNZCaBAQfsQ/formResponse?entry.164115360=Email+Responder&entry.462227184=Probably&submit=Submit">Probably</a></li>
        </ul>
        <br/>
        <a href="https://docs.google.com/forms/d/e/1FAIpQLSf1ZzOoMllQlGFaQzSGWyv5VXUpKrUa8DRKp_XRNZCaBAQfsQ/viewanalytics">See response summary</a>
      </body>
    </html>
    """

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Send the message via local SMTP server.
    s = smtplib.SMTP('smtp.office365.com',587)
    s.ehlo()
    s.starttls()
    s.ehlo
    s.login(me, config['SENDER_PASSWD'])
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(me, recipients, msg.as_string())
    s.quit()