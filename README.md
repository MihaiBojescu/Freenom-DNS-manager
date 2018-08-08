# Freenom DNS manager
A _hacky_ (as in not using the API, but the website itself) Freenom DNS manager written in Python 3 using
* requests for login, domain page content getter, removing address records and adding address records
* HTMLParser for parsing the domain pages

## Usage
Use freenom-dns-manager with the following args:
* `username=<your e-mail>` to specify the username
* `password=<your password>` to specify the password
* `workDomain=<working domain>` _(Optional, leaving this blank or not writing this will result in **all** domains being managed by this script)_
* `+add` to tell the script to add your current public IP to the address record list
* `+remove` to tell the script to remove all old address records
* `+cron` to tell the script to run an internal cron job. It manages the DNS records **only if** the IP changes
* `time=<number of seconds>` to tell the script to run at `<number of seconds>` seconds. Only useful when used with `+cron`. Default: 100
* `timeout=<number of seconds>` to set the timeout for requests to `<number of seconds>` seconds.

Leaving username or password blank will result in the script asking these values.

## Usage examples
`$ freenom-dns-manager username=foo@bar.org password=foobar workDomain=foobar.tk +add +remove`<br>
Manages domain foobar.tk using username foo@bar.org, with password foobar, removes old records, adds current public IP address to the address records list.

`$ freenom-dns-manager username=foo@bar.org +add`<br>
Manages **all** domains for user foo@bar.org, will prompt for password, and adds current public IP address to **all** domains.

`$ freenom-dns-manager workDomain=foobar.tk +remove`<br>
Manages domain foobar.tk, will prompt for username and password, will remove **all** address records for the specified domain

`$ freenom-dns-manager workDomain=foobar.tk +cron time=1000`<br>
Manages domain foobar.tk, will prompt for username and password, will remove **all** address records and add current IP address for the specified domain. Runs at 1000 seconds, and only if the IP address has changed.
