
from django.core.management.base import BaseCommand #, CommandError
from django.db.utils import IntegrityError 
#from django.conf import settings
from urllib.request import Request, urlopen, HTTPError
# from warmplaceadmin.random_words import load_words_from_file
from bs4 import BeautifulSoup
#import random, requests, json, re
#from collections import Counter
#from datetime import time, datetime
from propertyadmin.models import *

#https://www.warmwelcome.uk/#find-a-space
postcodes = ['AB','AL','B','BA','BB','BD','BF','BH','BL','BN','BR','BS','BT','CA','CB','CF','CH','CM','CO','CR','CT','CV','CW','DA','DD','DE','DG','DH','DL','DN','DT','DY','E','EC','EH','EN','EX','FK','FY','G','GL','GU','HA','HD','HG','HP','HR','HS','HU','HX','IG','IP','IV','KA','KT','KW','KY','L','LA','LD','LE','LL','LN','LS','LU','M','ME','MK','ML','N','NE','NG','NN','NP','NR','NW','OL','OX','PA','PE','PH','PL','PO','PR','RG','RH','RM','S','SA','SE','SG','SK','SL','SM','SN','SO','SP','SR','SS','ST','SW','SY','TA','TD','TF','TN','TQ','TR','TS','TW','UB','W','WA','WC','WD','WF','WN','WR','WS','WV','YO','ZE',]
day_keys = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']


def get_soup(request):
    source_code = None
    try:
        data = urlopen(request)
        data_bytes = data.read()
        source_code = data_bytes.decode('utf8')
        data.close()
    except HTTPError as e:
        print(e.fp.read())
        return None
    return BeautifulSoup(source_code, 'html.parser')


class Command(BaseCommand):
    help = 'Get postcodes.'

    def handle(self, *args, **options):

        districts = []

        hdr = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Mobile Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive',
        }


        for postcode in postcodes:
            req = Request(
                f'https://www.doogal.co.uk/UKPostcodes?Search={postcode}',
                data=None,
                headers = hdr
            )
            soup = get_soup(req)

            if soup:
                target = soup.find_all('h4',text='Filter by district')[0]
                links = target.find_next_siblings('a')

                for link in links:
                    #Go to the district page
                    district = link.get('href')
                    district_code = district.split('UKPostcodes?Search=')[1]
                    req = Request(
                        f'https://www.doogal.co.uk/{district}',
                        data=None,
                        headers = hdr
                    )
                    soup = get_soup(req)
                    if soup:
                        district_name = soup.find('small')
                    try:
                        District.objects.create(
                            code = district_code,
                            name = district_name.string.strip()
                        )
                    except IntegrityError as ie:
                        print(ie)
        self.stdout.write(self.style.SUCCESS(f'Postcodes have been loaded.'))