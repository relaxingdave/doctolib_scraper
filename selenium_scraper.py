import time
# Selenium Wire extends Selenium’s Python bindings to give you access
# to the underlying requests made by the browser.
from seleniumwire import webdriver

# in order to always select the proper webdriver
from webdriver_manager.chrome import ChromeDriverManager


# To do:
# clean up: write a function for getting the json url
# use the chromedrivermaanger in production


url = "https://www.doctolib.de/praxis/berlin/praxis-an-der-kulturbrauerei/booking/availabilities?isNewPatient=false&isNewPatientBlocked=false&motiveIds[]=2020154&placeId=practice-127977&practitionerId=22131971&specialityId=1795&telehealth=false"

def gecko_test(url=url):
    """
    simple overview:
        1) set up webdriver
        2) load this article 
        3) close up shop 
    
    input:
        >> site_000
            > default: url of this article ('friend link')
    """
    # set the driver 
    driver = webdriver.Chrome(ChromeDriverManager().install())

    # get url
    driver.get(url)
    # and chill a bit
    time.sleep(7)

    # k, cool. let's bounce. 
    driver.quit()


def get_json_url():

    # Set up a headless Chrome browser
    # chrome_options = Options()
    # chrome_options.add_argument('--headless')
    driver = webdriver.Chrome('/Users/davidbiermann/Downloads/chromedriver_mac64/chromedriver')
    # wait 5 seconds before throwing any error, or continue when it's ready
    driver.implicitly_wait(5)

    # Navigate to the webpage
    url = 'https://www.doctolib.de/kinderorthopadie/berlin/silke-halbhuebner/booking/availabilities?insuranceSector=public&insuranceSectorEnabled=true&motiveIds[]=410798&placeId=practice-25555&specialityId=1142&telehealth=false'
    driver.get(url)
    driver.find_element(
        'xpath',
        '//*[@id="didomi-notice-agree-button"]',
    ).click()

    availabilities_json_files = []
    for r in driver.requests:
        if 'availabilities.json' in r.url:
            availabilities_json_files.append(r.url)

    # pick one of the received json objects
    if len(availabilities_json_files) > 0:
        json_url = availabilities_json_files[0]
        return json_url
    else:
        raise ValueError('No json objects meeting the defined criteria are requested.')

    # Close the browser
    driver.quit()


if __name__ == '__main__':
    # here we go
    #gecko_test()
    get_json_url()
