from datetime import datetime
from os import geteuid
from sys import version
def getVersion():
	return("1.0.0")
def getDate(fmt="uk"):
	now = datetime.now()
	if not type(fmt) == str:
		fmt="uk"
	if fmt.lower() == "uk":
		return(now.strftime("%d/%m/%Y"))
	elif fmt.lower() == "us":
		return(now.strftime("%Y/%m/%d"))
	else:
		return(now.strftime(fmt))
def getTime(fmt="%H:%M:%S"):
	now = datetime.now()
	if not type(fmt) == str:
		fmt="%H:%M:%S"
	return(now.strftime(fmt))
def getDateTime(fmt="uk",jnr="@"):
	now = datetime.now()
	if not type(fmt) == str:
		fmt="uk"
	if not type(jnr) == str:
		jnr="@"
	if fmt.lower() == "uk":
		return(now.strftime("%d/%m/%Y "+jnr+" %H:%M:%S"))
	elif fmt.lower() == "us":
		return(now.strftime("%Y/%m/%d "+jnr+" %H:%M:%S"))
	else:
		return(now.strftime(fmt))
def checkToken(tkn,ibl=False):
	if not type(ibl) == bool:
		ibl = False
	if type(tkn) == str and 3 < len(tkn) < 17:
		badChar = False
		exceptions = "1234567890-_."
		for c in range(len(tkn)):
			if tkn[c].isalpha() == False and exceptions.find(tkn[c]) < 0:
				badChar = True
				break
		if badChar == True:
			return(False)
		if ibl == True:
			return(True)
		try:
			f = open("/usr/share/stech/api/blacklist.txt","r")
			lines = f.readlines()
			f.close()
		except:
			lines = []
		if lines == []:
			return(True)
		found = False
		for l in range(len(lines)):
			if lines[l] == tkn+"\n":
				found = True
				break
		return(not found)
	return(False)
def checkRoot():
	return(geteuid() == 0)
def combineLists(l1,l2):
	if not type(l1) == list or not type(l2) == list:
		return([])
	for a in range(len(l2)):
		found = False
		for b in range(len(l1)):
			if type(l2[a]) == type(l1[b]) and l2[a] == l1[b]:
				found = True
				break
		if found == False:
			l1.append(l2[a])
	return(l1)
def alignList(li):
	if not type(li) == list:
		return([])
	olist = []
	for i in range(len(li)):
		if type(li[i]) == str:
			if not li[i] == "":
				olist.append(li[i])
		elif type(li[i]) == list:
			if not li[i] == []:
				olist.append(li[i])
		else:
			olist.append(li[i])
	return(olist)
def insertList(li,val,pos):
	if not type(li) == list or not type(pos) == int or 0 > pos > len(li):
		return([])
	olist = []
	for l in range(len(li)):
		if l == pos:
			olist.append(val)
		olist.append(li[l])
	return(olist)
def pythonVersion():
	v = version.split(" ")[0].split(".")
	return(v[0]+"."+v[1])
