import requests
from bs4 import BeautifulSoup as bs
import sqlite3


#connection to sqlite
sqliteConnection = sqlite3.connect('mainPython.db')
connection = sqliteConnection.cursor()

connection.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='BookDetails' ''')

if connection.fetchone()[0] != 1 : 

    tableSqlite = '''CREATE TABLE BookDetails(
        title text primary key,
        price varchar,
        availibility varchar,
        rating varchar
        );'''

    connection= sqliteConnection.execute(tableSqlite)
    sqliteConnection.commit()


for i in range(1,51):
    response = requests.get("http://books.toscrape.com/catalogue/page-"+str(i)+".html")
    content = response.text
    extract = bs(content,'html.parser')

    titleTag = extract.find_all('h3')
    priceTag = extract.find_all('p',class_ = 'price_color')
    availabilityTag = extract.find_all('p',class_ = "instock availability")
    ratingTag = extract.find_all('p',class_ = "star-rating")

    for i in range(len(titleTag)):
        insertQuery = """INSERT INTO BookDetails  VALUES (?,?,?,?);"""
        details = (titleTag[i].text,priceTag[i].text.replace('Â',''),availabilityTag[i].text.strip(),ratingTag[i].text.strip())
        connection.execute(insertQuery,details)
        sqliteConnection.commit()



