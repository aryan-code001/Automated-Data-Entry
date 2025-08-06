import time
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

response = requests.get("https://appbrewery.github.io/Zillow-Clone/")
response_data = response.text

soup = BeautifulSoup(response_data, "html.parser")

# Extract prices and clean strings properly:
price_elements = soup.findAll(name="span", class_="PropertyCardWrapper__StyledPriceLine")
price_list = []
for p in price_elements:
    # Extract only digits from price string (handle "$2,895+/mo 1 bd" etc.)
    price = re.findall(r'\$\d[\d,]*', p.text)
    price_list.append(price[0] if price else "N/A")

# Extract addresses
address_elements = soup.findAll("address")
address_list = [a.text.strip() for a in address_elements]

# Extract links
link_elements = soup.findAll("a", class_="StyledPropertyCardDataArea-anchor")
links_list = [l.get("href") for l in link_elements]

# Selenium setup
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driver.get("https://docs.google.com/forms/d/e/1FAIpQLSfpWyzqlwrCuzGFUK-l4ZDgFJbqgvq1xVirN42ftCAyPIBuvA/viewform?usp=header")

time.sleep(3)  # wait for form to load

for i in range(len(address_list)):
    # Find elements:
    address_ans = driver.find_element(By.XPATH,
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_ans = driver.find_element(By.XPATH,
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_ans = driver.find_element(By.XPATH,
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit = driver.find_element(By.XPATH,
        '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')

    # Fill form:
    address_ans.clear()
    address_ans.send_keys(address_list[i])
    price_ans.clear()
    price_ans.send_keys(price_list[i])
    link_ans.clear()
    link_ans.send_keys(links_list[i])

    time.sleep(1)
    submit.click()

    time.sleep(3)
    # Click "Submit another response"
    another_response = driver.find_element(By.LINK_TEXT, "Submit another response")
    another_response.click()

    time.sleep(2)

driver.quit()
