import requests
from bs4 import BeautifulSoup
import csv
import re

base_url = "https://dubellay.mx"

# 1. Obtener todas las colecciones desde el menú principal
resp = requests.get(base_url)
soup = BeautifulSoup(resp.text, "html.parser")

# Buscar enlaces que apunten a /collections/
links = [a["href"] for a in soup.select("a") if a.get("href", "").startswith("/collections/")]

# Eliminar duplicados
links = list(set(links))

with open("catalogo_dubellay.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Categoria", "Marca", "Título", "Precio Original", "Precio +40%", "Imagen URL"])

    for link in links:
        categoria_url = base_url + link
        categoria_nombre = link.split("/")[-1].replace("-", " ").title()

        response = requests.get(categoria_url)
        soup = BeautifulSoup(response.text, "html.parser")

        productos = soup.select(".product-item")

        for producto in productos:
            marca = producto.select_one(".product-item-meta__vendor")
            titulo = producto.select_one(".product-item-meta__title")
            precio_texto = producto.select_one(".price")
            imagen = producto.select_one(".product-item__primary-image")

            if titulo and precio_texto and imagen:
                marca_texto = marca.get_text(strip=True) if marca else ""
                titulo_texto = titulo.get_text(strip=True)

                # Limpieza del precio
                precio_raw = precio_texto.get_text(strip=True)
                match = re.search(r"[\d\.]+", precio_raw)
                if match:
                    precio = float(match.group())
                    precio_final = round(precio * 1.4, 2)
                else:
                    precio = 0
                    precio_final = 0

                imagen_url = imagen["src"]
                if imagen_url.startswith("//"):
                    imagen_url = "https:" + imagen_url

                writer.writerow([categoria_nombre, marca_texto, titulo_texto, precio, precio_final, imagen_url])

print("✅ Archivo catalogo_dubellay.csv generado con todas las categorías.")
