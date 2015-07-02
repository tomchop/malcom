from Malcom.analytics.analytics import Analytics
from Malcom.intel.model.entities import *

a = Analytics()

a.data._db[BaseEntity.entity_graph].drop()
a.data._db[BaseEntity.entity_collection].drop()

incident = Incident("Spamvertized Dridex - wave 1970-01-01")
incident.idref = 17880
incident.save()

incident = Incident.find_one({'idref': 17880})
print incident.to_dict()
print incident['idref']
print incident

m = Malware("Dridex")
c = Malware("Cridex")
m.save()
c.save()
incident.link(m)
incident.link(c)

print "Destinations"
nn = incident.dst_link()
for n in nn:
	print n

incident2 = Incident("Spamvertized Dridex - wave 2015-01-01")
incident2.save()
incident2.link(incident)

print "Sources"
nn = incident.src_link()
for n in nn:
	print n


print "Neighbors"
nn = incident.neighbors()
for n in nn:
	print n


exit()


# Indicators / observables
email = Email("Email containing malicious Dridex Macro", value='<email_file>')  # free 
dropper_doc = File("Dridex Word payload", value='<word_file>')					# free
drop_url = URL("Intermediary script URL", value='hxxp', type=['C2', 'dropper'])	# free
payload_url = URL("Dridex dropper URL", value='hxxp', type=['C2', 'dropper'])	# free
dropper_exe = File("Dridex Word payload", value='<exe_file>', type=['dropper'])	# free
dridex_reg_key = Registry("Configuration for dridex", value='HKCU\\Software\\CSLID\\NANANA', type=['configuration'])


# Campaign / Malware
campaign = Campaign("Dridex spam campaign for 1970-01-01")						# free
malware = Malware("Dridex")														# constraint


# TTP
phishing = TTP("Phishing")														# constraint
macro = TTP("Malicious Office document with macro")								# constraint
pastebin = TTP("Uses pastebin in C2")											# constraint
config = TTP("Hides configuration data in registry")							# constraint



# Graph - easy and automatic
incident.add_observable(email)
incident.add_observable(dropper_doc)
incident.add_observable(drop_url)
incident.add_observable(payload_url)
incident.add_observable(dropper_exe)

incident.associate(phishing)
incident.associate(macro)
incident.associate(pastebin)

incident.associate(campaign)
incident.associate(malware)

# Manual? (some may be automatised)
# TTPs
malware.associate(config)
campaign.associate([phishing, macro, pastebin])

# observables / indicators
malware.associate(dridex_reg_key)
campaign.assocaite([email, dropper_doc, drop_url, payload_url, dropper_exe])




#
# 1- add ttps / observables / campaign / malware to incident
# 2- associate observables to TTPs
# 3- associate TTP to malware, campaign, or both
# 4- 
# 