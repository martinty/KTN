import json

addressbook = {}
addressbook['Martin'] = {
    'name': 'Martin', 'address': 'Alfred getz 2', 'phone':34435667
}

addressbook['Adshy'] = {
    'name': 'Adshy', 'address': 'eirik jarls gate 2', 'phone':41277119
}

s = json.dumps(addressbook)
print addressbook
print s

k  = json.loads(s)
print k
number = k['Adshy']['phone']
print number