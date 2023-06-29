import pandas as pds
from interface import ShoeSwiper
import random
from nikescrape import NikeScraper


data = pds.read_csv('Nike Price Notifier/data.csv')

nike = ShoeSwiper(data)
nike.run()
nike.save_liked_shoes()