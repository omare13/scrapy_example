import scrapy
from abc import ABC
import Extractors
import URLS


class GradoSpider(scrapy.Spider, ABC):
    """
    Spider para el scraping de grados
    """

    # Asignación del nombre de la araña
    name = "grado_spider"

    # Por defecto en Scrapy, las arñas comienzan a lanzar peticiones para cada una de las urls del atributo "start_urls"
    start_urls = ["http://portal.uned.es/portal/page?_pageid=93,1643102&_dad=portal&_schema=PORTAL"]

    # Método de inicialización del objeto por si quisiéramos pasarle algún parámetro de inicialización
    def __init__(self, ruta_grafo, **kwargs):
        super(GradoSpider, self).__init__(**kwargs)
        self.ruta_grafo = ruta_grafo

    # Por defecto en Scrapy, las arañas comienzan a lanzar peticiones en el método llamado "start_requests"
    # Este método, si no es sobreescrito, envía las respuestas de las peticiones al método llamado "parse"
    # Nosotros cambiamos este comportamiento para pasar las respuesta al método grado_to_listAsigs
    # Es obligatorio que cada spider comience el scraping desde el método con este nombre
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, method="GET", callback=self.grado_to_list_asigs)

    # Este emplea el parámetro response para manejar la respuesta de cada petición en start_requests
    def grado_to_list_asigs(self, response):
        # Obtengo el HTML de la respuesta
        html_text = response.body_as_unicode()

        # Extraigo los items con la infromación de los grados contenida en el HTML obtenido
        items_grados = Extractors.extract_grados(html_text)
        # Por cada uno de los items grado extraidos
        for item_grado in items_grados:
            # Creo una nueva petición y proceso su respuesta en el método parse_grado_to_asigs
            # Incluyo también la información del ItemGrado que acabo de extraer para manejarlo en el método callback
            url = URLS.url_lista_asignaturas_grado(item_grado["codigo"])
            yield scrapy.Request(url=url, method="GET", callback=self.list_asigs_to_asig_info,
                                 meta={"item_grado": item_grado})

        # Extraigo los items con la información de facultades contenida en el HTML obtenido
        items_facultades = Extractors.extract_facultades(html_text)
        # Por cada uno de los items facultad extraidos
        for item_facultad in items_facultades:
            # Envío el ítem al pipeline
            yield item_facultad

    def list_asigs_to_asig_info(self, response):
        # Obtengo el HTML de la respuesta
        html_text = response.body_as_unicode()

        # Obtengo el item de grado recopilado hasta el momento
        item_grado = response.meta["item_grado"]

        # Extraigo el listado de codigos de asignaturas
        codigos_asignaturas = Extractors.extract_lista_asignaturas(html_text)
        # Asigno el listado de asignaturas al item grado y lo envío al Pipeline de Items
        item_grado["asignaturas"] = codigos_asignaturas
        yield item_grado

        # Por cada codigo de asignatura, lanzo una petición a la página de información básica de asignatura
        for codigo_asignatura in codigos_asignaturas:
            url = URLS.url_informacion_asignatura(item_grado["codigo"], codigo_asignatura)
            yield scrapy.Request(url=url, method="GET", callback=self.asig_info_to_end,
                                 meta={"item_grado": item_grado})

        # La respuesta será procesada en el método listAsigs_to_basicInfo

    def asig_info_to_end(self, response):
        # Obtengo el html de la respuesta
        html_text = response.body_as_unicode()

        # Obtengo el item del grado
        item_grado = response.meta["item_grado"]

        # Extraigo información básica de la asignatura
        item_asignatura = Extractors.extract_info_asignatura(html_text)
        # Añado el codigo del grado al item asignatura
        item_asignatura["cod_grado"] = item_grado["codigo"]
        # Envío la información de la asignatura el Pipeline de Items para su almacenaje
        yield item_asignatura


class MasterSpider(scrapy.Spider, ABC):

    name = "master_spider"
