from math import log2, ceil

class SequenceError(Exception):
	pass	

def bitlen(n):
	return ceil(log2(n))

valid_enco = ['def','hex','bin','onehot','seq', 'abc']

def encoding() :
	return valid_enco

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
	if s.count('0')+s.count('1') < len(s) :
		raise(SequenceError('Sequence can only contain 0 / 1'))
	
	
	l = [s[:i] for i in range(len(s)+1)]
	l_len = len(l)
	if enco_type == 'bin' :
		# digs = 1
		# while (1<<digs) < l_len : digs+=1
		digs = bitlen(l_len)
		enco = [format(i,'0'+str(digs)+'b') for i in range(l_len)]
	elif enco_type == 'hex' :
		digs = 1
		while (1<<(digs*4)) < l_len : digs+=1
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

	
def verilog(s,enco_type='def',input_wire='in',state ='state',next_state='next',output_wire = 'out'):
	
	
	if not enco_type in valid_enco :
		print("Not a valid encoding format. Taking default")
		enco_type = 'def'
	if s.count('0')+s.count('1') < len(s) :
		raise(SequenceError('Sequence can only contain 0 / 1'))
	
	l,enco,x = fsm(s,enco_type)
	
	if enco_type is not 'onehot':
		n = str(bitlen(len(enco))) # number of bits needed for state n = str(len(format(len(enco),'b'))  )
	else: n= str(len(enco))#n = str(len(format(len(enco)-1,'b'))) 
	
	print ('reg['+n+':0] ', state ,' , ', next_state ,';')
	
	if enco_type not in ['bin', 'hex','onehot','def' ] : # identification requires parameterization
		print('parameter' ,end='\t')
		for i in range(len(enco)):
			if (i == len(enco)-1):
				print (enco[i] , '=',i,	end=';\n')
			else: print (enco[i] , '=',i,	end=',  ')
	b = ''
	if enco_type in ['bin' , 'onehot'] : b = n + "'b" 
	elif enco_type == 'hex' : b = n + "'h" 
	elif enco_type == 'abc' : pass
	else : b = n+"'d" 
	print('always@*')
	print('\tcase(state)')
	for i in x:
		print('\t\t',b+i[0],':\t',next_state,'<=',input_wire,'?',b+i[2],':',b+i[1],';')
	if len(enco)<2**int(n) :
		print('\t\tdefault:\t',next_state,'<=',b+enco[0],';')
	print('\tendcase')
	
	if enco_type is not 'onehot' :
		print ('assign ',output_wire,' = ',state,'==',enco[-1])
	else :
		print ('assign ',output_wire,' = ',state ,'[', len(enco)-1,']')
	
def reverse_state_table(enco,x):
	print ('Next state :: current_state_and_1 : current_state_and_0')
	y = dict()
	for i in enco : y[i] = [[],[]]
	for i in x:
		y[i[1]][0].append(i[0])
		y[i[2]][1].append(i[0])
	for i in y: print(i,'::',y[i][1] , ':' , y[i][0] )