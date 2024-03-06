# y implementation of the Nand2Tetris Compiler in nand2tetris
# Author: Shaun Cassar
# Usage: SymbolTable
# Description: Used to hold through compilation references to Class and Subroutine scope for variables.

class SymbolTable: 

    def __init__ (self): 
        self.class_symbols = {}
        self.subroutine_symbols = {}
        self.class_static_count = 0
        self.class_field_count = 0
        self.subroutine_local_count = 0
        self.subroutine_arg_count = 0

    #Reset the subroutine table back to default indexes
    def reset(self): 
        self.subroutine_symbols = {}
        self.subroutine_local_count = 0
        self.subroutine_arg_count = 0
    
    #Print method for symbol tables (used for debugging if required)
    def print_symbol_table(self):
        print("class params")
        for key, value in self.class_symbols.items():
            print(key,value)
        print("subroutine params")
        for key, value in self.subroutine_symbols.items():
            print(key,value)

    #responsible to push certain types of variables into the right symbol tables
    def define(self, name, type, kind): 
        if kind == "static": 
            self.class_symbols[name] = {"type": type, "kind": "static", "index": self.class_static_count}
            self.class_static_count+=1
        if kind == "field": 
            self.class_symbols[name] = {"type": type, "kind": "field", "index":  self.class_field_count}
            self.class_field_count+=1            
        if kind == "local": 
            self.subroutine_symbols[name] = {"type": type, "kind": "local", "index": self.subroutine_local_count}
            self.subroutine_local_count+=1                    
        if kind == "argument": 
            self.subroutine_symbols[name] = {"type": type, "kind": "argument", "index":  self.subroutine_arg_count}
            self.subroutine_arg_count+=1   

    #Return the total number of the kind in the table
    def var_count(self, kind): 
        if kind == "static": 
            return self.class_static_count
        if kind == "field": 
            return self.class_field_count
        if kind == "local": 
            return self.subroutine_local_count
        if kind == "argument": 
            return self.subroutine_arg_count

    #return the kind for a given variable
    def kind_of(self, name): 
        if name in self.subroutine_symbols.keys(): 
            return self.subroutine_symbols[name]['kind']
        if name in self.class_symbols.keys(): 
            return self.class_symbols[name]['kind']
        else:
            return None

    #return the kind for a given variable
    def type_of(self, name): 
        if name in self.subroutine_symbols.keys(): 
            return self.subroutine_symbols[name]['type']
        if name in self.class_symbols.keys(): 
            return self.class_symbols[name]['type']
        else:
            return None

    #return the kind for a given variable
    def index_of(self, name): 
        if name in self.subroutine_symbols.keys():
            return self.subroutine_symbols[name]['index']
        if name in self.class_symbols.keys(): 
            return self.class_symbols[name]['index']
        else:
            return None