# measure_calendar_occupancy
This is a Python 3 script that connects to an Exchange account and calculates occupation fraction for the calendar.

It uses `exchangelib` to query an Exchange Web Services backend, and it gets the username, exchange server, and email from a `.ewscfg.yaml` file on the user's home directory.

Requires the following packages installed:
 * `exchangelib`
 * `pyyaml`
 * `astropy` for easier unit conversion; dependency will be removed in future releases

It also requires as a prerequisite that:
 1. A `.ewscfg.yaml` file is created at the users `HOME` path.
 2. Someone used `keyring.set_password(my_pwd_key, user, the_password)`, where: 
   `my_pwd_key` is the value that can be found on `.ewscfg.yaml` under the key `EWS_PWDKEY`; 
   `user` is the value that can be found under the key `EWS_USER`; 
   and `the_password` is the relevant Exchange password for that user.

# Usage
TBW
