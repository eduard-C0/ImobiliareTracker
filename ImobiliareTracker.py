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
    DIRECTORY
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
        print(f"Looking for{self.search_term}products...")
        print("....................LOAN.................")
        loan_links = self.get_loan_apartments_links()
        print(loan_links)
        print("....................TO BUY.................")
        buy_links = self.get_to_buy_links()
        print(buy_links)
        self.driver.quit()

    def get_all_the_links_to_sell(self):
        links = {'houses':[],'apartments':[],'spaces':[]}
        links['houses'].append(self.get_loan_houses_links())
        links['apartments'].append(self.get_loan_apartments_links())
        links['spaces'].append(self.get_loan_spaces_links())
        return links

    def get_all_the_links_to_buy(self):
        links = {'houses':[],'apartments':[],'spaces':[],'lands':[]}
        links['houses'].append(self.get_to_buy_houses_links())
        links['apartments'].append(self.get_to_buy_apartments_links())
        links['spaces'].append(self.get_to_buy_spaces_links())
        links['lands'].append(self.get_to_buy_lands_links())
        return links

    def get_loan_houses_links(self):
        self.driver.get(self.base_url)
        links = []
        links = self.driver.find_elements_by_xpath('//*[@id="inchiriere"]/ul/li[1]/ul/li/a')
        for elem in links:
            print(elem.get_attribute('href'))

        return links

    def get_loan_apartments_links(self):
        self.driver.get(self.base_url)

        elements = self.driver.find_elements_by_xpath('//*[@id="inchiriere"]/ul/li[2]/ul/li/a')

        for elem in elements:
            print(elem.get_attribute('href'))

        time.sleep(5)
        links = []

    def get_loan_spaces_links(self):
        self.driver.get(self.base_url)
        links = []
        links = self.driver.find_elements_by_xpath('//*[@id="inchiriere"]/ul/li[3]/ul/li/a')
        for elem in links:
            print(elem.get_attribute('href'))

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