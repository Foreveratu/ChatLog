import Tkconstants
from tkinter import *
import tkinter.filedialog
import re
from tkinter import scrolledtext
from tkscrolledframe import ScrolledFrame

class ChatlogViewer(Tk):
	def __init__(self):
		Tk.__init__(self)
		self.initGui()

	def initGui(self):
		self.menubar = Menu(self)
		self.config(menu=self.menubar)
		self.menufichier = Menu(self.menubar,tearoff=0)
		self.menubar.add_cascade(label="Fichier", menu=self.menufichier)
		self.menufichier.add_command(label="Ouvrir", command=self.open)
		self.menufichier.add_command(label="Quitter", command=self.destroy)

		self.ScrolledCheckBox = ScrolledFrame(self, padx=5, pady=5)
		self.ScrolledCheckBox.bind_arrow_keys(self)
		self.ScrolledCheckBox.bind_scroll_wheel(self)

		self.chkList = list()
		self.chkValueList = dict()
		self.layerCount = dict()
		self.listLayer = list()
		self.listLine = list()
		self.CheckBoxFrame = self.ScrolledCheckBox.display_widget(Frame)
		self.labelFrame = LabelFrame(self, text="Log", padx=5, pady=5)

		self.labelFrame.grid(row=0, column=0, padx=10, pady=10, sticky=E+W+N+S)
		self.ScrolledCheckBox.grid(row=0, column=1, padx=10, pady=10, sticky=E+W+N+S)

		self.columnconfigure(0, weight=30)
		self.columnconfigure(1, weight=1)
		self.rowconfigure(0, weight=1)

		self.ScrolledCheckBox.rowconfigure(0, weight=1)
		self.ScrolledCheckBox.columnconfigure(0, weight=1)
		self.labelFrame.rowconfigure(0, weight=1)
		self.labelFrame.columnconfigure(0, weight=1)
		self.CheckBoxFrame.columnconfigure(0, weight=1)
		self.CheckBoxFrame.columnconfigure(1, weight=1)

		self.hscrollbar=Scrollbar(self.labelFrame ,orient=Tkconstants.HORIZONTAL)
		self.hscrollbar.grid(row=1,column=0,sticky=E+W)

		self.vscrollbar=Scrollbar(self.labelFrame)
		self.vscrollbar.grid(row=0,column=1,sticky=N+S)

		# Create the textbox
		self.textbox = Text(self.labelFrame,wrap=NONE,bd=0,
			xscrollcommand=self.hscrollbar.set,
			yscrollcommand=self.vscrollbar.set)
		self.textbox.grid(row=0, column=0, sticky=E+W+N+S)

		self.checkAllButton = Button(self.CheckBoxFrame, text="Check all", command=self.checkAll)
		self.checkAllButton.grid(row=0, column=0, sticky=W)

		self.uncheckAllButton = Button(self.CheckBoxFrame, text="Uncheck all", command=self.uncheckAll)
		self.uncheckAllButton.grid(row=1, column=0, sticky=W)

	def handle_line(self, nb_line, line):
		line_splitted = re.split(" ", line, 2)
		#print(line_splitted)

		if (len(line_splitted) != 3):
			#print("====> Invalid skip")
			return False

		date = line_splitted[0]
		hour = line_splitted[1]
		rest = line_splitted[2].strip()

		line_splitted = re.split(" ", rest, 1)
		#print(line_splitted)

		if (len(line_splitted) != 2):
			#print("====> Invalid skip")
			return False

		pid = line_splitted [0]
		rest = line_splitted[1].strip()

		line_splitted = re.split(" ", rest, 1)
		#print(line_splitted)

		if (len(line_splitted) != 2):
			#print("====> Invalid skip")
			return False

		tid = line_splitted [0]
		rest = line_splitted[1].strip()

		line_splitted = re.split(" ", rest, 1)
		#print(line_splitted)

		if (len(line_splitted) != 2):
			#print("====> Invalid skip")
			return False

		level = line_splitted [0]
		rest = line_splitted[1]

		line_splitted = re.split(":", rest, 1)
		#print(line_splitted)

		if (len(line_splitted) != 2):
			#print("====> Invalid skip")
			return False

		layer = line_splitted[0].strip()
		log = line_splitted[1].strip()

		# print("line " + str(nb_line))
		# print(">" + date + "<")
		# print(">" + hour + "<")
		# print(">" + pid + "<")
		# print(">" + tid + "<")
		# print(">" + level + "<")
		# print(">" + layer + "<")
		# print(">" + log + "<")
		# print("=====================================")

		# if len(self.chkValueList) == 0:
			# print("chkValueList is empty")
		# else:
			# print("chkValueList is not empty ==> size %d" % len(self.chkValueList))

		if (len(self.chkValueList) > 0 and self.chkValueList[layer].get() == False):
			return False

		self.textbox.insert(INSERT, line)

		self.textbox.tag_add(nb_line, str(nb_line)+".0", str(nb_line)+".end")

		if (level == "W"):
			self.textbox.tag_config(nb_line, background="black", foreground="yellow")
		elif (level == "E"):
			self.textbox.tag_config(nb_line, background="black", foreground="red")
		elif (level == "D"):
			self.textbox.tag_config(nb_line, background="black", foreground="green")
		else:
			self.textbox.tag_config(nb_line, background="white", foreground="black")

		if (layer not in self.listLayer):
			self.listLayer.append(layer)
			self.layerCount[layer] = 1
		else:
			self.layerCount[layer] += 1

		return True

	def handleLayerCheckbox(self):
		# for layer in self.listLayer:
			# if (self.chkValueList[layer].get() == True):
				# print layer + " is selected"
		# print "======================="
		self.textbox.configure(state="normal")
		self.clearTextBox()
		self.handleListLine()
		self.textbox.configure(state="disabled")
		self.textbox.bind("<1>", lambda event: self.textbox.focus_set())
		self.hscrollbar.config(command=self.textbox.xview)
		self.vscrollbar.config(command=self.textbox.yview)

	def checkAll(self):
		#print "Check all size list %d" % len(self.chkList)
		for checkbox in self.chkList:
			checkbox.select()
		self.textbox.configure(state="normal")
		self.clearTextBox()
		self.handleListLine()
		self.textbox.configure(state="disabled")
		self.textbox.bind("<1>", lambda event: self.textbox.focus_set())
		self.hscrollbar.config(command=self.textbox.xview)
		self.vscrollbar.config(command=self.textbox.yview)

	def uncheckAll(self):
		#print "Uncheck all size list %d" % len(self.chkList)
		for checkbox in self.chkList:
			checkbox.deselect()
		self.textbox.configure(state="normal")
		self.clearTextBox()
		self.handleListLine()
		self.textbox.configure(state="disabled")
		self.textbox.bind("<1>", lambda event: self.textbox.focus_set())
		self.hscrollbar.config(command=self.textbox.xview)
		self.vscrollbar.config(command=self.textbox.yview)

	def handleListLayer(self):
		indexRow = 0
		self.chkValueList.clear()
		self.listLayer.sort(key=lambda v: v.upper())

		indexRow = 2

		for layer in self.listLayer:
			self.chkValueList[layer] = BooleanVar()
			self.chkValueList[layer].set(True)
			self.chkLayer = Checkbutton(self.CheckBoxFrame, text=layer + " ("+ str(self.layerCount[layer]) + ")", var=self.chkValueList[layer], command=self.handleLayerCheckbox)
			self.chkList.append(self.chkLayer)
			self.chkLayer.grid(row=indexRow, column=0, sticky=W)
			indexRow = indexRow +1

	def clearTextBox(self):
		self.textbox.delete('1.0', END)

	def clearCheckBoxFrame(self):
		#print "\tBefore clearing size list %d" % len(self.chkList)
		for checkbox in self.chkList:
			#print "\t\tremoving %s" % checkbox.cget("text")
			#self.chkList.remove(checkbox)
			checkbox.destroy()
		del self.chkList[:]

		#print "\tAfter clearing size list %d" % len(self.chkList)

	def handleListLine(self):
		nb_line = 0
		for line in self.listLine:
			nb_line = nb_line + 1
			if (self.handle_line(nb_line, line) == FALSE):
				nb_line = nb_line -1

	def open(self):
		self.textbox.configure(state="normal")

		filename=tkinter.filedialog.askopenfilename(
			title="Ouvrir un fichier",
			filetypes=[('logcat files','.log')])

		#print "Before open file size list %d" % len(self.chkList)

		self.clearTextBox()
		self.clearCheckBoxFrame()
		del self.listLayer[:]
		del self.listLine[:]
		self.chkValueList.clear()
		self.layerCount.clear()

		nb_line = 0

		fichier = open(filename, "r")
		while 1:
			line = fichier.readline()
			if len(line) == 0:
				break
			else:
				self.listLine.append(line)
		fichier.close()

		self.handleListLine()
		self.handleListLayer()

		#print "After open file size list %d" % len(self.chkList)
		#print "===================================="

		self.textbox.configure(state="disabled")
		self.textbox.bind("<1>", lambda event: self.textbox.focus_set())
		self.hscrollbar.config(command=self.textbox.xview)
		self.vscrollbar.config(command=self.textbox.yview)

if __name__ == "__main__":
	fenetre = ChatlogViewer()
	fenetre.mainloop()
