#  Copyright (C) 2021 Aayush Soni <aayush.soni795@gmail.com>
# 
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program.	 If not, see <http://gnu.org/licenses/gpl-3.0.txt>


from math import log2, ceil

class SequenceError(Exception):
	pass	

def bitlen(n): # however n will always be >=2 (shortest strign is length 1 ('0' or '1' ) has 2 states ('' , '0')/('','1')
	if n==1: return 1
	return ceil(log2(n))
def hexlen(n):
	if n==1: return 1
	return ceil(log2(n)/4)


valid_enco = ['def','hex','bin','seq', 'abc','onehot'] #

def encoding() :
	return valid_enco

def states(str):
	state_list=['']
	state_generator = ['']
	for i in str:
		temp=[]
		for temp_state in state_generator:
			if i=='x':
				temp.append( temp_state+'0')
				temp.append( temp_state+'1')
			else:
				temp.append( temp_state+i)
		state_list = state_list + [i for i in temp]
		state_generator = [i for i in temp]
	return state_list


def get_list(s,enco_type='def'):
	# 'def' is numbered '0' to '999' and beyond
	# 'bin' is binary numbered e.g. for 16 states '0000' to '1111'
	# 'hex' is hex numbered e.g. for 256 states '00' to 'ff'
	# 'onehot' is one-hot encoding , e.g. for 3 states '001', '010' , '100'
	# 'seq' is '_0' , '_01' ... sequence encoded
	# 'abc' is 'A' , ... , 'Z' (for up to 26 states)
	
	if not enco_type in valid_enco :
		print("Not a valid encoding format. Taking default")
		enco_type = 'def'
	
	s=s.replace('X','x')
	s=s.replace('?','x')
	
	if s.count('0')+s.count('1')+s.count('x') < len(s) :
		raise(SequenceError('Sequence can only contain 0 / 1 / x(X) / ? '))
	
	
	l = states(s)#[s[:i] for i in range(len(s)+1)]
	l_len = len(l)
	if enco_type == 'bin' :
		digs = bitlen(l_len)
		enco = [format(i,'0'+str(digs)+'b') for i in range(l_len)]
	elif enco_type == 'hex' :
		# digs = 1
		# while (1<<(digs*4)) < l_len : digs+=1
		digs = hexlen(l_len)
		enco = [format(i,'0'+str(digs)+'x') for i in range(l_len)]
	elif enco_type == 'onehot':
		enco = [format(1<<i,'0'+str(l_len)+'b') for i in range(l_len)]
	elif enco_type == 'abc' :
		if l_len <=26:
			enco = [chr(i+ord('A') )for i in range(l_len)]
		else:
			print ('FSM Length too long. Reverting to default encoding')
			enco = [str(i) for i in range(l_len)]
	elif enco_type == 'seq' :
		enco = ['_' +i for i in l]
	else : #default
		enco = [str(i) for i in range(l_len)]
	return l,enco

def fsm(s,enco_type='def'):
	l,enco = get_list(s,enco_type)
	x=[]#d=dict()
	for i in l:
		v0 = i+'0'	#add '0' to current matching sequence-part
		v1 = i+'1'	#add '1' ...
		while not v0 in l: v0 = v0[1:] # keep removing oldest bits from sequence till a new hit is found
		while not v1 in l: v1 = v1[1:]	# ditto, but for v1
		x.append( (	  enco[ l.index(i)] , enco[l.index(v0)], enco[l.index(v1)] )) # the 'new hit' is the next state to jump to for 0/1
	return l,enco,x
def state_table(x):
	print ('Current state :: next_state_if_1 : next_state_if_0')
	for i in x:print (i[0],'::',i[2],':',i[1])

	
def verilog(s,enco_type='def',input_wire='in',state ='state',next_state='next',output_wire = 'out' ,clock_name = 'clk', edge = 'p', reset = 'rst'):
	
	clock_edge = 'posedge ' if edge =='p' else 'nedgedge '
	clock_edge += clock_name
	### check that inputs are of a valid format
	if not enco_type in valid_enco :
		print("Not a valid encoding format. Taking default")
		enco_type = 'def'
	
	s=s.replace('X','x')
	s=s.replace('?','x')
	
	if s.count('0')+s.count('1')+s.count('x') < len(s) :
		raise(SequenceError('Sequence can only contain 0 / 1 / x(X) / ? '))
	
	### calculate  l , encoding, and state_table (x)
	l,enco,x = fsm(s,enco_type)
	
	
	### n = number of bits needed for state register 
	if enco_type != 'onehot':
		n = bitlen(len(enco))-1
		np1=str(n+1)
		n=str(n)
	else: n= str(len(enco)-1)
	
	
	### b=	beginning character to number e.g. 4'b, 6'h, etc.
	b = ''
	if enco_type in ['bin' , 'onehot'] : b = n + "'b" 
	elif enco_type == 'hex' : b = n + "'h" 
	elif enco_type == 'abc' : pass
	else : b = np1+"'d" 
	
	## prerequisite calculations are done... begin printing :)
	
	##parameter
	if enco_type not in ['bin', 'hex','onehot','def' ] : # identification requires parameterization
		print('parameter' ,end='\t')
		for i in range(len(enco)):
			if (i == len(enco)-1):
				print (enco[i] , '=',i, end=';\n')
			else: print (enco[i] , '=',i,	end=',	')
	
	##register declaration
	print ('reg['+n+':0] ', state ,' , ', next_state ,';')
	
	## next_state logic ( combinational)
	print('always@*')
	if enco_type != 'onehot':
		print('\tcase(state)')
		for i in x:
			print('\t\t',b+i[0],':\t',next_state,'<=',input_wire,'?',b+i[2],':',b+i[1],';')
		if len(enco)<2**int(n) :
			print('\t\tdefault:\t',next_state,'<=',b+enco[0],';')
		print('\tendcase')
	else:
		X = reverse_state_table(enco,x)
		print (onehot_gen(X,next_state=next_state,state=state,data=input_wire,init_tab=1 ) )
	
	
	## sequential circuit
	print('always@('+clock_edge+')')
	if enco_type != 'onehot':
		print('\tif('+reset+') '+state+'<= '+enco[0] +';')
	else :
		print('\tif('+reset+') '+state+'<= '+ str(len(l))+'\'d1;')
	print('else '+state+' <= '+next_state+';')
	
	##output logic ( combinational)
	num_final_states = [len(i) for i in l].count(len(l[-1])) #count how many states are 'longest'.These are the final states, e.g. for 1x1 it is 101 and 111 i.ee 2 states
	if enco_type != 'onehot' :
		print ('assign ',output_wire,' = ',end = '')
		for i in range(1,num_final_states+1) :  print('(',state,'==',enco[-i],') |',end='')
		print('\b;')
	else :
		if num_final_states ==1:
			print ('assign ',output_wire,' = ',state ,'[', len(enco)-1,']',';')
		else :
			print ('assign ',output_wire,' = |{',state ,'[', len(enco)-1,':',len(enco)-num_final_states,']}',';')
		

##Reverse state-table, i.e. where 'x' gives current_state : next_state logic,
## 'X' will give current_state : previous_state logic
def reverse_state_table(enco,x,do_print = False):
	if do_print: print ('Next state :: current_state_and_1 : current_state_and_0')
	y = dict()
	for i in enco : y[i] = [[],[]]
	for i in x:
		y[i[1]][0].append(i[0])
		y[i[2]][1].append(i[0])
	if do_print:
		for i in y: print(i,'::',y[i][1] , ':' , y[i][0] )
	return y

## Generate next-state logic for one-hot encoding
def onehot_gen(X,next_state='next',state='state',data='in',init_tab =0):
	s=''
	for i in X:
		s +=init_tab*'\t' +str(f'{next_state}[{index(i)}] =')
		is_1 = len (X[i][1])>0
		if is_1:
			s += str(f' {data}&(')
			for j in X[i][1]: s += str(f'{state}[{index(j)}]|')
			s=s[:-1] + ');\n'
		else:
			
			s += str(f' ~{data}&(')
			for j in X[i][0]: s += str(f'{state}[{index(j)}]|')
			s=s[:-1] + ');\n'
	return s

def index(p): #return '2' for '00000100'
	return len(p) -1 - p.index('1')
