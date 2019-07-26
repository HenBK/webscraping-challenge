from selenium import webdriver
import csv
import os

def crearLibro(title,price,stock,category,cover,upc,productType,priceExclTax,priceInclTax,tax,availability,numReviews):
    libro = { 
        'Title': title,
        'Price': price,
        'Stock': stock,
        'Category': category,
        'Cover': cover,
        'UPC': upc,
        'Product Type': productType,
        'Price (excl. tax)': priceExclTax,
        'Price (incl. tax)': priceInclTax,
        'Tax': tax,
        'Availability': availability,
        'Number of reviews': numReviews
    }

    print(libro)
    return libro

def fetchDatosLibros(links,driver):
    # list que guardara los dictionaries de los libros a registrar en el csv
    dictLibros = []

    # contador del libro de la iteracion actual (solo para propositos visuales en el terminal)
    contador = 1

    for link in links:
        driver.execute_script(f"window.open('{link}', 'new_window')")
        driver.switch_to_window(driver.window_handles[1])

        title = driver.find_element_by_css_selector('#content_inner > article > div.row > div.col-sm-6.product_main > h1').get_attribute('textContent')

        price = driver.find_element_by_css_selector('#content_inner > article > div.row > div.col-sm-6.product_main > p.price_color').get_attribute('textContent')

        category = driver.find_element_by_css_selector('#default > div > div > ul > li:nth-child(3) > a').get_attribute('textContent')

        cover = driver.find_element_by_css_selector('#product_gallery > div > div > div > img').get_attribute('src')

        upc = driver.find_element_by_css_selector('#content_inner > article > table > tbody > tr:nth-child(1) > td').get_attribute('textContent')

        productType = driver.find_element_by_css_selector('#content_inner > article > table > tbody > tr:nth-child(2) > td').get_attribute('textContent')

        priceExclTax = driver.find_element_by_css_selector('#content_inner > article > table > tbody > tr:nth-child(3) > td').get_attribute('textContent')

        priceInclTax = driver.find_element_by_css_selector('#content_inner > article > table > tbody > tr:nth-child(4) > td').get_attribute('textContent')

        tax = driver.find_element_by_css_selector('#content_inner > article > table > tbody > tr:nth-child(5) > td').get_attribute('textContent')

        availability = driver.find_element_by_css_selector('#content_inner > article > table > tbody > tr:nth-child(6) > td').get_attribute('textContent')

        numReviews = driver.find_element_by_css_selector('#content_inner > article > table > tbody > tr:nth-child(7) > td').get_attribute('textContent')

        #saco el stock del string availability
        stock = availability.split()

        for palabra in stock:
            if palabra.startswith('('):
                stock = palabra[1:]

        print(contador)
        dictLibros.append(crearLibro(title,price,stock,category,cover,upc,productType,priceExclTax,priceInclTax,tax,availability,numReviews))
        contador += 1
        driver.close()
        driver.switch_to_window(driver.window_handles[0])

    # creo el csv 
    with open('libros.csv', 'w', newline='') as archivo:
        campos = [
            'Title',
            'Price',
            'Stock',
            'Category',
            'Cover',
            'UPC',
            'Product Type',
            'Price (excl. tax)',
            'Price (incl. tax)',
            'Tax',
            'Availability',
            'Number of reviews'
        ]

        writter = csv.DictWriter(archivo, fieldnames=campos)
        writter.writeheader()

        # inserto los datos de los libros en el csv
        for libro in dictLibros:
            writter.writerow(libro)

def limpiarPantalla():
    if os.name == 'nt': 
        os.system('cls') 
    else: 
        os.system('clear')