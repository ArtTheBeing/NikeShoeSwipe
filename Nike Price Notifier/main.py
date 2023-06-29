import pandas as pds
from interface import ShoeSwiper
from nikescrape import NikeScraper
from pathlib import Path
path = Path('Nike Price Notifier/data.csv')

if path.is_file() == False:  
    scrape = NikeScraper(3)
data = pds.read_csv('Nike Price Notifier/data.csv')

nike = ShoeSwiper(data)
nike.run()
nike.save_liked_shoes()