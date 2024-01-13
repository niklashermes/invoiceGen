# Installation

## Dependencies
- inquirer
- requests
- vdirsyncer
- Khard version 0.18.0 or higher
- pdflatex
- s-nail

## Install commands
`pip install inquirer requests vdirsyncer khard`

## Setup LaTeX
sudo apt install texlive-latex-full s-nail

## Files

- working khard config at: `~/.config/khard/khard.conf`:
add the path to the business addressbook:
```
[addressbooks]
[[business]]
path = /path/to/invoiceGen/contacts/[addressbookid]`
```

- working vdirsyncer config at: `~/.config/vdirsyncer/config`
add the local and remote CardDAV locations:
```
[general]
status_path = "~/.vdirsyncer/status/"

[pair business_contacts]
a = "business_contacts_local"
b = "business_contacts_remote"

# You need to run `vdirsyncer discover` if new calendars/addressbooks are added
# on the server.

collections = ["from a", "from b"]

# Synchronize the "display name" property into a local file (~/.contacts/displayname).
metadata = ["business"]

conflict_resolution = "a wins"

[storage business_contacts_local]
type = "filesystem"
path = "~/path/to/invoiceGen/contacts/"
fileext = ".vcf"

[storage business_contacts_remote]
type = "carddav"
url = "https://example.com/remote.php/dav/addressbooks/users/[username]/[addressbookid]/"
# The password can also be fetched from the system password storage, netrc or a
# custom command. See http://vdirsyncer.pimutils.org/en/stable/keyring.html
```

- working `.netrc` config at \~ containing:
`machine [host-fqdn] login [username] password [password]`

- working `.mailrc` config at \~ containing:

```
account [accountname] {
    set v15-compat
    set from="[name] [surname] <[email@example.com]>"
    set mta=smtp://email%40example.com:[password]@smtp.example.com:[smtp-port (default 587)] smtp-use-starttls
}```
