
from collections import namedtuple
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
import re

Info = namedtuple('Info', ['formula', 'active_phase_to_ki'])

NIST_BASE_URL = 'https://webbook.nist.gov/cgi/cbook.cgi';

class NIST:

    def __init__(self, baseURL = NIST_BASE_URL):
        nisBaseURL = urlparse(baseURL)
        schemaURL = nisBaseURL.scheme or 'http'
        self.nistBaseURL = f'{schemaURL}://{nisBaseURL.hostname}'
        self.nistBasePath = nisBaseURL.path
   
    def nist_url(self):
        return f'{self.nistBaseURL}{self.nistBasePath}'

    def nist_query(self, name, unit):
        queryURLparams = f'Name={name}&Units={unit}'
        return f'{self.nist_url()}?{queryURLparams}'

    def __get_formula(self, nist_page_source):
        soup = BeautifulSoup(nist_page_source, 'html.parser')
        
        sub = soup.select_one("li sub")
        formulaReg = re.search("Formula:\s(?P<formula>\w+)",sub.parent.get_text())
        formula = formulaReg.group('formula')
        return formula

    def __get_table(self, nist_page_source):
        table_vals = []
        soup = BeautifulSoup(nist_page_source, 'html.parser')
        for a in soup.select("li a"):
            if a.get_text() == "Gas Chromatography":
                gas_chromatography_link_path += a.get('href')
        
        if gas_chromatography_link_path:
            gas_chromatography_link = f'{self.nist_url}{gas_chromatography_link_path}'
            result = requests.get(gas_chromatography_link)
            soup = BeautifulSoup(result.content, 'html.parser')

            table = soup.find("table", {"aria-label" : re.compile("Kovats.*RI.*non-polar.*column")})
            
            if table:
                th_list = [] 
                for th in table.find_all('th'):
                    th_list.append(th.text)
                active_phase_idx = th_list.index('Active phase')
                ki_idx = th_list.index('I')
                if active_phase_idx and ki_idx:
                    td_list = []
                    for tr in table.find_all('tr', class_="exp"):
                        td_list = tr.find_all('td')
                        table_vals.append(( td_list[active_phase_idx].get_text(), td_list[ki_idx].get_text())) 
        return table_vals


    def getInfoNIST(self, name: str, unit: str = 'SI'):
        url = self.nist_query(name, unit)
        result = requests.get(url)
        formula = self.__get_formula(result.content)
        table_vals = self.__get_table(result.content)

        NISTInfo = Info(formula, table_vals)
        return NISTInfo

nist = NIST()
def get_compounds(name, unit = 'SI'):
    return nist.getInfoNIST(name, unit)