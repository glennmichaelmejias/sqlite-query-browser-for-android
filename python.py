import Tkinter as tk
import structure
from structure import *
import ttk
from Tkinter import *
from ttk import *
import tkMessageBox as msgbox


root = tk.Tk(className=" SQLite Query Browser for Android")
root.geometry("600x450")
packagename="ecandroid.ebs.ec"

m1 = PanedWindow()
frmpackage = LabelFrame(m1, text="Packagename",width=200,height=50)
txtpackage = tk.Entry(frmpackage)
txtpackage.insert(0,packagename)
txtpackage.pack(fill="x",padx=5,pady=5)
def applypackage():
	setpackagename("ecandroid.ebs.ec");
	refreshdevices()

btnapply = Button(frmpackage, text ="Apply",command=applypackage)
btnapply.pack(fill="x",padx=5,pady=5)

m1.add(frmpackage)

frmdevices = LabelFrame(m1, text="Android Devices",width=200,height=50)
lstdevices = Listbox(frmdevices,height=3)

def refreshdevices():
	devices = getdevices()
	lstdevices.delete(0,END)
	for dev in devices:
		if dev != "":
			lstdevices.insert(1,dev)

def selectdevices(event):
	setdevices(lstdevices.get(lstdevices.curselection()))
	databases = getdatabases()
	lstdatabases.delete(0,END)
	for db in databases:
		if db !="":
			lstdatabases.insert(1,db)

lstdevices.pack(fill="x",padx=5,pady=5)
lstdevices.bind('<Double-Button-1>',selectdevices)

m1.add(frmdevices)

frmdatabase = LabelFrame(m1, text="Databases",width=200,height=50)
lstdatabases = Listbox(frmdatabase,height=3)
lstdatabases.pack(fill="y",padx=5,pady=5)

def selectdb(event):
	global db
	db = lstdatabases.get(lstdatabases.curselection())
	pulldatabase(db)
	tables = pulltables();
	lsttables.delete(0,END)
	for table in tables:
		if table !="":
			lsttables.insert(1,table)

lstdatabases.bind('<Double-Button-1>',selectdb)
m1.add(frmdatabase)

frmtables = LabelFrame(m1, text="Tables",width=200,height=50)
lsttables = Listbox(frmtables,height=3)
lsttables.pack(fill="y",expand="yes",padx=5,pady=5)

def selecttable(event):
	global table
	table = lsttables.get(lsttables.curselection())
	settable(table)
	txtquery.delete(1.0,END)
	txtquery.insert(1.0,"SELECT * FROM " + table)
	sqlquery(txtquery.get(1.0,END))

def sqlquery(query):
	columns,rows = execquery(query)
	colcount=0
	columnsid = []
	for col in columns:
		columnsid.append(colcount)
		colcount +=1

	tree['columns'] = columnsid
	colcount=0
	for col in columns:
		tree.column(colcount, width=100, anchor='center',stretch=NO)
		tree.heading(colcount, text=col)
		colcount += 1
	tree.column("#0", width=0,stretch=NO)
	tree.delete(*tree.get_children())
	rowcount=0;
	for row in rows:
		theval = []
		for item in row:
			theval.append(item)

		tree.insert('',"end",rowcount,values=theval)
		rowcount += 1
	
lsttables.bind('<Double-Button-1>',selecttable)
m1.add(frmtables)

m1.pack(side="left", fill="y",padx=10,pady=10)

m2 = PanedWindow()

frmquery = LabelFrame(m2, text="Query",width=100,height=100)
txtquery = Text(frmquery,height=5)
txtquery.pack(fill="x",padx=10,pady=10)
def btnexecute():
	sqlquery(txtquery.get(1.0,END))
	
btnexecute = Button(frmquery,text="execute",width=10,command=btnexecute)
btnexecute.pack(side="left",padx="10")
m2.add(frmquery)

frmresult = LabelFrame(m2, text="Result",width=100,height=100)

tree = ttk.Treeview(frmresult)
tree.pack(fill="both",expand="yes",padx=10,pady=10)

vsb = ttk.Scrollbar(tree, orient="vertical", command=tree.yview)
vsb.pack(side='right', fill='y')
tree.configure(yscrollcommand=vsb.set)

m2.add(frmresult)
m2.pack(side="left", fill="both", expand="yes",padx=10,pady=10)

root.mainloop()