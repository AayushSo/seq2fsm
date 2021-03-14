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
import fsm_gen as F

import argparse

#a = sys.argv # destination filename, sequence to find, encoding type, input_wire, state, output_wire, clock_edge,reset 

ap = argparse.ArgumentParser()
#ap.add_argument('-f','--filename', required = True, help = "File name to store code")
ap.add_argument('-e','--encoding', required = False,default = 'def', help = "Encoding for FSM. Default to decimal encoding")
ap.add_argument('-i','--input-signal', required = False,default = 'in', help = "Name of input signal. Default to 'in'")
ap.add_argument('-st','--state', required = False,default = 'state', help = "State name. Default 'state'")
ap.add_argument('-ns','--next-state', required = False,default = 'next', help = "Next state name. Default 'next'")
ap.add_argument('-o','--output-signal', required = False,default = 'out', help = "Name of output signal. Default 'out'")
ap.add_argument('-s','--sequence', required = True, help = "Sequence of bits to detect.")
ap.add_argument('-ce','--clock-edge', required = False,default = 'p', help = "clock edge. 'p' for positive edge, 'n' for negative edge. Default positive edge")
ap.add_argument('-cn','--clock', required = False,default = 'clk', help = "Name of clock signal. Default 'clk'")
ap.add_argument('-r','--reset', required = False,default = 'rst', help = "Name of reset signal")

args = vars(ap.parse_args())
#print(args)


F.verilog(args["sequence"],enco_type=args["encoding"],input_wire=args["input_signal"],state =args["state"],
	next_state=args["next_state"],output_wire = args['output_signal'] ,clock_name = args['clock'],
	edge = args['clock_edge'], reset = args['reset']);
	
