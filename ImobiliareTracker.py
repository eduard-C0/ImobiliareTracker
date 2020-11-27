import time
from selenium.common.exceptions import NoSuchElementException
import json
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from config import (
    get_web_driver_options,
    get_chrome_web_driver,
    set_ignore_certificate_error,
    set_browser_as_incognito,
    set_automation_as_head_less,
    NAME,
    CURRENCY,
    FILTERS,
    BASE_URL,
    DIRECTORY,
    NUMBEROFROOMS,
    TYPE,
    SERVICE
)


class GenerateReport:
    pass

class ImobiliareAPI:
    def __init__(self, search_term, filters, base_url, currency):
        self.base_url = base_url
        self.search_term = search_term
        options  = get_web_driver_options()
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        self.driver = get_chrome_web_driver(options)
        self.currency = currency

    def run(self):
        print("Starting Script....")
        print(f"Looking for {self.search_term}...")

        links = self.get_all_the_deals()
        print(f"The number of results: {len(links)}.")
        if not links:
            print("Stopped script!")
            return
        products = self.get_products_info(links)
        print(f"Got info about {len(products)} products...")
        self.driver.quit()

    def get_the_outputlinks(self):
        if SERVICE == 'loan':
            links = self.get_all_the_links_to_loan()
            output_links = links[NAME]
            for l in output_links:
                string = 'camere=' + str(NUMBEROFROOMS)
                if l.find(string) != -1:
                    return l
        else:
            links = self.get_all_the_links_to_buy()
            output_links = links[NAME]
            for l in output_links:
                string = 'camere=' + str(NUMBEROFROOMS)
                if l.find(string) != -1:
                    return l

    def get_id_of_product(self,link):
        return link[link.find('oferta/') + 7:]

    def get_single_product_info(self,link):
        ID = self.get_id_of_product(link)
        print(f"Product ID: {ID} - getting data...")
        self.driver.get(link)
        time.sleep(2)
        price = self.get_price()
        neighbourhood = self.get_neighbourhood()
        partitioning = self.get_partitioning()
        comfort_level = self.get_level_of_comfort()
        #usable_area = self.get_usable_area()
        city = self.get_city()
        if link and ID and price:
            product_info = {
                'url': link,
                'ID': ID,
                'city': city,
                'price':price,
                'neighbourhood':neighbourhood,
                'partitioning':partitioning,
                'comfort_level':comfort_level

            }
            print(product_info)
            return product_info

        return None
    def get_products_info(self,links):
        products = []
        for asin in links:
            product = self.get_single_product_info(asin)
            if product:
                products.append(product)
        return products

    def get_city(self):
        city = None
        try:
            city = self.driver.find_element_by_xpath('//*[@id="spec"]/ul/li[1]/b').text
        except NoSuchElementException as err:
            print(err)
        return city

    def get_price(self):
        price = None
        try:
            price = self.driver.find_element_by_id("MainContent_lblPrice").text
        except NoSuchElementException as err:
            print(err)
        return price

    def get_neighbourhood(self):
        neighbourhood = None
        try:
            neighbourhood = self.driver.find_element_by_xpath('//*[@id="spec"]/ul/li[2]/b').text
        except NoSuchElementException as err:
            print(err)
        return neighbourhood
    def get_partitioning(self):
        partitioning = None
        try:
            partitioning = self.driver.find_element_by_xpath('//*[@id="spec"]/ul/li[6]/b').text
        except NoSuchElementException as err:
            print(err)
        return partitioning
    def get_level_of_comfort(self):
        comfort = None
        try:
            comfort = self.driver.find_element_by_xpath('//*[@id="spec"]/ul/li[4]/b').text
        except NoSuchElementException as err:
            print(err)
        return comfort
    def get_usable_area(self):
        area = None
        try:
            area = self.driver.find_element_by_xpath('//*[@id="spec"]/ul/li[5]/b/text()').text
        except NoSuchElementException as err:
            print(err)
        return area

    def get_all_the_deals(self):
        link = self.get_the_outputlinks()
        self.driver.get(link)
        pages = self.driver.find_elements_by_class_name('pagerLink')
        links = []
        for p in range(1,len(pages)):
            objects = self.driver.find_elements_by_xpath('//*[@id="main"]/ul/li/div/a')
            for element in objects:
                links.append(element.get_attribute('href'))
            pages[p].click()
            pages = self.driver.find_elements_by_class_name('pagerLink')
        return links


    def get_all_the_links_to_loan(self):
        links = {'houses':[],'apartments':[],'spaces':[]}
        links['houses'] = self.get_loan_houses_links()
        links['apartments'] = self.get_loan_apartments_links()
        links['spaces'] = self.get_loan_spaces_links()
        return links

    def get_all_the_links_to_buy(self):
        links = {'houses':[],'apartments':[],'spaces':[],'lands':[]}
        links['houses'] = self.get_to_buy_houses_links()
        links['apartments'] = self.get_to_buy_apartments_links()
        links['spaces'] = self.get_to_buy_spaces_links()
        links['lands'] = self.get_to_buy_lands_links()
        return links

    def get_loan_houses_links(self):
        self.driver.get(self.base_url)
        links = []
        houses = self.driver.find_elements_by_xpath('//*[@id="inchiriere"]/ul/li[1]/ul/li/a')
        for elem in houses:
            links.append(elem.get_attribute('href'))

        return links

    def get_loan_apartments_links(self):
        self.driver.get(self.base_url)
        links = []
        apartments = self.driver.find_elements_by_xpath('//*[@id="inchiriere"]/ul/li[2]/ul/li/a')
        for elem in apartments:
            links.append(elem.get_attribute('href'))

        return links


    def get_loan_spaces_links(self):
        self.driver.get(self.base_url)
        links = []
        spaces = self.driver.find_elements_by_xpath('//*[@id="inchiriere"]/ul/li[3]/ul/li/a')
        for elem in spaces:
            links.append(elem.get_attribute('href'))
        return links

    def get_to_buy_houses_links(self):
        self.driver.get(self.base_url)
        links = []
        houses = self.driver.find_elements_by_xpath('//*[@id="vanzare"]/ul/li[1]/ul/li/a')
        for elem in houses:
            links.append(elem.get_attribute('href'))
        return links

    def get_to_buy_apartments_links(self):
        self.driver.get(self.base_url)
        links = []
        apartments = self.driver.find_elements_by_xpath('//*[@id="vanzare"]/ul/li[2]/ul/li/a')
        for elem in apartments:
            links.append(elem.get_attribute('href'))
        return links

    def get_to_buy_spaces_links(self):
        self.driver.get(self.base_url)
        links = []
        spaces = self.driver.find_elements_by_xpath('//*[@id="vanzare"]/ul/li[3]/ul/li/a')
        for elem in spaces:
            links.append(elem.get_attribute('href'))
        return links

    def get_to_buy_lands_links(self):
        self.driver.get(self.base_url)
        links = []
        lands = self.driver.find_elements_by_xpath('//*[@id="vanzare"]/ul/li[4]/ul/li/a')
        for elem in lands:
            links.append(elem.get_attribute('href'))
        return links


if __name__ == '__main__':
    imobiliare = ImobiliareAPI(NAME,FILTERS,BASE_URL,CURRENCY);
    imobiliare.run()