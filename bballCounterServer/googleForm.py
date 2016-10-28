__author__ = 'Matthew'
try:
    import requests
except ImportError:
    import pip
    pip.main(['install','requests'])
    import requests

try:
    import googleapiclient
except ImportError:
    import pip
    pip.main(['install','google-api-python-client'])
    import googleapiclient

import timestamp

import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from math import floor


class FormConstants:
    YES = 'Yes'
    NO = 'No'
    MAYBE = 'Probably'
    YES_LATE = 'Yes+-+Late'
    _GOOGLE_YES_LATE = 'Yes - Late'


def post(response):
    print "{0}: Posting {1} to Google Form".format(timestamp.timeStamp(), response)
    URL = 'https://docs.google.com/forms/d/e/1FAIpQLSf1ZzOoMllQlGFaQzSGWyv5VXUpKrUa8DRKp_XRNZCaBAQfsQ/formResponse?entry.164115360=Widget+Responder&entry.462227184={0}&submit=Submit'.format(response)
    r = requests.get(URL)
    print "{0}: Response code {1} from Google Form".format(timestamp.timeStamp(), r.status_code)



# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get():
    count = 0
    print "{0}: Getting data from Sheet".format(timestamp.timeStamp())
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1Ii89N4fBiEWBvzdAOjdS_4ECq7DLH40CK1DmGQIhguQ'
    rangeName = 'Form Responses!A2:C'
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            if len(row) > 2: #if all values are there
                if row[2].upper() == FormConstants.YES.upper() or row[2].upper() == FormConstants._GOOGLE_YES_LATE.upper():
                    count += 1
                elif row[2].upper() == FormConstants.MAYBE.upper():
                    count += .5
            # print('%s, %s' % (row[1], row[2]))
    print "{0}: Counted {1}".format(timestamp.timeStamp(), count)
    return int(floor(count))


if __name__ == '__main__':
    print "Expecting: {0}".format(get())
