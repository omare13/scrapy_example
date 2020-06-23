# Aquí mantengo una lista de métodos para obtener las urls que voy a emplear en el scraping (en las Spiders)

def url_lista_asignaturas_grado(cod_grado):
    return "http://portal.uned.es/pls/portal/url/page/UNED_MAIN/Grados/Listado%20de%20Asignaturas/2021/" + \
           "?idTitulacion=" + cod_grado


def url_informacion_asignatura(cod_grado, cod_asig):
    return "http://portal.uned.es/pls/portal/url/page/UNED_MAIN/GRADOS/Listado%20de%20Asignaturas/2021/" + \
           "ConsultaGuiaCurso?idAsignatura=" + cod_asig + "&idTitulacion=" + cod_grado
