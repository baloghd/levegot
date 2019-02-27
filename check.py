import argparse
import requests
import random
from bs4 import BeautifulSoup

from typing import List, Tuple, Iterable
from itertools import islice


parser = argparse.ArgumentParser()

parser.add_argument("varos", help="az ellenőrizendő város(ok)")
parser.add_argument("-e", "--egyszeru",
					help="egyszerű kiírás (csak a légszennyezés mértéke)",
					action="store_true")

args = parser.parse_args()

__SOURCE_URL__ = "http://legszennyezes.hu/%s"

def chunk(it: Iterable, size: int = 5) -> List[str]:
    it = iter(it)
    return iter(lambda: list(islice(it, size)), None)

def get_data(link: str) -> BeautifulSoup:
    desktop_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']
    req = requests.get(link, headers = {'User-Agent': random.choice(desktop_agents)})
    soup = BeautifulSoup(req.content, "html5lib")
    return soup

def parse_data(soup: BeautifulSoup) -> Tuple[List[List[str]], List[str]]:
	tabla = soup.find("div", {"id": "current-air"}).text.strip().split("\n")
	tabla = [item.strip() for item in tabla if len(item.strip()) > 0]

	parsed_tabla = []
	iterator = chunk(tabla, 5)
	for anyag in iterator:
		if len(anyag) > 0:
			parsed_tabla.append(anyag)

	egyszeru = soup.find("div", {"class": "current-air-lower"}).text.strip().split("\n")
	#egyszeru = list(filter(lambda x: len(x) > 0, map(str.strip, egyszeru)))
	egyszeru = [item.strip() for item in egyszeru if len(item.strip()) > 0]
	
	return parsed_tabla, egyszeru