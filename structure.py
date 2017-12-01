import sqlite3

def runcmd(cmd):
	from subprocess import check_output
	return check_output(cmd, shell=True)

def getdevices():

	runcmd(getadb()+' devices > tmp')
	devices = []
	frombat = iter(open('tmp', 'r').read().split("\n"))
	next(frombat)
	for dev in frombat:
		devices.append(dev.split("\t")[0])
	return devices

def getdatabases():

	runcmd(getadb() + ' -s '+ device +' -d shell "run-as ' + packagename + ' ls /data/data/' + packagename + '/databases/" > tmp')
	#print open('tmp','r').read()
	frombat = open('tmp','r').read().split("\r\n")
	databases = frombat
	return databases

def setpackagename(name):
	global packagename
	packagename = name

def setdevices(dev):
	global device
	device = dev

def settable(tablename):
	global curtable
	curtable = tablename

def pulldatabase(dbname):
	runcmd(getadb() + ' -s '+ device + ' -d shell "run-as ' + packagename + ' cat /data/data/' + packagename + '/databases/' + dbname + ' > /sdcard/temp.db" > tmp');
	runcmd(getadb() + ' -s '+ device + ' pull /sdcard/temp.db > tmp')

def pulltables():
	global tables
	tables = []
	conn = sqlite3.connect('temp.db')
	c = conn.cursor()
	for row in c.execute("SELECT name FROM sqlite_master WHERE type='table';"):
	   tables.append(row[0])
	return tables

def execquery(thequery):
	conn = sqlite3.connect('temp.db')
	c = conn.execute(thequery)
	columns=[]
	rows=[]
	for col in c.description:
		columns.append(col[0])

	for row in c:
		rows.append(row)

	return columns,rows
	
def getadb():
	import psutil
	system_process_names = {'adb.exe'}
	system_processes = []

	theadb=""

	for proc in psutil.process_iter():
	    try:
	        name = proc.name().lower()
	        path = proc.exe()
	    except psutil.AccessDenied:
	        continue

	    if name in system_process_names:
	        system_process_names.remove(name)
	   
	        theadb = (path.replace("\\","/")).strip()

	if theadb != "":
		return ' "' + theadb + '"'
	else:
		return "adb"

	
