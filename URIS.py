# Este archivo lo empleo para crear recursos RDFlib acorde a patrones de URIs que he definido y usarlos en RDFization

from rdflib import URIRef


base_uri = "http://data.ia.uned.es/resource/"


def uri_asignatura(cod_grado, cod_asignatura):
    uri = base_uri + "asignatura_{0}_{1}".format(cod_grado, cod_asignatura)
    return URIRef(uri)


def uri_facultad(cod_facultad):
    uri = base_uri + "facultad_" + cod_facultad
    return URIRef(uri)


def uri_grado(cod_grado):
    uri = base_uri + "grado_" + cod_grado
    return URIRef(uri)
