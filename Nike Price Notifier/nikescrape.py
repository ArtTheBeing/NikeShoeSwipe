import requests
import pandas as pds
class NikeScraper:
    def __init__(self, times):
        self.df = []
        self.scrape_api(times)
        self.to_dataframe()

    def scrape_api(self, times):
        anchor = 0
        count = 60
        for i in range(times):
            #This recurssion is to fetch the next 60
            self.url = f'https://api.nike.com/cic/browse/v2?queryid=products&anonymousId=C1A1B7BE17EFE4D2599DFBE5D326287A&country=us&endpoint=%2Fproduct_feed%2Frollup_threads%2Fv2%3Ffilter%3Dmarketplace(US)%26filter%3Dlanguage(en)%26filter%3DemployeePrice(true)%26filter%3DattributeIds(16633190-45e5-4830-a068-232ac7aea82c%2C0f64ecc7-d624-4e91-b171-b83a03dd8550)%26anchor%3D168%26consumerChannelId%3Dd9a5bc42-4b9c-4976-858a-f159cf99c647%26count%3D24&language=en&localizedRangeStr=%7BlowestPrice%7D%20%E2%80%94%20%7BhighestPrice%7D'
            response = requests.get(self.url)
            narrowed = response.json()['data']['products']['products']
            anchor = count
            count += 60
            for i in range(len(narrowed)):

                #Data Cleaning and Data Forming
                name = narrowed[i]['title']
                currentp = narrowed[i]['price']['currentPrice']
                fullp = narrowed[i]['price']['fullPrice']
                image = narrowed[i]['images']['portraitURL']
                segment = narrowed[i]['url'].replace('{countryLang}', "" )
                url = f'nike.com{segment}'
                data = {'Name': name, 'CurrentPrice': currentp, 'MaxPrice': fullp, 'image-link' : image, 'url': url}
                self.df.append(data)
    
    def to_dataframe(self):
        df = pds.DataFrame(self.df)
        df.to_csv('Nike Price Notifier/data.csv', index= False)


scrape = NikeScraper(5)