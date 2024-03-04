#My implementation of the Nand2Tetris Compiler in nand2tetris
#Author: Shaun Cassar
#Usage: python3 JackAnalyzer.py
#Output: Can accept directory, file as output and produces 1 .vm file per jack file. 
#Note: For project 10, we will produce XML

import os
import sys
from JackTokenizer import *
from JackCompilationEngine import *



if __name__ == '__main__': 
    
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

        print("end processing of " + file)




        
