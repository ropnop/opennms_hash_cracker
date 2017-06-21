# OpenNMS Password Cracker
This script ingests a "users.xml" file from an OpenNMS installation and extracts the hashes and salts, then runs a standard dictionary attack against them.

The default hashing scheme for OpenNMS uses a 16byte salt and 100,000 iterations of SHA256.

There's a blogpost explaining the reasoning behind the tool and the steps taken in figuring out the hashes here:

https://TODO

## Example Usage
The OpenNMS source code has an example "users.xml" file [here](https://github.com/OpenNMS/opennms/blob/2b2ed9a50a88e9ce898842784ad3fcf2f6d1ae3f/features/springframework-security/src/test/resources/org/opennms/web/springframework/security/users.xml). This file is included in the repo as `test_users.xml`. A test wordlist with the known plaintexts is also included in `test_wordlist.txt`.

To use:

```
$ python opennms_crack.py
Usage: opennms_crack.py <users.xml file> <wordlist file>

$ python opennms_crack.py test_users.xml test_wordlist.txt
[+] Extracting Hashes...
[+] Extracted 4 user hashes
[+] Running crack with test_wordlist.txt...

[*] Cracked!	tempuser : mike
[*] Cracked!	admin : admin
[*] Cracked!	rtc : rtc

[*] ...done
```

Enjoy!
@ropnop
