import time as time1
import sys, webbrowser, re
import requests
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
from splinter import Browser
import datetime
time = datetime.datetime.now

mainUrl = "http://www.supremenewyork.com/shop/all"
baseUrl = "http://supremenewyork.com"
checkoutUrl = "https://www.supremenewyork.com/checkout"


def main(product_type):
    r = requests.get(mainUrl).text
    cartFull = False
    if product_type in r: # Add Selected Product-Type To Cart
        print('Product Identified. Checking Product-Type Page: {}'.format(product_type))
        parse(r, mainUrl, 'product_type')
        print('Parse Complete: {}'.format(product_type))
        cartFull = True
    else:
        print('Product not found: {}'.format(product_type))
    if cartFull:
        checkout(checkoutUrl)

def checkout(courl):
    browser.get(courl)
    try:
        name_input_path = "//input[@id='order_billing_name']"
        text_input_field = browser.find_element_by_xpath(name_input_path)
        text_input_field.send_keys(fullName)
        print('SUCCESS | Added Name.')
    except:
        print('Checkout Error. Cannot find Name field.')
    try:    
        email_input_path = "//input[@id='order_email']"
        text_input_field = browser.find_element_by_xpath(email_input_path)
        text_input_field.send_keys(emailField)
        print('SUCCESS | Added Email.')
    except:
        print('Checkout Error. Cannot find Email field.')
    try:
        tel_input_path = "//input[@id='order_tl']"
        text_input_field = browser.find_element_by_xpath(tel_input_path)
        text_input_field.send_keys(phoneField)
        print('SUCCESS | Added Telephone.')
    except:
        print('Checkout Error. Cannot find Telephone field.') 
    try:
        address_input_path = "//input[@name='order[billing_address]']"
        text_input_field = browser.find_element_by_xpath(address_input_path)
        text_input_field.send_keys(addressField)
        print('SUCCESS | Added Address.')
    except:
        print('Checkout Error. Cannot find Address field.')
    try:
        zip_input_path = "//input[@id='order_billing_zip']"
        text_input_field = browser.find_element_by_xpath(zip_input_path)
        text_input_field.send_keys(zipField)
        print('SUCCESS | Added ZIP')
    except:
        print('Checkout Error. Cannot find ZIP field.')
    try:
        city_input_path = "//input[@id='order_billing_city']"
        text_input_field = browser.find_element_by_xpath(city_input_path)
        text_input_field.send_keys(cityField)
        print('SUCCESS | Added City')
    except:
        print('Checkout Error. Cannot find City field.') 
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
        print('Checkout Error. Cannot fill Credit Card Type field.') 
        print(e)
    try:
        city_input_path = "//input[@id='cnb']"
        text_input_field = browser.find_element_by_xpath(city_input_path)
        text_input_field.send_keys(ccNumberField)
        print('SUCCESS | Added Credit Card Number')
    except:
        print('Checkout Error. Cannot find Credit Card Number field.') 
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
        print('Checkout Error. Cannot fill Credit Card Exp. Year field.') 
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
        print('Checkout Error. Cannot fill Credit Card Exp. Month field.') 
        print(e)
    try:
        city_input_path = "//input[@id='cvw']"
        text_input_field = browser.find_element_by_xpath(city_input_path)
        text_input_field.send_keys(ccCvcField)
        print('SUCCESS | Added CVW CVV')
    except Exception, e:
        print('Checkout Error. Cannot find CVW CVV field: {}'.format(e))
        try:
            city_input_path = "//input[@id='vval']"
            text_input_field = browser.find_element_by_xpath(city_input_path)
            text_input_field.send_keys(ccCvcField)
            print('SUCCESS | Added VVAL CVV')
        except Exception, e:
            print('Checkout Error. Cannot find VVAL CVV field: {}'.format(e))
    try:
        city_input_path = "//input[@name='order[terms]']"
        text_input_field = browser.find_element_by_xpath(city_input_path)
        text_input_field.click()
        print('SUCCESS | Filled Order Terms Checkbox')
    except Exception, e:
        print('Checkout Error. Cannot fill Order Terms Field.')
        print e
    #try:
    #    city_input_path = "//input[@value='process payment']"
    #    text_input_field = browser.find_element_by_xpath(city_input_path)
    #    text_input_field.click()
    #    print('SUCCESS | Clicked Process Payment button')
    #except Exception, e:
    #    print('Checkout Error. Cannot click Process Payment button.')
    #    print e
    return

def parse(r, url, parse_type):
    soup = BeautifulSoup(r, "lxml")
    add_to_cart_links = {}
    if parse_type == 'product_type': # Check a single product-type's page
        for a in soup.find_all('a', href=True):
            link = a['href']
            category_view_url_suffix = 'shop/all/{}'.format(product_type)
            if (product_type in link) and (category_view_url_suffix != link[-1 * len(category_view_url_suffix):]):
                print('Checking Link on Product-Type Page: {}'.format(link))
                checkproduct(link)
    elif parse_type == 'add_to_cart': # Check add-to-cart page
        print('Clicking Add-to-Cart Button. Page link: {}'.format(url))

        add_cart_button_path = "//input[@value='add to cart']"

        browser.get(url)
        try:
            button = browser.find_element_by_xpath(add_cart_button_path)
            button.click()
            print('Clicked Add-to-Cart button on {}'.format(url))
        except:
            print('Item Sold Out: {}'.format(url))



def checkproduct(l):
    prdurl = baseUrl + l
    print('Option to buy product here: {}'.format(prdurl))
    r = requests.get(prdurl).text
    parse(r, prdurl, 'add_to_cart')
    #buyprd(prdurl)



i = 0
if __name__ == '__main__':

    product_type = 'jackets'
    product = "supreme-hanes-tagless-tees"
    mainUrl = mainUrl
    baseUrl = baseUrl
    checkoutUrl = checkoutUrl
    selectOption = "Large"
    fullName = "BRANDON J FLANNERY"
    emailField = "brandonjflannery@gmail.com"
    phoneField = "5555555555"
    addressField = "2417 Prospect Street"
    zipField = "94704"
    cityField = 'Berkeley'
    stateField = "CA"
    ccTypeField = "american_express"  # "master" "visa" "american_express"
    ccNumberField = "55555555555555555"  # Randomly Generated Data (aka, this isn't mine)
    ccMonthField = "08"  # Randomly Generated Data (aka, this isn't mine)
    ccYearField = "2019"  # Randomly Generated Data (aka, this isn't mine)
    ccCvcField = "063"  # Randomly Generated Data (aka, this isn't mine)

    st = time()
    print('PROCESS INITIATED | Supreme Auto Purchase. Start Time: {}'.format(st))
    browser = Chrome()
    while (True):
        print("On try number " + str(i))
        main(product_type)
        i = i + 1
        time1.sleep(2)
        break
    print('Done. Total Time: {}'.format(time() - st))
