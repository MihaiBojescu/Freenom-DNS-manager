# Freenom DNS manager
A Freenom DNS manager written in Python.

## Usage
Use freenom-dns-manager with the following args:
* **username=**&lt;your e-mail&gt;
* **password=**&lt;your password&gt;
* **workDomain=**&lt;working domain&gt; _(Optional, leaving this blank or not writing this will result in **all** domains being managed by this script)_
* **+add** to tell the script to add your current public IP to the address record list
* **+remove** to tell the script to remove all old address records

Leaving username or password blank will result in the script asking these values.

## Usage examples
`$ freenom-dns-manager username=foo@bar.org password=foobar workDomain=foobar.tk +add +remove`<br>
Manages domain foobar.tk using username foo@bar.org, with password foobar, removes old records, adds current public IP address to the address records list.<br><br>
`$ freenom-dns-manager username=foo@bar.org +add`<br>
Manages **all** domains for user foo@bar.org, will prompt for password, and adds current public IP address to **all** domains.<br><br>
`$freenom-dns-manager workDomain=foobar.tk +remove`
Manages domain foobar.tk, will prompt for username and password, will remove **all** address records for the specified domain
