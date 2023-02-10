import requests
from bs4 import BeautifulSoup

def query(keyword):
    data = requests.get("https://search.books.com.tw/search/query/key/" + keyword + "/cat/all")
    
    soup = BeautifulSoup(data.text,"html.parser")
    
    div_tr = soup.find("div",class_ = "table-tr")
    
    divs = div_tr.find_all("div",class_ = "table-td")
    
    for div in divs:
        img = div.find("img")
        
        book_name = img["alt"]
        head = img["data-src"][20:].find("https")
        tail = img["data-src"][20:].find("&")
        book_url = img["data-src"][20:][head:tail]
        book_price = div.find_all("b")[-1].text + "元"
        print(book_name,book_url,book_price)

query("旅遊")