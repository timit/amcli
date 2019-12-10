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

class AmAttributions:

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
            'core_addonLicenseId':'',
            'core_hostLicenseId':'',
            'core_licenseId':'',
            'core_addonKey':'',
            'core_addonName':'',
            'core_hosting':'',
            'core_lastUpdated':'',
            'core_licenseType':'',
            'core_maintenanceStartDate':'',
            'core_maintenanceEndDate':'',
            'core_status':'',
            'core_tier':'',
            'core_extras':'',
            'contactDetails_company':'',
            'contactDetails_country':'',
            'contactDetails_region':'',
            'contactDetails_extras':'',
            'contactDetails_technicalContact_email':'',
            'contactDetails_technicalContact_name':'',
            'contactDetails_technicalContact_address1':'',
            'contactDetails_technicalContact_address2':'',
            'contactDetails_technicalContact_city':'',
            'contactDetails_technicalContact_state':'',
            'contactDetails_technicalContact_postcode':'',
            'contactDetails_technicalContact_phone':'',
            'contactDetails_technicalContact_extras':'',
            'contactDetails_billingContact_email':'',
            'contactDetails_billingContact_name':'',
            'contactDetails_billingContact_address1':'',
            'contactDetails_billingContact_address2':'',
            'contactDetails_billingContact_city':'',
            'contactDetails_billingContact_state':'',
            'contactDetails_billingContact_postcode':'',
            'contactDetails_billingContact_phone':'',
            'contactDetails_billingContact_extras':'',
            'partnerDetails_partnerName':'',
            'partnerDetails_partnerType':'',
            'partnerDetails_extras':'',
            'partnerDetails_technicalContact_email':'',
            'partnerDetails_technicalContact_name':'',
            'partnerDetails_technicalContact_address1':'',
            'partnerDetails_technicalContact_address2':'',
            'partnerDetails_technicalContact_city':'',
            'partnerDetails_technicalContact_state':'',
            'partnerDetails_technicalContact_postcode':'',
            'partnerDetails_technicalContact_phone':'',
            'partnerDetails_technicalContact_extras':'',
            'partnerDetails_billingContact_email':'',
            'partnerDetails_billingContact_name':'',
            'partnerDetails_billingContact_address1':'',
            'partnerDetails_billingContact_address2':'',
            'partnerDetails_billingContact_city':'',
            'partnerDetails_billingContact_state':'',
            'partnerDetails_billingContact_postcode':'',
            'partnerDetails_billingContact_phone':'',
            'partnerDetails_billingContact_extras':'',
            'attribution_channel':'',
            'attribution_campaignName':'',
            'attribution_campaignSource':'',
            'attribution_campaignMedium':'',
            'attribution_campaignContent':'',
            'attribution_extras':''
        }
        self.headers = self.template_row.keys()
        self.table = []

    def __append (self, json_result):
        print('processing: ' + json_result['_links']['self']['href'])
        for license in json_result['licenses']:
            # we only record licenses with attributions liceneses that have been updated within the range specifified
            if (('attribution' in license) and (datetime.strptime(license['lastUpdated'],"%Y-%m-%d").replace(tzinfo=pytz.UTC)<=self.criteria.end_date)):
                data_row = copy.deepcopy(self.template_row)
                for name, value in license.items():
                    if (name == 'addonLicenseId'):
                        data_row.update(core_addonLicenseId = value)
                    elif (name == 'hostLicenseId'):
                        data_row.update(core_hostLicenseId = value)
                    elif (name == 'licenseId'):
                        data_row.update(core_licenseId = value)
                    elif (name == 'addonKey'):
                        data_row.update(core_addonKey = value)
                    elif (name == 'addonName'):
                        data_row.update(core_addonName = value)
                    elif (name == 'hosting'):
                        data_row.update(core_hosting = value)
                    elif (name == 'lastUpdated'):
                        data_row.update(core_lastUpdated = value)
                    elif (name == 'licenseType'):
                        data_row.update(core_licenseType = value)
                    elif (name == 'maintenanceStartDate'):
                        data_row.update(core_maintenanceStartDate = value)
                    elif (name == 'maintenanceEndDate'):
                        data_row.update(core_maintenanceEndDate = value)
                    elif (name == 'status'):
                        data_row.update(core_status = value)
                    elif (name == 'tier'):
                        data_row.update(core_tier = value)
                    elif (name == 'contactDetails'):
                        for name, value in value.items():
                            if (name == 'company'):
                                data_row.update(contactDetails_company = value)
                            elif (name == 'country'):
                                data_row.update(contactDetails_country = value)
                            elif (name == 'region'):
                                data_row.update(contactDetails_region = value)
                            elif (name == 'technicalContact'):
                                for name, value in value.items():
                                    if (name == 'email'):
                                        data_row.update(contactDetails_technicalContact_email = value)
                                    elif (name == 'name'):
                                        data_row.update(contactDetails_technicalContact_name = value)
                                    elif (name == 'address1'):
                                        data_row.update(contactDetails_technicalContact_address1 = value)
                                    elif (name == 'address2'):
                                        data_row.update(contactDetails_technicalContact_address2 = value)
                                    elif (name == 'city'):
                                        data_row.update(contactDetails_technicalContact_city = value)
                                    elif (name == 'state'):
                                        data_row.update(contactDetails_technicalContact_state = value)
                                    elif (name == 'postcode'):
                                        data_row.update(contactDetails_technicalContact_postcode = value)
                                    elif (name == 'phone'):
                                        data_row.update(contactDetails_technicalContact_phone = value)
                                    else:
                                        contactDetails_technicalContact_extras = data_row['contactDetails_technicalContact_extras']
                                        contactDetails_technicalContact_extras += ("(" + name + "=" + json.dumps(value) + ")")
                                        data_row.update(contactDetails_technicalContact_extras = contactDetails_technicalContact_extras)
                            elif (name == 'billingContact'):
                                for name, value in value.items():
                                    if (name == 'email'):
                                        data_row.update(contactDetails_billingContact_email = value)
                                    elif (name == 'name'):
                                        data_row.update(contactDetails_billingContact_name = value)
                                    elif (name == 'address1'):
                                        data_row.update(contactDetails_billingContact_address1 = value)
                                    elif (name == 'address2'):
                                        data_row.update(contactDetails_billingContact_address2 = value)
                                    elif (name == 'city'):
                                        data_row.update(contactDetails_billingContact_city = value)
                                    elif (name == 'state'):
                                        data_row.update(contactDetails_billingContact_state = value)
                                    elif (name == 'postcode'):
                                        data_row.update(contactDetails_billingContact_postcode = value)
                                    elif (name == 'phone'):
                                        data_row.update(contactDetails_billingContact_phone = value)
                                    else:
                                        contactDetails_billingContact_extras = data_row['contactDetails_billingContact_extras']
                                        contactDetails_billingContact_extras += ("(" + name + "=" + json.dumps(value) + ")")
                                        data_row.update(contactDetails_billingContact_extras = contactDetails_billingContact_extras)
                            else:
                                contactDetails_extras = data_row['contactDetails_extras']
                                contactDetails_extras += ("(" + name + "=" + json.dumps(value) + ")")
                                data_row.update(contactDetails_extras = contactDetails_extras)
                    elif (name == 'partnerDetails'):
                        for name, value in value.items():
                            if (name == 'partnerName'):
                                data_row.update(partnerDetails_partnerName = value)
                            elif (name == 'partnerType'):
                                data_row.update(partnerDetails_partnerType = value)
                            elif (name == 'technicalContact'):
                                for name, value in value.items():
                                    if (name == 'email'):
                                        data_row.update(partnerDetails_technicalContact_email = value)
                                    elif (name == 'name'):
                                        data_row.update(partnerDetails_technicalContact_name = value)
                                    elif (name == 'address1'):
                                        data_row.update(partnerDetails_technicalContact_address1 = value)
                                    elif (name == 'address2'):
                                        data_row.update(partnerDetails_technicalContact_address2 = value)
                                    elif (name == 'city'):
                                        data_row.update(partnerDetails_technicalContact_city = value)
                                    elif (name == 'state'):
                                        data_row.update(partnerDetails_technicalContact_state = value)
                                    elif (name == 'postcode'):
                                        data_row.update(partnerDetails_technicalContact_postcode = value)
                                    elif (name == 'phone'):
                                        data_row.update(partnerDetails_technicalContact_phone = value)
                                    else:
                                        partnerDetails_technicalContact_extras = data_row['partnerDetails_technicalContact_extras']
                                        partnerDetails_technicalContact_extras += ("(" + name + "=" + json.dumps(value) + ")")
                                        data_row.update(partnerDetails_technicalContact_extras = partnerDetails_technicalContact_extras)
                            elif (name == 'billingContact'):
                                for name, value in value.items():
                                    if (name == 'email'):
                                        data_row.update(partnerDetails_billingContact_email = value)
                                    elif (name == 'name'):
                                        data_row.update(partnerDetails_billingContact_name = value)
                                    elif (name == 'address1'):
                                        data_row.update(partnerDetails_billingContact_address1 = value)
                                    elif (name == 'address2'):
                                        data_row.update(partnerDetails_billingContact_address2 = value)
                                    elif (name == 'city'):
                                        data_row.update(partnerDetails_billingContact_city = value)
                                    elif (name == 'state'):
                                        data_row.update(partnerDetails_billingContact_state = value)
                                    elif (name == 'postcode'):
                                        data_row.update(partnerDetails_billingContact_postcode = value)
                                    elif (name == 'phone'):
                                        data_row.update(partnerDetails_billingContact_phone = value)
                                    else:
                                        partnerDetails_billingContact_extras = data_row['partnerDetails_billingContact_extras']
                                        partnerDetails_billingContact_extras += ("(" + name + "=" + json.dumps(value) + ")")
                                        data_row.update(partnerDetails_billingContact_extras = partnerDetails_billingContact_extras)
                            else:
                                partnerDetails_extras = data_row['partnerDetails_extras']
                                partnerDetails_extras += ("(" + name + "=" + json.dumps(value) + ")")
                                data_row.update(partnerDetails_extras = partnerDetails_extras)
                    elif (name == 'attribution'):
                        for name, value in value.items():
                            if (name == 'channel'):
                                data_row.update(attribution_channel = value)
                            elif (name == 'campaignName'):
                                data_row.update(attribution_campaignName = value)
                            elif (name == 'campaignSource'):
                                data_row.update(attribution_campaignSource = value)
                            elif (name == 'campaignMedium'):
                                data_row.update(attribution_campaignMedium = value)
                            elif (name == 'campaignContent'):
                                data_row.update(attribution_campaignContent = value)
                            else:
                                attribution_extras = data_row['attribution_extras']
                                attribution_extras += ("(" + name + "=" + json.dumps(value) + ")")
                                data_row.update(attribution_extras = attribution_extras)
                    else:
                        core_extras = data_row['core_extras']
                        core_extras += ("(" + name + "=" + json.dumps(value) + ")")
                        data_row.update(core_extras = core_extras)
                self.table.append(data_row.values())

    def report(self):
        FILE_DATE = time.strftime("%Y%m%d")
        # get vendor licenses
        parms = {
            'limit':'50',
            'lastUpdated':self.criteria.beg_date.strftime("%Y-%m-%d"),
            'licenseType':'evaluation'
        }
        result = self.client.get('/rest/2/vendors/' + self.criteria.vendor + '/reporting/licenses', parms)
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
        # write table for reference
        #outfile = open('/var/data/' + FILE_DATE + '_vendor' + VENDOR + '_attributions' + '.txt', 'w')
        #print(tabulate(table, headers=headers, tablefmt='simple', floatfmt='.2f'), file = outfile)
        #outfile.close()
        # write table for reference
        outfile = open('/var/data/' + FILE_DATE + '_vendor' + self.criteria.vendor + '_attributions' + '.csv', 'w')
        writer=csv.writer(outfile)
        writer.writerow(self.headers)
        writer.writerows(self.table)
        outfile.close()
