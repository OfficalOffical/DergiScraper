import pandas
import requests, PyPDF2
from io import BytesIO


from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By

def runThePyPDFApi(url):



    #take links in df and run them through the api

    response = requests.get(url)
    my_raw_data = response.content

    tempTextHolder = []

    with BytesIO(my_raw_data) as data:
        read_pdf = PyPDF2.PdfReader(data)

        for page in read_pdf.pages:
            tempTextHolder.append(page.extractText())
            tempTextHolder.append("\nnextpageseperator\n")

    return tempTextHolder


def pullLinksFromThePage():


    url = 'https://services.tubitak.gov.tr/edergi/yillaraGoreArsiv.htm'

    #create basic selenium driver
    driver = webdriver.Chrome()

    driver.get(url)

    tempCounter = 0

    #get the page source


    tempTur =0


    #create dictionary for each year, link, and x

    df = pandas.DataFrame(columns=['Tur','Yıl','Ay', 'Link'])
    error = pandas.DataFrame(columns=['Tur','Yıl','Ay'])

    for i in range(1, 4):
        if i == 1:
            tempTur = "Bilim ve Teknik E-dergisi"


        if (i == 2):

            driver.find_element(By.ID, "dergiSelect").click()
            dropdown = driver.find_element(By.ID, "dergiSelect")
            dropdown.find_element(By.XPATH, "//option[. = 'Bilim Çocuk E-dergisi']").click()
            tempTur = "Bilim Çocuk E-dergisi"


        elif (i == 3):
            driver.find_element(By.ID, "dergiSelect").click()
            dropdown = driver.find_element(By.ID, "dergiSelect")
            dropdown.find_element(By.XPATH, "//option[. = 'Meraklı Minik E-dergisi']").click()
            tempTur = "Meraklı Minik E-dergisi"


        for year in range(2022, 2007, -1):
            driver.find_element(By.ID, "yilSelect").click()
            dropdown = driver.find_element(By.ID, "yilSelect")
            tempYearHolder = "//option[. = '{}']".format(year)
            dropdown.find_element(By.XPATH, tempYearHolder).click()


            for x in range(1, 13):

                try:
                    tempTextHolder = ".col-sm-3:nth-child({0}) img".format(x)
                    driver.find_element(By.CSS_SELECTOR, tempTextHolder).click()

                    b = driver.find_element(By.LINK_TEXT, "Tüm sayıyı görmek için tıklayınız.")
                    c = b.get_attribute('href')

                    #create nested dictionary

                    #add to dataframe with pandas concat function
                    df = pandas.concat([df, pandas.DataFrame({'Tur': [tempTur], 'Yıl': [year], 'Ay': [x], 'Link': [c]})], ignore_index=True)





                    driver.back()


                except Exception as e:
                    error = pandas.concat([error, pandas.DataFrame({'Tur': [tempTur], 'Yıl': [year], 'Ay': [x]})], ignore_index=True)
                    driver.get(url)


    df.to_csv('output.csv', index=False)
    error.to_csv('error.csv', index=False)
    print(df.head())
    print(df.tail())

    driver.close()


    return df



"""tempArray = []



maindf = pandas.read_csv('output.csv')
for x in range(0, 451):

    if x % 50 == 0:
        print(x)
        tempStr = "Text" + str(x) + ".csv"
        tempArray.append(pandas.read_csv(tempStr))


tempArray.append(pandas.read_csv("LastText.csv"))

df = pandas.concat(tempArray, ignore_index=True)
print(df.head())

maindf = pandas.concat([maindf, df], axis=1)

maindf.to_csv('outputWithText.csv', index=False)
"""

maindf = pandas.read_csv('output.csv')
print(maindf.head())


