import requests, PyPDF2
from io import BytesIO


from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By

def runThePyPDFApi():
    url = 'https://services.tubitak.gov.tr/edergi/yazi.pdf?dergiKodu=4&cilt=46&sayiid=801&yil=2013&ay=3&mod=tum'
    response = requests.get(url)
    my_raw_data = response.content


    with BytesIO(my_raw_data) as data:
        read_pdf = PyPDF2.PdfReader(data)

        for page in read_pdf.pages:
            print(page.extractText())
            print('--------------------------------------')


def pullLinksFromThePage():
    links = []

    url = 'https://services.tubitak.gov.tr/edergi/yillaraGoreArsiv.htm'

    #create basic selenium driver
    driver = webdriver.Chrome()

    driver.get(url)

    tempCounter = 0

    #get the page source







    for i in range(1, 4):
        if (i == 2):
            driver.find_element(By.ID, "dergiSelect").click()
            dropdown = driver.find_element(By.ID, "dergiSelect")
            dropdown.find_element(By.XPATH, "//option[. = 'Bilim Çocuk E-dergisi']").click()
        elif (i == 3):
            driver.find_element(By.ID, "dergiSelect").click()
            dropdown = driver.find_element(By.ID, "dergiSelect")
            dropdown.find_element(By.XPATH, "//option[. = 'Meraklı Minik E-dergisi']").click()
        for year in range(2022, 2020, -1):

            driver.find_element(By.ID, "yilSelect").click()
            dropdown = driver.find_element(By.ID, "yilSelect")
            tempYearHolder = "//option[. = '{}']".format(year)
            dropdown.find_element(By.XPATH, tempYearHolder).click()


            for x in range(1, 8):
                try:
                    tempTextHolder = ".col-sm-3:nth-child({0}) img".format(x)
                    driver.find_element(By.CSS_SELECTOR, tempTextHolder).click()

                    b = driver.find_element(By.LINK_TEXT, "Tüm sayıyı görmek için tıklayınız.")
                    c = b.get_attribute('href')
                    print(c)
                    driver.back()

                except Exception as e:
                    print("Dergi :", year , "Sayı :", x)
                    driver.get(url)














    sleep(5)










    sleep(11)




    #find text in driver
    """
    b = driver.find_element(By.LINK_TEXT, "Tüm sayıyı görmek için tıklayınız.")
    c = b.get_attribute('href')
    print(c)"""






    return links


pullLinksFromThePage()


