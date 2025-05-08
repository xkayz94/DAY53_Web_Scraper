from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options

#BEUTIFUL SOUP

response = requests.get('https://appbrewery.github.io/Zillow-Clone/')
zillow_web_page = response.text

soup = BeautifulSoup(zillow_web_page, 'html.parser')

price_span = soup.find_all("span", class_="PropertyCardWrapper__StyledPriceLine")
all_prices = [price.getText()[:6] for price in price_span]

address_property = soup.find_all(name='address')
all_addresses = [" ".join(address.getText().replace("\n", "").split()) for address in address_property]


link_hrefs = soup.find_all(class_='StyledPropertyCardDataArea-anchor', href=True)
all_links = [link['href'] for link in link_hrefs]


#SELENIUM

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)

driver = webdriver.Chrome(options=chrome_options)

driver.get('https://docs.google.com/forms/d/e/1FAIpQLSeJqTZvLBZu8MJNBlL9jRM5gkGvee2hgZM1RUU1x9IzdbFEiQ/viewform?usp=header')
driver.maximize_window()

hoover_div = driver.find_elements(By.CLASS_NAME, value='ibnC6b-LpPrec-GfpNfc')

for element in range(len(all_prices)):
    property_div = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    property_div.send_keys(f'{all_addresses[element]}', Keys.ENTER)
    price_div = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_div.send_keys(f'{all_prices[element]}', Keys.ENTER)
    link_div = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_div.send_keys(f'{all_links[element]}', Keys.ENTER)
    time.sleep(1)
    confirm_btn = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span')
    confirm_btn.click()
    time.sleep(1)
    next_answer = driver.find_element(By.XPATH, value='/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    next_answer.click()

driver.quit()

