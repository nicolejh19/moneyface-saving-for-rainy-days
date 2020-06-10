from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://kiasufoodies.com/monthly-promo-code/"

#Fetch the raw html content
html_content = requests.get(url).text
#Parse html content
soup = BeautifulSoup(html_content, "lxml")
table = soup.find_all("table") #get List of tables

name = []
validity = []
promo_code = []
terms_cond = []

#First table in this webpage is the list of companies
company = table[0].tbody.find_all("tr")
company_list = []
for i in range(0, len(company)):
    company_list.append(company[i].text.replace('\n',' ').strip())

#Generate the lists in order
for i in range(1, len(table)):
    table_data = table[i].tbody.find_all("tr") #gives a list of table data
    comp = company_list[i-1]
    for j in range(0, len(table_data)):
        #e.g['', 'Unspecified', 'NO CODE 20% OFF Pick Up', '-', '']
        split = table_data[j].text.split('\n') #gives 5 element array: 
        name.append(comp)
        validity.append(split[1])
        promo_code.append(split[2])
        terms_cond.append(split[3])

df = pd.DataFrame({'Company':name,'Validity':validity,'Promo-Code':promo_code, 'Terms & Conditions': terms_cond}) 
df.to_csv('test.csv', index=False, encoding='utf-8')
