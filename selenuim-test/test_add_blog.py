import time
import random
from selenium import webdriver

driver = webdriver.Chrome('C:\chromedriver')  # Optional argument, if not specified will search path.

driver.get('http://127.0.0.1:8000/login')

time.sleep(5) # Let the user actually see something!

search_name = driver.find_element_by_name('username')
search_name.send_keys('Username77')

search_pas = driver.find_element_by_name('password')
search_pas.send_keys('rustler4453')

search_login = driver.find_element_by_name('login').submit()

search_add = driver.find_element_by_name('create').click()

search_button_add = driver.find_element_by_name('add').click()

search_title = driver.find_element_by_name('title')
search_title.send_keys("Test:Text fsdjfkjsdlfasdfjsaldkfjgfjafsdfasdafsdafsdfdsafasdfsadfsadfsdafsdafsdfsadfsadkjfsadkulgfsadlufglsadjfglsadjfgalsfsadlsdfas")
search_body = driver.find_element_by_name('body')
search_body.send_keys("Text fdsfjslidfhas;fdhispaddhsakjd;jkfha;jkfh;saofh;jksadfa;kshfja;ksdfh;kasjhfkjashf;kajsfhjkasfd")
search_add_body = driver.find_element_by_name('body_add').click()
time.sleep(5) # Let the user actually see something!

driver.quit()