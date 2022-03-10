import requests
from bs4 import BeautifulSoup
from pubchempy import get_compounds

for compound in get_compounds('glucose', 'name'):
    print(compound.cid)
    print(vars(compound))
    print(compound.isomeric_smiles)