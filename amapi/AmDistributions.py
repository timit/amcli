import requests
import json
import sys
import csv
from tabulate import tabulate
import time
from amapi.AmClient import AmClient
from amapi.AmCriteria import AmCriteria

class AmDistributions:

    def __init__(self, args):
        self.criteria = AmCriteria(
            app=args.app,
            verbosity=args.verbosity
            )
        self.client = AmClient(
            verbosity=args.verbosity
            )
        self.headers = ['CATEGORY', 'APP', 'BUNDLED', 'BUNDLEDCLOUD', 'DOWNLOADS', 'TOTALINSTALLS', 'TOTALUSERS']
        self.table = []

    def __append (self, category_name, json_result):
        #json_result['count']
        for i in json_result['_embedded']['addons']:
            print('processing: ', category_name, i['key'])
            app_name = i['name']
            # capture distributions for each app
            if ('bundled' in i['_embedded']['distribution']):
                bundled = i['_embedded']['distribution']['bundled']
            else:
                bundled = False
            if ('bundledCloud' in i['_embedded']['distribution']):
                bundled_cloud = i['_embedded']['distribution']['bundledCloud']
            else:
                bundled_cloud = False
            if ('downloads' in i['_embedded']['distribution']):
                downloads = i['_embedded']['distribution']['downloads']
            else:
                downloads = 0
            if ('totalInstalls' in i['_embedded']['distribution']):
                total_installs = i['_embedded']['distribution']['totalInstalls']
            else:
                total_installs = 0
            if ('totalUsers' in i['_embedded']['distribution']):
                total_users = i['_embedded']['distribution']['totalUsers']
            else:
                total_users = 0
            self.table.append((category_name, app_name, bundled, bundled_cloud, downloads, total_installs, total_users))

    def __generate(self):
        # get app listing
        result = self.client.get('/rest/2/addons/' + self.criteria.app)
        if result.status_code != 200:
            print(result.status_code)
            print(result.text)
            sys.exit()
        json_result = json.loads(result.text)
        for category in json_result['_embedded']['categories']:
            # get all apps in each category
            parms = {
                'category': category['name']
            }
            result = self.client.get('/rest/2/addons', parms)
            if result.status_code != 200:
                print(result.status_code)
                print(result.text)
                sys.exit()
            # page through results
            json_result = json.loads(result.text)
            self.__append(category['name'], json_result)
            print(category['name'])
            while ('next' in json_result['_links']):
                result = self.client.get(json_result['_links']['next'][0]['href'])
                if result.status_code != 200:
                    print(result.status_code)
                    print(result.text)
                    sys.exit()
                json_result = json.loads(result.text)
                self.__append(category['name'], json_result)

    def reportTXT(self):
        self.__generate()
        FILE_DATE = time.strftime("%Y%m%d")
        outfile = open('/var/data/' + FILE_DATE + '_' + self.criteria.app + '_distributions.txt', 'w')
        print(tabulate(self.table, headers=self.headers, tablefmt='simple', floatfmt='.2f'), file = outfile)
        outfile.close()

    def reportCSV(self):
        self.__generate()
        FILE_DATE = time.strftime("%Y%m%d")
        outfile = open('/var/data/' + FILE_DATE + '_' + self.criteria.app + '_distributions.csv', 'w')
        writer=csv.writer(outfile)
        writer.writerow(self.headers)
        writer.writerows(self.table)
        outfile.close()
