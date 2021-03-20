# seq2fsm
## Create an FSM state table (and generate Verilog code!) that can detect a sequence in a bitstream

### This is a python library that generates an FSM to detect an arbritary pattern on an input bitstream. 

The user can choose to display the states in decimal / binary/ hex/ one-hot encoded/ sequence-names.
E.g. for detecting a sequence '1011001110'
1. Decimal encoding :  '0', '1', '2' , .. , '10'
2. Binary encoding : '0000' ,'0001' , ... , '1010'
3. Hex encoding : '0' , '1', '2', ... , 'a'
4. One-hot encoding : '00000000001', '000000000010' , ... ,'10000000000'

I also added a small program to print out the necessary Verilog code for :
1. Parameter definitions (for select encodings)
2. Assign registers for current and next states
3. Case states for next-state
4. Assign output based on matching condition


### EDIT: I added support for including dont-care's in the sequence! ( fsm_gen_v2.py)
E.g. A sequence '1x1' will trigger output for both '111' and '101'.
A sequence '1x01x' will trigger output for '10010', '10011','11010' and '11011'.

### EDIT2: I added a python script that can directly be run to dump verilog code to console/ to a specified file 
Syntax to dump directly to a file :
python call_generator.py -s '101_enter_the_seq_101' > 'file_to_print.txt'
<br>WARNING : IF A FILE ALREADY EXISTS IT MAY BE OVERWRITTEN

Excluding the '> filename.extension' will print onto terminal directly 
|Argument|Arguement Shorthand|Required|Format|Description|
|---|---|---|---|---|
|--sequence|-s|**Yes**|Sequence of binary/hex/decimal values. <br> (For binary) Supports 'x' for don't care (to detect multiple sequences in single fsm) <br> (For hex/dec) Add multiple sequences by separating with a '\|'|Sequence to detect. Default binary representation |
|--seq-hex|-sh|No|-|Sequence is a hex number representation. Does not support X!<br> **Default binary**|
|--seq-dec|-sd|No|-|Sequence is a decimal number representation. Does not support X!<br> **Default binary**|
|--bitlength|-b|No|-|Bit length of sequence. <br>Default is the default length of sequence|
|--encoding|-e|No|-|Bit length of sequence. <br>Default is length of sequence|
|--moore|-m|No|-|Moore type FSM. <br>**Default Mealy**|
|--input-signal|-i|No|string|Name of input signal. <br>**Default 'in'**|
|--state|-st|No|string| State name. <br>**Default 'state'**|
|--next-state|-ns|No|string|Next state name. <br>**Default 'next'**|
|--output-signal|-o|No|string|Name of output signal. <br>**Default 'out'**|
|--clock-edge|-ce|No|'p' / 'posedge' for positive edge <br> 'n' /'negedge' for negative edge|Clock edge. 'p' for positive edge, 'n' for negative edge. <br>**Default positive edge**|
|--clock|-cn|No|string| Name of clock signal. <br>**Default 'clk'**|
|--reset|-r|No|string|Name of reset signal. <br>**Default 'rst'**|

Also are function definitions for : 
1.  seq_gen : Used to create state table, and envoded state names
    - input( sequence e.g. '101011' , encoding .e.g 'hex')
    - output l = list of sequence-parts that each state represents ( e.g. '' , '1' , '10', '101' for sequence 101)
            enco = encoded state names
            x = state table
2.  state_table : Print the state table in a clean way
    - input ( x = state table)
    - output _None_ 
3. verilog : Print Verilog-style code to create the FSM
   - input (sequence, encoding_type , input_wire (default 'in') , state_name (default 'state'), next_state ( default 'next') , output_wire (default 'out')
   - output _None_
4. reverse_state_table : Used to create efficient one-hot encoding. Returns table of "current_state : previous_state" entries
5. onehot_gen : Generate next-state logic for one-hot encoding
