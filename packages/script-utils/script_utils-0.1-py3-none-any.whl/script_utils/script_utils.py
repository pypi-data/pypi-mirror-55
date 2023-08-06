from os.path import join, isfile
import yaml
import json
from pprint import pprint
from os.path import realpath, dirname
from io import open as iopen
import pickle

# TODO ############################ CUSTOMIZE THESE ############################

LOGGING = True
SETTINGS_FNAME = join(dirname(realpath(__file__)), '../../settings_local.yaml')

################################################################################

if not isfile(SETTINGS_FNAME):
    assert False, "Brak pliku z konfiguracją w katalogu głównym!"

ROOT = yaml.load(open(SETTINGS_FNAME, 'r'), yaml.FullLoader)['PATHS']['ABSOLUTE_ROOT_PATH']

SKLEPY = ['lidl', 'carrefour', 'biedronka', 'auchan', 'tesco']


################################       BRANDS HANDLERS      #################################

BRANDS_ROOT = join(ROOT, yaml.load(open(SETTINGS_FNAME, 'r'), yaml.FullLoader)['PATHS']['BRANDS_ROOT'])

TRIMMED_BRANDS_PATH = join(BRANDS_ROOT, 'trimmed.json')

SCRAPED_BRANDS_PATH = join(BRANDS_ROOT, 'scraped.json')

FINAL_BRANDS_PATH = join(BRANDS_ROOT, 'final.json')

BRANDS_LOAD = lambda path: json.load(open(path, 'r'))['brands']

BRANDS2DICT = lambda brand_lst: {'brands': brand_lst}

_CLEAN_BRANDS_JSON_PATH = '../scraping/save/clear_brands.json'  # direct from web scraping, rather do not use



################################       PRODUCTS HANDLERS      #################################


ANNO_ROOT = join(ROOT, yaml.load(open(SETTINGS_FNAME, 'r'), yaml.FullLoader)['PATHS']['ANNO_ROOT'])

FINAL_ANNO_ROOT = join(ROOT, yaml.load(open(SETTINGS_FNAME, 'r'), yaml.FullLoader)['PATHS']['FINAL_ANNO_ROOT'])

PRODS_PATH = lambda shop_name: join(ANNO_ROOT, 'scraped/{}/products.json'.format(shop_name.lower()))

FINAL_PRODS_PATH = lambda shop_name: join(FINAL_ANNO_ROOT, 'scraped/{}/products.json'.format(shop_name.lower()))

PRODS = lambda shop_name: json.load(open(PRODS_PATH(shop_name), "r"))['products']

FINAL_PRODS = lambda shop_name: json.load(open(FINAL_PRODS_PATH(shop_name), "r"))['products']

CATS_PATH = lambda shop_name: join(ANNO_ROOT, 'scraped/{}/cats.json'.format(shop_name.lower()))

CATS = lambda: dict([(S, json.load(open(CATS_PATH(S), 'r'))['categories']) for S in SKLEPY])

SUBCATS_PATH = lambda shop_name: join(ANNO_ROOT, 'scraped/{}/subcats.json'.format(shop_name.lower()))

SUBCATS = lambda shop_name, cat_name: json.load(open(SUBCATS_PATH(shop_name), 'r'))['subcategories'][cat_name]

PRODS2DICT = lambda prod_lst, shop: {'shop': shop, 'products': prod_lst}

PROMS2DICT = lambda prod_lst, shop: {'shop': shop, 'proms': prod_lst}

PROMS_PATH = lambda shop_name: join(ANNO_ROOT, 'scraped/{}/proms.json'.format(shop_name.lower()))

PROMS = lambda shop_name: json.load(open(PROMS_PATH(shop_name), "r"))['proms']

FINAL_PROMS_PATH = lambda shop_name: join(FINAL_ANNO_ROOT, 'scraped/{}/proms.json'.format(shop_name.lower()))

FINAL_PROMS = lambda shop_name: json.load(open(FINAL_PROMS_PATH(shop_name), "r"))['products']


#########################       PARSED RECORDS HANDLERS      ########################

RECORDS = lambda: pickle.load(open('records.pkl', 'rb'))

RECORDS = lambda pth: pickle.load(open(pth, 'rb'))

################################       UTILS        #################################

JSON_DUMP = lambda dic, path: json.dump(dic, iopen(path, 'w+', encoding='utf8'), indent=2, ensure_ascii=False)

pt = lambda _x: print(type(_x))

pd = lambda _x: print(dir(_x))

pp = lambda _x: pprint(_x)

pl = lambda _x: print(len(_x))

p = print

if LOGGING:
    log = print
else:
    log = lambda _: True
