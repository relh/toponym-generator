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
			
			#button = Tkinter.Button(self, text=u"Pick file", command=lambda: self.load_file(entry))
			#button.grid(column=2,row=row, columnspan=2)

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

		self.entries.append(self.entry_row("Rule", 0))
		self.entries.append(self.entry_row("Allowed vowels", 1))
		self.entries.append(self.entry_row("Allowed consonants", 2))
		self.entries.append(self.entry_row("Allowed double vowels", 3))
		self.entries.append(self.entry_row("Allowed double consonants", 4))

		infix_prob_label = Tkinter.Label(self,anchor="w",fg="white",bg="blue", text="Mutation Probability:")
		infix_prob_label.grid(column=0,row=5,sticky='EW')
		self.infix_prob_entry = Tkinter.Entry(self)
		self.infix_prob_entry.insert(0, '0.15')
		self.infix_prob_entry.grid(column=1, row=5, sticky='EW')	
		
		# num to generate
		num_label = Tkinter.Label(self,anchor="w",fg="white",bg="blue", text="Number to generate:")
		num_label.grid(column=0,row=6,sticky='EW')
		self.num_entry = Tkinter.Entry(self)
		self.num_entry.insert(0, '10')
		self.num_entry.grid(column=1, row=6, sticky='EW')

		generate = Tkinter.Button(self, text=u"Generate Toponyms", command=self.generate)
		generate.grid(column=0,row=7, columnspan=2)

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

		rule = self.entries[0].get()

		vowels = self.entries[1].get()
		consonants = self.entries[2].get()
		dvowels = self.entries[3].get()
		dconsonants = self.entries[4].get()

		vowels = [x.strip() for x in vowels.split(',')]
		consonants = [x.strip() for x in consonants.split(',')]
		dvowels = [x.strip() for x in dvowels.split(',')]
		dconsonants = [x.strip() for x in dconsonants.split(',')]
		
		# TODO drop ending commas
		#for v in vowels:
		#	if len(v) > 0:
		#		print v

		outFile = tkFileDialog.asksaveasfile(mode='w+')
		generated = []
		i = 0
		if1Flag = False
		if2Flag = False
		if1 = ""
		if2 = ""

		while i < num_gen:
			result = ""
			for symbol in rule:
				ret = ""
				if symbol == 'S':
					if random.random() < 0.33:
						ret = random.choice(consonants) + random.choice(vowels)
					elif random.random() < 0.66:
						ret = random.choice(vowels) + random.choice(consonants)
					else:
						ret = random.choice(consonants) + random.choice(vowels) + random.choice(consonants)
				elif symbol == 'V':
					ret = random.choice(vowels)
				elif symbol == 'Y':
					ret = random.choice(vowels) + random.choice(vowels)
				elif symbol == 'U':
					if random.random() < 0.50:
						ret = random.choice(vowels)
					else:
						ret = random.choice(vowels) + random.choice(vowels)
				elif symbol == 'C':
					ret = random.choice(consonants)
				# If section
				elif symbol == '(':
					if1Flag = True
					if1 = ""
				elif symbol == '|':
					if1Flag = False
					if2Flag = True
					if2 = ""
				elif symbol == ')':
					if2Flag = False
					if random.random() < 0.50:
						ret = if1
					else:
						ret = if2
				elif symbol == 'F':
					if random.random() < 0.50:
						ret = random.choice(consonants)
					else:
						ret = random.choice(consonants) + random.choice(consonants)
				elif symbol == "'":
					ret = "'";
				elif symbol == "-":
					ret = "-";
				# TODO bracketed stuff
				if if1Flag:
					if1 += ret
				elif if2Flag:
					if2 += ret
				else:
					result += ret

			if result not in generated:
				if i < 10:
					gen_label = Tkinter.Label(self,anchor="w",fg="white",bg="blue", text=result)
					gen_label.grid(column=0,row=8+i,columnspan=2,sticky='EW')
				
				generated.append(result)
				outFile.write(result + "\n")
				i = i + 1

if __name__ == "__main__":
	app = scrambler(None)
	app.title('Rule Constructed Words')
	app.mainloop()
