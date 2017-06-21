#!/usr/bin/env python

import sys, os
from xml.dom.minidom import parse
from hashlib import sha256


def extractHashes(usersfile):
	usersDict = {} 
	with open(usersfile) as fp:
		dom = parse(fp)
	userElements = dom.getElementsByTagName("user")
	for userElement in userElements:
		username = userElement.getElementsByTagName('user-id')[0].firstChild.nodeValue
		passwordNode = userElement.getElementsByTagName('password')[0]
		hasSalt = passwordNode.getAttribute('salt') 
		passwordString = passwordNode.firstChild.nodeValue
		pSalt, pHash = getHexValues(passwordString, hasSalt)
		usersDict[username] = {"salt": pSalt, "hash": pHash}
	
	return usersDict

	
def getHexValues(passwordString, hasSalt=True):
	hexstring = passwordString.decode('base64').encode('hex') # i hate working with bytes
	if not hasSalt:
		return '', hexstring
	
	pSalt = hexstring[:32]
	pHash = hexstring[32:]
	return pSalt, pHash


def doBrute(usersDict, wordlistFile, iterations=100000):
	wordlist = open(wordlistFile,'r')

	for plaintext in wordlist:
		plaintext = plaintext.rstrip()
		for username in usersDict.keys():
			pHash = usersDict[username]['hash']
			pSalt = usersDict[username]['salt']
			if checkPassword(plaintext, pHash, pSalt, iterations):
				print "[*] Cracked!\t{} : {}".format(username, plaintext)

	wordlist.close()


def checkPassword(plaintext, pHash, pSalt, iterations=100000):
	testinput = pSalt.decode('hex')+plaintext
	for i in range(0,iterations):
		s = sha256(testinput)
		h = s.hexdigest()
		testinput = s.digest()	
	
	if h == pHash:
		return True
	else:
		return False


if __name__ == '__main__':
	if len(sys.argv) < 3:
		print "Usage: {} <users.xml file> <wordlist file>".format(sys.argv[0])
		sys.exit(1)
	
	usersFile = sys.argv[1]
	wordlistFile = sys.argv[2]

	if not (os.path.isfile(usersFile) and os.path.isfile(wordlistFile)):
		print "[!] Error reading files"
		sys.exit(1)

	print "[+] Extracting Hashes..."
	usersDict = extractHashes(usersFile)
	print "[+] Extracted {} user hashes".format(len(usersDict))
	print "[+] Running crack with {}...".format(wordlistFile)

	doBrute(usersDict, wordlistFile)
	print "\n[*] ...done"




