#VM Translater Parser class 
#Author: Shaun Cassar
#Purpose: This will take in an input file, strip unwanted characters and then create
#         a list of the commands. It will orchestrate the moving through the file

class VMParser:    
    
    def __init__(self, file_name): 

        print("Parsing vm file: " + file_name)
        self.file_name = file_name
        self.command_count = -1
        self.current_command = ""
        self.command_list = []

        self.clean_and_open()

        self.total_commands = len(self.command_list) 

    #Function will read and clean the inputs into the buffer for each parsed file
    #We will ignore comments both at the stard and on a particular line
    def clean_and_open(self): 
        
        self.file = open(self.file_name, "r")
        all_lines = self.file.readlines()

        for line in all_lines: 
            clean_line = ""

            if line[0] == '/':
                continue
            if line == "\n": 
                continue
            for letter in line:
                if letter == "/":
                    break
                
                clean_line = clean_line + letter
            
            line = clean_line
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
    # Check for keywords in the command line. Specification as per the course.
    def command_type(self): 
        if 'push' in self.current_command:
            return 'C_PUSH'
        elif 'pop' in self.current_command: 
            return 'C_POP'
        elif 'label' in self.current_command: 
            return 'C_LABEL'
        elif 'if-goto' in self.current_command: 
            return 'C_IF'
        elif 'goto' in self.current_command and 'if-goto' not in self.current_command: 
            return 'C_GOTO'
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
        if self.command_type() == "C_ARITHMETIC" or self.command_type() == "C_RETURN": 
            return self.current_command
        else:
            return self.current_command.split()[1]

    def arg2(self): 
        if self.command_type() == "C_ARITHMETIC" or self.command_type() == "C_RETURN": 
            return self.current_command
        else: 
            return self.current_command.split()[2]







        