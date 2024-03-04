#My implementation of the Nand2Tetris Compiler in nand2tetris
#Author: Shaun Cassar


#Class reponsible for 3 main things: 
# 1) Read in the input file, clean it, and produce a list of tokens
# 2) Provide hasMoreCommands, and method for Advance
# 3) Return the type of the current token
# We must focus on first reading and tockenzing a file into a buffer, then its something that can be interated on. 

class JackTokenizer: 
    
    def __init__(self, input_file): 
        
        self.keywords = ["class","constructor","function","method","field", "static","var","int","char","boolean","void","true","false","null","this","let","do","if","else","while","return"]
        self.symbols = ['(',')','{','}','[',']','.',',',';','+','-','=','*','/','&','|','<','>','~']        
        
        self.file_name = input_file
        self.list_tokens = []
        self.total_tokens = 0
        
        self.previous_token= ""
        self.current_token = ""
        self.token_count = -1

        #Simple remove comments where its the start of the line
        self.clean_input_file()
        self.create_tokens()

        print("total tokens: " + str(self.total_tokens))

        #Print the entire token buffer

        #for token in self.list_tokens: 
        #    print("token: " + token + " type: " + self.token_type(token))

    def get_lookahead(self):
        return self.list_tokens[self.token_count+1]

    def get_token(self): 
        return self.current_token

    def get_previous_token(self): 
        return self.previous_token

    def clean_input_file(self): 
        
        output_buffer = []
        self.file = open(self.file_name, "r")
        all_lines = self.file.readlines()
        ignore_line = False

        for line in all_lines:
            if not ignore_line:
                if line[0] == '/' and line[1] == '/':
                    continue
                if line == "\n": 
                    continue
                if "/*" in line and not "*/" in line:
                    print("set true")
                    ignore_line = True
                    continue

            else:
                if "*/" in line:
                    print("set false")
                    ignore_line = False
                continue

            print(line.split('//')[0])
            output_buffer.append(line.split('//')[0])
            
        
        self.outputfile = open(self.file_name, "w")

        for line in output_buffer:
            self.outputfile.write(line)     

        self.outputfile.close()
        self.file.close()
    
    #Return the current token_type
    def token_type(self, token): 
    
        if self.is_keyword(token): 
            #print(f"Token: {token} is type: KEYWORD")
            return "KEYWORD"
        elif self.is_symbol(token): 
            #print(f"Token: {token} is type: SYMBOL")
             return "SYMBOL"
        elif self.is_string_const(token): 
            #print(f"Token: {token} is type: STRING")
            return "STRING_CONST"
        elif self.is_int_const(token): 
            #print(f"Token: {token} is type: INT")
            return "INT_CONST"
        else: 
            #print(f"Token: {token} is type: IDENTIFIER")
            return "IDENTIFIER"


    #As per the course API, creating functions to return the value of the token

    def is_string_const(self, token): 
        if token[0] == '"':
            return True
        else: 
            return False
    
    def is_int_const(self,token): 
        return token.isnumeric()


    #Function responsible for reading through the input file, and create a list of tokens
    #Output: Full list of tokens in order stored in self.list_tokens
    
    #return true if there is more tokens to process
    def has_more_tokens(self): 
        return self.token_count < self.total_tokens-1


    def advance(self): 
        self.previous_token = self.current_token
        self.token_count+=1
        self.current_token = self.list_tokens[self.token_count]


    def create_tokens(self): 
        
        temp_buffer = ""
        store_token = False
        processing_string = False
        
        with open(self.file_name, "r") as read_file:

            #Read the entire Jack file processing character by character
            while(True): 
                character = read_file.read(1)

                if self.is_symbol(character):
                    if len(temp_buffer) > 0:
                        self.list_tokens.append(temp_buffer)  
                        temp_buffer = "" 
                        self.list_tokens.append(character)
                    else: 
                        self.list_tokens.append(character)
                        temp_buffer = "" 
                elif character == '"': 
                    #All characters until we hit another " should be stored"
                    processing_string = not processing_string

                    if not processing_string: 
                        self.list_tokens.append('"'+temp_buffer+'"') 
                        temp_buffer = "" 
                
                elif character == " " and not processing_string: 
                    if len(temp_buffer) > 0:
                        self.list_tokens.append(temp_buffer)  
                        temp_buffer = ""   
                elif character == '\n' or character == "\t": 
                    continue
                else:
                    temp_buffer = temp_buffer + character

                if not character: 
                    break
            
            self.total_tokens = len(self.list_tokens)

    def is_symbol(self, character): 
        check = False

        for symbol in self.symbols: 
            if symbol == character: 
                check = True
                
        return check

    #Returns true if current procesing is a keyword 
    def is_keyword(self, buffer): 
        check = False

        for keyword in self.keywords: 
            if keyword == buffer: 
                check = True
                
        return check



    def close_file(): 
        self.token_file.close()