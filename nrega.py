from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException

import os, time, json

browser = webdriver.Firefox()


def go_to_wph(option="Works Progress History(Since Inception)"):
  # Go to home for the website
  browser.get('http://www.nrega.ap.gov.in/Nregs/')

  browser.find_element_by_link_text('Works').click()

  browser.find_element_by_link_text(option).click()

def go_to_place(option="",district="", mandal="", panchayat="", village="", year=None):
  go_to_wph(option=option)

  for category, name in [("District",district),
                         ("Mandal",mandal),
                         ("Panchayat",panchayat),
                         ("Village", village)]:
    option_box = Select(browser.find_element_by_id(category))
    option_box.select_by_visible_text(name)
    time.sleep(1.0)

  if year:
    Select(browser.find_element_by_id("Financial")).select_by_visible_text(year)

  browser.find_element_by_id("go").click()


def print_state():
  print "levels: {0}".format(levels)

def hierarchical_wrapper():
  try:
    get_hierarchical_dict()
  except StaleElementReferenceException:
    print "\n\n Stale Element Reference Error Suppressed \n\n"
    print_state()
    hierarchical_wrapper()

def get_hierarchical_dict():

  districts = [ d.text for d in Select(browser.find_element_by_id("District")).options ]

  for district in districts[levels[0]:]:
    print "In District  {0}:".format(district)
    options[district] = {}
    Select(browser.find_element_by_id("District")).select_by_visible_text(district)

    time.sleep(1) # sleep for 1 sec
    mandals= [m.text for m in Select(browser.find_element_by_id("Mandal")).options ]
    
    for mandal in mandals[levels[1]:]:
      print "  In Mandal {0}:".format(mandal)
      options[district][mandal] = {}
      Select(browser.find_element_by_id("District")).select_by_visible_text(district)
      Select(browser.find_element_by_id("Mandal")).select_by_visible_text(mandal)
      time.sleep(1)

      panchayats = [ p.text for p in  Select(browser.find_element_by_id("Panchayat")).options ]

      for panchayat in panchayats[levels[2]:]:
        print "    In Panchayat {0}:".format(panchayat)
        options[district][mandal][panchayat] = {}
        Select(browser.find_element_by_id("District")).select_by_visible_text(district)
        Select(browser.find_element_by_id("Mandal")).select_by_visible_text(mandal)
        Select(browser.find_element_by_id("Panchayat")).select_by_visible_text(panchayat)
        time.sleep(1)

        villages = [ v.text for v in Select(browser.find_element_by_id("Village")).options ]

        for village in villages[levels[3]:]:
          print "      {0}".format(village)
          options[district][mandal][panchayat][village] = " "
          levels[3] += 1
        levels[3] = 0
        levels[2] += 1
      with open('villages_dict.json','w') as outfile:
        json.dump(options,outfile)
        outfile.close()
      levels[2] = 0
      levels[1] += 1
    levels[1] = 0
    levels[0] += 1
