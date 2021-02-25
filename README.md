# seq2fsm
## Create an FSM that can detect a sequence in a bitstream

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
4. reverse_state_table : I'm going to use this to create efficient one-hot encoding
