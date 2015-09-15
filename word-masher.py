#!/usr/bin/python

import Tkinter, tkFileDialog, tkMessageBox
import random
import os

# TODO turn into windows executable

class scrambler(Tkinter.Tk):
	def __init__(self, parent):
		Tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.entries = []
		self.initialize()

	def entry_row(self, tag, row):
			label = Tkinter.Label(self,anchor="w",fg="white",bg="blue", text=tag)
			label.grid(column=0,row=row,sticky='EW')

			entry = Tkinter.Entry(self)
			entry.grid(column=1, row=row, sticky='EW')		
			
			button = Tkinter.Button(self, text=u"Pick file", command=lambda: self.load_file(entry))
			button.grid(column=2,row=row, columnspan=2)

			return entry

	def load_file(self, entry):
	    file_name = tkFileDialog.askopenfilename(filetypes=(("Text files", "*.txt"),
	                                       ("All files", "*.*") ))
	    if file_name:
	        try:
	            print("Loaded file")
	        except:                     # <- naked except is a bad idea
	            showerror("Open File", "Failed to read file\n'%s'" % file_name)
	    entry.delete(0, 'end')
	    entry.insert(0, file_name)

	def initialize(self):
		self.grid()

		self.entries.append(self.entry_row("Prefixes:", 0))
		self.entries.append(self.entry_row("Roots:", 1))
		self.entries.append(self.entry_row("Infixies:", 2))
		self.entries.append(self.entry_row("Suffixes:", 3))
		
		infix_prob_label = Tkinter.Label(self,anchor="w",fg="white",bg="blue", text="Infix Probability:")
		infix_prob_label.grid(column=0,row=4,sticky='EW')
		self.infix_prob_entry = Tkinter.Entry(self)
		self.infix_prob_entry.insert(0, '0.15')
		self.infix_prob_entry.grid(column=1, row=4, sticky='EW')	
		
		# num to generate
		num_label = Tkinter.Label(self,anchor="w",fg="white",bg="blue", text="Number to generate:")
		num_label.grid(column=0,row=5,sticky='EW')
		self.num_entry = Tkinter.Entry(self)
		self.num_entry.insert(0, '10')
		self.num_entry.grid(column=1, row=5, sticky='EW')

		generate = Tkinter.Button(self, text=u"Generate Toponyms", command=self.generate)
		generate.grid(column=0,row=6, columnspan=2)

		self.grid_columnconfigure(0,weight=1)
		self.grid_rowconfigure(0,weight=1)

	def generate(self):
		print "Generating..."

		try:
		    i_prob = float(self.infix_prob_entry.get())
		except ValueError:
		    tkMessageBox.showerror("Error", "Infix probability should be between 0.00 and 1.00")
		    return

		try:
		    num_gen = int(self.num_entry.get())
		except ValueError:
		    tkMessageBox.showerror("Error", "The number to generate should be an integer")
		    return

		pf = open(self.entries[0].get())
		rf = open(self.entries[1].get())
		inf = open(self.entries[2].get())
		sf = open(self.entries[3].get())

		plist = [line[:-1] for line in pf]
		rlist = [line[:-1] for line in rf]
		ilist = [line[:-1] for line in inf]
		slist = [line[:-1] for line in sf]
		
		outFile = tkFileDialog.asksaveasfile(mode='w')
		generated = []

		i = 0
		while i < num_gen:
			if random.random() < i_prob:
				if random.random() > 0.50:
					string = random.choice(plist) + random.choice(ilist) + random.choice(rlist) + random.choice(slist)
				else:
					string = random.choice(plist) + random.choice(rlist) + random.choice(ilist) + random.choice(slist)
			else:
				string = random.choice(plist) + random.choice(rlist) + random.choice(slist)

			if string not in generated:
				if i < 10:
					gen_label = Tkinter.Label(self,anchor="w",fg="white",bg="blue", text=string)
					gen_label.grid(column=0,row=7+i,columnspan=2,sticky='EW')

				generated.append(string)
				outFile.write(string + "\n")
				i = i + 1

if __name__ == "__main__":
	app = scrambler(None)
	app.title('Word Masher')
	app.mainloop()
