// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen
// by writing 'black' in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen by writing
// 'white' in every pixel;
// the screen should remain fully clear as long as no key is pressed.

//// Replace this comment with your code.

//First I want to solve how to black the whole screen
//Then we will focus on the infinite loop 


//Mow add the keyboard Check

// SET VARIABLES

@i    //Rows
M=0

@j    //Columns
M=0

@256
D=A

@rowsize
M=D

@32
D=A

@columnsize
M=D

@SCREEN    //Get the screen address pointer and store it below
D=A

@addressptr
M=D

@colour
M=0


// LEAVE VARIABLES   // 
// BEGIN PROCESSING  // 

(WHILE)  // Loop forever until keys pressed

@KBD
D=M

@SETBLACK
D;JNE

@colour   //This one is working - draws the colour
M=0

@SETWHITE
0;JMP

(SETBLACK)

@colour
M=-1

(SETWHITE)

//Outer for loop that will take care of the  rows. This will be every 32 memory addresses.
//Reset screen

@SCREEN    //Get the screen address pointer and store it below
D=A
@addressptr
M=D

(FOROUTER)   // i variable

@i 
D=M

@rowsize //Check if the numbner of loops > row size
D=D-M

@EXITOUTER
D;JGE


//Inner loop that will take care of the columns. This will be every indidiaul address of the 32 per row
(FORINNER)

@j 
D=M

@columnsize //Check if the numbner of loops > column size
D=D-M

@EXITINNER
D;JGE

//THIS IS WHERE THE BIT MANIPULATION HAPPENS
//Set value

//Check if colour is 0 or -1

@colour
D=M

@BLACKDRAW
D;JNE

@addressptr
D=M
A=D
M=0

@WHITEDRAW
0;JMP

(BLACKDRAW)

@addressptr
D=M
A=D
M=-1

(WHITEDRAW)

//Increment now the value of addressptr (starts at 16505) then goes to 16506 etc
@addressptr   //Has the initial screen value inside
D=M
M=D+1


//Increment j for the loop
@j
D=M
M=D+1

@FORINNER
0; JMP

(EXITINNER)   //Continue with the outer code because we are done with the inner loop

//Reset J
@j 
M=0

@i   //Increment I
D=M
M=D+1

@FOROUTER
0; JMP

(EXITOUTER)   //We are done with all the rows

//Reset I
@i 
M=0

@WHILE
0;JMP

(END)
@END
0;JMP







