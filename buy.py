import time as time1
import sys, webbrowser, re
import requests
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
from pyjarowinkler import distance
import datetime
import multiprocessing
time = datetime.datetime.now

fakeUserAgentHeader = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}  #http://www.useragentstring.com/pages/useragentstring.php
mainUrl = "https://www.supremenewyork.com/shop/all"
baseUrl = "http://supremenewyork.com"
checkoutUrl = "https://www.supremenewyork.com/checkout"
unicode_num_dict = {'0': u'\ue01a', '1': u'\ue01b', '2': u'\ue01c', '3': u'\ue01d', '4': u'\ue01e', '5': u'\ue01f', 
            '6': u'\ue020', '7': u'\ue021', '8': u'\ue022', '9': u'\ue023'}


def main(product_type_list):
    r = requests.get(mainUrl, headers = fakeUserAgentHeader).text
    for product_type in product_type_list:
        if product_type in r: # Add Selected Product-Type To Cart
            print('-----')
            print('PRODUCT-TYPE | Product-Type Identified. Checking Product-Type Page: {}'.format(product_type))
            parse(r, mainUrl, 'product_type', product_type)
            print('PRODUCT-TYPE | Parse Complete: {}'.format(product_type))
            print('-----')
        else:
            print('-----\nProduct-Type not found: {}\n-----'.format(product_type))
    checkout(checkoutUrl)
    browser.delete_all_cookies() # Delete all cookies

def checkout(courl):
    print('CHECKOUT | Initiating Checkout. Current Time: {}'.format(time()))
    browser.get(courl)
    try:
        name_input_path = "//input[@id='order_billing_name']"
        text_input_field = browser.find_element_by_xpath(name_input_path)
        text_input_field.send_keys(fullName)
        print('SUCCESS | Added Name.')
    except:
        print('ERROR | Checkout Error. Cannot find Name field.')
    try:    
        email_input_path = "//input[@id='order_email']"
        text_input_field = browser.find_element_by_xpath(email_input_path)
        text_input_field.send_keys(emailField)
        print('SUCCESS | Added Email.')
    except:
        print('ERROR | Checkout Error. Cannot find Email field.')
    try:
        tel_input_path = "//input[@id='order_tl']"
        text_input_field = browser.find_element_by_xpath(tel_input_path)
        browser.execute_script("arguments[0].value = {}".format(phoneField), text_input_field)
        while int(text_input_field.get_attribute('value')) != int(phoneField): # Loop until field is correct
            text_input_field.clear()
            browser.execute_script("arguments[0].value = {}".format(phoneField), text_input_field)
        print('SUCCESS | Added Telephone.')
    except Exception, e:
        print('ERROR | Checkout Error. Cannot find Telephone field.') 
        print e
    try:
        address_input_path = "//input[@name='order[billing_address]']"
        text_input_field = browser.find_element_by_xpath(address_input_path)
        text_input_field.send_keys(addressField)
        print('SUCCESS | Added Address.')
    except:
        print('ERROR | Checkout Error. Cannot find Address field.')
    try:
        zip_input_path = "//input[@id='order_billing_zip']"
        text_input_field = browser.find_element_by_xpath(zip_input_path)
        text_input_field.send_keys(zipField)
        print('SUCCESS | Added ZIP')
    except:
        print('ERROR | Checkout Error. Cannot find ZIP field.')
    try:
        city_input_path = "//input[@id='order_billing_city']"
        text_input_field = browser.find_element_by_xpath(city_input_path)
        text_input_field.send_keys(cityField)
        print('SUCCESS | Added City')
    except:
        print('ERROR | Checkout Error. Cannot find City field.') 
    # Note: Don't need to add country and state after adding zip code
    try:
        city_input_path = "//select[@id='credit_card_type']"
        text_input_field = browser.find_element_by_xpath(city_input_path)
        all_options = text_input_field.find_elements_by_tag_name("option")
        for option in all_options:
            temp_value = option.get_attribute("value")
            if temp_value == ccTypeField:
                option.click()
                print('SUCCESS | Added Credit Card Type')
    except Exception, e:
        print('ERROR | Checkout Error. Cannot fill Credit Card Type field.') 
        print(e)
    try:
        city_input_path = "//input[@id='cnb']"
        text_input_field = browser.find_element_by_xpath(city_input_path)
        browser.execute_script("arguments[0].value = {}".format(ccNumberField), text_input_field)
        while str(text_input_field.get_attribute('value')) != ccNumberField: # Loop until field is correct
            text_input_field.clear()
            browser.execute_script("arguments[0].value = {}".format(ccNumberField), text_input_field)
        print('SUCCESS | Added Credit Card Number')
    except Exception, e:
        print('ERROR | Checkout Error. Cannot find Credit Card Number field.') 
    try:
        city_input_path = "//select[@id='credit_card_year']"
        text_input_field = browser.find_element_by_xpath(city_input_path)
        all_options = text_input_field.find_elements_by_tag_name("option")
        for option in all_options:
            temp_value = option.get_attribute("value")
            if str(temp_value) == ccYearField:
                option.click()
                print('SUCCESS | Added Credit Card Exp Year')
    except Exception, e:
        print('ERROR | Checkout Error. Cannot fill Credit Card Exp. Year field.') 
        print(e)
    try:
        city_input_path = "//select[@id='credit_card_month']"
        text_input_field = browser.find_element_by_xpath(city_input_path)
        all_options = text_input_field.find_elements_by_tag_name("option")
        for option in all_options:
            temp_value = option.get_attribute("value")
            if str(temp_value) == ccMonthField:
                option.click()
                print('SUCCESS | Added Credit Card Type')
    except Exception, e:
        print('ERROR | Checkout Error. Cannot fill Credit Card Exp. Month field.') 
        print(e)
    try:
        city_input_path = "//input[@id='cvw']"
        text_input_field = browser.find_element_by_xpath(city_input_path)
        text_input_field.send_keys(ccCvcField)
        print('SUCCESS | Added CVW CVV')
    except Exception, e:
        print('ERROR | Checkout Error. Cannot find CVW CVV field: {}'.format(e))
        try:
            city_input_path = "//input[@id='vval']"
            text_input_field = browser.find_element_by_xpath(city_input_path)
            text_input_field.send_keys(ccCvcField)
            print('SUCCESS | Added VVAL CVV')
        except Exception, e:
            print('ERROR | Checkout Error. Cannot find VVAL CVV field: {}'.format(e))
    try:
        city_input_path = "//input[@name='order[terms]']"
        text_input_field = browser.find_element_by_xpath(city_input_path)
        text_input_field.click()
        print('SUCCESS | Filled Order Terms Checkbox')
    except Exception, e:
        print('ERROR | Checkout Error. Cannot fill Order Terms Field.')
        print e
    try:
        city_input_path = "//input[@value='process payment']"
        text_input_field = browser.find_element_by_xpath(city_input_path)
        text_input_field.click()
        print('SUCCESS | Clicked Process Payment button')
    except Exception, e:
        print('Checkout Error. Cannot click Process Payment button.')
        print e
    return

def checkProductLink(a, product_type):
    cartFull = (len(product_id_list) == 0) # Desired item list empty
    if cartFull: # backup if cartFull boolean is not identified in parseProductTypePage
        print '--\nCART-UPDATE | All requested items added to cart.\n--'
        return 0
    link = a['href']
    category_view_url_suffix = 'shop/all/{}'.format(product_type)
    if (not cartFull) and (product_type in link) and (category_view_url_suffix != link[-1 * len(category_view_url_suffix):]):
        # if (cart not full) and (product type in link) and (link is not a product type page link)
        print('--')
        print 'CART-UPDATE | {} items left to add to cart.'.format(len(product_id_list))
        print('INFO | Checking Link on Product-Type Page: {}'.format(link))
        checkproduct(link)
        print('--')
    return 1

def parseProductTypePage(r, url, product_type):
    # Parse a product type page. EG: http://www.supremenewyork.com/shop/all/skate
    soup = BeautifulSoup(r, "lxml")
    link_list = soup.find_all('a', href=True) # Search through all links on the page
    #pool = multiprocessing.Pool(3)
    #success = pool.map(checkProductLink, link_list)
    success = [checkProductLink(a, product_type) for a in link_list if (len(product_id_list) != 0)]
    print('SLEEP | Sleep before checkout')
    time1.sleep(.5)
    return 1

def parseAddToCartPage(r, url):
    # Parse a product page, with the option to add the item to the cart
    # EG: http://www.supremenewyork.com/shop/skate/h5yxk4q20/j93gthoeu
    soup = BeautifulSoup(r, "lxml") 
    try:
        prod_name = soup.find('h1', attrs={"itemprop": "name"}).text
        prod_name = re.sub(u'\xae', '', prod_name)
    except:
        prod_name = None
    try:
        prod_model = soup.find('p', attrs={"class": "style", "itemprop": "model"}).text
    except:
        prod_model = None
    prod_full = " -- ".join([prod_name, prod_model])
    prod_match_list = [distance.get_jaro_distance(prod_full, product_id, winkler=True, scaling=0.1) for product_id in product_id_list]
    max_match = max(prod_match_list)
    if (max_match >= .97):
        prod_list_index = prod_match_list.index(max(prod_match_list))
        prod_size = product_list[prod_list_index][2]
        del product_id_list[prod_list_index] # Remove item from search list
        print('INFO | Clicking Add-to-Cart Button. Product Name: {}. Product Model: {}. Match Distance: {}'.format(prod_name, prod_model, max_match))
        add_cart_button_path = "//input[@value='add to cart']"
        browser.get(url)
        try:
            size_input_path = "//select[@id='size']"
            text_input_field = browser.find_element_by_xpath(size_input_path)
            all_options = text_input_field.find_elements_by_tag_name("option")
            size_selected = False
            for option in all_options:
                temp_value = option.get_attribute("value")
                temp_text = option.text
                if temp_text == prod_size:
                    option.click()
                    print('SUCCESS | Added Size: {}'.format(temp_text))
                    size_selected = True
                    break
            if size_selected == False:
                raise Exception('SOLD-OUT | Item size sold out: {}'.format(prod_size))
            button = browser.find_element_by_xpath(add_cart_button_path)
            button.click()
            print('SUCCESS | Clicked Add-to-Cart button on {}, {}, {}'.format(prod_name, prod_model, prod_size))
        except Exception, e:
            print('SOLD-OUT | Item Sold Out: {}, {}, {}'.format(prod_name, prod_model, prod_size))
            print e
    else:
        print('INFO | Skipped Product. Product Name: {}. Product Model: {}. Match Distance: {}'.format(prod_name, prod_model, max_match))
    return 1
    
    
            

def parse(r, url, parse_type, product_type):
    if parse_type == 'product_type': # Check a single product-type's page
        parseProductTypePage(r, url, product_type)
    elif parse_type == 'add_to_cart': # Check add-to-cart page
        parseAddToCartPage(r, url)
    return 1



def checkproduct(l):
    prdurl = baseUrl + l
    r = requests.get(prdurl, headers = fakeUserAgentHeader).text
    parse(r, prdurl, 'add_to_cart', None)
    return 1



i = 0
if __name__ == '__main__':

    product_type_list = ['pants']
    product_list = [
                    ["Wool Trousers", "Burgundy", "34"]
#                    ["Cable Knit Cardigan", "Light Blue", "Large"]
#                    ["Shadow Plaid Wool Overcoat", "Gold", 'Large'],
#                    ["Supreme/Schott Shearling Bomber", "Black", 'Medium'],
                    ]
    product_id_list = []
    for product_name, product_model, prod_size in product_list:
        product_id = " -- ".join([product_name, product_model])
        product_id_list.append(product_id)
    mainUrl = mainUrl
    baseUrl = baseUrl
    checkoutUrl = checkoutUrl
    fullName = "BRANDON J FLANNERY"
    emailField = "brandonjflannery@gmail.com"
    phoneField = "8055513213"
    addressField = "2417 Prospect Street"
    zipField = "94704"
    cityField = 'Berkeley'
    stateField = "CA"
    ccTypeField = "visa"  # "master" "visa" "american_express"
    ccNumberField = "4833160140614014"  
    ccMonthField = "09"  # Randomly Generated Data (aka, this isn't mine)
    ccYearField = "2019"  # Randomly Generated Data (aka, this isn't mine)
    ccCvcField = "444"  # Randomly Generated Data (aka, this isn't mine)

    browser = Chrome()
    start_input = raw_input('SUPREME START-GATE | TYPE <ENTER> TO START PROCESS')
    st = time()
    print('PROCESS INITIATED | Supreme Auto Purchase. Start Time: {}'.format(st))
    while (True):
        main(product_type_list)
        break
    et = time()
    print('PROCESS COMPLETE | Done. Exit Time: {}. Total Time: {}'.format(et, et - st))


'''
NOTES

Bot detection: http://stackoverflow.com/questions/33174804/python-requests-getting-connection-aborted-badstatusline-error




'''
