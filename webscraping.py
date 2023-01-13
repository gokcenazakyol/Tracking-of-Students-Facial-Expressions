import bs4
import requests
from selenium import webdriver
import os
import time

# setting urls and driver
driver1 = webdriver.Chrome(r'C:\Users\gokce\Downloads\chromedriver.exe')
yawning_face_URL = "https://www.google.com/search?q=yawning+human+face+students&tbm=isch&hl=tr&chips=q:yawning+human+face+students,online_chips:sleepy+face:p6ROzTlO7bc%3D&sa=X&ved=2ahUKEwjbkeSn2rz7AhWH5LsIHTQQBbIQ4lYoA3oECAEQKw&biw=1519&bih=722"
sleepy_students_URL = "https://www.google.com/search?q=sleepy+students&tbm=isch&ved=2ahUKEwjdk7Op2rz7AhW_if0HHQUIBQgQ2-cCegQIABAA&oq=sleep&gs_lcp=CgNpbWcQARgAMgQIIxAnMgQIIxAnMgQIABBDMgQIABBDMgQIABBDMgUIABCABDIFCAAQgAQyBAgAEEMyBQgAEIAEMgcIABCxAxBDOgcIIxDqAhAnOggIABCxAxCDAToICAAQgAQQsQNQmQhYmxRg0R9oAXAAeACAAbUBiAHABpIBAzAuNpgBAKABAaoBC2d3cy13aXotaW1nsAEKwAEB&sclient=img&ei=MhZ6Y92yAb-T9u8PhZCUQA&bih=722&biw=1519&hl=tr"

# directory is named as 'class009' because this is the 9th class for our training set
folder_name = 'class009'
if not os.path.isdir(folder_name):
    os.makedirs(folder_name)


# crating directory to save images
def download_image(url, folder_name, number):
    # writing image to file
    response = requests.get(url)
    if response.status_code == 200:
        with open(os.path.join(folder_name, "image" + str(0) + str(number) + ".jpg"), 'wb') as file:
            file.write(response.content)


def webscrapper(driver, url):
    driver.get(url)

    # we need to scroll the page to see every image on the page
    driver.execute_script("window.scrollTo(0,0);")

    # we need to reach to the containers
    page_html = driver.page_source
    pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
    containers = pageSoup.findAll('div', {'class': "isv-r PNCib MSM1fd BUooTd"})
    number_of_containers = len(containers)
    print("Found %s image containers" % number_of_containers)

    for i in range(1, number_of_containers + 1):

        # to avoid the 'Related Searches' on the page
        if i % 25 == 0:
            continue

        # getting the url of the small preview image
        preview_image_xPath = """//*[@id="islrg"]/div[1]/div[%s]/a[1]/div[1]/img""" % (i)
        preview_image_element = driver.find_element("xpath", preview_image_xPath)
        preview_image_URL = preview_image_element.get_attribute("src")

        # clicking on the container
        xPath = """//*[@id="islrg"]/div[1]/div[%s]""" % (i)
        driver.find_element("xpath", xPath).click()

        # starting a while True loop to wait until we get the the URL inside the large image view
        time_started = time.time()

        while True:
            # xPath stays same
            image_element = driver.find_element("xpath",
                                                """//*[@id="Sva75c"]/div/div/div/div[3]/div[2]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/a/img""")
            image_url = image_element.get_attribute('src')

            if image_url != preview_image_URL:
                # this breaks loop, because we got the high resolution of the image
                print(
                    "The preview of the image and larger size of the image have different resolutions. Got the high resolution image.")
                break

            else:
                # making a timeout if the full resolution image can not be loaded
                current_time = time.time()

                if current_time - time_started > 10:
                    print("Timeout! Program will download a lower resolution image and move on")
                    break


        # downloading
        try:
            download_image(image_url, folder_name, i)
            print('....................Downloaded %s/%s' % (i, number_of_containers))
        except:
            print('....................Could not download the image index with %s' % (i))


start = input("press 's' to start...")

if start == 's':
    webscrapper(driver1, sleepy_students_URL)

else:
    print('Program is closed.')
