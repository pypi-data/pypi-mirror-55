from os.path import exists
from fuji.generalclass import checkToken, alignList
def __checkstr__(val):
	if not val.find("\n") < 0:
		return(False)
	badChars = "{|}"
	for c in range(len(val)):
		if not badChars.find(val[c]) < 0:
			return(False)
	return(True)
def __convert__(val):
	val = val.replace("\n","")
	if val.lower() == "false":
		return(False)
	elif val.lower() == "true":
		return(True)
	elif val.endswith("}") == True:
		val = val.replace("{","")
		val = val.replace("}","")
		return(val.split("|"))
	try:
		return(int(val))
	except:
		return(val)
def getList(tkn):
	if checkToken(tkn,True) == False:
		return([])
	try:
		f = open("/usr/share/fuji/api/reg_"+tkn+".txt","r")
		lines = f.readlines()
		f.close()
	except:
		return([])
	olist = []
	for l in range(len(lines)):
		if not lines[l].find("#") == 0:
			olist.append(lines[l].split(" : ")[0])
	return(olist)
def get(tkn,ttl,sf=False):
	if checkToken(tkn,True) == False or checkToken(ttl,True) == False:
		return([])
	if not type(sf) == bool:
		sf = False
	try:
		f = open("/usr/share/fuji/api/reg_"+tkn+".txt","r")
		lines = f.readlines()
		f.close()
	except:
		return([])
	for l in range(len(lines)):
		if not lines[l].find("#") == 0 and lines[l].split(" : ")[0] == ttl:
			r = lines[l].split(" : ")[1]
			if sf == False or r.endswith("}\n"):
				r = __convert__(r)
				if not type(r) == list or sf == True:
					return(r)
				for v in range(len(r)):
					r[v] == __convert__(r[v])
			return(r)
	return("")
def set(tkn,ttl,val):
	if checkToken(tkn,True) == False or checkToken(ttl,True) == False:
		return(False)
	if type(val) == list:
		ostr = "{"
		for e in range(len(val)):
			if (type(val[e]) == str and __checkstr__(val[e]) == False) and not (type(val) == int or type(val) == bool):
				return(False)
			if not e == 0:
				ostr = ostr + "|"
			ostr = ostr + str(val[e])
		ostr = ostr + "}"
		val = ostr
	elif not (type(val) == str or type(val) == int or type(val) == bool):
		return(False)
	print(val)
	if exists("/usr/share/fuji/api/reg_"+tkn+".txt") == False:
		try:
			f = open("/usr/share/fuji/api/reg_"+tkn+".txt","w")
			f.write("# Please try to avoid editing this file manually if possible.\n")
			f.write(ttl+" : "+str(val)+"\n")
			f.close()
			return(True)
		except:
			return(False)
	try:
		f = open("/usr/share/fuji/api/reg_"+tkn+".txt","r")
		lines = f.readlines()
		f.close()
	except:
		return(False)
	found = False
	for l in range(len(lines)):
		if not lines[l].find("#") == 0 and lines[l].split(" : ")[0] == ttl:
			found = True
			lines[l] = ttl+" : "+str(val)+"\n"
			break
	if found == False:
		lines.append(ttl+" : "+str(val)+"\n")
	try:
		f = open("/usr/share/fuji/api/reg_"+tkn+".txt","w")
		f.writelines(lines)
		f.close()
	except:
		return(False)
	return(True)
def unset(tkn,ttl):
	if checkToken(tkn,True) == False or checkToken(ttl,True) == False:
		return(False)
	try:
		f = open("/usr/share/fuji/api/reg_"+tkn+".txt","r")
		lines = f.readlines()
		f.close()
	except:
		return(False)
	olist = []
	for l in range(len(lines)):
		if lines[l].find(ttl+" : ") < 0:
			olist.append(lines[l])
			break
	try:
		f = open("/usr/share/fuji/api/reg_"+tkn+".txt","w")
		f.writelines(olist)
		f.close()
		return(True)
	except:
		return(False)
def unsetAll(tkn):
	if checkToken(tkn,True) == False:
		return(False)
	lst = getList(tkn)
	if lst == []:
		return(False)
	for s in range(len(lst)):
		if unset(tkn,lst[s]) == False:
			return(False)
	return(True)
