import requests
from bs4 import BeautifulSoup

url = 'https://movies.yahoo.com.tw/movie_thisweek.html'
data = requests.get(url)
soup = BeautifulSoup(data.text,"html.parser")

#取得yahoo本周新片10部
ul = soup.find("ul",class_="release_list")
movies = ul.find_all("li")
for movie in movies:
    foto = movie.find("div",class_="release_foto")
    movie_image = foto.find("img")["data-src"]
    
    info = movie.find("div",class_="release_info")
    movie_name = info.find_all("a")[0].text.strip()
    
    print(movie_name)
    print(movie_image)