# library used
from bs4 import BeautifulSoup as soup
import urllib.request as url
import urllib.error as url_error
#import pandas as pd


link = ''

# mobile phone details
data_dictionary = {}


def create_dictionary():
    global data_dictionary
    data_dictionary = {
        'Store Name': [],
        'Additional Information': [],
        'Price': [],
        'Product Link': []
    }


create_dictionary()


# Generating product link
def generate_link(input_mobile):
    global link
    link = 'https://www.91mobiles.com/'+input_mobile.replace(' ','-').lower()+'-price-in-india'


# fetching and parsing
def fetch_and_parse():
    try:
        web_page = url.urlopen(link)
    except url_error.HTTPError:
        return False

    data = soup(web_page, 'lxml')
    return data


def scrap(data):
    read_data = data.find_all('table', {'class': 'table'})
    read_data = read_data[0].find_all('td')

    # sub_index to access all attributes of each entity
    # that is Store Name, Additional Information, Price and Product Link
    sub_index = 2

    for index in range(len(read_data) // 3):
        sub_index *= index

        data_dictionary['Store Name'].append(read_data[sub_index].text)
        data_dictionary['Additional Information'].append(read_data[sub_index + 1].text)
        data_dictionary['Price'].append(read_data[sub_index + 2].text)

        sub_index = 3

    # getting links
    link = data.find_all('div', {'class': 'goto_newstore'})

    if link:
        for l in link:
            v = l.find('span', {'class': "gotoBtn go_to_store target_link_external"})
            data_dictionary['Product Link'].append('https://www.91mobiles.com' + v['data-href-url'])

    # filling Empty Link value with None
        else:
            for l in range(len(data_dictionary['Store Name'])):
                data_dictionary['Product Link'].append(None)


    # creating dataframe using pandas
    # dataframe = pd.DataFrame(data_dictionary)
    #
    # print(dataframe[['Store Name','Additional Information', 'Price']])

    return data_dictionary

    data_dictionary.clear()

    create_dictionary()