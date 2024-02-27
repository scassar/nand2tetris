#VM Translater Parser class 
#Author: Shaun Cassar
#Purpose: This will take in an input file, strip unwanted characters and then create
#         a list of the commands. It will orchestrate the moving through the file

class VMParser:    
    
    def __init__(self, file_name): 

        print("Setting up parser file")

        self.file_name = file_name
        self.command_count = -1
        self.current_command = ""
        self.command_list = []

        #Read and clean in the input file
        self.clean_and_open()

        #Store commands in an array for processing over another file
        self.total_commands = len(self.command_list)

        print("total commands in file: " + str(self.total_commands))

    def print_comands(self): 
        for line in self.command_list: 
            print(line)    

    def clean_and_open(self): 
        
        self.file = open(self.file_name, "r")
        all_lines = self.file.readlines()

        for line in all_lines: 
            if line[0] == '/':
                continue
            if line == "\n": 
                continue
            
            self.command_list.append(line)

        self.file.close()
    

    # Function will focus on parsing one single command
    def advance(self): 
        self.command_count+=1
        self.current_command = self.command_list[self.command_count]
        

    # True if total lines is less than current count
    def has_more_commands(self): 
        return self.command_count < self.total_commands-1

    # Function responsible for taking the current line, producing instruction code for the CodeWriter
    # Check for keywords in the command line. Specification as per the course
    def command_type(self): 
        if 'push' in self.current_command:
            return 'C_PUSH'
        elif 'pop' in self.current_command: 
            return 'C_POP'
        elif 'label' in self.current_command: 
            return 'C_LABEL'
        elif 'label' in self.current_command: 
            return 'C_IF'
        elif 'goto' in self.current_command: 
            return 'C_LABEL'
        elif 'function' in self.current_command: 
            return 'C_FUNCTION'
        elif 'call' in self.current_command: 
            return 'C_CALL'		
        elif 'return' in self.current_command: 
            return 'C_RETURN'	
        else: 
            return 'C_ARITHMETIC'

    #Capture and return the arguement value based on the command type
    def arg1(self): 
        if self.command_type() == "C_ARITHMETIC": 
            return self.current_command
        else:
            return self.current_command.split()[1]

    def arg2(self): 
        if self.command_type() == "C_ARITHMETIC": 
            return self.current_command
        else: 
            return self.current_command.split()[2]








        