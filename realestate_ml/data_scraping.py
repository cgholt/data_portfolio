from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

DELAY = 0.25
PATH = 'C:\\Users\\corey\\Desktop\\MachineLearning\\realestateData\\data\\houston_houses.csv'

CITIES = ['Houston','Sugar Land','Spring','Katy','Kingwood','Stafford','Conroe','Texas City','Cypress','The Woodlands','Webster',
 'League City','Bellaire','Missouri City','Friendswood','Humble','Richmond','Pasadena','Baytown','Tomball','Galveston',
 'Angleton','Pearland','Seabrook','Lake Jackson','Channelview','New Caney','Manvel','South Houston','Magnolia','Kemah',
 'Rosenberg','Alvin','Hempstead','Dickinson','Fulshear','New Ulm','Wallisville','Hunters Creek Village','Brookshire','Sweeny',
 'Hardin','Hankamer','Danbury','Needville','Simonton','Gilchrist','High Island','Raywood','Piney Point Village','Orchard',
 'North Houston','Anahuac','Romayor','Huffman','Cat Spring','Bellville','Dobbin','Damon','Highlands','Bacliff','San Felipe',
 'Winnie','Kendleton','Guy','Galena Park','Danciger','Pinehurst','Liberty','Stowell','Daisetta','Industry','Mont Belvieu',
 'Bleiblerville','Old Ocean','Clear Lake Shores','Santa Fe','Bunker Hill Village','Porter','Liverpool','La Porte','Brazoria',
 'Prairie View','Willis','Cleveland','Clute','Port Bolivar','Rosharon','Dayton','Crosby','Montgomery','Deer Park','Freeport',
 'Sealy','Fresno','Alief','Hitchcock','West Columbia','La Marque','Beasley','Wallis','Splendora','Devers','Hull','Hufsmith',
 'Pattison','Thompsons','Oak Ridge North','Rye','West University Place','Kenney','Hockley','Barker','Waller']
TEST_CITIES = ['Thompsons','Oak Ridge North']

with requests.session() as s:
    url = ''
    url_list = []
    
    #Loop through cities to make a list of URLs
    for city in CITIES:
        city_str = city.replace(' ', '').lower()
        page = 1
        url = 'https://www.har.com/' + city_str + '/realestate/for_sale'
        request = s.get(url)
        soup = BeautifulSoup(request.content, 'html.parser')
        end_page = int(soup.find(class_='act_total').text.strip().replace(',','')) // 100 + 1
        
        # If there's more than one page, add pagination to the URL
        if end_page == 1:
            url_list.append(url)
        else:
            while page <= end_page:
                url = 'https://www.har.com/' + city_str + '/realestate/for_sale' + f'?page={page}'
                url_list.append(url)
                page += 1

    # For each URL, make a get request
    request = ''
    request_list = []
    
    for url in url_list:
        time.sleep(DELAY)
        request = s.get(url)
        request_list.append(request)

# Creat a list of beautifulSoup strings        
soup = ''
soup_list = []

for request in request_list:
    soup = BeautifulSoup(request.content, 'html.parser')
    soup_list.append(soup)

def getHouseInfo(home):
    """
    input: html class containing the housing information
    output: key/value pair address: [home information]
    """
    address_raw = home.find(class_='cardv2--landscape__content__body__details_address_left_add').text.strip()
    address = " ".join(address_raw.split())
    details_raw = home.find_all(class_='cardv2--landscape__content__body__details_features_item')
    details = [detail.text.strip() for detail in details_raw]
    price = home.find(class_="cardv2--landscape__content__body__details_price").text.strip()
    
    return address, details, price

def mysplit(s):
    """
    input: String containing home details
    output: Details separated by leading numbers and trailing letters
    """
    nums = s.rstrip('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz. ')
    letters = s[len(nums):]
    return nums.strip(), letters.strip()

def getDataFromSoup(soup):
    """
    input: list of BSoup strings
    output: list of (address, details) tuples
    """
    data = []
    all_homes = soup.find_all(class_='col-12 pt-3 pt-md-0')
    
    for home in all_homes:
        data.append(getHouseInfo(home))
    return data

def getListOfHomes(soup_list):
    home_data = []
    for s in soup_list:
        home_data += getDataFromSoup(s)
    return home_data

def createDataDict(data):
    """
    input: list containing (address, [details list])
    output: data formatted in dictionary
    """
    home_dict = {}
    
    for home in data:
        if home[0] not in home_dict:
            home_dict[home[0]] = {'bedrooms': 0, 
                                  'Sqft.': 0, 
                                  'lot Sqft.': 0,
                                  'full baths': 0,
                                  'half baths': 0,
                                  'stories': 0,
                                  'year built': None,
                                  'Private Pool': False,
                                  'Acres': None,
                                  'zip': home[0][-5:].strip() if home[0][-5] != '-' else home[0][-10:-5].strip(),
                                  'price': float(home[2].replace(',', '').replace('$', ''))}

            details_raw = home[1]

            for d in details_raw:
                value, key = mysplit(d)
                if key == 'half baths':
                    home_dict[home[0]]['half baths'] = int(value[-1])
                    home_dict[home[0]]['full baths'] = int(value[0])
                elif key == 'Private Pool':
                    home_dict[home[0]]['Private Pool'] = True
                elif key == 'story':
                    home_dict[home[0]]['stories'] = float(value)
                elif key =='Acres':
                    home_dict[home[0]]['Acres'] = float(value.replace(',', ''))
                else:
                    home_dict[home[0]][key] = float(value.replace(',', ''))
    
    return home_dict

def coordFromAddress(address):
    """
    input: Dictionary containing home data where the keys
           are the addresses
    output: tuple containing lat and long coordinates
    """

    with requests.session() as s:
        url = "https://eec19846-geocoder-us-census-bureau-v1.p.rapidapi.com/locations/onelineaddress"

        querystring = {"benchmark":"Public_AR_Current","address": address,"format":"json"}

        headers = {
            # Don't push key to git
            "X-RapidAPI-Key": "6262cbd686msh73cbc177a03db54p12cbc2jsn9a294af6563b",
            "X-RapidAPI-Host": "eec19846-geocoder-us-census-bureau-v1.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        response_dict = {}
        response_dict = response.json()

        # Return None if the api doesn't match the address
        if response_dict == {}:
            return (None, None)
        if response_dict['result']['addressMatches'] == []:
            return (None, None)

        coord = response_dict['result']['addressMatches'][0]['coordinates']
        return (float(coord['x']), float(coord['y']))

home_data = getListOfHomes(soup_list)
data_dict = createDataDict(home_data)

add_list = list(data_dict.keys())
for address in add_list:
    coordinates = coordFromAddress(address)
    data_dict[address]['long'] = coordinates[0]
    data_dict[address]['lat'] = coordinates[1]

home_df = pd.DataFrame.from_dict(data_dict, orient='index')

home_df.to_csv(PATH)
#print(home_df.head())
