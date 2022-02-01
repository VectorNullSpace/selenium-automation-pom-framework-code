from selenium.webdriver.common.by import By
import time

from base.base_driver import BaseDriver
from pages.search_flights_results_page import SearchFlightResults
from utilities.utils import Utils

class LaunchPage(BaseDriver):
    log = Utils.custom_logger()
    
    def __init__(self,driver,achains):
        super().__init__(driver)
        self.driver = driver
        self.achains = achains
    #locators
    DEPART_FROM_FIELD = "//input[@id='BE_flight_origin_city']"
    GOING_TO_FIELD = "//input[@id='BE_flight_arrival_city']"
    ALL_AIRPORTS = "//div[@class='viewport']//div[1]/li"
    SELECT_DATE_FIELD = "//input[@id='BE_flight_origin_date']"
    ALL_DATES = "//td[@data-date]"
    SEARCH_BUTTON = "//input[@value='Search Flights']"
    ONE_WAY_BUTTON = "//a[@title='One Way']"
    POP_UP_DENY_BUTTON = '//*[@id="deny"]'

    def getPopUpButton(self):
        return self.driver.find_element(By.XPATH, self.POP_UP_BUTTON)    

    def getDepartFromField(self):
        return self.driver.find_element(By.XPATH, self.DEPART_FROM_FIELD) 
    
    def getGoingToField(self):
        return self.driver.find_element(By.XPATH, self.GOING_TO_FIELD) 
    
    def getAllAirports(self):
        return self.driver.find_elements(By.XPATH, self.ALL_AIRPORTS) 
    
    def getSelectDateField(self):
        return self.driver.find_element(By.XPATH, self.SELECT_DATE_FIELD) 
    
    def getAllDates(self):
        return self.driver.find_elements(By.XPATH, self.ALL_DATES) 
    
    def getSearchButton(self):
        return self.driver.find_element(By.XPATH, self.SEARCH_BUTTON) 

    def getOneWayButton(self):
        return self.driver.find_element(By.XPATH, self.ONE_WAY_BUTTON)

    def removePopUp(self):
        #check if pop up exists
        self.log.info("feature does not exist yet")
        #if pop up exists remove it
        #else do nothing

    def selectOneWayButton(self):
        self.getOneWayButton().click()

    def enterDepartFromLocation(self,departlocation):
        self.getDepartFromField().click()
        self.log.info("Clicked on depart from")
        time.sleep(2)
        self.getDepartFromField().send_keys(departlocation)
        self.log.info("Typed {} into departing from field successfully".format(departlocation))
        time.sleep(2)
        airports = self.getAllAirports()
        for airport in airports:
            self.log.info(airport.text)
            if departlocation in airport.text:
                self.achains.move_to_element(airport).click().perform()
                break


     #providing going to location 
    def enterGoingToLocation(self, goingtolocation):
        self.getGoingToField().click()
        self.log.info("Clicked on going to")
        time.sleep(2)
        self.getGoingToField().send_keys(goingtolocation)
        self.log.info("Typed {} into departing from field successfully".format(goingtolocation))
        time.sleep(2)
        airports = self.getAllAirports()
        for airport in airports:
            self.log.info(airport.text)
            if goingtolocation in airport.text:
                self.achains.move_to_element(airport).click().perform()
                break
        
    #selecting flight date
    def enterDepartureDate(self,departuredate):
        self.getSelectDateField().click()
        self.log.info("Clicked on select date field(departure)")
        self.log.info("searching for {} date".format(departuredate))
        flight_dates = self.getAllDates()
        time.sleep(500)
        for date in flight_dates:
            if date.get_attribute("id") == departuredate:
                date.click()
                self.log.info("clicked on a departure date now waiting(for a firefox sync issue)")
                time.sleep(2)
                break

        #click on flight search button and waiting for page to load
    def clicksearch(self):
        self.getSearchButton().click()
        self.log.info("Clicked on search button")
        time.sleep(8) 

    def searchFlights(self, departlocation, goingtolocation, departuredate):
        self.removePopUp()
        self.selectOneWayButton()
        self.enterDepartFromLocation(departlocation)
        self.enterGoingToLocation(goingtolocation)
        self.enterDepartureDate(departuredate)
        self.clicksearch()
        search_flights_result = SearchFlightResults(self.driver)
        return search_flights_result