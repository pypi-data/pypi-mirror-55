from generalclass import checkToken, getDateTime
def write(tkn,val):
	if not type(tkn) == str or not type(val) == str or checkToken(tkn) == False:
		return(False)
	try:
		f = open("/usr/share/stech/api/log.txt","a")
		f.write(tkn+": "+getDateTime()+": "+val)
		f.close()
		return(True)
	except:
		return(False)
def read(cnt,tkn=""):
	if not type(cnt) == int:
		cnt=5
	if checkToken(tkn) == False:
		tkn=""
	try:
		f = open("/usr/share/stech/api/log.txt","r")
		lines = f.readlines()
		f.close()
	except:
		lines = []
	if lines == []:
		return([])
	if cnt == 0 or cnt > len(lines):
		cnt = len(lines)
	lines.reverse()
	olist = []
	for e in range(cnt):
		if not tkn == "" and lines[e].split(":")[0] == tkn:
			olist.append(lines[e])
		else:
			olist.append(lines[e])
	return(olist)
