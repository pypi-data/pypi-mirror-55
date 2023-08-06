#  The python-based setuptest for the CYBR CSCW-SUITE (CCS) Version 0.9.6 
 (python3, selenium, pytest, ChromeDriver - you can get ChromeDriver from: https://chromedriver.chromium.org/)
 
## The setuptest will:
  * Open the Conf/test_configVars.py file, so you can modify the values (The IP of your CCS, the SendGrid API-Key, E-Mail-Address & publicPGP-Key ..)
  * Call the installation-script for creating the database-tables of your CCS
  * Make the automated setup for your first 5 projects
  * Will create a testing-project and simulate an admin who is creating a project, a WBS, creates a user-profile, testst the user's CFLX, starts to make a posting. 

## Usage

	python3 ./Start/start.py

<1st page>
* The yellow [CONTINUE] button
will open the page displaying the actual setup-install values.

<2nd page>
* The yellow [SETUP] button will open the Conf/test_configVars.py file, so you can modify the values (The IP of your CCS, the SendGrid API-Key, E-Mail-Address & publicPGP-Key ..)

**make the changes, save & re-run with:**


	python3 ./Start/start.py

<2nd page>
* The red [INSTALL] button (bottom of 2nd page) will perform the installation with the values
 & perform a fully automated show-up-test showing and explaining you the basic functionalities
 for setting-up the projects as well as how to use the application.

**NOTE: this will use the first slot of your CCS and populate it with an example project!**

This means, your per default available projects for your productive work will be reduced to 4,
unless you decide to fully delete the database-tables of projectdb1 database - and rebuild the tables by calling:
https://[IP or domain]/1/zubringer/create8Tables.php

### manually start & select the setup, installation & testing-scripts
At first, you need to make the settings by modifying the Conf/test_configVars.py file with the text-editor of your choice (nano, gedit, touch, editor) - then you can call the scripts via pytest


#### You can call the skripts manually and only the selected one or ones from your terminal / console/ bash/ shell/ as well:
  *  for running all tests within the directory: pytest foldername/

eg for running all setups or running all tests:


    pytest RunSetups/
or:

    pytest Tests/


  *  for running a single test, cd to the test and type: pytest filename.py (see details below)

#### Setup-Scripts available:
**`cd RunSetups/`**


	pytest test_ini_1_createTables.py

	pytest test_ini_2_registerSuperadmin.py

	pytest test_ini_3_1stProjectSetup.py

	pytest test_ini_4_4ProjectsSetup.py

#### Walk-Through tests available (still in beta: will work, but might throw errors. Its a test-script issue then - not an application one!):
**`cd Tests/`**


	pytest test_loginCreateProjectCreateWBS.py

	pytest test_loginMakePosts.py 

	pytest test_loginPersProfileComplete.py
 

