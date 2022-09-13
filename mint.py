from selenium.webdriver import FirefoxOptions
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from datetime import datetime
import os, csv, sys, time, codecs

# User Variables 
CSV_PATH = os.path.join(sys.path[0], ('data_' + datetime.today().strftime('%Y-%m-%d_T%H-%M') + '.csv'))
PATH_FIREFOX = 'C:/Users/bonilhfe/AppData/Roaming/Mozilla/Firefox/'
PATH_GECKODRIVER = 'C:\\geckodriver.exe'
IMPLICIT_WAIT = 2.0 #seconds - time selenium will wait for EVERY information, until its found
BATCH_SIZE = 30 # This can't be higher than 20

def get_list():
    # Import seller list from csv file 
    l = []
    with open('list.csv', 'rb') as f:
        for line in f:
            if len(line) > 0: 
                l.append(line.rstrip().decode('utf-8'))
    return l

def start_driver():
    # Defining Firefox Driver Configs
    firefox_options = FirefoxOptions()
    firefox_options.add_argument('--log-level=3')
    firefox_options.add_argument('--user-data-dir={}'.format(PATH_FIREFOX))
    firefox_options.add_argument('--width=1600')
    firefox_options.add_argument('--height=900')    
    
    # Opening Firefox instance
    ser = Service(PATH_GECKODRIVER)
    driver = webdriver.Chrome(options=firefox_options, service = ser)
    driver.implicitly_wait(IMPLICIT_WAIT)
    
    driver.get('https://denali-website-na.aka.amazon.com/item-refresh')
    input('Logged In? Press enter to continue...\r\n')
    return driver
    
def main():

    skus = get_list()
    print(skus)

    driver = start_driver()
    driver.get('https://denali-website-na.aka.amazon.com/item-refresh')
    # input('Press enter after logging in... ')
    # els = driver.find_elements('css selector', '.css-ackcql')
    # try: el = els[0].find_element('tag name', 'input')
    # except: 
        # print('oops, cannot find element!')
        # exit()
    
    # diving in batches of 30
    batches = [skus[i:i+BATCH_SIZE] for i in range(0,len(skus),BATCH_SIZE)]
    for batch in batches:
        el = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class=' css-ackcql']/input"))
        )
        for sku in batch:
            el.send_keys(sku + ' ') # Writing sku code in the text field and adding a space to separate
        time.sleep(.3)
        driver.find_element('css selector', '.item-refresh__actions').click()
        time.sleep(1)    

if __name__ == '__main__': main()