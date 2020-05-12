import os
from exchangelib import Credentials, Configuration, Account, DELEGATE, EWSDateTime
import datetime as dt

email  = os.environ['EWS_EMAIL']
user   = os.environ['EWS_USER']
server = os.environ['EWS_SERVER']
pwd    = os.environ['EWS_PWD']

creds = Credentials(username=user, password=pwd)
config = Configuration(server=server, credentials=creds)
account = Account(
    primary_smtp_address=email, config=config, autodiscover=False, access_type=DELEGATE
)


# Getting data for each week
year=2020
num_weeks = 25

year_start = dt.datetime(year,1,1)
delta = dt.timedelta(days=7)

