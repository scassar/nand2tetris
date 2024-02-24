// Mult program for the Nand2Tetris course. 
// Once run we can test the program using a script
// Repository of c
// Multiply the contents of RAM[0] and RAM[1] and
// Store this in RAM[2]

// Some syntax R1,R2 etc refer to the first 16 spots of RAM
// (POSITIVE) refer to a label position, and can be mapped with @. JMP or JLT (jump less than) 

//First variables we want to use 

//Set the address randomyl to these variables initialise to 0

@count
M=1

//Set the number of loops = R1
@R1
D=M
@n
M=D

//Set start sum to 0
@sum
M=0


(LOOP)

@count
D=M

//Here we see the difference between our n times and our count variable
@n
D=D-M

//JGT = jump if greater than 0 of the computation to the specifed A register address. This means the count is > n
@STOP
D; JGT  

// Enter the loop and perform one addition. R1 + R1

@sum
D=M

@R0
D=D+M

@sum
M=D

//Now increment counter
@count
D=M

@count
M=D+1

@LOOP
0; JMP

//Once we have got the number in SUM, store to R2
(STOP)  

@sum
D=M

@R2
M=D 

(END)
@END
0;JMP
