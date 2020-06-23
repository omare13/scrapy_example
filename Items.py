# En este archivo defino una especie de modelo de datos para tener claros los campos de los objetos que recupero
# scrapy.Field() puede ser cualquier cosa
# Si intentamos acceder a una clave inexistente de un ítem, devolverá error

import scrapy


class ItemGrado(scrapy.Item):
    codigo = scrapy.Field()
    nombre = scrapy.Field()
    cod_facultad = scrapy.Field()
    asignaturas = scrapy.Field()
    enlace = scrapy.Field()


class ItemFacultad(scrapy.Item):
    codigo = scrapy.Field()
    nombre = scrapy.Field()


class ItemAsignatura(scrapy.Item):
    codigo = scrapy.Field()
    nombre = scrapy.Field()
    curso = scrapy.Field()
    periodo = scrapy.Field()
    creditos = scrapy.Field()
    tipo = scrapy.Field()
    cod_grado = scrapy.Field()
