#!/usr/bin/env python3
"""
Created on 31.10.2019

@author: Florian Strahberger

Content: a starter for showing the values for the CCS-installation stored in the Conf/test_configVars.py
& a button to run the setup & initial-tests / show-up tests

Context: The setuptest is made for automating the initial setup, so the following steps are covered:
 1. create database-tables for meta-db & 5 project-databases
 2. register a Super-User, the "User-Number-One" (will have mandatory administration permission everywhere in the CCS)
 3. insert the email-provider (we use sendgrid, else customizing is needed) & project-manager for slot1
 4. insert email-provider & project-manager for slot2, slot3, slot4 & slot5
 5. create a project and a wbs
 6. login and make some posts
 7. login and create a user-profile including the personality test

Requires to work:

Steps needed to be done before
 1. Installed an instance of the CCS, manually installed or via docker (your "$docker-compose up --build")
 2. a sendgrid-account with its API-Key at hand (application is working well with FREE accounts)
 3. In the Conf/test_configVars.py the correct values - from the IP, the sendgrid-Key, the admin's name, email,
  password, public pgp key for that email, project-Numbers.
  below is a list for the needed values:

 The following variables need to be set prior running the setup: (number is test_ini_1 to 4)
    ccsIP				        1,2,3,4
    sendgridAPIkey			    3,4
    usrNumberOneName		    2,4
    usrNumberOnePW			    2,4
    usrNumberOneEmail		    2,3,4
    usrNumberOnesPublicPGPkey	2,3,4
    firstProjectNumber		    3,4
    secondProjectNumber		    4
    thirdProjectNumber		    4
    fourthProjectNumber		    4
    fifthProjectNumber		    4
"""
import starterclass

starterclass.startclass()

