from fuji.generalclass import checkToken
from fuji.settingsclass import get, unset
from os import remove
def getPath(tkn):
	if checkToken(tkn,True) == False:
		return("")
	prst = get("fuji-api","persist")
	if type(prst) == bool and prst == True:
		return("/usr/share/fuji/pst_tmp_"+tkn+".txt")
	return("/tmp/tfile_"+tkn+".txt")
def writeLines(tkn,lns):
	if checkToken(tkn,True) == False or not type(lns) == list or lns == []:
		return(False)
	badType = False
	for l in range(len(lns)):
		if not type(lns[l]) == str:
			badType = True
			break
		if lns[l].endswith("\n") == False:
			lns[l] = lns[l] + "\n"
	try:
		f = open(getPath(tkn),"w")
	except:
		return(False)
	f.writelines(lns)
	f.close()
	return(True)
def append(tkn,val):
	if checkToken(tkn) == False or not type(val) == str:
		return(False)
	if val.endswith("\n") == False:
		val = val + "\n"
	try:
		f = open(getPath(tkn),"a")
		f.write(val)
		f.close()
	except:
		return(False)
	return(True)
def readLines(tkn,pttrn=""):
	if checkToken(tkn) == False:
		return([])
	if not type(pttrn) == str:
		pttrn = ""
	pth = getPath(tkn)
	try:
		f = open(pth,"r")
		lines = f.readlines()
		f.close()
	except:
		return([])
	if not pth.find("/usr/share/") < 0:
		remove(pth)
	if not pttrn == "":
		olist = []
	for l in range(len(lines)):
		lines[l].replace("\n","")
		if not pttrn == "" and not lines[l].find(pttrn) < 0:
			olist.append(lines[l])
	return(lines)
