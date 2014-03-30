#SE3310 - Assignment 3
#Turing Machine Interpreter
#Nicholas Chang-Fong
#March 28th, 2014

import fileinput
import sys
from collections import namedtuple

trans_list = []
final_states = []
tape_list = []
Transition = namedtuple('Transition', ['current','input','next','write','move'])

#parse input
for line in fileinput.input():
	#build transitions
	if line.startswith('t'):
		s = line.split()
		del(s[0])
		trans = Transition(s[0],s[1],s[2],s[3],s[4])
		# print trans
		trans_list.append(trans)
	#build input strings
	elif line.startswith('i'):
		newstr = ""
		s = line.split()
		#append blank character to start and end of tape just because?
		s[0]='Z'
		s.append('Z')
		for l in s:
			newstr += l
		tape_list.append(newstr)
	#create list of final states
	elif line.startswith('f'):
		s = line.split()
		del(s[0])
		for stateNo in s:
			final_states.append(stateNo)
	else:
		pass
		
class Machine:
	def __init__(self,transitions,haltstates):
		self.transitions = transitions
		self.haltstates = haltstates
		#start at first actual character of input, offset for appended blank char
		self.tapePos = 1
		self.currentState = None
		self.tape = None
		self.currentRead = None
		self.isComplete = False

	def run(self,tape):
		self.tapePos = 1		
		self.currentState = '0' #assuming first state is always 0	
		self.tape = list(tape) #turn input string into array
		self.currentRead = self.tape[self.tapePos] #perform read operation
		self.isComplete = False
		#checking for no transitions out of current state on current input
		while self.isComplete is False:
			searching = self.search()
			if searching is False:
				self.isComplete = True

		if self.currentState in self.haltstates:
			#slicing list to exclude the Z's added on ln 20,21
			#relatively untested, recently added before submission
			#hoping this doesn't break it, previously: self.tape
			print "Accepted:",''.join(self.tape[1:-1]) 
		else:
			print "Rejected:",''.join(self.tape[1:-1])

	def search(self):
		for state in self.transitions:
			#match current state and input symbol to those in transition list
			if state.current is self.currentState and state.input is self.currentRead:				
				self.tape[self.tapePos] = state.write #perform write operation
				#perform move operations
				if state.move is 'L':
					self.tapePos -= 1
					self.currentRead = self.tape[self.tapePos]		
					
				elif state.move is 'R':
					self.tapePos += 1
					self.currentRead = self.tape[self.tapePos]

				elif state.move is 'H':
					self.isComplete = True

				self.currentState = state.next
				return True
		return False

#main program?
x=Machine(trans_list,final_states)
#cycle through input tapes
for tape in tape_list:
	x.run(str(tape))