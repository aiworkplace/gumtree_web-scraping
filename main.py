import undetected_chromedriver as uc
import gspread
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import csv

import time



# from xlwt import Workbook
# wb = Workbook()
# sheet1 = wb.add_sheet('Sheet 1')
# # sheet1.col(0).width = 7000
# header=['Car Name', 'Price', 'Year', 'Miles', 'Link', 'Image']
# for i in range(len(header)):
#     sheet1.write(0, i, header[i])
#     wb.save("Audi_gumtree.xls")



sa = gspread.service_account(filename="keys.json")
sh= sa.open("Gumtree")
wks = sh.worksheet("Audi")
header=[['Car Name', 'Price', 'Year', 'Miles', 'Link', 'Image']]
for i in range(len(header)):
    wks.update("A1",header)


if __name__ == '__main__':

    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir=C:/Users/winName/AppData/Local/Google/Chrome/User Data')
    options.add_argument('--profile-directory=Profile 12')

    browser = uc.Chrome(
        options=options,
    )

    browser.get('https://my.gumtree.com/login')

    time.sleep(2)
    browser.find_element(By.ID, 'email').send_keys('Enter Email')
    browser.find_element(By.ID,'fld-password').send_keys('Enter Password')
    time.sleep(1)
    browser.find_element(By.CSS_SELECTOR,"#login-form > div > form > fieldset > div.grid-col-12.space-mbs.space-mtm.g-recaptcha-container > button").click()

    time.sleep(2)
    browser.get("https://www.gumtree.com/cars")
    time.sleep(2)
    element=browser.find_element(By.CSS_SELECTOR, '#structured-search > div > div > div > div:nth-child(1) > div:nth-child(1) > div > select')
    drp=Select(element)
    drp.select_by_visible_text("Audi")
    time.sleep(1)
    browser.find_element(By.CSS_SELECTOR,"#structured-search > div > div > div > div:nth-child(2) > div.grid-col-m-6.btn-container.txt-right > button > span:nth-child(1)").click()

    # browser.get("https://www.gumtree.com/cars/uk/audi")

    time.sleep(4)
    count = 1
    while True:
        titles = browser.find_elements(By.XPATH, '//div[@class="listing-content"]/h2')
        prices = browser.find_elements(By.XPATH, '//div[@class="listing-price-posted-container "]/span/strong')
        years = browser.find_elements(By.XPATH, '//ul[@class="listing-attributes inline-list "]/li[1]/span[2]')
        miles = browser.find_elements(By.XPATH,'//ul[@class="listing-attributes inline-list "]/li[2]/span[2]')
        links = browser.find_elements(By.XPATH, '//article[@class="listing-maxi"]/a')
        images = browser.find_elements(By.XPATH, '//div[@class="listing-thumbnail"]/img')

        ######### Google Sheet
        try:
            wks.update(f"A{count+1}",[[titles[car].text,prices[car].text,years[car].text,miles[car].text.split(" ")[0],links[car].get_attribute('href'),images[car].get_attribute('src')] for car in range(len(titles))])
            next=browser.find_element(By.CSS_SELECTOR,"#srp-results > div.grid-row > div > ul > li.pagination-next > a > span")
            next.click()
            time.sleep(3)
            count+=30
        except:
            time.sleep(4)
            browser.quit()

        ########## xls
        # try:
        #     for car in range(len(titles)):
        #         miles_number, string_=miles[car].text.split(" ")
        #         data = [titles[car].text,prices[car].text,years[car].text,miles_number,links[car].get_attribute('href'),images[car].get_attribute('src')]
        #
        #         sheet1.write(car+count+1, 0, titles[car].text)
        #         sheet1.write(car+count+1, 1, prices[car].text)
        #         sheet1.write(car+count+1, 2, years[car].text)
        #         sheet1.write(car+count+1, 3, miles_number)
        #         sheet1.write(car+count+1, 4, links[car].get_attribute('href'))
        #         sheet1.write(car+count+1, 5, images[car].get_attribute('src'))
        #         wb.save("Audi_gumtree.xls")
        #
        #     next=browser.find_element(By.CSS_SELECTOR,"#srp-results > div.grid-row > div > ul > li.pagination-next > a > span")
        #     next.click()
        #     time.sleep(3)
        #     count += 30
        # except:
        #     # browser.find_element(By.CSS_SELECTOR,"#srp-results > div.grid-row > div > ul > li.pagination-next")
        #     time.sleep(10)
        #     browser.quit()
