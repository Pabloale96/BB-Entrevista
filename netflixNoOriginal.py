import bs4 as bs
import urllib.request
import csv


CLASS_NAME_TO_TAKE_MOVIE = "nm-content-horizontal-row-item" #Buscando esta variable podemos sacar la fila de las peliculas que aparecen en la pagina
TAKE_NAME_MOVIE = "title-info" #Buscando esta variable podemos sacar el nombre de las peliculas
TAKE_DESCRIPTION = "title-info-synopsis" #Buscando esta variable podemos sacar la descripcion de las peliculas
TAKE_YEAR = "title-info-metadata-item item-year" #Buscando esto podemos sacr el año
TAKE_GENRE = "title-info-metadata-item item-genre" #Buscando esto podemos sacar el genero
TAKE_DIRECTORS = "title-data-info-item-list"#Buscando esta variable podemos buscar los directores
TAKE_CAST = "more-details-item item-cast" #Buscando esta variable podemos encontrar el cast

headers = ["Name", "Year","Gender", "Link","Cast","Directors", "Description"]

url = 'https://www.netflix.com/ar/browse/genre/839338'

source = urllib.request.urlopen(url).read()

soup = bs.BeautifulSoup(source,'html.parser')


movies = soup.findAll('li',class_ = CLASS_NAME_TO_TAKE_MOVIE) #Me quedo con las peliculas

#Busco los links de cada pelicula
links=[] 
for movie in movies:
    links.append(movie.a['href'])
names =[]
descriptions=[]
year=[]
genre=[]
directors=[]
cast=[]
for link in links:
    source = urllib.request.urlopen(link).read()
    soup = bs.BeautifulSoup(source,'html.parser')
    try:    
        names.append(soup.find('div',class_=TAKE_NAME_MOVIE).h1.text)
    except:
        names.append("No Info")
    try:    
        descriptions.append(soup.find('div',class_=TAKE_DESCRIPTION).text)
    except:
        descriptions.append("No Info")
    try:    
        year.append(soup.find('span',class_=TAKE_YEAR).text)
    except:
        year.append("No Info")
    try:    
        genre.append(soup.find('a',class_=TAKE_GENRE).text)
    except:
        genre.append("No Info")
    try:    
        directors.append(soup.find('span',class_=TAKE_DIRECTORS).text)
    except:
        directors.append("No Info")
    try:    
        cast.append(soup.find('div',class_=TAKE_DESCRIPTION).text)
    except:
        cast.append("No Info")
        

data = [names,year,genre,links,cast,directors,descriptions]
data =list(map(list,zip(*data)))
with open('netflix.csv', 'w',encoding="utf-8",newline="") as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(data)