#VM Translater CodeWriter class 
#Author: Shaun Cassar
#Purpose: This will process each line and write to Hack assembly. 


import os

class CodeWriter: 

    # Usage: 
    # Accepts first the directory path and second the filename for the current file to be parsed
    def __init__(self,output_directory, output_file_name): 
        
        self.output_file_name = output_file_name.split(".")[0]
        print("Code writer has been created for " + output_directory+self.output_file_name+".asm")

        self.file_name = ""
        self.file = open(output_directory+self.output_file_name+".asm","w")
        self.next_jump = 0
        self.current_func = "main"
        self.call_number = 0

    #Process and print the assembly for all of the instructions that are arithmetic
    # Add, Sub, Not, Neg, lt, gt, eq, and, or 
    #
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
                final_write.append("M=D+M")
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
       
    #Process and print the assembly for all of the instructions that are push/pop
    # push, pop
    # local, arg, temp, pointer, this,that, static
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
                final_write.append(("@"+self.file_name+"."+arg2))
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
                final_write.append("@"+self.file_name+"."+arg2)
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
                final_write.append("A=M-1")
                final_write.append("D=M") 
                
                #get the current stack location again
                final_write.append("@R13")
                final_write.append("A=M")
                final_write.append("M=D")  

                final_write.append("@SP")
                final_write.append("M=M-1")       

            elif arg1 == "argument":
                final_write.append("@ARG")
                final_write.append("D=M")
                final_write.append("@"+arg2)   
                final_write.append("D=D+A")  
                final_write.append ("@R13")  
                final_write.append ("M=D")

                final_write.append("@SP")
                final_write.append("A=M-1")
                final_write.append("D=M") 

                final_write.append("@R13")
                final_write.append("A=M")
                final_write.append("M=D") 

                final_write.append("@SP")
                final_write.append("M=M-1")       
            elif arg1 == "this":
                final_write.append("@THIS")
                final_write.append("D=M")
                final_write.append("@"+arg2)   
                final_write.append("D=D+A")  
                final_write.append ("@R13")  
                final_write.append ("M=D")

                final_write.append("@SP")
                final_write.append("A=M-1")
                final_write.append("D=M") 

                final_write.append("@R13")
                final_write.append("A=M")
                final_write.append("M=D")

                final_write.append("@SP")
                final_write.append("M=M-1")        
            elif arg1 == "that":
                final_write.append("@THAT")
                final_write.append("D=M")
                final_write.append("@"+arg2)   
                final_write.append("D=D+A")  
                final_write.append ("@R13")  
                final_write.append ("M=D")

                final_write.append("@SP")
                final_write.append("A=M-1")
                final_write.append("D=M") 

                final_write.append("@R13")
                final_write.append("A=M")
                final_write.append("M=D")

                final_write.append("@SP")
                final_write.append("M=M-1")        
            elif arg1 == "temp":
                final_write.append("@R5")
                final_write.append("D=A")
                final_write.append("@"+arg2)   
                final_write.append("D=D+A")  
                
                final_write.append ("@R13")  
                final_write.append ("M=D")

                final_write.append("@SP")
                final_write.append("A=M-1")
                final_write.append("D=M") 

                final_write.append("@R13")
                final_write.append("A=M")
                final_write.append("M=D") 

                final_write.append("@SP")
                final_write.append("M=M-1")       
            elif arg1 == "pointer":
                final_write.append("@R3")
                final_write.append("D=A")
                final_write.append("@"+arg2)   
                final_write.append("D=D+A")  
                
                final_write.append ("@R13")  
                final_write.append ("M=D")

                final_write.append("@SP")
                final_write.append("A=M-1")
                final_write.append("D=M") 

                final_write.append("@R13")
                final_write.append("A=M")
                final_write.append("M=D")
                
                final_write.append("@SP")
                final_write.append("M=M-1")              

        
        for line in final_write: 
            self.file.write(line+"\n")   

    #Generate written label
    def writeLabel(self, command, label): 
        final_write = []
        final_write.append("//" + command + " " + label)

        final_write.append("("+self.current_func+"$"+label+")")
        
        for line in final_write: 
            self.file.write(line+"\n")   

    #How this works is we need to look at the previous value on the stack, and pop it off
    #This value will determine if we are going to go to the new location
    def writeIFGoto(self, command, label): 
        
        final_write = []
        final_write.append("//" + command + " " + label)

        final_write.append("@SP")
        final_write.append("A=M-1")
        final_write.append("D=M")

        #Essentially a "POP off the stack"
        final_write.append("@SP")
        final_write.append("M=M-1")

        #Compute D value. if its non zero then jump. 0 = false
        final_write.append("@"+self.current_func+"$"+label)
        final_write.append("D;JNE")

        for line in final_write: 
            self.file.write(line+"\n")   

    
    def writeGoto(self, command, arg1): 

        final_write = []
        final_write.append("//" + command + " " + arg1)

        final_write.append("@"+self.current_func+"$"+arg1)
        final_write.append("0;JMP")

        for line in final_write: 
            self.file.write(line+"\n")   

    #This function has the responsibility to do the following:
    # 1) Grab the return address from further up the stack
    # 2) push LCL, ARG, THIS, THAT onto the stack
    # 3) ARG = SP-5-nArgs
    # 4) LCL = SP
    # 5) goto functionName
    # 6) Drop a label in this location (also set the current_function for the writer object)

    def writeCallFunction(self, command, functionName, nArgs): 
        
        final_write = []
        final_write.append("//" + command + " " + functionName + " " + nArgs)
        
        self.call_number+=1
        return_address = functionName+"$ret."+str(self.call_number)

        #Push the return address onto the stack
        final_write.append("@"+return_address)
        final_write.append("D=A")

        final_write.append("@SP")
        final_write.append("A=M")
        final_write.append("M=D")   #Push to the stack the value of where the pre-generated label is sitting

        final_write.append("@SP")
        final_write.append("M=M+1")

        #push LCL,ARG,THIS,THAT
        final_write.append("@LCL")
        final_write.append("D=M")

        final_write.append("@SP")
        final_write.append("A=M")
        final_write.append("M=D")
        final_write.append("@SP")
        final_write.append("M=M+1")

        final_write.append("@ARG")
        final_write.append("D=M")

        final_write.append("@SP")
        final_write.append("A=M")
        final_write.append("M=D")
        final_write.append("@SP")
        final_write.append("M=M+1")

        final_write.append("@THIS")
        final_write.append("D=M")
        final_write.append("@SP")
        final_write.append("A=M")
        final_write.append("M=D")
        final_write.append("@SP")
        final_write.append("M=M+1")

        final_write.append("@THAT")
        final_write.append("D=M")
        final_write.append("@SP")
        final_write.append("A=M")
        final_write.append("M=D")
        final_write.append("@SP")
        final_write.append("M=M+1")

        #now set the arg address back to where the first arg was. Calculate first the nargs, then add 5, then subtract 7 from the stack pointer

        final_write.append("@"+str(int(nArgs)+5))
        final_write.append("D=A")

        final_write.append("@SP")
        final_write.append("D=M-D")

        #Write new address of ARG
        final_write.append("@ARG")
        final_write.append("M=D")

        #set LCL = SP
        final_write.append("@SP")
        final_write.append("D=M")

        final_write.append("@LCL")
        final_write.append("M=D")

        final_write.append("@"+functionName)
        final_write.append("0;JMP")
        final_write.append("(" + return_address + ")")


        for line in final_write: 
            self.file.write(line+"\n")   

    #Handle function returns
    # 1) create temp endFrame to hold LCL address
    # 2) fetch return address from (endFrame - 5)
    # 3) *ARG = POP(), # 4) SP = ARG + 1
    # 5) THAT = *(endFrame-1), # 6) THIS = *(endFrame-1)
    # 7) ARG = *(endFrame-1), # 8) LCL = *(endFrame-1)
    # 9) Goto return address

    def writeReturn(self, command, arg1): 
        
        command=command.strip()
        
        final_write = []
        final_write.append("//" + command)

        final_write.append("@LCL")   #Temp we will use to hold LCL. #EndFrame = R13
        final_write.append("D=M")
        
        final_write.append("@R14")
        final_write.append("M=D")   #Store LCL in EndFrame
        
        #Get return address (D shopuld still be = LCL address)
        final_write.append("@5")
        final_write.append("A=D-A")
        final_write.append("D=M")     #Get return address into D register
        
        final_write.append("@R15")    #retAddr temp variable
        final_write.append("M=D")   #Store return address in retAddress variable
        
        #Now we need to set the value at current *ARG = SP-1 (the last computed value)
        final_write.append("@SP")
        final_write.append("A=M-1")
        final_write.append("D=M")   #Get the vlaue of the last variable

        final_write.append("@ARG")
        final_write.append("A=M")
        final_write.append("M=D")   #Set the value of the last variable into the location of ARG

        final_write.append("D=A")   #Grab the current address of ARG where we just put the return value
        final_write.append("@SP")
        final_write.append("M=D+1")   #Set SP to ARG address + 1

        #Now we need to set the THAT, THIS, ARG and LCL back to that of the caller. Will re-use the code to get the return address

        final_write.append("@R14")   #get the restore value for THAT
        final_write.append("AM=M-1")
        final_write.append("D=M")     #grab the memory location saved
        
        final_write.append("@THAT")
        final_write.append("M=D")

        final_write.append("@R14")   #get the restore value for THIS
        final_write.append("AM=M-1")
        final_write.append("D=M")     #grab the memory location saved
        final_write.append("@THIS")
        final_write.append("M=D")

        final_write.append("@R14")   #get the restore value for ARG
        final_write.append("AM=M-1")
        final_write.append("D=M")     #grab the memory location saved
        final_write.append("@ARG")
        final_write.append("M=D")

        final_write.append("@R14")   #get the restore value for LCL
        final_write.append("AM=M-1")
        final_write.append("D=M")     #grab the memory location saved
        final_write.append("@LCL")
        final_write.append("M=D")


        final_write.append("@R15")
        final_write.append("A=M")   #dont forget - we jump to the line which is the value of the a register
        final_write.append("0;JMP")


        for line in final_write: 
            self.file.write(line+"\n")   

    #This function will write the assembly function for the VM translation. Input arg2 = number of local variables.
    # Add a label for the jump to function
    # Localise the LCL stack for the number of args to 0
    # SP will sit at LArgs + 1

    def writeFunction(self, command, function_name, LArgs):
        
        final_write = []
        final_write.append("//" + command + " " + LArgs)

        self.current_func = function_name

        #Push the return address onto the stack
        final_write.append("("+function_name+")")

        #push local variables onto the stack

        for i in range(int(LArgs)): 
            
            final_write.append("@SP")
            final_write.append("A=M")
            final_write.append("M=0")
            
            final_write.append("@SP")
            final_write.append("M=M+1")

        
        for line in final_write: 
            self.file.write(line+"\n")   

    #Bootloader code
    #Requires that input VM code atleast has a starting function called Sys.Init
    def writeInit(self):
        
        final_write = []

        final_write.append('@256')
        final_write.append('D=A')
        final_write.append('@SP')
        final_write.append('M=D')

        for line in final_write: 
            self.file.write(line+"\n") 

        self.writeCallFunction("call","Sys.init","0")


    ##Here we need to handle if directory
    def setFileName(self, file_name):
        basename_without_ext = os.path.splitext(os.path.basename(file_name))[0]
        self.file_name = basename_without_ext

    #Close the active file
    def close(self):
        print ("file now closed")
        self.file.close()