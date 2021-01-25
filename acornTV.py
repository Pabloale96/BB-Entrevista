from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import bs4 as bs
import time
import csv

"""
Realice un web scaping de las pagina de https://acorn.tv/browse/all/, al navegar por la pagina me di cuenta que le faltaba informacion sobre las peliculas por lo que decidi usar selenium para poder navegar sobre la pagina y buscar por los nombres en google para terminar de completar la informacion. 
Selenium necesita un driver para poder ejecutar el webdriver.Chrome(), dejare ese driver en un archivo .rar para poder utilizarlo. La instalacion de selenium es usando la herramienta "pip install selenium".
"""

"""
Varibles usadas en la pagina para realizar web scrapting
"""
CLASS_NAME_TO_TAKE_CATALOGO_INFORMATION = "col-sm-6 col-md-6 col-lg-3" #Si inspeccionas la pagina encontraras que la informacion sobre las peliculas/series estan de la siguiente forma <div class="col-sm-6 col-md-6 col-lg-3" ...> por lo que busco los div que tienen una class name igual a "col-sm-6 col-md-6 col-lg-3"

NAME_BAR_SEARCHE_GOOGLE = "q"# es el nombre que tiene la barra de google para buscar que se usa para buscar el search 

TABLE_GOOGLE_SEARCH = "liYKde g VjDLd"#buscando esta variable se obtine la tabla que aparece al buscar alguna informacion puntual en google

FRIST_INFORMATION_OF_TABLE = "wwUB2c PZPZlf" #buscando esta variable se obtine la primera informacion de la tabla sin contar el nombre buscado y la imagen, esto para una serie seria AÑO-GENERO-CANTIDAD DE TEMPORADAS

DIRECTOR_INFORMATION_TABLE = "Eq0J8 LrzXr kno-fv" # buscando esta variable se obtine la informacion sobre el cuadro principal, entre ellos se encuentra la de los directores que se encuentra al final

RATING_INFORMATION_TABLE = "xt8Uw TVtOme" # buscando esta variable se obtine la informacion del rating de la peliculo o serie

DESCRIPTION_INFORMATION = "franchise-description" # buscando esta variablew dentro de la pagina de una pelicula o serie te termina devolviendo la descripcion de la pelicula

#Path del driver para abrir el chrome:
PATH = ".\chromedriver.exe"

#La siguiente linea te habre una pagina de chrome:
driver = webdriver.Chrome(PATH)

#Informacion a buscar, lo uso para imprimir despues en un csv:
headers = ["Name", "Year","Type","Gender","Rating", "Link","Cast","Directors", "Description"]

#Cargo la pagina para hacer web scraping:
driver.get("https://acorn.tv/browse/all/")

#Estas lineas sirven para clickear sobre el boton de series, entonces se que todas las siguientes nombres son series
click = driver.find_element_by_link_text("SERIES") #me devuelve un objeto donde me dice el link cuando presione series
click.click() #hago click en series de la pagina
time.sleep(10) #tiempo de espera hasta que cargue la pagina

#Lo que realizo es usar bs para poder buscar la informacion necesaria, escrive el codigo de html en forma bonita
soup = bs.BeautifulSoup(driver.page_source,'html.parser')

#Me creo una lista con el type de lo que voy a buscar, en este caso es una serie
type = ["Serie"]

#Las siguientes dos lineas son para sacar el nombre de todo el catalogo:
contents = soup.find_all('div',class_=CLASS_NAME_TO_TAKE_CATALOGO_INFORMATION)
names = driver.find_element_by_class_name("item").text.split("\n") #me crea una lista con todos los nombres, por lo que len(names) es la cantidad de series de la pagina.
type = type*len(names) #Agrando la lista hasta la cantidad de series
links = [] #lista vacia donde estaran los links de cada pelicula

#contents seria la informacion de todas las peliculas/series y content seria de una, por lo que barro toda la lista de contents para obetener el link de cada pelicula/serie.
for content in contents:
    links.append(content.a["href"])# los links de las peliculas/series se encuentran en la parte de "href", por lo que filtro por href
    
# me quedo con la descripcion de cada pelicula/serie
description = []
#En link tengo todas las paginas de las series, por lo que lo que hago ahora es cambiar el driver para ir a cada link, luego estraigo la descripcion de cada una y lo agrego a la lista.
for link in links:
    driver.get(link)
    main = driver.find_element_by_id(DESCRIPTION_INFORMATION)
    description.append(main.text)
    
#Repito el proceso para las peliculas:
driver.get("https://acorn.tv/browse/all/") #Vuelvo a la primera pagina
click = driver.find_element_by_link_text("MOVIES")
click.click()
time.sleep(10)
soup = bs.BeautifulSoup(driver.page_source,'html.parser')
type2 = ["Movie"]
contents = soup.find_all('div',class_=CLASS_NAME_TO_TAKE_CATALOGO_INFORMATION)
names=names + (driver.find_element_by_class_name("item").text.split("\n"))
type = type +(type2*len(names))
link2 = []
for content in contents:
    link2.append(content.a["href"])
for link in link2:
    driver.get(link)
    main = driver.find_element_by_id(DESCRIPTION_INFORMATION)
    description.append(main.text)
links = links + link2
"""
Como dije antes saqueremos alguna informacion extra desde la pagina de google, la idea es buscar el nombre de la pelicula/serie y obtener de google el genero, directores, año y el rating de cada pelicula/serie
"""


#ahora voy a buscar los nombres de cada pelicula/serie

urlGoogle = "https://www.google.com/"
year = []
directors=[]
rating=[]
gender=[]
cast=[]
for i in range(0,len(names)): 
    

    #abro google
    driver.get(urlGoogle)
    try:
        searchString = names[i] + " " + type[i]  #esto va a ser lo que voy a buscar que seria el nombre de la serie o pelicula mas el tipo. Ejemplo, "Lost Serie"
        
        search = driver.find_element_by_name(NAME_BAR_SEARCHE_GOOGLE) #busco la barra de busquedo
        search.send_keys(searchString+Keys.RETURN)#Hago la busqueda
        time.sleep(5)
        #Realizo un BeutifulSoup de la pagina buscada de google
        soup = bs.BeautifulSoup(driver.page_source,'html.parser')
        
        #Me quedo con la tabla con toda la informacion de la pagina, siempre que se busca una pelicula o serie en google aparece esta tabla con todo el contenido manteniendo el mismo orden, es importante para extraer correctamente los actrices o directores
        table = soup.find('div',class_=TABLE_GOOGLE_SEARCH)
        try:
            listAux= table.find('div',class_=FRIST_INFORMATION_OF_TABLE) #Uso esta lista para sacar el año y genero, tambien se puede sacar la cantidad de temporadas
            listAux = listAux.text.split('‧') #transforma la cadena que encontre en una lista con el siguiente patron AÑO-GENERO-CANTIDAD DE TEMPORADAS
            if len(listAux) == 1:
                year.append("No Info")
                gender.append("No Info")
            #Me quedo con el AÑO y el GENERO
            else:
                year.append(listAux[0])
                gender.append(listAux[1])
        except :
            year.append("No Info")
            gender.append("No Info")
            rating.append("No Info")
            cast.append("No Info")
            directors.append("No Info")
            continue  
        #ahora busco los directores que se encuentra al final de la siguiente lista:
        
            
        try:
            directorAux= table.find_all('span',class_=DIRECTOR_INFORMATION_TABLE)
            directors.append(directorAux[-1].text)
        except:
            rating.append("No Info")
            cast.append("No Info")
            directors.append("No Info")
            continue  
        #Ahora buscamos los actores que se encuentra al principio de la lista, teniendo en cuenta que google solo pone 5 actores , nos qedamos con esos actores
        try:
            casters= table.find_all('div',class_="fl ellip oBrLN S1gFKb rOVRL")[0:5]
            string=""
            for caster in casters:
                string = string + caster.text+"," #guardo cada uno de los actores en string de la forma actor1,actor2,actor3,...,
            string = string[0:-1] #saco la ultima coma
            cast.append(string)#lo guardo en la lista
        except:
            rating.append("No Info")
            directors.append("No Info")
            continue
        
        try:
            rating.append(table.find('div',class_="xt8Uw TVtOme").text)
        except:
            rating.append("No Info")
            
    except:
          year.append("No Info")
          gender.append("No Info")
          rating.append("No Info")
          caster.append("No Info")
          directors.append("No Info")
          continue  

#Guardo toda la infoprmacion en un csv
data = [names,year,type,gender,rating,links,cast,directors,description]
data =list(map(list,zip(*data)))
with open('acron.csv', 'w',encoding="utf-8",newline="") as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(data)
driver.close()
