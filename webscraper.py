from selenium import webdriver
import foo

# opciones para que el navegador no aparezca en pantalla, no descargue las imagenes
# del sitio web e intente usar el cache del navegador para capturar datos mas rapidamente
options = webdriver.ChromeOptions()
options.add_argument('headless')
prefs = {'profile.managed_default_content_settings.images':2, 'disk-cache-size': 4096 }
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome('./chromedriver',options=options)

driver.get('http://books.toscrape.com/')

contadorLibros = 1

# list que almacenara todos los links de los libros
links = []

# itero por las 50 paginas
for i in range(50):

    libros = driver.find_elements_by_css_selector("#default > div > div > div > div > section > div:nth-child(2) > ol > li")
    print('Cargando links...')
    for libro in libros:

        linkLibro = libro.find_element_by_css_selector('.product_pod h3 a').get_attribute('href')
        links.append(linkLibro)
        contadorLibros += 1

    if contadorLibros < 1000:
        btnNext = driver.find_element_by_css_selector("#default > div > div > div > div > section > div:nth-child(2) > div > ul > li.next > a")
        btnNext.click()
    else:   
        foo.limpiarPantalla()
        print('Links cargados exitosamente !!!')
        print('Capturando datos....')

# funcion que recorre los links de los libros capturando sus datos y guardandolos en el csv
foo.fetchDatosLibros(links,driver)
foo.limpiarPantalla()
print('Datos registrados correctamente !')
driver.quit()