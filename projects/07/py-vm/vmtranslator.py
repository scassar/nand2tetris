#My implementation of the Nand2Tetris VM Translater in Python
#Author: Shaun Cassar
#Usage: python3 vmtranslator.py filename.vm OR python3 vmtranslator.py "full_file_path"
#Output: Various .ASM files corresponding to input .VM files found in the directory

import sys
import os 
from vmparser import * 
from vmcodewriter import *

if __name__ == '__main__': 
    
    print("Running the VM translator")

    total_files = 0
    default_file = os.path.basename(os.getcwd())
    import_directory = ""
    files=""

    #Determine if a directory or file has been passed to the translator.
    if len(sys.argv) > 1: 
        if '.vm' in sys.argv[1]:
            print("Processing supplied file")
            temp_path = sys.argv[1]
            default_file = os.path.basename(temp_path)
            if '/' in sys.argv[1] or '\\' in sys.argv[1]:
                import_directory = os.path.dirname(temp_path)+ '/'
            else: 
                import_directory = os.path.dirname(temp_path)
            
            files = [default_file]
        else: 
            print("Processing supplied directory")
            import_directory = sys.argv[1]
            if '/' not in import_directory: 
                import_directory = import_directory + '/'
            files = os.listdir(import_directory)
            default_file = os.path.basename(os.path.dirname(import_directory))
            print("default file: " +default_file )
    else: 
        print ("Executing on current directory")
        files = [f for f in os.listdir() if os.path.isfile(f)]  
    
    process_files = []

    #Process only .vm files
    for file in files: 
       extension = file.split(".")[1]
       if(extension) == 'vm':
            total_files+=1
            process_files.append(import_directory+file)
            
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
