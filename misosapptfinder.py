import requests
import time
import csv
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import urllib.parse

# List of SOS locations
# This could be stripped down so it just has element 3 because that's all that gets used in this script
locations = [[3531591, 'Adrian - 1040 S Winter St. ', '', 'Adrian', ''] ,[3573803, 'Albion - 308 S Superior St.', '', 'Albion', ''] ,[3573805, 'Allegan - 430 Western Ave.', '', 'Allegan', ''] ,[3573808, 'Alma - 1586 Wright Ave.', '', 'Alma', ''] ,[3573809, 'Alpena - 2666 US Highway 23 S.', '', 'Alpena', ''] ,[3531665, 'Ann Arbor - 295 N Maple Rd.', '', 'Ann Arbor - North Maple Road', ''] ,[3573811, 'Atlanta - 12519 State St.', '', 'Atlanta', ''] ,[3573813, 'Bad Axe - 33 Patrick Dr.', '', 'Bad Axe', ''] ,[3573815, 'Baldwin - 5653 S M-37 ', '', 'Baldwin', ''] ,[3531695, 'Battle Creek - 5420 Beckley Road, Suite L ', '', 'Battle Creek', ''] ,[3531717, 'Bay City - 1007 N Euclid Ave.', '', 'Bay City', ''] ,[3573819, 'Bellaire - 4607 S, M-88', '', 'Bellaire', ''] ,[3573820, 'Belleville - 164 E. Columbia Ave.', '', 'Belleville', ''] ,[3573825, 'Benton Harbor - 1960 Mall Place', '', 'Benton Harbor', ''] ,[3573828, 'Bessemer - 206 E Mary St.', '', 'Bessemer', ''] ,[3573830, 'Big Rapids - 206 N Michigan Ave.', '', 'Big Rapids', ''] ,[3573834, 'Brownstown - 18412 Telegraph Rd.', '', 'Brownstown', ''] ,[3573837, 'Cadillac - 1911 N Mitchell St.', '', 'Cadillac', ''] ,[3531742, 'Canton - 8565 N Lilley Rd.', '', 'Canton', ''] ,[3573842, 'Caro - 150 Millwood St.', '', 'Caro', ''] ,[3573844, 'Charlevoix- 185 M-66 Highway', '', 'Charlevoix', ''] ,[3573847, 'Cheboygan - 300 Mill St Suite 10 ', '', 'Cheboygan', ''] ,[3573848, 'Chelsea - 1113 S Main St.', '', 'Chelsea', ''] ,[3531763, 'Chesterfield - 51305 Gratiot Ave.', '', 'Chesterfield', ''] ,[3573853, 'Clare - 121 Schoolcrest Ave.', '', 'Clare', ''] ,[3531113, 'Clarkston - 7090 Sashabaw Rd.', '', 'Clarkston', ''] ,[3531772, 'Clinton Township - 37015 S Gratiot Ave.', '', 'Clinton Township', ''] ,[3531803, 'Clio - 4256 W Vienna Rd.', '', 'Clio', ''] ,[3573857, 'Coldwater - 7 Vans Ave.', '', 'Coldwater', ''] ,[3531836, 'Davison - 300 N Main St.', '', 'Davison', ''] ,[3573858, 'Dearborn - 5094 Schaefer Rd.', '', 'Dearborn', ''] ,[3517017, 'Detroit - 14634 Mack Ave.', '', 'Detroit Mack Avenue', ''] ,[3573864, 'Detroit - 17500 Livernois Ave.', '', 'Detroit Livernois Avenue', ''] ,[3573866, 'Detroit - 20220 W 7 Mile Rd.', '', 'Detroit West Seven Mile Road', ''] ,[3573862, 'Detroit - 2835 Bagley', '', 'Detroit Bagley Street', ''] ,[3531892, 'Detroit - 3046 W Grand Blvd.', '', 'Detroit - West Grand Blvd.', ''] ,[3573868, 'Dowagiac - 601 N. Front St Suite C  ', '', 'Dowagiac', 'Branch located to temporary location until mid-August'] ,[3573871, 'East Tawas - 1712 N US 23', '', 'East Tawas', ''] ,[3531878, 'Eastpointe - 18809 E 9 Mile Rd.', '', 'Eastpointe', ''] ,[3573872, 'Escanaba - 305 Ludington St.', '', 'Escanaba', ''] ,[3573875, 'Flint - 408 S Saginaw St.', '', 'Flint South Saginaw Street', ''] ,[3531864, 'Flint - 5512 Fenton Rd # G ', '', 'Flint Fenton Rd', ''] ,[3573880, 'Fremont - 7159 W 48th Street ', '', 'Fremont', ''] ,[3573882, 'Gaylord - 931 S. Otsego Ave Ste 4 ', '', 'Gaylord', ''] ,[3573883, 'Gladwin - 675 E. Cedar Ave, Suite 1 ', '', 'Gladwin', ''] ,[3573886, 'Grand Haven - 1110 Robbins Road', '', 'Grand Haven', ''] ,[3573887, 'Grand Rapids - 1 Divsion Ave N.', '', 'Grand Rapids Division Avenue', ''] ,[3531832, 'Grand Rapids - 3472 Plainfield Ave NE', '', 'Grand Rapids - Plainfield Ave.', ''] ,[3531844, 'Grand Rapids - 3601 28th St SE ', '', 'Grand Rapids - 28th Street', ''] ,[3573891, 'Grayling - 2384 C I-75 Business Loop ', '', 'Grayling', ''] ,[3573895, 'Greenville - 701 S Greenville West Dr.', '', 'Greenville', ''] ,[3573900, 'Hamtramck - 9001 Joseph Campau St.', '', 'Hamtramck', ''] ,[3573904, 'Harrisville - 205 N State St.', '', 'Harrisville', ''] ,[3573909, 'Hart - 3740 W Polk Rd.', '', 'Hart', ''] ,[3573912, 'Hastings - 1611 S Hanover St.', '', 'Hastings', ''] ,[3573914, 'Hazel Park - 20809 Dequindre Rd.', '', 'Hazel Park', ''] ,[3573917, 'Highland - 672 N. Milford Rd.', '', 'Highland', ''] ,[3573919, 'Hillsdale - 59 E St Joe St.', '', 'Hillsdale', ''] ,[3531818, 'Holland - 587 E 8th St Ste 90', '', 'Holland', ''] ,[3573921, 'Honor - 10577 Main St.', '', 'Honor', ''] ,[3573923, 'Houghton - 902 Razorback Drive Suite 1', '', 'Houghton', ''] ,[3531802, 'Howell - 1448 Lawson Rd.', '', 'Howell', ''] ,[3531792, 'Hudsonville - 5211 Cherry Avenue Plaza ', '', 'Hudsonville', ''] ,[3573926, 'Inkster - 26603 Michigan Ave.', '', 'Inkster', ''] ,[3573928, 'Ionia - 603 W Adams St.', '', 'Ionia', ''] ,[3573929, 'Iron Mountain - 1044 S Stephenson Ave.', '', 'Iron Mountain', ''] ,[3573930, 'Iron River - 992 Lalley Road', '', 'Iron River', ''] ,[3531780, 'Jackson - 1184 Jackson Crossing', '', 'Jackson', ''] ,[3531770, 'Kalamazoo - 3298 Stadium Dr.', '', 'Kalamazoo', ''] ,[3573937, 'Kalkaska - 114 Northland Plaza Northland Plaza Suite F ', '', 'Kalkaska', ''] ,[3573943, 'L\'Anse - 115 N Front St.', '', 'L\'Anse', ''] ,[3573947, 'Lake City - 49 N Morey Rd.', '', 'Lake City', ''] ,[3531764, 'Lansing - 3315 E Michigan Ave.', '', 'Lansing - East Michigan Ave', ''] ,[3531752, 'Lansing - 8158 Executive Ct.', '', 'Lansing Executive Court', ''] ,[3531743, 'Lapeer - 301 W. Genesee St., Suite 1', '', 'Lapeer', ''] ,[3517016, 'Livonia - 17176 Farmington Rd.', '', 'Livonia', ''] ,[3573951, 'Ludington - 5902 W US Highway 10', '', 'Ludington', ''] ,[3573954, 'Manistee - 1638 US 31 South Hillsdale Plaza Suite 400', '', 'Manistee', ''] ,[3573957, 'Manistique - 300 Walnut St Rm 164', '', 'Manistique', ''] ,[3531730, 'Marquette - 1250 Wilson St.', '', 'Marquette', ''] ,[3573961, 'Mason - 806 Hogsback Rd. Suite A', '', 'Mason', ''] ,[3573964, 'Menominee - 1305 8th Ave.', '', 'Menominee', ''] ,[3573968, 'Midland - 1832 N Saginaw Rd.', '', 'Midland', ''] ,[3573971, 'Mio - 302 N Morenci Ave PO Box 298', '', 'Mio', ''] ,[3573973, 'Mohawk - 3616 US Hwy 41 PO Box 378 ', '', 'Mohawk', ''] ,[3531720, 'Monroe - 1107 S Telegraph Rd.', '', 'Monroe', ''] ,[3573983, 'Mt. Pleasant - 1245 N Mission St.', '', 'Mt Pleasant', ''] ,[3573986, 'Munising - 418 Mill St.', '', 'Munising', ''] ,[3531711, 'Muskegon - 1485 E Apple Ave.', '', 'Muskegon', ''] ,[3573992, 'Newberry - 504 W McMillan ', '', 'Newberry', ''] ,[3574000, 'Niles - 110 E Main St.', '', 'Niles', ''] ,[3531699, 'Novi - 31164 Beck Rd.', '', 'Novi', ''] ,[3531688, 'Oak Park - 13401 W 10 Mile Rd.', '', 'Oak Park', ''] ,[3574004, 'Ontonagon - 728 South 7th St.', '', 'Ontonagon', ''] ,[3574009, 'Owosso - 1720 E. Main St Suite #2 ', '', 'Owosso', ''] ,[3278277, 'Paw Paw - 32849 Red Arrow Highway ', '', 'Paw Paw', ''] ,[3574012, 'Petoskey - 1185 N US 31 Hwy ', '', 'Petoskey', ''] ,[3531675, 'Pontiac - 1270 Pontiac Rd.', '', 'Pontiac', ''] ,[3531659, 'Port Huron - 2887 Krafft Rd.', '', 'Port Huron', ''] ,[3531649, 'Portage - 603 Romence Rd.', '', 'Portage', ''] ,[3574016, 'Prudenville - 2565 S Gladwin Rd PO Box 169 ', '', 'Prudenville', ''] ,[3574018, 'Redford - 25700 Joy Rd.', '', 'Redford', ''] ,[3574021, 'Reed City - 21719 Howard St.', '', 'Reed City', ''] ,[3531641, 'Rochester Hills - 2250 Crooks Rd.', '', 'Rochester Hills', ''] ,[3574024, 'Rogers City - 246 N Bradley Hwy.', '', 'Rogers City', ''] ,[3574029, 'Romeo - 71130 Van Dyke, Bruce Township ', '', 'Romeo', ''] ,[3574031, 'Saginaw - 4212 Dixie Hwy.', '', 'Saginaw Dixie Highway', ''] ,[3531632, 'Saginaw - 4404 Bay Rd.', '', 'Saginaw Bay Rd', ''] ,[3574033, 'Sandusky - 277 E Sanilac Rd.', '', 'Sandusky', ''] ,[3574037, 'Sault Ste Marie - 2700 Davitt St.', '', 'Sault Ste Marie', ''] ,[3531092, 'Shelby Township - 50640 Schoenherr Rd.', '', 'Shelby Township', ''] ,[3531627, 'Southfield - 25263 Telegraph Rd.', '', 'Southfield', ''] ,[3574041, 'Sparta - 534 S State St.', '', 'Sparta', ''] ,[3574049, 'St Ignace - 395 N State St St Ignace, Mi 49781-1484', '', 'St. Ignace', '395 N State St St Ignace, Mi 49781-1484'] ,[3574045, 'St. Charles - 115 S Saginaw St.', '', 'St. Charles', ''] ,[3574052, 'St. Johns - 1041 S Us Highway 27 ', '', 'St. Johns', ''] ,[3574056, 'Standish - 529 S Main PO Box 10 ', '', 'Standish', ''] ,[3531620, 'Sterling Heights - 7917 19 Mile Rd.', '', 'Sterling Heights', ''] ,[3574058, 'Sturgis - 931 S Centerville Rd.', '', 'Sturgis', ''] ,[3574060, 'Suttons Bay - 100B Cedar St PO Box 236', '', 'Suttons Bay', ''] ,[3531605, 'Taylor - 21572 Ecorse Rd.', '', 'Taylor', ''] ,[3574064, 'Temperance - 7200 Lewis Ave.', '', 'Temperance', ''] ,[3531597, 'Traverse City - 1759 Barlow St.', '', 'Traverse City', ''] ,[3531588, 'Trenton - 3040 Van Horn Rd.', '', 'Trenton', ''] ,[3531580, 'Troy - 1111 E Long Lake Rd.', '', 'Troy', ''] ,[3531561, 'Warren - 11533 E 12 Mile Rd.', '', 'Warren', ''] ,[3574066, 'West Bloomfield - 4297 Orchard Lake Rd.', '', 'West Bloomfield', ''] ,[3574069, 'West Branch - 2394 West M-55 ', '', 'West Branch', ''] ,[3574073, 'Westland - 6090 N Wayne Rd.', '', 'Westland', ''] ,[3531538, 'Wyoming - 1056 Rogers Plz SW', '', 'Wyoming', ''] ,[3574078, 'Ypsilanti - 4675 Washtenaw Ave.', '', 'Ypsilanti', '']  ];

'''
Function to get the available dates for the specified location

    Inputs:
        driver      Expecting an initialized webdriver.
        location    Expecting a string with the location name to be queried.  This needs to match what the SOS website is expecting.

    Output:
        Returns an array in the following format:
            location,date1
            location,date2
            ...

    Notes:       
        - I passed the selenium driver to this to speed up the script because opening / closing the driver took multiple seconds.
        - The location text is expected to be the raw format including spaces.  
            I added the urlib.parse.quote function to format it properly for the URL request.
'''
def getDatesForLocation(driver,location):

    # Prints the location its processing
    print("Getting available dates for " + location)

    # Build URL
        # Type casts location to string
        # Parses location string so it is properly formatted for a URL.  E.g. converts a space to %20
    url = 'https://sosmakeanappointment.as.me/schedule.php?location=' + urllib.parse.quote(str(location))

    # Gets page content for URL
    driver.get(url)

    # Clicks on "BOOK AN APPOINTMENT IN ADVANCE"
    driver.find_element_by_xpath("/html/body/div[2]/form/div[3]/div[2]/div[1]/label[2]").click()

    # Clicks on "Driver's license/state ID transactions that must be done in person"
    driver.find_element_by_xpath("/html/body/div[2]/form/div[3]/div[2]/div[2]/div[4]/div[1]/div[2]").click()

    # Initialize counter
    counter=0   

    # Loops while counter is less than 10 essentially giving up to 10 retries before giving up
    while counter < 10:
        # Gets page content and parses it so it can be searched
        page = BeautifulSoup(driver.page_source,'html.parser')

        # Gets all table column (<td>) elements where it has activeday in the class
            # These are days there is one or more available appointments
        activedays = page.find_all('td',attrs={'class':'scheduleday activeday'})

        # If it found objects, break the loop.  If not, retry
        if( len(activedays)):
            break
        else:
            print("Retrying...")
            
            # Increment counter
            counter+=1

            # Wait 1 second before retrying
            time.sleep(1)
        
    # Initialize date array
    dates = []

    # Loop through the active days it found and append them to the dates array with the location
    for day in activedays:
        print(day['day'])
        dates.append([location,day['day']])

    return dates


# Initialize selenium webdriver
driver = webdriver.Firefox()

# Open file for output
with open('sos_available_dates.csv', 'w', newline='') as csvfile:

    # Initialize csv writer for output file
    writer = csv.writer(csvfile, delimiter=',')

    # Define headers to write to file
    csvheaders = ['Location','Date']

    # Write headers to file
    writer.writerow(csvheaders)

    # Loop through each location
    for location in locations:

        # Get the location name we need for the URL
        locationName = location[3]

        # Call function to get dates for location
        dates = getDatesForLocation(driver,locationName)

        # Loop through returned array and write available date to file
        for date in dates:
            writer.writerow(date)

# Close driver
driver.quit()
