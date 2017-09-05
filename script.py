#!/usr/bin/env python3
import os
import sys
import getpass
import requests
import warnings
from html.parser import HTMLParser

# URLs
LOGIN_URL = "https://my.freenom.com/dologin.php"
DOMAINS_PAGE_URL = "https://my.freenom.com/clientarea.php?action=domains"
MANAGE_DOMAIN_PAGE_URL = "https://my.freenom.com/clientarea.php?managedns=&domainid="
FREENOM_STUB_URL = "https://my.freenom.com/"

class domain:
    def __init__(self):
        self.domain = ""
        self.id = ""
        self.token = ""
        self.manageURL = ""
        self.deleteURLs = []

    def createManageURL(self):
        self.manageURL = MANAGE_DOMAIN_PAGE_URL.replace("managedns=", "managedns=" + self.domain).replace("domainid=", "domainid=" + self.id)

    def createDeleteURL(self, url):
        self.deleteURLs.append(FREENOM_STUB_URL + url)

    def createToken(self, token):
        self.token = token

    def removeOldAddresses(self, session):
        for deleteURL in self.deleteURLs:
            session.get(deleteURL)

    def addCurrentAddress(self, IP, session):
        newRecord = {
            "token": self.token,
            "dnsaction": "add",
            "addrecord[0][name]": "home",
            "addrecord[0][type]": "A",
            "addrecord[0][ttl]": 14440,
            "addrecord[0][value]": IP
        }
        session.post(self.manageURL, data = newRecord)


class domainGetter(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.domainList = list()
        self.foundDomain = False
        self.foundDomainID = False

    def handle_starttag(self, tag, attr):
        if tag == 'td':
            for attribute in attr:
                if attribute[0] == "class" and attribute[1] == "second":
                    self.currentDomain = domain()
                    self.foundDomain = True

        elif tag == "a":
            for attribute in attr:
                if attribute[0] == "class" and attribute[1] == "smallBtn whiteBtn pullRight":
                    self.foundDomainID = True

                elif attribute[0] == "href" and self.foundDomainID == True:
                    self.currentDomain.id = attribute[1][39:]
                    self.currentDomain.createManageURL()
                    self.domainList.append(self.currentDomain)
                    self.foundDomainID = False


    def handle_data(self, data):
        if self.foundDomain == True:
            self.currentDomain.domain = data[:-1]
            self.foundDomain = False


    def getDomainList(self):
        return self.domainList

class domainDeleterLinkGetter(HTMLParser):
    def __init__(self, domain):
        HTMLParser.__init__(self)
        self.domain = domain

    def handle_starttag(self, tag, attr):
        if tag == "a":
            for attribute in attr:
                if attribute[0] == "href":
                    if attribute[1].find("&dnsaction=delete") != -1 and attribute[1].find("&records=A") != -1:
                        self.domain.createDeleteURL(attribute[1])

        elif tag == "input":
            foundToken = False
            for attribute in attr:
                if attribute[0] == "name" and attribute[1] == "token":
                    foundToken = True

                elif attribute[0] == "value" and foundToken == True:
                    self.domain.createToken(attribute[1])
                    foundToken = False

def readCredentials():
    credentials = {
        "username": input("Username: "),
        "password": getpass.getpass("Password: ")
    }
    return credentials

def getIP():
    return requests.get("https://api.ipify.org/").text

if __name__ == '__main__':
    if len(sys.argv) == 3:
        credentials = {
            "username": sys.argv[1],
            "password": sys.argv[2]
        }
        workDomain = ""
    elif len(sys.argv) == 4:
        credentials = {
            "username": sys.argv[1],
            "password": sys.argv[2]
        }
        workDomain = sys.argv[3]
    else:
        credentials = readCredentials()
        workDomain = ""

    warnings.simplefilter("ignore")
    session = requests.Session()
    session.verify = False

    IP = getIP()
    print("Public IP address: " + IP)

    session.post(LOGIN_URL, data = credentials)
    response = session.get(DOMAINS_PAGE_URL)
    domainParser = domainGetter()
    domainParser.feed(response.text)
    domainList = domainParser.getDomainList()

    domainParser = domainDeleterLinkGetter(domain)
    if workDomain != "":
        print(' '.join(("Working with domain", workDomain, "...")))
        for domain in domainList:
            if domain.domain == workDomain:
                domainParser = domainDeleterLinkGetter(domain)
                print("Getting delete URLs...")
                domainParser.feed(session.get(domain.manageURL, verify = False).text)
                print("Removing old address records...")
                domain.removeOldAddresses(session)
                print("Adding new address record...")
                domain.addCurrentAddress(IP, session)
                print("Done")
                sys.exit()
        print(''.join(("Working domain (", workDomain, ") not found.")))
    else:
        for domain in domainList:
            print(' '.join(("Working with domain", domain.domain, "...")))
            domainParser = domainDeleterLinkGetter(domain)
            print("Getting delete URLs...")
            domainParser.feed(session.get(domain.manageURL, verify = False).text)
            print("Removing old address records...")
            domain.removeOldAddresses(session)
            print("Adding new address record...")
            domain.addCurrentAddress(IP, session)
        print("Done")
