#  The python-based setuptest for the CYBR CSCW-SUITE (CCS) Version 0.9.6 
 (python3, selenium, pytest, ChromeDriver - you can get ChromeDriver from: https://chromedriver.chromium.org/)
 
## The setuptest will:
  * Open the Conf/test_configVars.py file, so you can modify the values (The IP of your CCS, the SendGrid API-Key, E-Mail-Address & publicPGP-Key ..)
  * Call the installation-script for creating the database-tables of your CCS
  * Make the automated setup for your first 5 projects
  * Will create a testing-project and simulate an admin who is creating a project, a WBS, creates a user-profile, testst the user's CFLX, starts to make a posting. 

You can call the skripts manually from your terminal / console/ bash/ shell/ as well. with the use of pytest: pytest filename.py