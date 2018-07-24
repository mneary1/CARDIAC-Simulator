from tkinter import Tk, Label, Entry, END, simpledialog

class CardiacGui:

	#instruction constants
	INP_OPCODE = 0
	LDA_OPCODE = 1
	ADD_OPCODE = 2
	BLZ_OPCODE = 3
	SHF_OPCODE = 4
	OUT_OPCODE = 5
	STO_OPCODE = 6
	SUB_OPCODE = 7
	JMP_OPCODE = 8
	HLT_OPCODE = 9

	CLOCK_SPEED = 1500 #speed in milliseconds

	def __init__(self, master):
		self.master = master
		master.title("CARDIAC Simulator")
		master.geometry("1000x1000")

		self.acc = 0 #accumulator
		self.input = 0 #input
		self.output = 0 #output
		self.pc = 0 #program counter
		self.ir = 0 #instruction registers

		self.memory = [0] * 100 #100 empty memory cells
		self.memory[0] = 1
		self.memory_labels = []


		#load a program into memory for now
		#prog = [34, 35, 134, 235, 636, 536, 900]
		#self.pc = 15
		prog = [3, 441, 103, 710, 342, 211, 611, 441, 110, 200, 610, 831, 511, 900]
		self.pc = 30
		#prog = [68, 404, 669, 70, 170, 700, 670, 319, 169, 268, 669, 811, 569, 900]
		#self.pc = 7
		self.pc_prev = 7
		for i in range(len(prog)):
			self.memory[self.pc + i] = prog[i]

		
		#construct the memory cells on the scene
		for i in range(10):
			for j in range(10):
				cell_num = i*10 + j
				label_text = self.pad(self.memory[cell_num])
				l = Label(master, text=label_text, borderwidth=10)
				self.memory_labels.append(l)
				l.grid(row=i, column=j)

		#add accumulator to the scene
		self.acc_label = Label(master, text="ACC", bg='gray80')
		self.acc_label.grid(row = 0, column=11, sticky="ew")
		self.acc_value_label = Label(master, text=self.pad(self.acc))
		self.acc_value_label.grid(row=0, column=12)

		#add input to the scene
		self.input_label = Label(master, text="INP", bg='gray80')
		self.input_label.grid(row = 1, column=11, sticky="ew")
		self.input_value_label = Label(master, text=self.pad(self.input))
		self.input_value_label.grid(row=1, column=12)

		#add output to the scene
		self.output_label = Label(master, text="OUT", bg='gray80')
		self.output_label.grid(row=2, column=11, sticky="ew")
		self.output_value_label = Label(master, text=self.pad(self.output))
		self.output_value_label.grid(row=2, column=12)

		#add Instruction Register to scene
		self.ir_label = Label(master, text="IR", bg='gray80')
		self.ir_label.grid(row=3, column=11, sticky="ew")
		self.ir_value_label = Label(master, text=self.pad(self.ir))
		self.ir_value_label.grid(row=3, column=12)

		#add Program Counter to scene
		self.pc_label = Label(master, text="PC", bg='gray80')
		self.pc_label.grid(row=4, column=11, sticky="ew")
		self.pc_value_label = Label(master, text=str(self.pc))
		self.pc_value_label.grid(row=4, column=12)

		#kick off the simulation
		self.master.after(3000, self.simulate)

	def pad(self, instruction):
		text = str(instruction)
		if len(text) < 3:
			text = '0' * (3 - len(text)) + text
		return text

	def reset_colors(self):
		self.acc_value_label['bg'] = 'white'
		self.memory_labels[self.pc_prev]['bg'] = 'white'

	def simulate(self):
	
		self.reset_colors()

		#fetch the next instruction
		self.ir = self.memory[self.pc]
		self.ir_value_label['text'] = self.pad(self.ir)
		self.memory_labels[self.pc]['bg'] = 'yellow'
		self.pc_value_label = str(self.pc)

		#decode the instruction
		opcode = self.ir // 100 #first number is instruction [0-9]
		memory_cell = self.ir % 100  #last two numbers is memory cell to work with [00-99]
		jumped = False

		if opcode == CardiacGui.INP_OPCODE:
			num = int(simpledialog.askstring("Number prompt", "Enter a number: "))
			self.input_value_label['text'] = self.pad(num)
			self.memory[memory_cell] = num
			self.memory_labels[memory_cell]['text'] = self.memory[memory_cell]

		elif opcode == self.LDA_OPCODE:
			self.acc = self.memory[memory_cell]
			self.acc_value_label['text'] = str(self.acc)

		elif opcode == self.ADD_OPCODE:
			self.acc = self.acc + self.memory[memory_cell]
			self.acc_value_label['text'] = str(self.acc)
			self.acc_value_label['bg'] = 'yellow'

		elif opcode == self.BLZ_OPCODE:
			if self.acc < 0:
				self.pc_prev = self.pc
				jumped = True
				self.pc = memory_cell - 1 #so advancing the PC will still work 

		elif opcode == CardiacGui.SHF_OPCODE: #TODO: make sure this works
			try:
				left = self.memory[memory_cell] // 10
				right = self.memory[memory_cell] % 10
				print("left:", left)
				print("right:", right)
				print("acc:", self.acc)
				shift = 10 ** left
				self.acc = self.acc * shift % 10000
				print("after left:", self.acc)
				shift = 10 ** right
				self.acc = self.acc // shift 
				print("after right:", self.acc)
			except:
				pass
			print()

		elif opcode == CardiacGui.OUT_OPCODE:
			self.output = self.memory[memory_cell]
			self.output_value_label['text'] = self.pad(self.output)

		elif opcode == CardiacGui.STO_OPCODE:
			self.memory[memory_cell] = self.acc
			self.memory_labels[memory_cell]['text'] = str(self.memory[memory_cell])

		elif opcode == CardiacGui.SUB_OPCODE:
			self.acc = self.acc - self.memory[memory_cell]
			self.acc_value_label['text'] = str(self.acc)

		elif opcode == CardiacGui.JMP_OPCODE:
			self.pc_prev = self.pc
			jumped = True
			self.pc = memory_cell - 1 #so the advance doesnt break it

		#advance the program counter
		if not jumped:
			self.pc_prev = self.pc 

		self.pc += 1

		#advance to the next instruction after one turn of the "clock"
		if opcode != self.HLT_OPCODE:
			self.master.after(CardiacGui.CLOCK_SPEED, self.simulate)
		
root = Tk()	
cardiac_gui = CardiacGui(root)
root.mainloop()