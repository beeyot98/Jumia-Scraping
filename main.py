import os
import re
from time import sleep
from typing import List

import selenium
import xlsxwriter
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

#  constants
TRED_URL = "https://www.jumia.com.ng/"
urls = os.listdir("""sample_url""")
new_urls = []
for url in urls:
    new_url = TRED_URL + url
    new_urls.append(new_url)
DRIVER_PATH = os.getenv(
    'DRIVER_PATH',
    os.getcwd() + '\\chromedriver\\chromedriver.exe'
)

WAIT_TIME = int(os.getenv('WAIT_TIME', '2'))
cat_list = ['groceries','computing','automobile','sporting-goods','video-games','baby-products',
            'category-fashion-by-jumia','electronics','phones-tablets','home-office','health-beauty']

class Product():
    """Details of the product
    """

    def __init__(self, name: str, brand: str, category: str, price: str, link: str) \
            -> None:
        self.name = name
        self.brand = brand
        self.category = category
        self.price = price
        self.link = link

        pass

    def __str__(self) -> str:
        return 'Name: {}, Price: {}, Link: {}'.format(self.name, self.price, self.link)
    

class Surfer():
    """This is a surfer class
    """

    # preferences
    _options = Options()
    _options.headless = True  # initiates a headless browser

    # disables image to load pages faster since image is not needed
    _options.add_experimental_option(
        "prefs",
        {"profile.managed_default_content_settings.images": 2}
    )

    _service = Service(DRIVER_PATH)  # path to chrome webdriver

    def __init__(self) -> None:

        # confirms browser set up is fine
        self._launch_browser()
        self._close_browser()
        print('browser set up is fine')

        pass

    def _launch_browser(self) -> bool:
        """Launches browser and opens tred url
        """
        try:
            # launch chrome as browser
            self.browser = Chrome(options=self._options, service=self._service)

            self.browser.get(TRED_URL)  # opens base url
            #self._confirm_page_load()  # confirms page load
        except selenium.common.exceptions.WebDriverException:
            raise ConnectionError('Browser connectivity issue')

        return True

    def _close_browser(self) -> None:
        """Closes current browser section
        """

        self.browser.quit()

        pass
   
    
    def _filter(self):
        
        self._launch_browser()  # delay to load page
        
        sleep(WAIT_TIME)   # delay to load page
        
        results = self._get_product_details()
        
        self._writes_to_file(results)  # writes results

        self._close_browser()  # closes browser for session

        return results
    

    def _get_product_details(self): 
        product_details = []
        count = 1
        for url in new_urls:
            self.browser.get(url)
            #self._confirm_page_load()
            print("Now scraping:", url, count)
            try:
                product_name = self.browser.find_element(
                        By.XPATH,
                        "//h1[contains(@class,'-fs20 -pts -pbxs')]"
                    ).text
            except selenium.common.exceptions.NoSuchElementException:
                product_name = "Not Found"

            try:
                product_brand = self.browser.find_element(
                        By.XPATH,
                        "//div[contains(@class,'-pvxs')]/a[contains(@class,'_more')]"
                    ).text
            except selenium.common.exceptions.NoSuchElementException:
                product_brand = "Not Found"
            try:
                product_category = self.browser.find_elements(
                        By.XPATH,
                        "//a[contains(@class,'cbs')]"
                    )[1].text

            except selenium.common.exceptions.NoSuchElementException:
                product_category = "Not Found"
            except IndexError:
                product_category = "Not Found"
            try:
                product_price = self.browser.find_element(
                        By.XPATH,
                        "//span[contains(@class,'-b -ltr -tal -fs24')]").text
            except selenium.common.exceptions.NoSuchElementException:
                product_price = "Not Found"
            



            current_product = Product(
                    name=product_name, brand=product_brand,
                    category=product_category,price=product_price,
                    link=url
                )

            product_details.append(current_product)
            count += 1
        return product_details

    def _writes_to_file(self, results: List[Product]) -> None:
        """Writes all car details to a .xlsx file
        Args:
            results (List[Product]): A list of product object
        """

        workbook = xlsxwriter.Workbook('search_results3.xlsx')  # opens .xlsx
        sheet = workbook.add_worksheet()

        # writes header
        sheet.write("A1", "Names")
        sheet.write("B1", "Brand")
        sheet.write("C1", 'Category')
        sheet.write("D1", 'Price')
        sheet.write("E1", 'Link')

        # writes details
        for i, result in enumerate(results):
            sheet.write(i + 1, 0, result.name)
            sheet.write(i + 1, 1, result.brand)
            sheet.write(i + 1, 2, result.category)
            sheet.write(i + 1, 3, result.price)
            sheet.write(i + 1, 4, result.link)

        workbook.close()  # closes .xlsx

        pass
    
    
    def _confirm_page_load(self) -> None:
        """checks if page loaded
        """

        try:
            WebDriverWait(self.browser, WAIT_TIME).until(
                EC.presence_of_element_located((By.ID, 'logo'))
            )
        except selenium.common.exceptions.TimeoutException:
            self._close_browser()
            raise TimeoutError('Service is unavailable at the moment')
        except selenium.common.exceptions.WebDriverException:
            self._close_browser()
            raise ConnectionError('Browser connectivity issue')

        pass
    
def main():
    surf = Surfer()  # initiate CredSurfer

    # gets radius input



    # filter cars by radius and zip
    surf._filter()


if __name__ == "__main__":
    main()
    