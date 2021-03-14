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
ap.add_argument('-ce','--clock-edge', required = False,default = 'posedge ', help = "clock edge. Default positive edge")
ap.add_argument('-cn','--clock', required = False,default = 'clk', help = "Name of clock signal. Default 'clk'")
ap.add_argument('-r','--reset', required = False,default = 'rst', help = "Name of reset signal")

args = vars(ap.parse_args())
#print(args)


F.verilog(args["sequence"],enco_type=args["encoding"],input_wire=args["input_signal"],state =args["state"],
	next_state=args["next_state"],output_wire = args['output_signal'] ,clock_name = args['clock'],
	clock_edge = args['clock_edge'], reset = args['reset']);
	