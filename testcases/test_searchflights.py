#go to yatra
#one way search
#select depart and go to 
# choose a depart date
#click on search flight
#next page is the search flight
#select 1 stop filter
#verify that all the instances show 1 stop
import softest
import pytest
from utilities.utils import Utils
from pages.yatra_launch_page import LaunchPage
from ddt import ddt, data,unpack, file_data


@pytest.mark.usefixtures("setup")
@ddt
class TestSearchAndVerifyFilter(softest.TestCase):
    log = Utils.custom_logger()


    @pytest.fixture(autouse=True)
    def class_setup(self):
        self.lp = LaunchPage(self.driver,self.achains)
        self.ut = Utils()
        yield 
        self.lp.driver.get("https://yatra.com/")

        
    # @data(("New Delhi","JFK","25/08/2022","1 stop"),("BOM","JFK","28/10/2022","2 stop"))
    # @unpack
    #the ./ is to go up a file
    # @file_data("../testdata/testdata.json")
    #the * is very important tells the unpack that this is a list of data that needs to be unpacked. the star is called a data decorator
    # @data(*Utils.read_data_from_excel("testdata\\tdataexcel.xlsx"))
    # @unpack
    @data(*Utils.read_dat_from_csv("testdata\\tdatacsv.csv"))
    @unpack
    def test_search_flights_stop(self,goingfrom,goingto,date,stops):
        #note four arguments and four per test case in the data tag
        search_flight_result = self.lp.searchFlights(goingfrom,goingto,date)
        self.lp.page_scroll()
        self.lp.go_to_top_of_page()
        search_flight_result.filter_flights_by_stop(stops)
        allstops = search_flight_result.get_search_flight_results()
        self.log.info(len(allstops))
        self.ut.assertListItemText(allstops,stops)

    # def test_search_flights_2_stop(self):

    #     search_flight_result = self.lp.searchFlights("New Delhi","JFK","25/08/2022")
    #     self.lp.page_scroll()
    #     self.lp.go_to_top_of_page()
    #     search_flight_result.filter_flights_by_stop("2 stop")
    #     allstops = search_flight_result.get_search_flight_results()
    #     self.log.info(len(allstops))
    #     self.ut.assertListItemText(allstops,"2 Stops")
    

