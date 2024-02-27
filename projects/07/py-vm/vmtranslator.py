#My implementation of the Nand2Tetris VM Translater in Python
#Author: Shaun Cassar
#Usage: python3 vmtranslator.py
#Output: Various .ASM files corresponding to input .VM files found in the directory

import sys
import os 
from vmparser import * 
from vmcodewriter import *


if __name__ == '__main__': 
    
    file_name = 'BasicTest.vm'

    print("Running the VM translater on input file")

    files = [f for f in os.listdir() if os.path.isfile(f)]
    process_files = []
    for file in files: 
       extension = file.split(".")[1]
       if(extension) == 'vm':
            process_files.append(file)

    for file in process_files: 
        print("Processing file: " + file)
        
        #Call the Parser class that will take the file as a constructor, and read in the data and break up a line
        
        parser = VMParser(file)
        code_writer = CodeWriter(file)

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
            else:
                pass
        
        #End file and close
        code_writer.addFinalLoop()
        code_writer.close()
