# En este archivo defino los métodos de extracción de datos particulares de cada paso
# Si cambiara la estructura de las páginas web, deberían modificarse estos métodos
# Empleo la librería BeautifulSoup para navegar por los elementos de la página HTML que voy a recuperar
# Es necesario tener instalada la librería html5lib para este propósito
import Items
from bs4 import BeautifulSoup


def extract_grados(html_text):
    grados = []
    html_soup = BeautifulSoup(html_text, "html5lib")
    for fila_grado in html_soup.find("div", {"class": "tabla_grados"}).select("table > tbody"):
        # Creo un nuevo ItemGrado y le asocio facultad e identificador
        cod = fila_grado.find_all("td")[0].get_text()
        nom = fila_grado.find_all("td")[1].get_text()
        link_grado = "http://portal.uned.es" + fila_grado.find_all("td")[1].find("a")["href"]
        link_fac = fila_grado.find_all("td")[2].find("a")["href"]
        cod_fac = link_fac[link_fac.rfind("/")+1:]
        item_grado = Items.ItemGrado(codigo=cod, nombre=nom, enlace=link_grado, cod_facultad=cod_fac)
        grados.append(item_grado)
    return grados


def extract_facultades(html_text):
    facultades = []
    html_soup = BeautifulSoup(html_text, "html5lib")
    for fila_grado in html_soup.find("div", {"class": "tabla_grados"}).select("table > tbody"):
        link_fac = fila_grado.find_all("td")[2].find("a")["href"]
        cod_fac = link_fac[link_fac.rfind("/") + 1:]
        nom = fila_grado.find_all("td")[2].get_text()
        item_facultad = Items.ItemFacultad(codigo=cod_fac, nombre=nom)
        facultades.append(item_facultad)
    return facultades


def extract_lista_asignaturas(html_text):
    codigos_asignaturas = []
    html_soup = BeautifulSoup(html_text, 'html5lib')
    for tabla_asignaturas in html_soup.find_all("table", {"class": "tabla_asignaturas"}):
        for fila_asignatura in tabla_asignaturas.tbody.find_all("tr"):
            # print(fila_asignatura)
            # Nos cercioramos de que es una fila de asignatura
            if len(fila_asignatura.find_all("td")) == 6:
                cod_asig = fila_asignatura.find_all("td")[0].get_text()
                codigos_asignaturas.append(cod_asig)

    return codigos_asignaturas


def extract_info_asignatura(html_text):
    html_soup = BeautifulSoup(html_text, 'html5lib')
    filas_info = html_soup.find("table", {"class": "tabla-guias"}).find_all("tr")
    nom, cod, curso, tipo, periodo, ects = None, None, None, None, None, None
    for fila_info in filas_info:
        if fila_info.find_all("td") and len(fila_info.find_all("td")) == 2:
            nombre_campo = fila_info.find_all("td")[0].get_text().strip()
            valor_campo = fila_info.find_all("td")[1].get_text().strip()
            # print(nombre_campo, valor_campo)

            if nombre_campo == "NOMBRE DE LA ASIGNATURA":
                nom = valor_campo
                nom = nom.replace("\n", " ")
            elif nombre_campo == "CÓDIGO":
                cod = valor_campo
            elif nombre_campo == "CURSO ACADÉMICO":
                curso = valor_campo
            elif nombre_campo == "TIPO":
                tipo = valor_campo
            elif nombre_campo == "PERIODO":
                periodo = valor_campo
                periodo = periodo.replace(u'\xa0', u' ')
                periodo = periodo.replace(u'  ', u' ')
            elif "ECTS" in nombre_campo:
                ects = valor_campo

    item_asignatura = Items.ItemAsignatura(codigo=cod, nombre=nom, curso=curso, periodo=periodo, tipo=tipo,
                                           creditos=ects)
    return item_asignatura
