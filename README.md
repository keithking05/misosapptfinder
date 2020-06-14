# misosapptfinder

This script will find the soonest available appointment(s) for Driver's license/state ID transactions that must be done in person for each of the Michigan Secretary of State locations and save them into a csv file.

Essentailly what this script does is it iterates through the calendar website for each of the SOS offices, then scrapes the calendar object looking for active days, and then outputs that into a CSV file.

It requires the following python modules to be installed for it to work:
BeautifulSoup
selenium

This script uses the Firefox driver for selenium.  You could modify this to use a different driver if you wanted.

In order for the Firefox driver for selenium to work, you'll need to download geckodriver for your OS (https://github.com/mozilla/geckodriver/releases) and then it needs to be moved into a folder that is included in your PATH.
