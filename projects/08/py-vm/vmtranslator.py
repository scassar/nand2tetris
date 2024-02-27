#My implementation of the Nand2Tetris VM Translater in Python
#Author: Shaun Cassar
#Usage: python3 vmtranslator.py
#Output: Various .ASM files corresponding to input .VM files found in the directory

import sys
import os 
from vmparser import * 
from vmcodewriter import *


if __name__ == '__main__': 
    
    print("Running the VM translater")

    total_files = 0
    default_file = "final.asm"
    import_directory = ""

    #Get input param
    if len(sys.argv) > 1: 
        extension = sys.argv[1].split(".")[1]
        if(extension) == 'vm':
            print("Processing supplied file")
            default_file = sys.argv[1].split(".")[0]
            files = [sys.argv[1]]
        else: 
            print("Processing supplied directory")
            import_directory = sys.argv[1]
            files = os.listdir(import_directory)
            default_file = os.path.basename(os.path.dirname(import_directory))
    else: 
        print ("Executing on current directory")
        files = [f for f in os.listdir() if os.path.isfile(f)]  
    
    process_files = []

    #Process only .vm files
    for file in files: 
       extension = file.split(".")[1]
       if(extension) == 'vm':
            total_files+=1
            print(import_directory+file)
            process_files.append(import_directory+file)

    code_writer = CodeWriter(import_directory, default_file)
    code_writer.writeInit()

    for file in process_files: 
               
        parser = VMParser(file)
        code_writer.setFileName(file)

        #Main control of the flow looping through the parser and the code writer per line
        while(parser.has_more_commands()):
            parser.advance()
            command_type = parser.command_type()

            if command_type == 'C_ARITHMETIC':
                code_writer.writeArithmetic(parser.arg1())
            elif command_type == 'C_PUSH':
                code_writer.writePushPop('push', parser.arg1(), parser.arg2())
            elif command_type == 'C_POP':
                code_writer.writePushPop('pop', parser.arg1(), parser.arg2())
            elif command_type == 'C_LABEL':
                code_writer.writeLabel('label', parser.arg1())
            elif command_type == 'C_IF':
                code_writer.writeIFGoto('if-goto', parser.arg1())
            elif command_type == 'C_GOTO':
                code_writer.writeGoto('goto', parser.arg1())
            elif command_type == 'C_CALL':
                code_writer.writeCallFunction('call', parser.arg1(), parser.arg2())
            elif command_type == 'C_FUNCTION':
                code_writer.writeFunction('function', parser.arg1(),parser.arg2())
            elif command_type == 'C_RETURN':
                code_writer.writeReturn('return', parser.arg1())
            else:
                pass
        
        #End file and loop
    code_writer.close()

