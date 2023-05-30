from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests

# NASA Exoplanet URL
START_URL = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"

# Webdriver
browser = webdriver.Chrome("C:/Users/Lenovo/Desktop/Project-127-Web-Data-Extraction-1-main/chromedriver.exe")
browser.get(START_URL)

time.sleep(10)

scraped_data = []

def scrape_more_data(hyperlink):
    try:
        page= requests.get(hyperlink)

        soup = BeautifulSoup(page.content, "html.parser")

        temp_list= []

        for tr_tag in soup.find_all("tr", attrs= {"class": "fact_row"}):
            td_tags= tr_tag.find_all("td")

           
            for td_tag in td_tags:
                try :
                    temp_list.append(td_tag.find_all("div", attrs= {"class": "value"})[0].contents[0])
                except:
                    temp_list.append("")
        
        scraped_data.append(temp_list)

    except:
        time.sleep(1)
        scrape_more_data

stars_df_1= pd.read_csv('scraped_data.csv')
for index, row in stars_df_1.iterrows(): 
    print(row['hyperlink']) 
    scrape_more_data(row['hyperlink']) 
    print(f"Data Scraping at hyperlink {index+1} completed")

scrapped_data = [] 
for row in scraped_data: 
    replaced = [] 
    for el in row: 
        el = el.replace("\n", "") 
        replaced.append(el) 
    scrapped_data.append(replaced) 
print(scrapped_data) 

headers = ['Star_name', 'Distance', 'Mass', 'Radius', 'Luminosity']
star_df_1 = pd.DataFrame(scrapped_data, columns = headers) 
star_df_1.to_csv('dwarf_stars.csv', index=True, index_label="id")



    