import nrega

import os, random, json

with open('data/villages_dict.json','r') as infile:
  addresses = json.loads(infile.read())

  def not_all(string):
    if string == 'ALL': return False
    else: return True

  our_district = random.choice(filter(not_all,addresses.keys()))
  our_mandal = random.choice(filter(not_all,addresses[our_district].keys()))
  our_panchayat = random.choice(filter(not_all,addresses[our_district][our_mandal].keys()))
  our_village = random.choice(filter(not_all,addresses[our_district][our_mandal][our_panchayat].keys()))

  print "Randomly selected:"
  print "District: {0}".format(our_district)
  print "Mandal: {0}".format(our_mandal)
  print "Panchayat: {0}".format(our_panchayat)
  print "Village: {0}".format(our_village)

  nrega.go_to_place(option="Total Works Overall Status",
                    district=our_district,
                    mandal=our_mandal,
                    panchayat=our_panchayat,
                    village=our_village,
                    year="2013-2014" )

  nrega.browser.find_element_by_id("Excel").click()
  """function ExportExcel()
{
	var url="/Nregs/FrontServlet?requestType=Common_engRH&actionVal=ExportToExcel&ExcelId=Overallworksstatus"
		  
		window.open(url, "newWin", "width=800,height=600,directories=yes,location=yes,menubar=yes,scrollbars=yes,status=yes,toolbar=yes,resizable=yes");   
}
"""
