from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import Spiders


def crawl_uned(ruta_grafo_grados):
    """Método para realizar la recopilación real de los datos
    :param ruta_grafo_grados la ruta del grafo donde se guardarán los resultados
    """

    # Comenzamos definiendo configuración de la recopilación
    # Ver https://docs.scrapy.org/en/latest/topics/settings.html#built-in-settings-reference
    mysettings = get_project_settings()
    # Añadimos las pipelines a emplear
    # mysettings.set("ITEM_PIPELINES", {'Pipelines.GreedyPipeline': 1000})
    mysettings.set("ITEM_PIPELINES", {'Pipelines.RDFPipeline': 1000})
    mysettings.set("RANDOMIZE_DOWNLOAD_DELAY", True)
    # Si queremos limitar la recopilación a 20 requests por segundo:
    # mysettings.set("DOWNLOAD_DELAY", 1/20)
    mysettings.set("CONCURRENT_REQUESTS_PER_IP", 20)
    mysettings.set("USER_AGENT", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)")
    # Defino cabeceras por defecto, aunque podría defininr cabeceras propias en las Spiders
    # Para este ejemplo siempre pediré las páginas en español y en html
    my_headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language': 'es'}
    mysettings.set("DEFAULT_REQUEST_HEADERS", my_headers)

    # Defino un nuevo proceso de recopilación con la configuracion anterior
    process = CrawlerProcess(mysettings)

    # Incluyo las Spiders que van a participar en el proceso de recopilación
    process.crawl(Spiders.GradoSpider, ruta_grafo_grados)
    # process.crawl(Spiders.MasterSpider, ruta_grafo_master)

    process.start()


if __name__ == "__main__":
    print("Iniciar Scraping UNED")
    crawl_uned("./grafo_grados.ttl")
