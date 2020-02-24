import requests
import json
import sys
import copy
import csv
from tabulate import tabulate
import pytz
from datetime import datetime
import time
from amapi.AmClient import AmClient
from amapi.AmCriteria import AmCriteria

class AmUninstalls:

    def __init__(self, args):
        self.criteria = AmCriteria(
            vendor=args.vendor,
            end_date=args.enddate,
            t_minus_days=args.t_minus_days,
            verbosity=args.verbosity
            )
        self.client = AmClient(
            username=args.username,
            password=args.password,
            verbosity=args.verbosity
            )
        self.template_row = {
            'feedback_addonKey':'',
            'feedback_addonVersion':'',
            'feedback_applicationKey':'',
            'feedback_applicationVersion':'',
            'feedback_hosting':'',
            'feedback_date':'',
            'feedback_feedbackType':'',
            'feedback_reasonKey':'',
            'feedback_message':'',
            'feedback_email':'',
            'feedback_fullName':'',
            'feedback_licenseId':'',
#            'transactions_transactionId':'',
#            'transactions_addonLicenseId':'',
#            'transactions_hostLicenseId':'',
#            'transactions_licenseId':'',
#            'transactions_addonKey':'',
            'transactions_addonName':'',
#            'transactions_lastUpdated':'',
            'transactions_customerDetails_company':'',
            'transactions_customerDetails_country':'',
            'transactions_customerDetails_region':'',
            'transactions_customerDetails_technicalContact_email':'',
            'transactions_customerDetails_technicalContact_name':'',
#            'transactions_customerDetails_technicalContact_address1':'',
#            'transactions_customerDetails_technicalContact_address2':'',
#            'transactions_customerDetails_technicalContact_city':'',
#            'transactions_customerDetails_technicalContact_state':'',
#            'transactions_customerDetails_technicalContact_postcode':'',
            'transactions_customerDetails_technicalContact_phone':'',
#            'transactions_customerDetails_technicalContact_extras':'',
            'transactions_customerDetails_billingContact_email':'',
            'transactions_customerDetails_billingContact_name':'',
#            'transactions_customerDetails_billingContact_address1':'',
#            'transactions_customerDetails_billingContact_address2':'',
#            'transactions_customerDetails_billingContact_city':'',
#            'transactions_customerDetails_billingContact_state':'',
#            'transactions_customerDetails_billingContact_postcode':'',
            'transactions_customerDetails_billingContact_phone':'',
#            'transactions_customerDetails_billingContact_extras':'',
            'transactions_purchaseDetails_saleDate':'',
            'transactions_purchaseDetails_tier':'',
            'transactions_purchaseDetails_licenseType':'',
            'transactions_purchaseDetails_hosting':'',
#            'transactions_purchaseDetails_billingPeriod':'',
            'transactions_purchaseDetails_purchasePrice':'',
            'transactions_purchaseDetails_vendorAmount':'',
            'transactions_purchaseDetails_partnerDiscountAmount':'',
#            'transactions_purchaseDetails_saleType':'',
            'transactions_purchaseDetails_maintenanceStartDate':'',
            'transactions_purchaseDetails_maintenanceEndDate':''
#            'transactions_partnerDetails_partnerName':'',
#            'transactions_partnerDetails_partnerType':'',
#            'transactions_partnerDetails_billingContact_email':'',
#            'transactions_partnerDetails_billingContact_name':'',
#            'transactions_partnerDetails_billingContact_address1':'',
#            'transactions_partnerDetails_billingContact_address2':'',
#            'transactions_partnerDetails_billingContact_city':'',
#            'transactions_partnerDetails_billingContact_state':'',
#            'transactions_partnerDetails_billingContact_postcode':'',
#            'transactions_partnerDetails_billingContact_phone':'',
#            'transactions_partnerDetails_billingContact_extras':'',
        }
        self.headers = self.template_row.keys()
        self.table = []
        self.row = []

    def __map_transactions (self, json_result):
        print('processing: ' + json_result['_links']['self']['href'])
        for transaction in json_result['transactions']:
            for name, value in transaction.items():
                if (name == 'addonName'):
                    self.row.update(transactions_addonName = self.row['transactions_addonName'] + value + "; ")
                elif (name == 'customerDetails'):
                    for name, value in value.items():
                        if (name == 'company'):
                            self.row.update(transactions_customerDetails_company = self.row['transactions_customerDetails_company'] + value + "; ")
                        elif (name == 'country'):
                            self.row.update(transactions_customerDetails_country = self.row['transactions_customerDetails_country'] + value + "; ")
                        elif (name == 'region'):
                            self.row.update(transactions_customerDetails_region = self.row['transactions_customerDetails_region'] + value + "; ")
                        elif (name == 'technicalContact'):
                            for name, value in value.items():
                                if (name == 'email'):
                                    self.row.update(transactions_customerDetails_technicalContact_email = self.row['transactions_customerDetails_technicalContact_email'] + value + "; ")
                                elif (name == 'name'):
                                    self.row.update(transactions_customerDetails_technicalContact_name = self.row['transactions_customerDetails_technicalContact_name'] + value + "; ")
                                elif (name == 'phone'):
                                    self.row.update(transactions_customerDetails_technicalContact_phone = self.row['transactions_customerDetails_technicalContact_phone'] + value + "; ")
                        elif (name == 'billingContact'):
                            for name, value in value.items():
                                if (name == 'email'):
                                    self.row.update(transactions_customerDetails_billingContact_email = self.row['transactions_customerDetails_billingContact_email'] + value + "; ")
                                elif (name == 'name'):
                                    self.row.update(transactions_customerDetails_billingContact_name = self.row['transactions_customerDetails_billingContact_name'] + value + "; ")
                                elif (name == 'phone'):
                                    self.row.update(transactions_customerDetails_billingContact_phone = self.row['transactions_customerDetails_billingContact_phone'] + value + "; ")
                elif (name == 'purchaseDetails'):
                    for name, value in value.items():
                        if (name == 'saleDate'):
                            self.row.update(transactions_purchaseDetails_saleDate = self.row['transactions_purchaseDetails_saleDate'] + value + "; ")
                        elif (name == 'tier'):
                            self.row.update(transactions_purchaseDetails_tier = self.row['transactions_purchaseDetails_tier'] + value + "; ")
                        elif (name == 'licenseType'):
                            self.row.update(transactions_purchaseDetails_licenseType = self.row['transactions_purchaseDetails_licenseType'] + value + "; ")
                        elif (name == 'hosting'):
                            self.row.update(transactions_purchaseDetails_hosting = self.row['transactions_purchaseDetails_hosting'] + value + "; ")
                        elif (name == 'purchasePrice'):
                            self.row.update(transactions_purchaseDetails_purchasePrice = self.row['transactions_purchaseDetails_purchasePrice'] + str(value) + "; ")
                        elif (name == 'vendorAmount'):
                            self.row.update(transactions_purchaseDetails_vendorAmount = self.row['transactions_purchaseDetails_vendorAmount'] + str(value) + "; ")
                        elif (name == 'partnerDiscountAmount'):
                            self.row.update(transactions_purchaseDetails_partnerDiscountAmount = self.row['transactions_purchaseDetails_partnerDiscountAmount'] + str(value) + "; ")
                        elif (name == 'maintenanceStartDate'):
                            self.row.update(transactions_purchaseDetails_maintenanceStartDate = self.row['transactions_purchaseDetails_maintenanceStartDate'] + value + "; ")
                        elif (name == 'maintenanceEndDate'):
                            self.row.update(transactions_purchaseDetails_maintenanceEndDate = self.row['transactions_purchaseDetails_maintenanceEndDate'] + value + "; ")

    def __append (self, json_result):
        print('processing: ' + json_result['_links']['self']['href'])
        for instance in json_result['feedback']:
            self.row = copy.deepcopy(self.template_row)
            for name, value in instance.items():
                if (name == 'addonKey'):
                    self.row.update(feedback_addonKey = value)
                elif (name == 'addonVersion'):
                    self.row.update(feedback_addonVersion = value)
                elif (name == 'applicationKey'):
                    self.row.update(feedback_applicationKey = value)
                elif (name == 'applicationVersion'):
                    self.row.update(feedback_applicationVersion = value)
                elif (name == 'hosting'):
                    self.row.update(feedback_hosting = value)
                elif (name == 'date'):
                    self.row.update(feedback_date = value)
                elif (name == 'feedbackType'):
                    self.row.update(feedback_feedbackType = value)
                elif (name == 'reasonKey'):
                    self.row.update(feedback_reasonKey = value)
                elif (name == 'message'):
                    self.row.update(feedback_message = value)
                elif (name == 'email'):
                    self.row.update(feedback_email = value)
                elif (name == 'fullName'):
                    self.row.update(feedback_fullName = value)
                elif (name == 'licenseId'):
                    self.row.update(feedback_licenseId = value)
            if (self.row['feedback_licenseId']):
                # get sales transactions
                parms = {
                    'limit':'50',
                    'addon':self.row['feedback_addonKey'],
                    'text':self.row['feedback_licenseId'],
                    'sortBy':'date',
                    'order':'desc'
                }
                result_transactions = self.client.get('/rest/2/vendors/' + self.criteria.vendor + '/reporting/sales/transactions', parms)
                if result_transactions.status_code != 200:
                    print(result_transactions.status_code)
                    print(result_transactions.text)
                    sys.exit()
                # page through results
                result_transactions_json = json.loads(result_transactions.text)
                self.__map_transactions(result_transactions_json)
                while ('next' in result_transactions_json['_links']):
                    result_transactions = self.client.get(result_transactions_json['_links']['next']['href'])
                    if result_transactions.status_code != 200:
                        print(result_transactions.status_code)
                        print(result_transactions.text)
                        sys.exit()
                    result_transactions_json = json.loads(result_transactions.text)
                    self.__map_transactions(result_transactions_json)
            self.table.append(self.row.values())

    def __generate(self):
        # get vendor uninstalls
        parms = {
            'limit':'50',
            'startDate':self.criteria.beg_date.strftime("%Y-%m-%d"),
            'endDate':self.criteria.end_date.strftime("%Y-%m-%d")
        }
        result = self.client.get('/rest/2/vendors/' + self.criteria.vendor + '/reporting/feedback/details', parms)
        if result.status_code != 200:
            print(result.status_code)
            print(result.text)
            sys.exit()
        # page through results
        json_result = json.loads(result.text)
        self.__append(json_result)
        while ('next' in json_result['_links']):
            result = self.client.get(json_result['_links']['next']['href'])
            if result.status_code != 200:
                print(result.status_code)
                print(result.text)
                sys.exit()
            json_result = json.loads(result.text)
            self.__append(json_result)

    def reportTXT(self):
        self.__generate()
        FILE_DATE = time.strftime("%Y%m%d")
        outfile = open('/var/data/' + FILE_DATE + '_vendor' + self.criteria.vendor + '_uninstalls.txt', 'w')
        print(tabulate(self.table, headers=self.headers, tablefmt='simple', floatfmt='.2f'), file = outfile)
        outfile.close()

    def reportCSV(self):
        self.__generate()
        FILE_DATE = time.strftime("%Y%m%d")
        outfile = open('/var/data/' + FILE_DATE + '_vendor' + self.criteria.vendor + '_uninstalls.csv', 'w')
        writer=csv.writer(outfile)
        writer.writerow(self.headers)
        writer.writerows(self.table)
        outfile.close()
