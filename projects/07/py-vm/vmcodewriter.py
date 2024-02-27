#VM Translater Parser class 
#Author: Shaun Cassar
#Purpose: This will process each line and write to Hack assembly


class CodeWriter: 

    def __init__(self,file_name): 
        
        self.file_name = file_name.split(".")
        print("Code writer has been created for " + self.file_name[0]+".asm")

        self.file = open(self.file_name[0]+".asm","w")
        self.next_jump = 0

    #Here we will process and print the assembly for all of the instructions that are arithmetic
    def writeArithmetic(self, command): 

        final_write = [] #output buffer
        final_write.append("//" + command.strip())
        command=command.strip()
        
        #Begin assembly writing
        final_write.append("@SP")
        final_write.append("A=M-1")
        
        if command == "neg": 
            final_write.append("M=-M")
        elif command == "not": 
            final_write.append("M=!M")
       
       #Non - neg or not commands
        else:      
            final_write.append("D=M")
            final_write.append("A=A-1")

            if command == "add": 
                final_write.append("M=M+D")
            elif command == "sub":
                final_write.append("M=M-D")
            elif command == "and":
                final_write.append("M=D&M")
            elif command == "or":
                final_write.append("M=D|M")  
            else:  #handle the lt, gt and eq operators in here if it is not one of the other commands

                if command == "eq": 
                    
                    final_write.append("D=M-D")  
                    final_write.append ("@TRUE"+str(self.next_jump))
                    final_write.append("D;JEQ")
                
                #Do this if not zero (meaning not equal)
                    final_write.append("@SP")
                    final_write.append("A=M")
                    final_write.append("A=A-1")
                    final_write.append("A=A-1")
                    final_write.append("M=0")
                    final_write.append ("@END"+str(self.next_jump))
                    final_write.append("0;JMP")
                
                #Do this if zero
                    final_write.append ("(TRUE"+str(self.next_jump)+")")
                    final_write.append("@SP")
                    final_write.append("A=M")
                    final_write.append("A=A-1")
                    final_write.append("A=A-1")
                    final_write.append("M=-1")

                    final_write.append ("(END"+str(self.next_jump)+")") 
                    self.next_jump+=1
                
                if command == "lt": 
                    final_write.append("D=M-D")  
                    final_write.append ("@TRUE"+str(self.next_jump))
                    final_write.append("D;JLT")
                
                #Do this if not less than
                    final_write.append("@SP")
                    final_write.append("A=M")
                    final_write.append("A=A-1")
                    final_write.append("A=A-1")
                    final_write.append("M=0")

                    final_write.append ("@END"+str(self.next_jump))
                    final_write.append("0;JMP")
                #Do this if less than 
                    final_write.append ("(TRUE"+str(self.next_jump)+")")
                    final_write.append("@SP")
                    final_write.append("A=M")
                    final_write.append("A=A-1")
                    final_write.append("A=A-1")
                    final_write.append("M=-1")
                    final_write.append ("(END"+str(self.next_jump)+")") 
                    self.next_jump+=1

                if command == "gt": 
                    final_write.append("D=M-D")  
                    final_write.append ("@TRUE"+str(self.next_jump))
                    final_write.append("D;JGT")
                
                #Do this if not greater than
                    final_write.append("@SP")
                    final_write.append("A=M")
                    final_write.append("A=A-1")
                    final_write.append("A=A-1")
                    final_write.append("M=0")

                    final_write.append ("@END"+str(self.next_jump))
                    final_write.append("0;JMP")
                
                #Do this if greater than
                    final_write.append ("(TRUE"+str(self.next_jump)+")")
                    final_write.append("@SP")
                    final_write.append("A=M")
                    final_write.append("A=A-1")
                    final_write.append("A=A-1")
                    final_write.append("M=-1")
                    final_write.append ("(END"+str(self.next_jump)+")") 
                    self.next_jump+=1

            #move the stack pointer back one address    
            final_write.append("@SP")
            final_write.append("M=M-1")
        
        #Write buffer to file
        for line in final_write: 
            self.file.write(line+"\n")   

            

    def writePushPop(self, command, arg1, arg2): 
        #A little bit more tricky. Here we want to write assembly to make use of a number of stacks.
        # LCL = local stack
        # Arg = Arugements stack
        # THIS = This stack used for scoping
        # THAT = Stack used for arrays
        # temp = R5
        # pointer = R3
        
        final_write = []
        final_write.append("//" + command + " " + arg1 + " " + arg2)

        if command == "push": 
            if arg1 == "constant": 
                final_write.append("@"+arg2)
                final_write.append("D=A")
                final_write.append("@SP")
                final_write.append("A=M")
                final_write.append("M=D")
            #Bring the value of the static variable onto the stack
            elif arg1 == "static": 
                final_write.append(("@"+self.file_name[0]+"."+arg2))
                final_write.append("D=M")
                final_write.append("@SP")
                final_write.append("A=M")
                final_write.append("M=D")
            elif arg1 == "local":
                #Add position to LCL and push into the current location of SP
                #Left duplicate code to increase visual clarity of each instruction. 
                #Could simplify these blocks into if/else due to repeated code
                
                final_write.append("@LCL")
                final_write.append("D=M")
                final_write.append("@"+arg2)   
                final_write.append("D=D+A")          
                final_write.append("A=D")
                final_write.append("D=M")
                final_write.append("@SP")
                final_write.append("A=M")
                final_write.append("M=D")
            elif arg1 == "argument":
                final_write.append("@ARG")
                final_write.append("D=M")
                final_write.append("@"+arg2)   
                final_write.append("D=D+A")          
                final_write.append("A=D")
                final_write.append("D=M")
                final_write.append("@SP")
                final_write.append("A=M")
                final_write.append("M=D")
            elif arg1 == "this":
                final_write.append("@THIS")
                final_write.append("D=M")
                final_write.append("@"+arg2)   
                final_write.append("D=D+A")          
                final_write.append("A=D")
                final_write.append("D=M")
                final_write.append("@SP")
                final_write.append("A=M")
                final_write.append("M=D")
            elif arg1 == "that":
                final_write.append("@THAT")
                final_write.append("D=M")
                final_write.append("@"+arg2)   
                final_write.append("D=D+A")          
                final_write.append("A=D")
                final_write.append("D=M")
                final_write.append("@SP")
                final_write.append("A=M")
                final_write.append("M=D")
            elif arg1 == "temp":
                final_write.append("@"+arg2)
                final_write.append("D=A")
                final_write.append("@R5")
                #Add position to LCL and push into the current location of SP
                final_write.append("A=A+D")
                final_write.append("D=M")
                final_write.append("@SP")
                final_write.append("A=M")
                final_write.append("M=D")
            elif arg1 == "pointer":
                final_write.append("@"+arg2)
                final_write.append("D=A")
                final_write.append("@R3")
                #Add position to LCL and push into the current location of SP
                final_write.append("A=A+D")
                final_write.append("D=M")
                final_write.append("@SP")
                final_write.append("A=M")
                final_write.append("M=D")
            else: 
                pass
            
                #increment the stack pointer to the next location
            final_write.append("@SP")
            final_write.append("M=M+1")

        else:  # Do pop commands (aka remove from stack) 
            if arg1 == "constant": 
                pass #not valid
            #Bring the value of the static variable onto the stack
            elif arg1 == "static": 
                final_write.append("@SP")
                final_write.append("A=M-1")
                final_write.append("D=M")
                final_write.append("@"+self.file_name[0]+"."+arg2)
                final_write.append("M=D")
                final_write.append("@SP")
                final_write.append("M=M-1")
                
                #Add position to LCL and push into the current location of SP
                #Left duplicate code to increase visual clarity of each instruction. 
                #Could simplify these blocks into if/else due to repeated code
            elif arg1 == "local":
                
                #pop off the stack into index location (index)
                final_write.append("@LCL")
                final_write.append("D=M")
                final_write.append("@"+arg2)   
                final_write.append("D=D+A")  
                #D has the address of the LCL location at index (meaning 1015 + index)
                #Store the variable in general register memory location 13 for later use
                final_write.append ("@R13")
                final_write.append ("M=D")

                #decrement stack pointer
                final_write.append("@SP")
                final_write.append("AM=M-1")
                final_write.append("D=M") 
                
                #get the current stack location again
                final_write.append("@R13")
                final_write.append("A=M")
                final_write.append("M=D")  

            elif arg1 == "argument":
                final_write.append("@ARG")
                final_write.append("D=M")
                final_write.append("@"+arg2)   
                final_write.append("D=D+A")  
                final_write.append ("@R13")  
                final_write.append ("M=D")

                final_write.append("@SP")
                final_write.append("AM=M-1")
                final_write.append("D=M") 

                final_write.append("@R13")
                final_write.append("A=M")
                final_write.append("M=D") 
            elif arg1 == "this":
                final_write.append("@THIS")
                final_write.append("D=M")
                final_write.append("@"+arg2)   
                final_write.append("D=D+A")  
                final_write.append ("@R13")  
                final_write.append ("M=D")

                final_write.append("@SP")
                final_write.append("AM=M-1")
                final_write.append("D=M") 

                final_write.append("@R13")
                final_write.append("A=M")
                final_write.append("M=D") 
            elif arg1 == "that":
                final_write.append("@THAT")
                final_write.append("D=M")
                final_write.append("@"+arg2)   
                final_write.append("D=D+A")  
                final_write.append ("@R13")  
                final_write.append ("M=D")

                final_write.append("@SP")
                final_write.append("AM=M-1")
                final_write.append("D=M") 

                final_write.append("@R13")
                final_write.append("A=M")
                final_write.append("M=D") 
            elif arg1 == "temp":
                final_write.append("@R5")
                final_write.append("D=A")
                final_write.append("@"+arg2)   
                final_write.append("D=D+A")  
                
                final_write.append ("@R13")  
                final_write.append ("M=D")

                final_write.append("@SP")
                final_write.append("AM=M-1")
                final_write.append("D=M") 

                final_write.append("@R13")
                final_write.append("A=M")
                final_write.append("M=D") 
            elif arg1 == "pointer":
                final_write.append("@R3")
                final_write.append("D=A")
                final_write.append("@"+arg2)   
                final_write.append("D=D+A")  
                
                final_write.append ("@R13")  
                final_write.append ("M=D")

                final_write.append("@SP")
                final_write.append("AM=M-1")
                final_write.append("D=M") 

                final_write.append("@R13")
                final_write.append("A=M")
                final_write.append("M=D")         
            else: 
                pass #to be added in later course project 8
        
        for line in final_write: 
            self.file.write(line+"\n")   

    #Write the final end of program loop to file
    def addFinalLoop(self):
        final_write = []
        
        final_write.append("(EOF)")
        final_write.append("@EOF")
        final_write.append("0;JMP")
        print("new lines")
        for line in final_write: 
            self.file.write(line+"\n")   

    #Close the active file
    def close(self):
        print ("file now closed")
        self.file.close()