# -*- coding: utf-8 -*-

import requests
import os, datetime
from bs4 import BeautifulSoup
import json, csv


class Crawler():
    def __init__(self, category='nightlord'):
        with open('./category.json','r', encoding='utf-8') as json_file:
            self.categories = json.load(json_file)
        self.url = os.path.join('https://maple.gg/job/', category)
        self.html = requests.get(self.url)

    def crawler(self): 
        
        self.bs = BeautifulSoup(self.html.text, 'lxml')
        self.kor_names = self.bs.select('li > a')
        

    def find_population(self):
        today = datetime.datetime.today()
        file_name = today.strftime('%y-%m-%d') + '_population.csv'
        pop_file = open(file_name, 'w', newline='')
        csv_writer = csv.writer(pop_file)

        for category in self.categories.keys():
            cat_name = category.lower().replace(' ', '')
            self.__init__(category = cat_name)
            self.crawler()
    
            lines = self.bs.select('.user-summary-box-content > div > span')
            for line in lines:
                if '명' in line.text:
                    num = int(line.text[4:-1].replace(',', ''))
                    
                    # import ipdb; ipdb.set_trace()
                    cat_info = self.categories[category]
                    csv_writer.writerow([cat_name, cat_info[0], cat_info[1], cat_info[2], num])

                    print('{} \t : {}'.format(cat_name, num))

cr = Crawler()
cr.find_population()

