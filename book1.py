from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def query(keyword):
    chrome = webdriver.Chrome()
    chrome.get("https://www.books.com.tw/")

    Inputfield = chrome.find_element(By.ID,"key")
    Inputfield.send_keys(keyword)
    Inputfield.send_keys(Keys.ENTER)
    
    soup = BeautifulSoup(chrome.page_source,"html.parser")
    
    div_tr = soup.find("div",class_ = "table-tr")
    
    divs = div_tr.find_all("div",class_ = "table-td")
    
    for div in divs:
        img = div.find("img")
        
        book_name = img["alt"]
        book_url = img["src"]
        book_price = div.find_all("b")[-1].text + "元"
        
        print(book_name,book_url,book_price)

query("嬰兒")