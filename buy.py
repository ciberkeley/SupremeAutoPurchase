import time as time1
import sys, webbrowser, re
import requests
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
from splinter import Browser
import datetime
time = datetime.datetime.now

product_type = 'jackets'
product = "supreme-hanes-tagless-tees"
mainUrl = "http://www.supremenewyork.com/shop/all"
baseUrl = "http://supremenewyork.com"
checkoutUrl = "https://www.supremenewyork.com/checkout"
selectOption = "Large"
namefield = "John Doe"
emailfield = "Test@example.com"
phonefield = "5555555555"
addressfield = "1600 Pennsylvania Avenue NW"
zipfield = "20500"
statefield = "DC"
cctypefield = "master"  # "master" "visa" "american_express"
ccnumfield = "5274576954806318"  # Randomly Generated Data (aka, this isn't mine)
ccmonthfield = "06"  # Randomly Generated Data (aka, this isn't mine)
ccyearfield = "2019"  # Randomly Generated Data (aka, this isn't mine)
cccvcfield = "800"  # Randomly Generated Data (aka, this isn't mine)


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
        text_input_field.send_keys('BRANDON J FLANNERY')
        print('SUCCESS | Added Name.')
    except:
        print('Checkout Error. Cannot find Name field.')
    try:    
        email_input_path = "//input[@id='order_email']"
        text_input_field = browser.find_element_by_xpath(email_input_path)
        text_input_field.send_keys('brandonjflannery@gmail.com')
        print('SUCCESS | Added Email.')
    except:
        print('Checkout Error. Cannot find Email field.')
    try:
        tel_input_path = "//input[@id='order_tl']"
        text_input_field = browser.find_element_by_xpath(tel_input_path)
        text_input_field.send_keys('805-551-3213')
        print('SUCCESS | Added Telephone.')
    except:
        print('Checkout Error. Cannot find Telephone field.') 
    try:
        address_input_path = "//input[@name='order[billing_address]']"
        text_input_field = browser.find_element_by_xpath(address_input_path)
        text_input_field.send_keys('2417 Prospect Street')
        print('SUCCESS | Added Address.')
    except:
        print('Checkout Error. Cannot find Address field.')
    try:
        zip_input_path = "//input[@id='order_billing_zip']"
        text_input_field = browser.find_element_by_xpath(zip_input_path)
        text_input_field.send_keys('94704')
        print('SUCCESS | Added ZIP')
    except:
        print('Checkout Error. Cannot find ZIP field.')
    try:
        city_input_path = "//input[@id='order_billing_city']"
        text_input_field = browser.find_element_by_xpath(city_input_path)
        text_input_field.send_keys('Berkeley')
        print('SUCCESS | Added City')
    except:
        print('Checkout Error. Cannot find City field.') 
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


def buyprd(u):
    browser = Browser('firefox')
    url = u
    browser.visit(url)
    # 10|10.5
    browser.find_option_by_text(selectOption).first.click()
    browser.find_by_name('commit').click()
    if browser.is_text_present('item'):
        print("Added to Cart")
    else:
        print("Error")
        return
    print("checking out")
    browser.visit(checkoutUrl)
    print("Filling Out Billing Info")
    browser.fill("order[billing_name]", namefield)
    browser.fill("order[email]", emailfield)
    browser.fill("order[tel]", phonefield)

    print("Filling Out Address")
    browser.fill("order[billing_address]", addressfield)
    browser.fill("order[billing_zip]", zipfield)
    browser.select("order[billing_state]", statefield)
    print("Filling Out Credit Card Info")

    browser.select("credit_card[type]", cctypefield)
    browser.fill("credit_card[number]", ccnumfield)
    browser.select("credit_card[month]", ccmonthfield)
    browser.select("credit_card[year]", ccyearfield)
    browser.fill("credit_card[verification_value]", cccvcfield)
    browser.find_by_css('.terms').click()
    print("Submitting Info")
    browser.find_by_name('commit').click()
    sys.exit(0)


i = 0
if __name__ == '__main__':

    product_type = 'accessories'
    product = "supreme-hanes-tagless-tees"
    mainUrl = "http://www.supremenewyork.com/shop/all"
    baseUrl = "http://supremenewyork.com"
    checkoutUrl = "https://www.supremenewyork.com/checkout"
    selectOption = "Large"
    namefield = "John Doe"
    emailfield = "Test@example.com"
    phonefield = "5555555555"
    addressfield = "1600 Pennsylvania Avenue NW"
    zipfield = "20500"
    statefield = "DC"
    cctypefield = "master"  # "master" "visa" "american_express"
    ccnumfield = "5274576954806318"  # Randomly Generated Data (aka, this isn't mine)
    ccmonthfield = "06"  # Randomly Generated Data (aka, this isn't mine)
    ccyearfield = "2019"  # Randomly Generated Data (aka, this isn't mine)
    cccvcfield = "800"  # Randomly Generated Data (aka, this isn't mine)

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
