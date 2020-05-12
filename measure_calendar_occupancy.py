#!/usr/bin/env python
"""
Measure the level of occupancy of your calendar.

Usage:
  measure_calendar_occupancy.py
  measure_calendar_occupancy.py -h | --help
  measure_calendar_occupancy.py -v | --version
  measure_calendar_occupancy.py -u=USER -d=DOMAIN
  measure_calendar_occupancy.py -u=USER --d=DOMAIN --e=EMAIL

Options:
  -h --help                    Show this screen.
  -v --version                 Show version.
  -u --user=USER               Username to login to Exchange
  -d --server_domain=DOMAIN    Domain for the server.
  -e --email=EMAIL             Email of the Username [default: USER+"@"+DOMAIN]
  --ad_domain=AD_DOMAIN        AD domain [default="ad"]
  --delegate=DELEGATE          Username for which you will be a DELEGATE [default: USER]
  --server=SERVER              Server to log in to. [default="exchange."+DOMAIN]
  --start_date=DATE            Date for which to do the profile [default: datetime.date.now()]
  --weeks=WEEKS                Number of weeks for which to do the profile [default: 1]
"""

import os
from exchangelib import Credentials, Configuration, Account, DELEGATE, EWSDateTime
import datetime as dt
from astropy import units as u
import functools 
import yaml
import keyring # requires having used keyring.set_password(pwdkey, user, the_password)

ewsfile = os.environ["HOME"]+"/.ewscfg.yaml"

with open(ewsfile) as f:
    cfg_data = yaml.load(f, Loader=yaml.FullLoader)
    
email  = cfg_data['EWS_EMAIL']
user   = cfg_data['EWS_USER']
server = cfg_data['EWS_SERVER']
pwdkey = cfg_data['EWS_PWDKEY']
pwd    = keyring.get_password(pwdkey, user)

creds = Credentials(username=user, password=pwd)
config = Configuration(server=server, credentials=creds)
account = Account(
    primary_smtp_address=email, config=config, autodiscover=False, access_type=DELEGATE
)


# Getting data for each week
delta = dt.timedelta(days=7)
date_range_start = dt.datetime(2019,12,30)-0*delta
num_weeks = 20


def reduce_sum(items):
    return functools.reduce(lambda x,y:x+y, items)

occupation_per_week = {}

start_date = date_range_start
for week in range(0,num_weeks):
    end_date   = start_date + delta

    ews_start = account.default_timezone.localize(
        EWSDateTime(start_date.year, start_date.month, start_date.day)
    )
    ews_end   = account.default_timezone.localize(
        EWSDateTime(end_date.year, end_date.month, end_date.day)
    )
    
    # Get calendar entries for the week
    calendar_entries = account.calendar.filter(
        start__range=(ews_start, ews_end),
        categories__exists=False
    )
    # Get only durations
    entries = calendar_entries.values_list("subject", "duration")
    # Decode durations by converting into
    durations = [x[0][1:].lower() for x in durations]
    durations = ["day ".join(z) for z in [x.split("d") for x in durations]]
    durations = ["".join(z) for z in [x.split("t") for x in durations]]
    durations = ["hour ".join(z) for z in [x.split("h") for x in durations]]
    durations = [x+"in" if x[-1]=="m" else x for x in durations]
    
    duration_tuples = [x.split(" ") for x in durations]
    durations_in_secs = [
        [u.Unit(item).to(u.s) for item in duration_tuple if len(item)>0]
            for duration_tuple in duration_tuples
    ]
    reduced_duration_in_secs = [
        reduce_sum(items)
        for items in durations_in_secs
    ]
    
    meetings_duration_in_secs = sum(reduced_duration_in_secs)
    
    fraction = float((meetings_duration_in_secs*u.s/(30*u.hour)).to(1))
    
    occupation_per_week[start_date] = fraction
    start_date = end_date
