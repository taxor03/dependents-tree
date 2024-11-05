import requests
from bs4 import BeautifulSoup
import core

package_name = core.package_name
for name in package_name:
    res = requests.get('https://www.npmjs.com/package/%s?activeTab=readme'%name)
    soup = BeautifulSoup(res.content, 'html.parser')
    package_download  = soup.find
    package_size = soup.find_all
    print (soup)
