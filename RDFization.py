# Este archivo lo empleo para pasar de los items a tripletas
from rdflib import RDF, RDFS, Namespace, Literal, URIRef
import URIS


UNED = Namespace("http://data.ia.uned.es/vocabulary/")

def asignatura_to_rdf(item):
    triplets = []
    asignatura = URIS.uri_asignatura(item["cod_grado"], item["codigo"])

    triplets.append( (asignatura, RDF.type, UNED.Asignatura) )

    # También podemos especificar datatype o lenguaje a los Literal en RDFLib
    triplets.append( (asignatura, RDFS.label, Literal(item["nombre"])) )
    triplets.append( (asignatura, UNED.creditos, Literal(item["creditos"])) )
    triplets.append( (asignatura, UNED.tipoAsignatura, Literal(item["tipo"])) )
    triplets.append( (asignatura, UNED.curso, Literal(item["curso"])) )
    triplets.append( (asignatura, UNED.semestre, Literal(item["periodo"])) )

    return triplets


def grado_to_rdf(item):
    triplets = []
    grado = URIS.uri_grado(item["codigo"])

    triplets.append( (grado, RDF.type, UNED.Grado) )
    triplets.append( (grado, RDFS.label, Literal(item["nombre"])) )
    triplets.append( (grado, RDFS.seeAlso, URIRef(item["enlace"])) )

    for codigo_asignatura in item["asignaturas"]:
        asignatura = URIS.uri_asignatura(item["codigo"], codigo_asignatura)
        triplets.append( (grado, UNED.tieneAsignatura, asignatura) )

    facultad = URIS.uri_facultad(item["cod_facultad"])
    triplets.append( (grado, UNED.adscrito, facultad) )
    return triplets


def facultad_to_rdf(item):
    triplets = []
    facultad = URIS.uri_facultad(item["codigo"])

    triplets.append( (facultad, RDF.type, UNED.Facultad) )
    triplets.append( (facultad, RDFS.label, Literal(item["nombre"])) )

    return triplets
