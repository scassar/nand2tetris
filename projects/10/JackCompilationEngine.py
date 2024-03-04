#My implementation of the Nand2Tetris Compiler
#Author: Shaun Cassar
#Code: CompilationEngine

#Class reponsible for 3 main things: 
# 1) Read a token
# 2) Determine if the token needs to kick off a specific grammer/statement
# 3) Process tokens as required
# 4) Write to XML to capture parsed tokens and report back errors and quit

from JackHelper import * 

class JackCompilationEngine: 
    
    def __init__(self, output_file, tokenizer): 
         
        self.tk = tokenizer
        self.file = output_file
        self.output_file = open(output_file,"w")
        self.output_buffer = []

    def write_buffer(self, line):
        self.output_buffer.append(line)
    
    def handle_error_type(self, function, compare_token): 
        if not self.tk.token_type(self.tk.current_token) in compare_token:
            raise Exception(f"Expecting token type of type {compare_token} in {function}")

    def handle_error_symbol(self, function, compare_token, message): 
        if not self.tk.current_token == compare_token:
            if not message == "": 
                    raise Exception(f"Expected token {compare_token} in {function} {message}")
            else: 
                raise Exception(f"Expected token {compare_token} in {function}")
    
    def process(self): 
        self.tk.advance()
        if self.tk.token_type(self.tk.current_token) == "KEYWORD": 
            if self.tk.current_token == "class": 
                self.compile_class()

        for value in self.output_buffer:
            self.output_file.write(value+'\n')

    def compile_class(self): 

        self.write_buffer(write_xml_header("class", "start"))
        self.write_buffer(write_xml("keyword", self.tk.current_token))
        self.tk.advance()

        self.write_buffer(write_xml("identifier", self.tk.current_token))
        self.tk.advance()
        
        self.handle_error_symbol("class", "{","expected for class command")
        self.write_buffer(write_xml("symbol", self.tk.current_token))

        while(self.tk.has_more_tokens()):

            self.tk.advance()

            if self.tk.current_token == "function" or self.tk.current_token == "method" or self.tk.current_token == "constructor":
                self.compile_subroutine()
            elif self.tk.current_token == "static" or self.tk.current_token == "field": 
                self.compile_class_var_dec()

        self.write_buffer(write_xml("symbol", self.tk.current_token))
        self.write_buffer(write_xml_header("class", ""))        


    def compile_param(self):
        
        self.write_buffer(write_xml_header("parameterList", "start"))
        self.tk.advance()

        while self.tk.has_more_tokens() and not (self.tk.current_token == ")"): 
            if self.tk.token_type(self.tk.current_token) == "IDENTIFIER":
                self.write_buffer(write_xml("identifier", self.tk.current_token))
            elif self.tk.token_type(self.tk.current_token) == "KEYWORD":
                self.write_buffer(write_xml("keyword", self.tk.current_token))
            elif self.tk.token_type(self.tk.current_token) == "SYMBOL":
                self.write_buffer(write_xml("symbol", self.tk.current_token))  
            else: 
                raise Exception("incorrect expected value in param list")

            self.tk.advance()
        
        self.write_buffer(write_xml_header("parameterList", ""))

    def compile_subroutine(self): 
            
            self.write_buffer(write_xml_header("subroutineDec", "start"))
            self.write_buffer(write_xml("keyword", self.tk.current_token))            
            
            self.tk.advance()
                       
            if self.tk.token_type(self.tk.current_token) == "IDENTIFIER": 
                self.write_buffer(write_xml("identifier", self.tk.current_token))
            elif self.tk.token_type(self.tk.current_token) == "KEYWORD": 
                self.write_buffer(write_xml("keyword", self.tk.current_token))
           
            self.tk.advance()

            if not (self.tk.token_type(self.tk.current_token) == "IDENTIFIER"): 
                raise Exception ("Identifier expected for subroutine")
            self.write_buffer(write_xml("identifier", self.tk.current_token))
            self.tk.advance()

            
            if not (self.tk.current_token == "("): 
                raise Exception ("( expected before parameter list")
            self.write_buffer(write_xml("symbol", self.tk.current_token))
            
            self.compile_param()

            if not self.tk.current_token == ")": 
                raise Exception (" ) expected after parameter list")
            self.write_buffer(write_xml("symbol", self.tk.current_token))

            self.write_buffer(write_xml_header("subroutineBody", "start"))

            self.tk.advance()

            if not self.tk.current_token == "{": 
                raise Exception (" { expected after to contain function body")
            self.write_buffer(write_xml("symbol", self.tk.current_token))
            
            while self.tk.has_more_tokens() and not (self.tk.current_token == '}'): 
                self.tk.advance()
                
                if self.tk.current_token == "var": 
                    self.compile_var_dec()
                elif self.tk.current_token == "}": 
                    self.write_buffer(write_xml("symbol", self.tk.current_token))
                else: 
                    self.compile_statements()
            
            self.write_buffer(write_xml_header("subroutineBody", ""))
            self.write_buffer(write_xml_header("subroutineDec", ""))

    
    def compile_class_var_dec(self): 
            
            current_data_type = ""
            
            self.write_buffer(write_xml_header("classVarDec", "start"))
            self.write_buffer(write_xml("keyword", self.tk.current_token))           
            self.tk.advance()
            
            self.handle_error_type("class var dec",["IDENTIFIER","KEYWORD"])

            if self.tk.token_type(self.tk.current_token) == "KEYWORD": 
                self.write_buffer(write_xml("keyword", self.tk.current_token))
            else:
                self.write_buffer(write_xml("identifier", self.tk.current_token))
                
            self.tk.advance()

            self.handle_error_type("class","IDENTIFIER")

            self.write_buffer(write_xml("identifier", self.tk.current_token))

            self.tk.advance()

            if self.tk.current_token == ",":
                while(self.tk.has_more_tokens() and not self.tk.current_token == ";"):
                        self.write_buffer(write_xml("symbol", self.tk.current_token))
                        self.tk.advance()
                        self.write_buffer(write_xml("identifier", self.tk.current_token)) 
                        self.tk.advance()
                      
            self.handle_error_symbol("class var dec", ";","at end of variable statement")

            self.write_buffer(write_xml("symbol", self.tk.current_token))
            self.write_buffer(write_xml_header("classVarDec", ""))
   
    def compile_var_dec(self): 

            self.write_buffer(write_xml_header("varDec", "start"))
            self.write_buffer(write_xml("keyword", self.tk.current_token))
           
            self.tk.advance()
            
            self.handle_error_type("variable",["IDENTIFIER","KEYWORD"])
            
            if self.tk.token_type(self.tk.current_token) == "KEYWORD": 
                self.write_buffer(write_xml("keyword", self.tk.current_token))
            else:
                self.write_buffer(write_xml("identifier", self.tk.current_token))
                
            self.tk.advance()

            self.handle_error_type("variable","IDENTIFIER")

            self.write_buffer(write_xml("identifier", self.tk.current_token))

            self.tk.advance()

            if self.tk.current_token == ",":
                while(self.tk.has_more_tokens() and not self.tk.current_token == ";"):
                        self.write_buffer(write_xml("symbol", self.tk.current_token))
                        self.tk.advance()
                        self.write_buffer(write_xml("identifier", self.tk.current_token)) 
                        self.tk.advance()               
            
            self.handle_error_symbol("variable", ";","at end of variable statement")
            self.write_buffer(write_xml("symbol", self.tk.current_token))
            self.write_buffer(write_xml_header("varDec", ""))
 

    def compile_statements(self):
        self.write_buffer(write_xml_header("statements", "start"))

        while self.tk.has_more_tokens() and self.tk.current_token in ('let','if','do','while','return'): 
           
            if self.tk.current_token == "let": 
                self.compile_let()
            elif self.tk.current_token == "if": 
                self.compile_if()
            elif self.tk.current_token == "do": 
                self.compile_do()
            elif self.tk.current_token == "while":
                self.compile_while()
            elif self.tk.current_token == "return":
                self.compile_return()

        self.write_buffer(write_xml_header("statements", ""))
    
    def compile_let(self): 
        
        self.write_buffer(write_xml_header("letStatement", "start"))        
        self.write_buffer(write_xml("keyword", self.tk.current_token))
        self.tk.advance()

        self.handle_error_type("let","IDENTIFIER")
        self.write_buffer(write_xml("identifier", self.tk.current_token))
        
        self.tk.advance()
       
        if self.tk.current_token == "[": 
            self.write_buffer(write_xml("symbol", self.tk.current_token))
            self.tk.advance()

            self.compile_expression()

            current_token = self.tk.get_token()

            self.handle_error_symbol("let", "]","expected for let command")
            self.write_buffer(write_xml("symbol", self.tk.current_token))

            self.tk.advance()
            current_token = self.tk.get_token() 

        self.handle_error_symbol("let", "=","expected for let command")
        
        self.write_buffer(write_xml("symbol", self.tk.current_token))

        self.tk.advance()

        self.compile_expression()
        self.handle_error_symbol("let", ";","expected for end of let command")
        self.write_buffer(write_xml("symbol", self.tk.current_token))        
        self.write_buffer(write_xml_header("letStatement", ""))
        self.tk.advance()

    def compile_do(self): 
        
        self.write_buffer(write_xml_header("doStatement", "start"))         
        self.write_buffer(write_xml("keyword", self.tk.current_token))
        self.tk.advance()
        
        self.handle_error_type("do","IDENTIFIER")

        self.write_buffer(write_xml("identifier", self.tk.current_token))
        
        self.tk.advance()

        if self.tk.current_token == ".": 
            self.write_buffer(write_xml("symbol", self.tk.current_token))
       
            self.tk.advance()

            self.handle_error_type("do","IDENTIFIER")
            self.write_buffer(write_xml("identifier", self.tk.current_token))

            self.tk.advance()
        
        self.handle_error_symbol("do", "("," symbol expected for do command to execute function")
        self.write_buffer(write_xml("symbol", self.tk.current_token))
        self.tk.advance()
       
        if self.tk.current_token == ")": 
            self.write_buffer(write_xml_header("expressionList", "start")) 
            self.write_buffer(write_xml_header("expressionList", "")) 
            self.write_buffer(write_xml("symbol", self.tk.current_token))
            self.tk.advance()

        else:
            self.compile_expression_list()
            self.handle_error_symbol("do", ")"," expected for do closure expression")
            self.write_buffer(write_xml("symbol", self.tk.current_token))  
            self.tk.advance()
        
        self.handle_error_symbol("do", ";"," Symbol expected for end of do command")

        self.write_buffer(write_xml("symbol", self.tk.current_token))  
        
        self.tk.advance()
        self.write_buffer(write_xml_header("doStatement", ""))

    def compile_while(self): 
        
        self.write_buffer(write_xml_header("whileStatement", "start"))
        self.write_buffer(write_xml("keyword", self.tk.current_token))
        self.tk.advance()
        
        self.handle_error_symbol("while", "("," expected for while expression")
        self.write_buffer(write_xml("symbol", self.tk.current_token))
        
        self.tk.advance()
        self.compile_expression()

        self.handle_error_symbol("while", ")"," expected for while expression")
        self.write_buffer(write_xml("symbol", self.tk.current_token))  
        
        self.tk.advance()

        self.handle_error_symbol("while", "{"," expected for start of while statement block")
        self.write_buffer(write_xml("symbol", self.tk.current_token))  

        self.tk.advance()
        self.compile_statements()
        
        self.handle_error_symbol("while", "}"," terminator expected for while expression")
        self.write_buffer(write_xml("symbol", self.tk.current_token))  

        self.tk.advance()
        self.write_buffer(write_xml_header("whileStatement", ""))

    def compile_return(self): 
        
        self.write_buffer(write_xml_header("returnStatement", "start"))
        self.write_buffer(write_xml("keyword", self.tk.current_token))
        self.tk.advance()
        
        if not (self.tk.current_token == ";"): 

            self.compile_expression()


            self.write_buffer(write_xml("symbol", self.tk.current_token))
        else:    
            self.write_buffer(write_xml("symbol", self.tk.current_token))
       
        self.write_buffer(write_xml_header("returnStatement", ""))
    
    def compile_if(self): 
        self.write_buffer(write_xml_header("ifStatement", "start"))               
        self.write_buffer(write_xml("keyword", self.tk.current_token))
        
        self.tk.advance()
        
        self.handle_error_symbol("if", "("," expected for if expression")
        self.write_buffer(write_xml("symbol", self.tk.current_token))
        
        self.tk.advance()

        self.compile_expression()
        
        self.handle_error_symbol("if", ")"," expected for if expression")
        self.write_buffer(write_xml("symbol", self.tk.current_token))  
        self.tk.advance()

        self.handle_error_symbol("if", "{"," expected for start of if statement block")
        self.write_buffer(write_xml("symbol", self.tk.current_token))  

        self.tk.advance()

        self.compile_statements()
        
        self.handle_error_symbol("if", "}"," terminator expected for if expression")
        self.write_buffer(write_xml("symbol", self.tk.current_token))  
        self.tk.advance()
  
        if self.tk.current_token == "else": 

            self.write_buffer(write_xml("keyword", self.tk.current_token))
            self.tk.advance()
            
            self.handle_error_symbol("if-else", "{"," expected for start of if-else statement block")
            self.write_buffer(write_xml("symbol", self.tk.current_token))  

            self.tk.advance()

            self.compile_statements()
            
            self.handle_error_symbol("if-else", "}"," expected for end of if-else statement block")
            self.write_buffer(write_xml("symbol", self.tk.current_token))  

            self.tk.advance()
        self.write_buffer(write_xml_header("ifStatement", ""))

    def compile_expression(self): 
        self.write_buffer(write_xml_header("expression", "start"))        
       
        if self.tk.current_token == "(": 
            self.write_buffer(write_xml_header("term", "start"))
            self.write_buffer(write_xml("symbol", self.tk.current_token))         
            
            self.tk.advance()
            self.compile_expression()
            self.write_buffer(write_xml("symbol", self.tk.current_token)) 
            self.write_buffer(write_xml_header("term", ""))
            self.tk.advance()

        else: 
            self.compile_term()

        while(self.tk.has_more_tokens and self.tk.current_token in ".+-*/&|<>="): 
            
            if not math_transform.get(self.tk.current_token) == None: 
                self.write_buffer(write_xml("symbol", math_transform.get(self.tk.current_token)))                
            else:
                self.write_buffer(write_xml("symbol", self.tk.current_token))               
            
            self.tk.advance()
            self.compile_term()
        self.write_buffer(write_xml_header("expression", ""))             

    def compile_term(self): 
        
        self.write_buffer(write_xml_header("term", "start"))
        
        if self.tk.token_type(self.tk.current_token) == "STRING_CONST": 
            self.write_buffer(write_xml("stringConstant", self.tk.current_token.replace('"',"")))
        elif self.tk.token_type(self.tk.current_token) == "INT_CONST": 
            self.write_buffer(write_xml("integerConstant", self.tk.current_token))            
        elif self.tk.token_type(self.tk.current_token) == "KEYWORD": 
            self.write_buffer(write_xml("keyword", self.tk.current_token))            
        elif self.tk.token_type(self.tk.current_token) == "SYMBOL":
            if self.tk.current_token == "(": 
                self.write_buffer(write_xml("symbol", self.tk.current_token))
                self.tk.advance()
                self.compile_expression()
                
                self.handle_error_symbol("compile-term", ")"," expected in return from term")  
                self.write_buffer(write_xml("symbol", self.tk.current_token))                             

            elif self.tk.current_token in ["-","~"]: 
                self.write_buffer(write_xml("symbol", self.tk.current_token))
                self.tk.advance()
                self.compile_term()
                
                self.write_buffer(write_xml_header("term", ""))
                return

        elif self.tk.token_type(self.tk.current_token) == "IDENTIFIER": 
            
            self.write_buffer(write_xml("identifier", self.tk.current_token))
            
            look_ahead = self.tk.get_lookahead()
            
            if look_ahead == "(": 
                self.tk.advance()
                self.compile_expression_list()
            
            elif look_ahead == "[": 
                self.tk.advance()
                self.write_buffer(write_xml("symbol", self.tk.current_token))               
                self.tk.advance()

                self.compile_expression()
                
                self.handle_error_symbol("compile-term", "]"," Missing ] in array element from term") 
                self.write_buffer(write_xml("symbol", self.tk.current_token))                      

            elif look_ahead == ".":
                self.tk.advance()

                self.write_buffer(write_xml("symbol", self.tk.current_token))
                
                self.tk.advance()
                
                self.handle_error_type("term","IDENTIFIER")
                self.write_buffer(write_xml("identifier", self.tk.current_token))
                self.tk.advance()
                self.write_buffer(write_xml("symbol", self.tk.current_token))   
                self.tk.advance()
                
                self.compile_expression_list()
                self.write_buffer(write_xml("symbol", self.tk.current_token))              

        self.tk.advance()
        self.write_buffer(write_xml_header("term", ""))

    def compile_expression_list(self):
        
        self.write_buffer(write_xml_header("expressionList", "start"))
        
        found_next = True
        total_args = 0

        if self.tk.current_token == ")": 
            self.write_buffer(write_xml_header("expressionList", ""))
            return 0

        while(self.tk.has_more_tokens and found_next):

            total_args+=1
            self.compile_expression()

            if self.tk.current_token == ",":
                found_next = True
                self.write_buffer(write_xml("symbol", self.tk.current_token))
            else: 
                found_next = False 
            
            self.tk.advance()

        #Given the structure, this will return the character after ) (;) - rollback one character in this case
        self.tk.current_token = self.tk.previous_token
        self.tk.token_count-=1
        self.write_buffer(write_xml_header("expressionList", ""))
        return total_args


    def close(self): 
        self.output_file.close()