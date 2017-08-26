# pulls B data from GISAID
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import time, datetime, re, csv
# starting up the webdriver
driver = webdriver.Firefox()

# opening GISAID
driver.get('http://platform.gisaid.org/epi3/')

# logging in
time.sleep(10)
username = driver.find_element_by_name('login')
username.send_keys('rohan') # login goes here
password = driver.find_element_by_name('password')
password.send_keys('vaccine_evolution') # password goes here
driver.find_element_by_class_name('form_button_submit').click()

# setting filters
time.sleep(10)
type = driver.find_element_by_id("ce_ov4qu3_7t_select")
type.send_keys("B")

time.sleep(10)
lineage = driver.find_element_by_id("ce_ov4qu3_7w_select")
lineage.send_keys("Yamagata")

time.sleep(10)
host = Select(driver.find_element_by_id("ce_ov4qu3_7x_select"))
host.select_by_visible_text("Human")

time.sleep(10)
location = driver.find_element_by_xpath("/html/body[@class='yui-skin-sam']"
"/form[@class='sys-form']/div[@class='page']/div[@id='c_ov4qu3_48']"
"/div[@id='c_ov4qu3_4b']/div[@id='c_ov4qu3_d1']/div[@id='c_ov4qu3_d4']"
"/div[@id='c_ov4qu3_d6-c_ov4qu3_d6']/div[@id='ce_ov4qu3_7s']/table"
"[@class='sys-form-firow']/tbody/tr/td[2]/table[@class='sys-form-filine']"
"/tbody/tr[2]/td[6]/div[@id='ce_ov4qu3_7y']/div[@class='sys-form-fi-"
"multiselectcolumns']/select[@class='sys-event-hook sys-fi-mark']"
"[1]/option[5]").click()

# generating seasons
# need to double check if this is the correct definition for a season
def start_season(year):
    # takes year and returns date of first day of week 40 of that year
    start_week = ''.join([str(year), "-W40"])
    return datetime.datetime.strptime(start_week + '-0', "%Y-W%W-%w")
    
def end_season(year):
    # takes year and returns date of the last day of week 39 of that year
    return start_season(year) - datetime.timedelta(days=1)
    
def input_season(year):
    # takes start year of a season, and then inputs the season start and
    # end dates into the GISAID date filter
    time.sleep(10)
    input_start = start_season(year)
    start_date_string  = ''.join([str(input_start.year),"-",
                                    str(input_start.month),"-",
                                    str(input_start.day)])
    input_end = end_season(year+1)
    end_date_string = ''.join([str(input_end.year),"-",
                                str(input_end.month),"-",
                                str(input_end.day)]) 
                                                               
    start_date = driver.find_element_by_id('ce_ov4qu3_81_input')
    end_date = driver.find_element_by_id('ce_ov4qu3_82_input')
    
    start_date.clear()
    end_date.clear()
    
    start_date.send_keys(start_date_string)
    end_date.send_keys(end_date_string)


# for selecting a country in Europe
def select_country(i, year):
    time.sleep(5)
    if i!=2:
        prev_country_path = ''.join(["/html/body[@class='yui-skin-sam']/form",
        "[@class='sys-form']/div[@class='page']/div[@id='c_ov4qu3_48']",
        "/div[@id='c_ov4qu3_4b']/div[@id='c_ov4qu3_d1']/div[@id='c_ov4qu3_d4']",
        "/div[@id='c_ov4qu3_d6-c_ov4qu3_d6']/div[@id='ce_ov4qu3_7s']/table",
        "[@class='sys-form-firow']/tbody/tr/td[2]/table[@class='sys-form-filine'",
        "]/tbody/tr[2]/td[6]/div[@id='ce_ov4qu3_7y']/div[@class='sys-form-fi-",
        "multiselectcolumns']/select[@class='sys-event-hook sys-fi-mark']",
        "[2]/option[", str(i-1), "]"])
        prev_country = driver.find_element_by_xpath(prev_country_path)    
        prev_country.click()   
    elif year!=2012:   
        prev_country_path = ''.join(["/html/body[@class='yui-skin-sam']/form",
        "[@class='sys-form']/div[@class='page']/div[@id='c_ov4qu3_48']",
        "/div[@id='c_ov4qu3_4b']/div[@id='c_ov4qu3_d1']/div[@id='c_ov4qu3_d4']",
        "/div[@id='c_ov4qu3_d6-c_ov4qu3_d6']/div[@id='ce_ov4qu3_7s']/table",
        "[@class='sys-form-firow']/tbody/tr/td[2]/table[@class='sys-form-filine'",
        "]/tbody/tr[2]/td[6]/div[@id='ce_ov4qu3_7y']/div[@class='sys-form-fi-",
        "multiselectcolumns']/select[@class='sys-event-hook sys-fi-mark']",
        "[2]/option[54]"])
        prev_country = driver.find_element_by_xpath(prev_country_path)    
        prev_country.click()
    time.sleep(5)
    country_path = ''.join(["/html/body[@class='yui-skin-sam']/form",
    "[@class='sys-form']/div[@class='page']/div[@id='c_ov4qu3_48']",
    "/div[@id='c_ov4qu3_4b']/div[@id='c_ov4qu3_d1']/div[@id='c_ov4qu3_d4']",
    "/div[@id='c_ov4qu3_d6-c_ov4qu3_d6']/div[@id='ce_ov4qu3_7s']/table",
    "[@class='sys-form-firow']/tbody/tr/td[2]/table[@class='sys-form-filine'",
    "]/tbody/tr[2]/td[6]/div[@id='ce_ov4qu3_7y']/div[@class='sys-form-fi-",
    "multiselectcolumns']/select[@class='sys-event-hook sys-fi-mark']",
    "[2]/option[", str(i), "]"])
    country = driver.find_element_by_xpath(country_path)
    country.click()
    return country
    

# looping through seasons and countries, putting data into lists
season_list = []
country_list = []
isolates_list = []

with open('test.csv','wb') as csvfile:
    gisaid_writer = csv.writer(csvfile)
    for year in range(2012,2017):
        input_season(year)
        for i in range(2,55):
            cur_country = select_country(i, year)
            country = cur_country.text.encode('ascii','ignore')
            time.sleep(5)
            iso_count = driver.find_element_by_id('ce_ov4qu3_7d')
            iso_count_string = iso_count.text.encode('ascii','ignore')
            isolates = filter(str.isdigit, iso_count_string)
            season = ''.join([str(year),"-",str(year+1)])
            season_list.append(isolates)
            season_list.append(season)
            country_list.append(country)
            isolates_list.append(isolates)
            print(season, country, isolates)
            gisaid_writer.writerow([season, country, isolates])

csvfile.close()

