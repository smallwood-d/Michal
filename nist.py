
from collections import namedtuple
from urllib.parse import urlparse, quote_plus
from bs4 import BeautifulSoup
import requests
import re

Info = namedtuple('Info', ['formula', 'active_phase_to_ki'])

NIST_BASE_URL = 'https://webbook.nist.gov/cgi/cbook.cgi';

class NIST:
    """Small API for the NIST website."""

    def __init__(self, baseURL: str = NIST_BASE_URL) -> None:
        nisBaseURL = urlparse(baseURL)
        schemaURL = nisBaseURL.scheme or 'http'
        self.nistBaseURL = f'{schemaURL}://{nisBaseURL.hostname}'
        self.nistBasePath = nisBaseURL.path
   
    def nist_url(self, suffix: str = '') -> str:
        """return the nist URL """
        return f'{self.nistBaseURL}{self.nistBasePath}{suffix}'

    def nist_query(self, name: str, unit: str) -> str:
        """build NIST basic compound query"""
        queryURLparams = f'Name={quote_plus(name)}&Units={unit}'
        return f'?{queryURLparams}'

    def __get_formula(self, nist_page_source: bytes) -> str:
        """return the formula of a compand"""
        formula = None
        soup = BeautifulSoup(nist_page_source, 'html.parser')
        
        sub = soup.select_one("li sub") # collect the sub tag - assume there is only one sub tag in the url - formula
        if sub:
            formulaReg = re.search("Formula:\s(?P<formula>\w+)",sub.parent.get_text())
            formula = formulaReg.group('formula')
        return formula

    def __get_table(self, nist_page_source: bytes) -> list[tuple[str, float]]:
        """return the Kovats' RI, non-polar column, isothermal table.
        active phase to Ki value"""
        table_vals = []
        gas_chromatography_link = None
        soup = BeautifulSoup(nist_page_source, 'html.parser')
        # search for the Gas Chromatography link
        for a in soup.select("li a"):
            if a.get_text() == "Gas Chromatography":
                gas_chromatography_link = a.get('href')
        if gas_chromatography_link:
            # get the link
            result = requests.get(self.nist_url(gas_chromatography_link))
            soup = BeautifulSoup(result.content, 'html.parser')

            # find the table 
            table = soup.find("table", {"aria-label" : re.compile("Kovats.*RI.*non-polar.*column")})
            
            if table:
                th_list = [] 
                # collect the table headers
                for th in table.find_all('th'):
                    th_list.append(th.text)
                
                #find the index's
                active_phase_idx = th_list.index('Active phase')
                ki_idx = th_list.index('I')
                if active_phase_idx and ki_idx:
                    # collect the data from each row.
                    td_list = []
                    for tr in table.find_all('tr', class_="exp"):
                        td_list = tr.find_all('td')
                        table_vals.append(( td_list[active_phase_idx].get_text(), float(td_list[ki_idx].get_text()))) 
        return table_vals


    def getInfoNIST(self, name: str, unit: str = 'SI') -> Info:
        """collect and return all the info from NIST about a compand"""
        url = self.nist_url(self.nist_query(name, unit))
        result = requests.get(url)
        formula = self.__get_formula(result.content)
        table_vals = self.__get_table(result.content)

        NISTInfo = Info(formula, table_vals)
        return NISTInfo

nist = NIST()
def get_compounds(name:str, unit:str = 'SI') -> Info : 
    """"Return the formula and the Ki values of a compand."""
    return nist.getInfoNIST(name, unit)