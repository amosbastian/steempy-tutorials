# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
account_sid = ''
auth_token = ''
number = '+'
client = Client(account_sid, auth_token)


# Send sms and return sid
def send_sms(to, body):
    message = client.messages.create(body=body, from_=number, to=to)
    return(message.sid)
