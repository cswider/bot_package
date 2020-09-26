# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 ##:##:## 2020

@author: chris
"""

## Bot to buy Nvidia RTX 3080
from parameters import *

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

#%%function declartions
def check_stock():
    in_stock = False
    # check if in stock
    while not in_stock:
        try:
            element = browser.find_element_by_xpath("//div[@class='fulfillment-add-to-cart-button']//button[.='Add to Cart']")
            #element = browser.find_element_by_xpath("//div[@class='fulfillment-add-to-cart-button']//button[.='Sold Out']")
        except NoSuchElementException: 
            print("Sold Out")
            in_stock = False
            print("refreshing...")
            browser.refresh()
        except: 
            print("Generic error message.")
        else:
            print("In Stock")
            in_stock = True

def sign_in():
    #browser.get('https://www.bestbuy.com/identity/global/signin')
    fields = {'fld-e': email,
              'fld-p1': password
              }
    #Auto fill info
    for name, value in fields.items():
        elem = browser.find_element_by_id(name)
        elem.send_keys(value)
    
    sign_in = browser.find_element_by_class_name('cia-form__controls__submit')
    sign_in.click()

def fill_shipping_info():
    #browser.get('https://www.bestbuy.com/checkout/c/r/fulfillment')
    fields = {'consolidatedAddresses.ui_address_2.firstName': shipping_first_name,
          'consolidatedAddresses.ui_address_2.lastName': shipping_last_name,
          'consolidatedAddresses.ui_address_2.street': shipping_address,
          'consolidatedAddresses.ui_address_2.city': shipping_city,
          'consolidatedAddresses.ui_address_2.state': shipping_state,
          'consolidatedAddresses.ui_address_2.zipcode': shipping_zip,
          'user.phone': phone_number
          }
    #Auto fill info
    for name, value in fields.items():
        elem = browser.find_element_by_id(name)
        elem.send_keys(value)
    
    save_billing = browser.find_element_by_class_name('save-for-billing-address')
    save_billing.click()
    
    continue_button = browser.find_element_by_class_name('button--continue').click()

def fill_payment_info():
    #browser.get('https://www.bestbuy.com/checkout/c/r/payment')
    fields = {'optimized-cc-card-number': CC_number,
              'payment.billingAddress.firstName': billing_first_name,
              'payment.billingAddress.lastName': billing_last_name,
              'payment.billingAddress.street': billing_address,
              'payment.billingAddress.city': billing_city,
              'payment.billingAddress.state': billing_state,
              'payment.billingAddress.zipcode': billing_zip,
              }
    #Auto fill info
    for name, value in fields.items():
        elem = browser.find_element_by_id(name)
        elem.send_keys(value)

def place_order():
    place_order = browser.find_element_by_xpath("//span[.='Place Your Order']").click()

#%%
print("Opening Chrome")
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
browser = webdriver.Chrome(desired_capabilities=options.to_capabilities())
browser.implicitly_wait(5) # seconds

#%%
print("Going to product page")
browser.get(product_URL)
check_stock()

#%%
print("Adding to cart")
add_to_cart = browser.find_element_by_xpath("//div[@class='fulfillment-add-to-cart-button']//button[.='Add to Cart']")
add_to_cart.click()

#%%
print("Going to cart")
browser.get('https://www.bestbuy.com/cart/')
QTY = browser.find_element_by_id('item-quantity')
QTY.send_keys(QTY_to_buy)

print("Going to checkout")
checkout = browser.find_element_by_class_name('checkout-buttons__checkout')
checkout.click()

#%%
print("Signing in")
sign_in()

#%%
print("Filling out shipping info")
fill_shipping_info()

#%%
print("Filling out payment info")
fill_payment_info()

#%%
print("Placing order")
place_order()

