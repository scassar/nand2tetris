#My implementation of the Nand2Tetris Compiler in nand2tetris
#Author: Shaun Cassar
#Usage: python3 JackAnalyzer.py <runs on current directory>
#Output: Can accept directory, file as output and produces 1 .vm file per jack file. 
#Note: For project 10, we will produce XML

import os
import sys
from JackTokenizer import *
from JackCompilationEngine import *



if __name__ == '__main__': 
    
    import_directory = ""

    if len(sys.argv) > 1: 

        extension = sys.argv[1].split(".")
        if(extension) == 'jack':
            print("Processing supplied jack file")
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
    for file in files: 
       extension = file.split(".")[1]
       if(extension) == 'jack':
            process_files.append(file)

    for file in process_files: 
        print("Processing file: " + file)
        file_name = file.split(".")[0]

        tokenizer = JackTokenizer(file)
        engine = JackCompilationEngine(file_name+".xml", tokenizer)
        engine.process()

        print("end compiling of " + file)




        
