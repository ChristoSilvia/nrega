from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException

import os, time, json

browser = webdriver.Firefox()


def go_to_wph():
  # Go to home for the website
  browser.get('http://www.nrega.ap.gov.in/Nregs/')

  # Click on the works button
  works_button = browser.find_element_by_link_text('Works')
  works_button.click()

  # Click on the works progress button.  this gets us to the form.
  works_progress_button = browser.find_element_by_link_text('Work Progress History(Since Inception)')
  works_progress_button.click()

def go_to_place(district="", mandal="", panchayat="", village=""):
  go_to_wph()

  for category, name in [("District",district),
                         ("Mandal",mandal),
                         ("Panchayat",panchayat),
                         ("Village", village)]:
    Select(browser.find_element_by_id(category)).select_by_visible_text(name)
    time.sleep(0.5)


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


if __name__ == '__main__':
  go_to_wph()

  if os.path.isfile('villages_dict.json'): 
    with open('villages_dict.json','r') as infile:
      options = json.loads(infile.read())
      levels = [0,0,0,0]
      levels[0] = len(options.keys()) - 1
      levels[1] = len(options[options.keys()[-1]]) - 1
      infile.close()

  hierarchical_wrapper() 

  print json.dumps(options, sort_keys=True, indent=2)
  with open('villages_dict.json','w') as outfile:
    json.dump(options,outfile)
    outfile.close()

