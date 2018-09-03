from selenium import webdriver
import time

# root url for the slader answers
slader_root_url = 'http://slader.com'
#linear applications textbook identifier
linear_apps_textbook_url = '/textbook/9780321982384-linear-algebra-and-its-applications-5th-edition'
# use the chrome driver
driver = webdriver.Chrome()

driver.get(slader_root_url + linear_apps_textbook_url)
time.sleep(2)  # wait for page to load


# chapter headers to click
chapter_headers = []
# urls for the sections to get answers for
section_urls = []

chapter_headers = driver.find_elements_by_class_name('toc-item')
#expand the chapter section
chapter_headers[0].click()

# get all the rows that have the pg nums
rows = driver.find_elements_by_tag_name('tr')

for row in rows:
    section_urls.append(row.get_attribute('data-url'))


driver.get(slader_root_url + section_urls[0].get_attribute('data-url'))

time.sleep(2)

#urls for the exercises
exercise_urls = []

exercises = driver.find_elements_by_xpath('//div[@class=\"list-item exercise-in-group-item\"]')
for exercise in exercises:
    exercise_urls.append(exercise.get_attribute('data-url'))

print(section_urls)