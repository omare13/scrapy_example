# Aquí defino los flujos de los ítems en un pipeline

from rdflib import Graph
import Items
import RDFization


class RDFPipeline(object):
    """Los pipelines son clases que heredan de object y tienen, por lo menos, un método llamaado 'process_item'.
    Los pipelines pueden tener más de un método, ver https://docs.scrapy.org/en/latest/topics/item-pipeline.html"""
    def __init__(self):
        self.graph = None  # Aquí almaceno el objeto grafo de RDFLib al que iré añadiendo tripletas en "process_item"

    def open_spider(self, spider):
        # Cuando se abra el pipeline por primera vez, crearemos un grafo vacío con la librería RDFlib
        print("Creating new graph")
        self.graph = Graph()
        self.graph.bind("unev", "http://data.ia.uned.es/vocabulary/")
        self.graph.bind("uner", "http://data.ia.uned.es/resource/")

    def process_item(self, item, spider):
        # Este método define qué hacer cada vez que se inyecta un item en este pipeline
        # Podemos acceder a los datos de la Spider que lo inyectó
        if spider.name == "grado_spider":

            if type(item) == Items.ItemAsignatura:
                triplets = RDFization.asignatura_to_rdf(item)
                for triplet in triplets:
                    self.graph.add(triplet)
            elif type(item) == Items.ItemFacultad:
                triplets = RDFization.facultad_to_rdf(item)
                for triplet in triplets:
                    self.graph.add(triplet)
            elif type(item) == Items.ItemGrado:
                triplets = RDFization.grado_to_rdf(item)
                for triplet in triplets:
                    self.graph.add(triplet)

    def close_spider(self, spider):
        # Cuando se acabe de recopilar ítems, se lanza este método
        # Puedo acceder a la ruta del grafo especificado en GradoSpider
        # Guardo el grafo empleando la librería RDFLib
        self.graph.serialize(destination=spider.ruta_grafo, format="turtle", encoding="UTF-8")


class GreedyPipeline(object):
    # Este pipeline solo imprime lo que se procesa
    def process_item(self, item, spider):
        print("Crawled item {0} from spider {1}".format(item, spider.name))
