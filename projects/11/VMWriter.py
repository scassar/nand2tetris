#My implementation of the Nand2Tetris Compiler in nand2tetris
#Author: Shaun Cassar
#Usage: VMWriter.py creates a simple VM command writer 


#Every instance of CompilationEngine will create a VMWriter
class VMWriter: 

    def __init__(self, file_name): 
        self.output_file = open(file_name, "w")


    def write_push(self, segment, index): 
        self.output_file.write(f"push {segment} {index} \n")
        

    def write_pop(self, segment, index): 
        self.output_file.write(f"pop {segment} {index} \n")
        

    def write_arithmetic(self, command): 
        self.output_file.write(f"{command} \n") 

    def write_label(self, label): 
        self.output_file.write(f"label {label} \n")        
    
    def write_goto(self, label): 
        self.output_file.write(f"goto {label} \n")   

    def write_if(self, label): 
        self.output_file.write(f"if-goto {label} \n")     

    def write_function(self, label, n_vars): 
        self.output_file.write(f"function {label} {n_vars} \n")  

    def write_call(self, label, n_vars): 
        self.output_file.write(f"call {label} {n_vars} \n")  

    def write_return(self): 
        self.output_file.write(f"return \n")  

    def close(self): 
        self.output_file.close()