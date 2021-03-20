#  Copyright (C) 2021 Aayush Soni <aayush.soni795@gmail.com>
# 
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://gnu.org/licenses/gpl-3.0.txt>


## USE THIS PROGRAM TO DIRECTLY GENERATE VERILOG CODE FROM SEQUENCE.
## To directly print to file add '>' along with file name in terminal :
## python call_generator.py -s '101_enter_the_seq_101' > 'file_to_print.txt'

import argparse

ap = argparse.ArgumentParser()
#Sequence
ap.add_argument('-s','--sequence', required = True, help = "Sequence of bits to detect.")
#Sequence decoder
ap.add_argument('-sh','--seq-hex', action = 'store_true', help = "Sequence is a hex number representation. Does not support X!	Default binary")
ap.add_argument('-sd','--seq-dec', action = 'store_true', help = "Sequence is a decimal number representation. Does not support X! Default binary")
ap.add_argument('-b','--bitlength', required = False, default = None, help = "Bit length of sequence. Default is length of sequence")

#encoding format
ap.add_argument('-e','--encoding', required = False,default = 'def', help = "Encoding for FSM. Default to decimal encoding")

#FSM type
ap.add_argument('-mo','--moore', action = 'store_true', help = "Moore type FSM. Default Mealy.")

#Signal naming
ap.add_argument('-i','--input-signal', required = False,default = 'in', help = "Name of input signal. Default to 'in'")
ap.add_argument('-st','--state', required = False,default = 'state', help = "State name. Default 'state'")
ap.add_argument('-ns','--next-state', required = False,default = 'next', help = "Next state name. Default 'next'")
ap.add_argument('-o','--output-signal', required = False,default = 'out', help = "Name of output signal. Default 'out'")
ap.add_argument('-ce','--clock-edge', required = False,default = 'p', help = "clock edge. 'p' for positive edge, 'n' for negative edge. Default positive edge")
ap.add_argument('-cn','--clock', required = False,default = 'clk', help = "Name of clock signal. Default 'clk'")
ap.add_argument('-r','--reset', required = False,default = 'rst', help = "Name of reset signal")
args = vars(ap.parse_args())

if args["moore"] : 
	try: import fsm_moore as F
	except: import fsm_gen as F #OLD VERSION 
else : import fsm_mealy as F

s = args["sequence"]
#print(s,'***')
##sequence modifier
if args["seq_hex"]:
	num_seq = s.count('|') +1
	if num_seq ==1 :
		#h =str(len(s)*4) if not	 args["bitlength"] else args["bitlength"] 
		max_len = int(s,16).bit_length()
		if args["bitlength"]:
			if max_len> args["bitlength"]:
				print(f'//Can\'t fit sequence in {args["bitlength"]} bits. Generating sequence of length {max_len}')
				h=str(max_len)
			else:
				h = args["bitlength"]
		else: h=max_len
		#print(h,s)
		try:
			s = format(int(s,16),'0'+h+'b')
			print('//Decoded Sequence ',s)
		except Exception as e:
			print("Expected hexadecimal represented sequence")
			exit()
	else:
		S = s.split('|')
		max_len = max([int(i,16).bit_length() for i in S])
		if not	args["bitlength"]: h = str(max_len)
		else:
			if max_len > int(args["bitlength"]):
				print(f'//Can\'t fit sequence in {args["bitlength"]} bits. Generating sequence of length {max_len}')
				h = str(max_len)
			else: h = args["bitlength"]
		s=format(int(S.pop(),16),'0'+h+'b')
		for i in S:
			s_temp = format(int(i,16),'0'+h+'b')
			s = ''.join([s[i] if s[i]==s_temp[i] else 'x' for i in range(len(s))])
		print('//Decoded Sequence ',s)

elif args["seq_dec"]:
	num_seq = s.count('|') +1
	if num_seq ==1 :
		#h ='' if not  args["bitlength"] else args["bitlength"] 
		max_len = int(s).bit_length()
		if args["bitlength"]:
			if max_len> args["bitlength"]:
				print(f'//Can\'t fit sequence in {args["bitlength"]} bits. Generating sequence of length {max_len}')
				h=str(max_len)
			else:
				h = args["bitlength"]
		else: h=max_len
		
		try:
			s = format(int(s,10),'0'+h+'b')
			print('//Decoded Sequence ',s)
		except Exception as e:
			print("Expected hexadecimal represented sequence")
			exit()
	else:
		S = s.split('|')
		max_len = max([int(i).bit_length() for i in S])
		if not	args["bitlength"]: h = str(max_len)
		else:
			if max_len > int(args["bitlength"]): h = str(max_len)
			else: h = args["bitlength"]
		s=format(int(S.pop()),'0'+h+'b')
		for i in S:
			s_temp = format(int(i),'0'+h+'b')
			s = ''.join([s[i] if s[i]==s_temp[i] else 'x' for i in range(len(s))])
		print('//Decoded Sequence ',s)

else:
	print('//Decoded Sequence ',s)


try :F.verilog(s,enco_type=args["encoding"],input_wire=args["input_signal"],state =args["state"],
	next_state=args["next_state"],output_wire = args['output_signal'] ,clock_name = args['clock'],
	edge = args['clock_edge'], reset = args['reset']);
except Exception as e: print("Error:",e)
