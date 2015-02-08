
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

