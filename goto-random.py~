import nrega

import os, random, json

with open('data/villages_dict.json','r') as infile:
  addresses = json.loads(infile.read())
  our_district = addresses[random.choice(addresses.keys)]
  our_mandal = addresses[our_district][random.choice(addresses[our_district].keys)]
  our_panchayat = addresses[our_district][our_mandal][random.choice(addresses[our_district][our_mandal].keys)]
  our_village = addresses[our_district][our_mandal][our_panchayat][random.choice(addresses[our_district][our_mandal][our_panchayat].keys)]

  go_to_place(district=our_district,
              mandal=our_mandal,
              panchayat=our_panchayat,
              village=our_village)
  
