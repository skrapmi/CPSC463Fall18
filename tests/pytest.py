#from app import createUser as testnewuser
import unittest 
import os
from selenium import webdriver

#testnewuser = app.createUser

#  Select your driver
#driver = webdriver.Chrome()
driver = webdriver.Firefox()
#driver = webdriver.Ie()

# Set driver timeout in secs
driver.set_page_load_timeout(15)

def databasetest(na,pa,passfail):
    a = 0
    b = 0
    check = ""
    if(passfail == "pass"):
        print("Unit test for new user ", na, " added to program")
    else:
        print("Unit test for existing user ", na, " not added to program")
    for file in os.listdir("."):
        if file.endswith(".db"):
            a += 1

    #testnewuser(na,pa)

    for file in os.listdir("."):
        if file.endswith(".db"):
            b += 1

    if a == b:
        check = "fail"
    else:
        check = "pass"
    if passfail == check:
        print("Unit test Pass")
    else:
        print("Unit test Fail")

#databasetest("testnewuser","testnewuser", "fail")
