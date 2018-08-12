from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
import time
import csv
from geolocation.main import GoogleMaps
from settings import city, radius, CHROME_PATH, url
import sys

if radius not in [1, 5, 10, 25, 50]:
    sys.exit('Invalid radius. Insert valid int: 1, 5, 10, 25, 50')
    

def parse_page(url):

    if CHROME_PATH != '' or None:
        driver = webdriver.Chrome(CHROME_PATH)
    else:
        driver = webdriver.Chrome()

    try:
        driver.get(url)
    except WebDriverException as e:
        print(str(e))
        driver.quit()

    #################################################
    ##### Perform Search / Navigate to Results Page
   
    # attempt to define results btn / 3x
    def get_results_btn():
        for i in range(2):
            try:
                show_all_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@class='posterior']"))
                )
                if show_all_btn != None:
                    return show_all_btn
                time.sleep(3)
            except Exception as e:
                print(str(e))
                driver.quit()
                
    try:
        input_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='addressInput']"))
        )
    except Exception as e:
        print(str(e))
        driver.quit()
        
    try:
        dropdown_select = driver.find_element_by_xpath(
            "//select[@id='radiusSelect']/option[contains(@value, '" \
                + str(radius) + "')]").click()
        input_field.send_keys(city)
        input_field.send_keys(Keys.ENTER)

        # assign btn but do not interact before scrolling to it
        show_all_btn = get_results_btn()
        # scroll to button - Do not click yet, let javascript change source
        show_all_btn.location_once_scrolled_into_view
        time.sleep(3)
        # re-assign button once scrolled down
        show_all_btn = get_results_btn()

        # avoid clicking / Send ENTER instead
        show_all_btn.send_keys(Keys.ENTER)
    except Exception as e:
        print(str(e))
        driver.quit()

    #################################################
    ### Get Restaurant Results html tags

    try:        
        tag_xpath = "//div[@class='module_result']"
        results_tags = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, tag_xpath))
        )
        results_tags = driver.find_elements_by_xpath(tag_xpath)

    except Exception as e:
        print('Error getting html tags:', str(e))
        driver.quit()

    #################################################    
    ### Parse Restaurants

    restaurants = []
    for tag in results_tags:
        restaurant = {}
        try:
            restaurant_tag = tag.find_element_by_xpath(
                ".//*[@class='grid_70_l']")
            name = tag.find_element_by_xpath(
                ".//p/a/strong").text
            address = tag.find_element_by_xpath(
                ".//p/a/following-sibling::span").text
        except NoSuchElementException as e:
            print('Error getting restaurant elems:', str(e))
            driver.quit()           

        try:
            phone_xpath = ".//p['intro_complementary']/span[strong[text()='Tlf:']]"
            phone = tag.find_element_by_xpath(phone_xpath).text
        except NoSuchElementException:
            phone = 'Unavailable'

        if phone is not 'Unavailable' and 'Tlf' in phone:
            # delete prefix
            phone = phone.split('lf: ')[1]


        ################################
        ### Get Geolocation
        coordinates = get_geolocation(address)
        coordinates_str = str(coordinates[0]) + ', ' + str(coordinates[1])
        #################################

        restaurant['name'] = name
        restaurant['address'] = address
        restaurant['phone'] = phone
        restaurant['gps_coordinates'] = coordinates_str

        restaurants.append(restaurant)

    driver.quit()
    return restaurants

def get_geolocation(address):

    google_maps = GoogleMaps(api_key='your_geocoding_api_key')
    location = google_maps.search(location=address)
    my_location = location.first()

    if my_location is not None:
        coordinates = (my_location.lat, my_location.lng)
        return coordinates
    else:
        return 'Not Found'


def export_to_csv(restaurants):
    
    filename = 'mcdonalds_' + city + '_' + str(radius) + 'kms.csv'

    keys = restaurants[0].keys()
    with open(filename, 'w', newline='') as f:
        dict_writer = csv.DictWriter(f, keys)
        dict_writer.writeheader()
        dict_writer.writerows(restaurants)

    print('Results stored in a CSV file:', filename)


def main():

    restaurants = parse_page(url)
    export_to_csv(restaurants)

    print('Found', len(restaurants) ,
        'McDonalds restaurants within', 
        str(radius), 'Kms of', city)


if __name__ == '__main__':
     main() 

