from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://www.kiasufoodies.com/student-deals/"

#Fetch the raw html content
html_content = requests.get(url).text
#Parse html content
soup = BeautifulSoup(html_content, "lxml")
table = soup.find_all("table") #get List of tables

merchant = []
deal = []
location = []
link = []

for i in range(0, len(table)):
    table_data = table[i].tbody.find_all("tr")
    for j in range(0, len(table_data)):
        split = table_data[j].text.split('\n')
        merchant.append(split[1])
        deal.append(split[2])
        location.append(split[3])
        link.append(split[4])

df = pd.DataFrame({'Merchant':merchant,'Deal':deal,'Location':location, 'Link': link}) 
df.to_csv('deal.csv', index=False, encoding='utf-8')
