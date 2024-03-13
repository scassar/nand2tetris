# My implementation of the Nand2Tetris Compiler in nand2tetris
# Author: Shaun Cassar
# Usage: python3 JackCompiler.py <directory> or file (blank for run on current dir)
# Output: Can accept directory, file as output and produces 1 .vm file per jack file. 
# Note: For project 10, we will produce XML

import os
import sys
from JackTokenizer import *
from JackCompilationEngine import *

if __name__ == '__main__': 
    
    import_directory = ""

    if len(sys.argv) > 1: 
        if '.jack' in sys.argv[1]:            
            print("Processing supplied file")
            temp_path = sys.argv[1]
            default_file = os.path.basename(temp_path)
            if '/' in sys.argv[1] or '\\' in sys.argv[1]:
                import_directory = os.path.dirname(temp_path)+ '/'
                print("dir: " + import_directory)
            else: 
                import_directory = os.path.dirname(temp_path)
                print("dir: " + import_directory)
            print(default_file)
            files = [default_file]
            generate_startup = False
        else: 
            print("Processing supplied directory")
            import_directory = sys.argv[1]
            if '/' not in import_directory: 
                import_directory = import_directory + '/'
            files = os.listdir(import_directory)
            default_file = os.path.basename(os.path.dirname(import_directory))
    else: 
        print ("Executing on current directory")
        files = [f for f in os.listdir() if os.path.isfile(f)]  


    process_files = []
    for file in files: 
       extension = file.split(".")[1]
       if(extension) == 'jack':
            process_files.append(import_directory+file)

    if len(process_files) <1:
        print("No files found")

    for file in process_files: 
        print("Processing file: " + file)
        file_name = file.split(".jack")

        tokenizer = JackTokenizer(file)
        engine = JackCompilationEngine(file_name[0], tokenizer)
        engine.process()

        print("end compiling of " + file)




        
