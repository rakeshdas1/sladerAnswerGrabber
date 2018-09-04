from selenium import webdriver
import urllib.request
import time, re, os

def get_num_from_string(string):
    match = re.findall(r'\d+', string)
    return match[0]

def create_folder_for_section(section):
    pathString = "./Answers/Section{}".format(section)
    #only create the directory if it already is not present
    if not os.path.exists(pathString):
        os.makedirs(pathString)

# root url for the slader answers
slader_root_url = 'http://slader.com'
# linear applications textbook identifier
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

# expand the chapter section
chapter_headers[0].click()

# get all the rows that have the pg nums
rows = driver.find_elements_by_xpath(
    '//section[@class="toc-item-expanded"][contains(@style,\'display: block\')]/table/tbody/tr')

# save the urls to the sections
for row in rows:
    section_urls.append(row.get_attribute('data-url'))

# navigate to the section
driver.get(slader_root_url + section_urls[0])

# wait for page to load
time.sleep(2)

# urls for the exercises
exercise_urls = []

# name of the section
section_name = driver.find_element_by_xpath('//span[@class="select2-chosen"]').text
#remove the forward slash in the section name
section_name = section_name.replace('/', '-')


# save the urls to the exercises
exercises = driver.find_elements_by_xpath('//div[@class=\"list-item exercise-in-group-item\"]')
for exercise in exercises:
    exercise_urls.append(exercise.get_attribute('data-url'))


# navigate to the exercies
driver.get(slader_root_url + exercise_urls[0])

#number of the current exercise
exercise_num = driver.find_element_by_xpath('//span[@class="exercises-by-group"]').text
exercise_num = get_num_from_string(exercise_num)

print("Now capturing section {}, exercise {}".format(section_name, exercise_num))

# find the answers to the exercises
answers = driver.find_element_by_xpath(
    '//section[@class=\"solutions-list reloadable\"]')
answer_imgs = driver.find_elements_by_xpath('//img[@class=\"image\"]')

#create the folder for the current chapter and section
create_folder_for_section(section_name)

for idx, answer_img in enumerate(answer_imgs):
    urllib.request.urlretrieve(
        answer_img.get_attribute('src'), "./Answers/Section{}/section{}-#{}_{}.png".format(section_name,section_name,exercise_num,idx))

driver.quit()



