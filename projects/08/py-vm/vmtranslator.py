#My implementation of the Nand2Tetris VM Translater in Python
#Author: Shaun Cassar
#Usage: python3 vmtranslator.py filename.vm OR python3 vmtranslator.py "full_file_path"
#Output: Various .ASM files corresponding to input .VM files found in the directory

import sys
import os 
from vmparser import * 
from vmcodewriter import *

#Usage: If directory is passed then output fill be <directory>.asm
#       Filename can also be passed in and will compire a singluar vm file
if __name__ == '__main__': 
    
    print("Running the VM translator")

    total_files = 0
    default_file = os.path.basename(os.getcwd())
    import_directory = ""
    files = ""
    generate_startup = True

    #Determine if a directory or file has been passed to the translator.
    if len(sys.argv) > 1: 
        if '.vm' in sys.argv[1]:            
            print("Processing supplied file - no startup code")
            temp_path = sys.argv[1]
            default_file = os.path.basename(temp_path)
            if '/' in sys.argv[1] or '\\' in sys.argv[1]:
                import_directory = os.path.dirname(temp_path)+ '/'
            else: 
                import_directory = os.path.dirname(temp_path)
            files = [default_file]
            generate_startup = False
        else: 
            print("Processing supplied directory - writing startup code")
            import_directory = sys.argv[1]
            if '/' not in import_directory: 
                import_directory = import_directory + '/'
            files = os.listdir(import_directory)
            default_file = os.path.basename(os.path.dirname(import_directory))
    else: 
        print ("Executing on current directory - writing startup code")
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

    if generate_startup: 
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

