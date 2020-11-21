import requests
import json
from bs4 import BeautifulSoup

class CatastroFinder:
    """CatastroFinder"""

    def __init__(self,catastro_dict_path="./catastro_artifacts.json"):
        """

        Args:
            catastro_dict_path (str, optional): Json file with catastro urls to scrap. Defaults to "./catastro_artifacts.json".
        """
        with open(catastro_dict_path) as json_file:
            self.catastro_dict=json.load(json_file)

    def get_provincias(self,filtro=""):
        """get_provincias

        Args:
            filtro (str, optional): Filtro. Defaults to "".

        Returns:
            (list): List of items with Codigo and Denominacion. ['Codigo': 15, 'Denominacion': 'A CORUÑA'}...]

        """
        url=self.catastro_dict["provincias"]["url"]
        headers=self.catastro_dict["provincias"]["headers"]
        payload = "{ 'filtro': '"+filtro+"'}"
        response = requests.request("POST", url, headers=headers, data = payload)
        return json.loads(response.content)['d']

    def get_municipios(self,provincia):
        """get_municipios

        Args:
            provincia (str): Provincia code to search.

        Returns:
            (list): List of items with Codigo and Denominacion. ['Codigo': 121, 'Denominacion': 'SANTA POLA'}...]
        
        """
        url=self.catastro_dict["municipios"]["url"]
        headers=self.catastro_dict["municipios"]["headers"]
        payload = "{\"filtro\":\"\",\"provincia\":"+str(provincia)+"}"
        response = requests.request("POST", url, headers=headers, data = payload)
        return json.loads(response.content)['d']

    def get_vias(self,provincia,municipio,input_via):
        """get_vias

        Args:
            provincia (str): Provincia code to search.
            municipio (str): Municipio code to search.
            input_via (str): Via input to search.
         
        Returns:
            (list): List of items with Codigo, Sigla, TipoVia, DenominacionCompleta and Denominacion. {'Codigo': 1212, 'Sigla': 'CL', 'TipoVia': 'CALLE', 'Denominacion': 'SANTA CRISTINA', 'DenominacionCompleta': 'SANTA CRISTINA (CALLE)'}

        """
        url=self.catastro_dict["vias"]["url"]
        headers=self.catastro_dict["vias"]["headers"]
        payload = "{\"filtro\":\""+str(input_via)+"\",\"provincia\":"+str(provincia)+",\"municipio\":"+str(municipio)+"}"
        response = requests.request("POST", url, headers=headers, data = payload)
        return json.loads(response.content)['d']

    def search_inmueble(self,via_result,via_numero,selected_provincia,selected_municipio,tipur="U",pest="urbana"):
        """search inmueble

        Args:
            via_result (dict): [description]
            via_numero (str): [description]
            selected_provincia (dict): [description]
            selected_municipio ([dict): [description]
            tipur (str, optional): tipur. Defaults to "U".
            pest (str, optional): pest. Defaults to "urbana".

        Returns:
            (list): List of inmuebles
        """
        url=self.catastro_dict["inmuebles"]["url"]
        headers=self.catastro_dict["inmuebles"]["headers"]
        via = via_result['Denominacion'].replace(" ","@")
        params = (
            ('via', str(via)),
            ('tipoVia', str(via_result['Sigla'])),
            ('numero', str(via_numero)),
            ('kilometro', ''),
            ('bloque', ''),
            ('escalera', ''),
            ('planta', ''),
            ('puerta', ''),
            ('DescProv', str(selected_provincia['Denominacion'])),
            ('prov', str(selected_provincia['Codigo'])),
            ('muni', str(selected_municipio['Codigo'])),
            ('DescMuni', str(selected_municipio['Denominacion'])),
            ('TipUR', str(tipur)),
            ('codvia', str(via_result['Codigo'])),
            ('comVia', str(via_result['DenominacionCompleta'])),
            ('pest', str(pest)),
            ('from', 'OVCBusqueda'),
            ('nomusu', ' '),
            ('tipousu', ''),
            ('ZV', 'NO'),
            ('ZR', 'NO'),
        )

        response = requests.get(url, headers=headers, params=params)
        soup = BeautifulSoup(response.content,features="html.parser")
        return soup.find_all("div", "panel-heading")

