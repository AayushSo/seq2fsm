  // Copyright (C) 2021 Aayush Soni <aayush.soni795@gmail.com>
 
  // This program is free software; you can redistribute it and/or modify
  // it under the terms of the GNU General Public License as published by
  // the Free Software Foundation.
 
  // This program is distributed in the hope that it will be useful,
  // but WITHOUT ANY WARRANTY; without even the implied warranty of
  // MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	 See the
  // GNU General Public License for more details.
 
  // You should have received a copy of the GNU General Public License
  // along with this program.	 If not, see <http://gnu.org/licenses/gpl-3.0.txt>

module top_module ();
	reg clk=0;
    reg [3:0] input_pattern;
    reg rst=1;
    reg load_pattern;
    wire out;
    reg in=0;
    
    always #5 clk = ~clk;  // Create clock with period=10
	// initial `probe_start;   // Start the timing diagram

	// `probe(clk);        // Probe signal "clk"
	// `probe(input_pattern);        // Probe signal "clk"
    // `probe(rst);        // Probe signal "clk"
    // `probe(load_pattern);        // Probe signal "clk"
    // `probe(out);        // Probe signal "clk"
    // `probe(in);        // Probe signal "clk"
	
	// A testbench
	initial begin
		#25
        input_pattern = 3'b101;
        rst = 0;
        load_pattern = 1;
        
		#10 in <= 0;
		#10 in <= 1;
		#10 in <= 0;
        #10 in <= 1;
        #10 in <= 1;
        #10 in <= 0;
        #10 in <= 1;
        #10 in <= 1;
        #10 in <= 1;
        #10 in <= 1;
        #10 in <= 1;
        #10 in <= 0;
        #10 in <= 1;
        #10 in <= 1;
        
		$display ("Hello world! The current time is (%0d ps)", $time);
		#50 $finish;            // Quit the simulation
	end

    pattern_recognition uut (.input_pattern(input_pattern),.rst(rst), .input_bitmask(3'b010),.clk(clk),.load_pattern(load_pattern), .in(in), .out(out));
	defparam uut.PATTERN_SIZE=3;
endmodule


module pattern_recognition 
#(parameter LEFT_FIRST = 1, PATTERN_SIZE = 8) // LEFT_FIRST -> pattern[PATTERN_SIZE-1] is inputted first, then pattern[PATTERN_SIZE-2] and so on
    (input wire [PATTERN_SIZE-1:0] input_pattern, input rst,input clk,input load_pattern, input [PATTERN_SIZE-1:0]input_bitmask, input in, output out);

reg [PATTERN_SIZE-1:0] pattern;// = 8'b00110101; 
reg [PATTERN_SIZE-1:0] bitmask; // = 8'b00000000;
reg [PATTERN_SIZE-1:0] state;

    //`probe(state);
always@(posedge clk) begin
    if (rst) state<=0;
	else state<= LEFT_FIRST ? {state[PATTERN_SIZE-2:0],in} : {in,state[PATTERN_SIZE-1:1]} ;
end

always@(posedge clk) begin
	pattern<= load_pattern ? input_pattern : pattern;
	end

always@(posedge clk) begin
	bitmask<= load_pattern ? input_bitmask : bitmask;
	end

assign out = ((pattern|bitmask) == (state|bitmask));

endmodule
