import time
import random
from selenium import webdriver

driver = webdriver.Chrome('C:\chromedriver')  # Optional argument, if not specified will search path.

driver.get('http://127.0.0.1:8000/reg')

time.sleep(5) # Let the user actually see something!

search_name = driver.find_element_by_name('username')
login = 'Username{}'.format(random.randint(3, 99))
search_name.send_keys(login)
password = 'rustler4453'
search_pas = driver.find_element_by_name('password')
search_pas.send_keys(password)
search_pas1 = driver.find_element_by_name('password1')
search_pas1.send_keys(password)
search_pas2 = driver.find_element_by_name('password2')
search_pas2.send_keys(password)
search_button = driver.find_element_by_name('button-reg').submit()

search_logout = driver.find_element_by_name('logout').click()

search_log = driver.find_element_by_name('log').click()

search_name = driver.find_element_by_name('username')
search_name.send_keys(login)

search_pas = driver.find_element_by_name('password')
search_pas.send_keys(password)

search_login = driver.find_element_by_name('login').submit()

time.sleep(5) # Let the user actually see something!

driver.quit()