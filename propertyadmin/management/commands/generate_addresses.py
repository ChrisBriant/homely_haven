
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError 
from django.conf import settings
from urllib.request import Request, urlopen, HTTPError
# from warmplaceadmin.random_words import load_words_from_file
import random, os
#from collections import Counter
#from datetime import time, datetime
from propertyadmin.models import *

def load_words_from_file(file_path):
    lines = []
    word_file_path = os.path.join(settings.BASE_DIR, file_path)
    with open(word_file_path,'r') as word_file:
        for line in word_file:
            lines.append(line.strip())
    return lines


class Command(BaseCommand):
    help = 'Generate fake addresses.'

    def add_arguments(self, parser):
        # Optional argument
        parser.add_argument('--amount', type=str, help='Amount of addresses to create')
        parser.add_argument('--postcode', type=str,nargs='+', help='Postcode to base addresses')

    def handle(self, *args, **options):
        #default
        amount = 1
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        addresses = []

        if not options['postcode']:
            raise CommandError('You must supply a vallue for --postcode')
        if options['amount']:
            amount = options['amount']
        street_names = load_words_from_file('street_names.txt')

        for i in range(0,int(amount)):
            random_house_number = random.randint(1, 1000)
            address_line_one = str(random_house_number) + ' ' + random.sample(street_names,k=1)[0]
            address_line_two = District.objects.filter(code=options['postcode'][0]).first().name
            address_line_three = options['postcode'][0] + ' ' + str(random.randint(1,10)) + ''.join(random.sample(letters,k=2))
            addresses.append({
                'address_line_one' : address_line_one,
                'address_line_two' : address_line_two,
                'address_line_three' : address_line_three
            })
            #Create in database
            Property.objects.create(
                address_line_one = address_line_one,
                town = address_line_two,
                postcode = address_line_three,
            )

        print(addresses)
        self.stdout.write(self.style.SUCCESS(f'Addresses have been output'))