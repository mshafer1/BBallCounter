import smtplib
import datetime

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import googleForm
import timestamp


def send_email(input):
    message = 'Looks like game on' if input > 8 else ('Need a few more to commit' if input >= 4 else 'Looks like no game today')
    # me == my email address
    # you == recipient's email address
    me = "matthew.shafer@ni.com"
    recipients = ['matthew.shafer@ni.com', 'mjshafer93@gmail.com']
    if len(recipients) == 0:
        raise Exception("Can't send to nobody")
    you = ', '.join(recipients)

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    when = '@ 4:30' if datetime.datetime.today().weekday() not in [4] else 'Saturday ({:%m/%d}) at 10:00'.format((tomorrow))
    msg['Subject'] = "Basketball {0} - ({1}) - {2}".format(when, input, message)
    msg['From'] = me
    msg['To'] = you

    # Create the body of the message (a plain-text and an HTML version).
    text = "Looks like about {0} people\n".format(input, message)
    html = """
    <html>
      <head></head>
      <body>
        <h1>Expecting: {0}</h1>
        <p>{1}</p>
        <a href="https://docs.google.com/forms/d/e/1FAIpQLSf1ZzOoMllQlGFaQzSGWyv5VXUpKrUa8DRKp_XRNZCaBAQfsQ/viewanalytics">See response summary</a>
      </body>
    </html>
    """.format(input, message)

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
    s.login(me, '2016Matt#')
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(me, recipients, msg.as_string())
    s.quit()


if __name__ == '__main__':
    count = googleForm.get()

    if count > 0:
        send_email(count)
    else:
        print '{0}: Not sending'.format(timestamp.time_stamp())

