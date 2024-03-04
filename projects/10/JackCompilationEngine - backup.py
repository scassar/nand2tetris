#My implementation of the Nand2Tetris Compiler in nand2tetris
#Author: Shaun Cassar
#CompilationEngine

#Class reponsible for 3 main things: 
# 1) Read a token
# 2) Determine if the token needs to kick off a specific grammer/statement
# 3) Process tokens as required
# 4) Write to XML to capture parsed tokens and report back errors and quit

#Takes in a tokenizer for the current file as input, so that it can process the tokens
class JackCompilationEngine: 
    
    def __init__(self, output_file, tokenizer): 
        
        self.keywords = ["class","constructor","function","method","field", "static","var","int","char","boolean","void","true","false","null","this","let","do","if","else","while","return"]
        self.symbols = ['(',')','{','}','[',']','.',',',';','+','-','=','*','/','&','|','<','>','~']      
        self.tk = tokenizer
        self.file = output_file
        self.output_file = open(output_file,"w")
        self.output_buffer = []
        self.math_transform = {"<": "&lt;", ">": "&gt;", '"': "&quot;","&":"&amp;"
        }

    #Main function to drive the entire compilation of the output file
    def process(self): 
        print("Start process of the compilation engine")
        current_token = "" 

        self.tk.advance()

        current_token = self.tk.get_token()
        print("current token: " + current_token)

        if self.tk.token_type(current_token) == "KEYWORD": 
            if current_token == "class": 
                self.compile_class(current_token)


        for value in self.output_buffer:
            #print(value)
            self.output_file.write(value+'\n')
            

    #Start to compile the class
    def compile_class(self,start_token): 
        
        print("compiling class")
        self.output_buffer.append("<class>")
        self.output_buffer.append("<keyword> " + start_token + " </keyword>" )
        self.tk.advance()
        current_token = self.tk.get_token()

        self.output_buffer.append("<identifier> " + current_token + " </identifier>")
        self.tk.advance()
        current_token = self.tk.get_token()

        if not current_token == "{": 
            raise Exception("Incorrect syntax, expecting {")
        else: 
            self.output_buffer.append("<symbol> " + current_token + " </symbol>")

        while(self.tk.has_more_tokens()):

            self.tk.advance()
            current_token = self.tk.get_token()

            if current_token == "function" or current_token == "method" or current_token == "constructor":
                self.compile_subroutine(current_token)
            elif current_token == "static" or current_token == "field": 
                self.compile_class_var_dec(current_token)
        
        current_token = self.tk.get_token()
        self.output_buffer.append("<symbol> " + current_token + " </symbol>")
        self.output_buffer.append("</class> ")

    def compile_param(self, start_token):
         self.output_buffer.append("<parameterList>")

         self.tk.advance()

         while self.tk.has_more_tokens() and not (self.tk.current_token == ")"): 
            if self.tk.token_type(self.tk.current_token) == "IDENTIFIER":
                self.output_buffer.append("<identifier> " + self.tk.current_token + " </identifier>")
            elif self.tk.token_type(self.tk.current_token) == "KEYWORD":
                self.output_buffer.append("<keyword> " + self.tk.current_token + " </keyword>")
            elif self.tk.token_type(self.tk.current_token) == "SYMBOL":
                self.output_buffer.append("<symbol> " + self.tk.current_token + " </symbol>")                
            else: 
                raise Exception("incorrect expected value in param list")

            self.tk.advance()
         
         print("final param list token: " + self.tk.current_token)
         self.output_buffer.append("</parameterList>")


    def compile_subroutine(self, start_token): 
            
            print("compiling subroutine")
            self.output_buffer.append("<subroutineDec>")
            self.output_buffer.append("<keyword> " + start_token + " </keyword>" )
            self.tk.advance()
            #data type (come back and cehck this later)
            current_token = self.tk.get_token()
            
            if self.tk.token_type(self.tk.current_token) == "IDENTIFIER": 
                self.output_buffer.append("<identifier> " + current_token + " </identifier>")
            elif self.tk.token_type(self.tk.current_token) == "KEYWORD": 
                self.output_buffer.append("<keyword> " + current_token + " </keyword>")
           
            self.tk.advance()
            current_token = self.tk.get_token()

            if not (self.tk.token_type(current_token) == "IDENTIFIER"): 
                raise Exception ("Identifier expected")
            self.output_buffer.append("<identifier> " + current_token + " </identifier>")
            self.tk.advance()
            current_token = self.tk.get_token()
            
            if not (current_token == "("): 
                raise Exception ("expected ( before parameter list")
            self.output_buffer.append("<symbol> " + current_token + " </symbol>")
            
            #compile_param not yet implemented to cater for params
            self.compile_param(current_token)
            current_token = self.tk.current_token
            print (self.tk.current_token)

            if not current_token == ")": 
                raise Exception (" ) expected after parameter list")
            self.output_buffer.append("<symbol> " + current_token + " </symbol>")
            self.output_buffer.append("<subroutineBody>")

            self.tk.advance()
            current_token = self.tk.get_token()
            if not current_token == "{": 
                raise Exception (" { expected after to contain function body")
            self.output_buffer.append("<symbol> " + current_token + " </symbol>")
            
            while self.tk.has_more_tokens() and not (self.tk.current_token == '}'): 
                
                self.tk.advance()
                current_token = self.tk.get_token()    
                if current_token == "var": 
                    self.compile_var_dec(current_token)
                elif current_token == "}": 
                    self.output_buffer.append("<symbol> " + "}" + " </symbol>")
                else: 
                    self.compile_statements(current_token)
                    self.output_buffer.append("<symbol> " + "}" + " </symbol>")

        
            current_token = self.tk.get_token() 
            print("subroutine final token:" + current_token)
            self.output_buffer.append("</subroutineBody>")
            self.output_buffer.append("</subroutineDec>")
    
    def compile_class_var_dec(self, start_token): 
            print("compiling class variable dec")
            
            current_data_type = ""

            self.output_buffer.append("<classVarDec>")
            self.output_buffer.append("<keyword> " + start_token + " </keyword>" )
           
            self.tk.advance()
            current_token = self.tk.current_token
            
            print(current_token)
            if not (self.tk.token_type(current_token) == "IDENTIFIER" or self.tk.token_type(current_token) == "KEYWORD"): 
                raise Exception ("Identifier expected for variable data type")
            
            current_data_type = self.tk.token_type(current_token)
            print(current_data_type)
            if current_data_type == "KEYWORD": 
                self.output_buffer.append("<keyword> " + current_token + " </keyword>")
            else:
                self.output_buffer.append("<identifier> " + current_token + " </identifier>")
                
            self.tk.advance()
            current_token = self.tk.current_token

            if not (self.tk.token_type(current_token) == "IDENTIFIER"): 
                raise Exception ("Identifier expected for variable name")
            self.output_buffer.append("<identifier> " + current_token + " </identifier>")

            self.tk.advance()
            current_token = self.tk.get_token()

            #Iterate for additional values
            if current_token == ",":
                while(self.tk.has_more_tokens() and not current_token == ";"):
                        self.output_buffer.append("<symbol> , </symbol>")
                        self.tk.advance()
                        current_token = self.tk.get_token()
                        self.output_buffer.append("<identifier> " + current_token + " </identifier>") 
                        self.tk.advance()
                        current_token = self.tk.get_token()                       
            
            if not current_token == ";": 
                raise Exception ("Must end variable statement with ; operator")
            self.output_buffer.append("<symbol> " + current_token + " </symbol>")
            self.output_buffer.append("</classVarDec>")
   
    #Runs per line of the XML
    def compile_var_dec(self, start_token): 
            print("compiling variable dec")
            
            current_data_type = ""

            self.output_buffer.append("<varDec>")
            self.output_buffer.append("<keyword> " + start_token + " </keyword>" )
           
            self.tk.advance()
            current_token = self.tk.current_token
            
            print(current_token)
            if not (self.tk.token_type(current_token) == "IDENTIFIER" or self.tk.token_type(current_token) == "KEYWORD"): 
                raise Exception ("Identifier expected for variable data type")
            
            current_data_type = self.tk.token_type(current_token)
            print(current_data_type)
            if current_data_type == "KEYWORD": 
                self.output_buffer.append("<keyword> " + current_token + " </keyword>")
            else:
                self.output_buffer.append("<identifier> " + current_token + " </identifier>")
                
            self.tk.advance()
            current_token = self.tk.current_token

            if not (self.tk.token_type(current_token) == "IDENTIFIER"): 
                raise Exception ("Identifier expected for variable name")
            self.output_buffer.append("<identifier> " + current_token + " </identifier>")

            self.tk.advance()
            current_token = self.tk.get_token()

            #Iterate for additional values
            if current_token == ",":
                while(self.tk.has_more_tokens() and not current_token == ";"):
                        self.output_buffer.append("<symbol> , </symbol>")
                        self.tk.advance()
                        current_token = self.tk.get_token()
                        self.output_buffer.append("<identifier> " + current_token + " </identifier>") 
                        self.tk.advance()
                        current_token = self.tk.get_token()                       
            
            if not current_token == ";": 
                raise Exception ("Must end variable statement with ; operator")
            self.output_buffer.append("<symbol> " + current_token + " </symbol>")
            self.output_buffer.append("</varDec>")
 

    def compile_statements(self, start_token):
        
        print("compiling statements")
        current_token = start_token
        print("start statements token: " + start_token)
        print("start statements tk token: " + self.tk.current_token)

        self.output_buffer.append("<statements>")

        while self.tk.has_more_tokens() and not self.tk.current_token == '}': 
           
            current_token = self.tk.current_token
            print("final loop: " + current_token)

            if current_token == "let": 
                self.compile_let(current_token)
            elif current_token == "if": 
                self.compile_if(current_token)
            elif current_token == "do": 
                self.compile_do(current_token)
            elif current_token == "while":
                self.compile_while(current_token)
            elif current_token == "return":
                self.compile_return(current_token)
            else:
                print("else loop")
                print(current_token)
                self.tk.advance() 
            
            print("exit loop: " + current_token)
        
        self.output_buffer.append("</statements>")
    
    def compile_let(self, start_token): 
        
        print("compiling let")
        current_token = start_token

        print(current_token)
        
        self.output_buffer.append("<letStatement>")
        self.output_buffer.append("<keyword> " + current_token + " </keyword>" )
        self.tk.advance()
        #data type (come back and cehck this later)
        current_token = self.tk.get_token()
       
        print(current_token)
        if not (self.tk.token_type(current_token) == "IDENTIFIER"): 
            raise Exception ("Identifier expected for let command")
        self.output_buffer.append("<identifier> " + current_token + " </identifier>")
        
        self.tk.advance()
        current_token = self.tk.get_token() 
       
        print(current_token)
        if current_token == "[": 
            print("enter [ let expression case")
            self.output_buffer.append("<symbol> " + current_token + " </symbol>")
            self.tk.advance()
            current_token = self.tk.get_token()             
            self.compile_expression(current_token)
            self.tk.advance()
            current_token = self.tk.current_token
            self.output_buffer.append("<symbol> " + "]" + " </symbol>")

        print(current_token)
        if not current_token == "=": 
            raise Exception ("= Symbol expected for let command")
        
        self.output_buffer.append("<symbol> " + current_token + " </symbol>")

        self.tk.advance()
        current_token = self.tk.get_token() 

        #HACK BECAUSE EXPRESSION IS NOT IMPLEMENTED FAKE EXPRESSION
        print("pre let expression token: " + self.tk.current_token)
        self.compile_expression(current_token)
        
        current_token = self.tk.current_token
        print("post expression token: " + current_token)
        ###############################################

        if not current_token == ";": 
            raise Exception ("; Symbol expected for end of let command")
        self.output_buffer.append("<symbol> " + current_token + " </symbol>")        
        self.output_buffer.append("</letStatement>")
        
        self.tk.advance()
        print("final let token:" + self.tk.current_token) 

    #Function for do - should be simple
    def compile_do(self, start_token): 
        
        print("compiling do statement")
        current_token = start_token

        print(current_token)
        print(self.tk.token_count)
        
        self.output_buffer.append("<doStatement>")
        self.output_buffer.append("<keyword> " + current_token + " </keyword>" )
        self.tk.advance()
        
        #data type (come back and cehck this later)
        current_token = self.tk.get_token()
        print(current_token)
        print(self.tk.token_count)
        if not (self.tk.token_type(current_token) == "IDENTIFIER"): 
            raise Exception ("Identifier expected for do command")
        self.output_buffer.append("<identifier> " + current_token + " </identifier>")
        
        self.tk.advance()
        #data type (come back and cehck this later)
        current_token = self.tk.get_token()

        print(current_token)
        print(self.tk.token_count)
        if current_token == ".": 
            self.output_buffer.append("<symbol> " + current_token + " </symbol>")
       
            self.tk.advance()
            current_token = self.tk.get_token() 
        
            print(current_token)
            print(self.tk.token_count)

            if not (self.tk.token_type(current_token) == "IDENTIFIER"): 
                raise Exception ("Identifier expected for do command")
            self.output_buffer.append("<identifier> " + current_token + " </identifier>")

            self.tk.advance()
            current_token = self.tk.get_token() 
      
            print(current_token)
            print(self.tk.token_count)

        if not current_token == "(": 
            raise Exception ("( Symbol expected for do command to execute function")
        self.output_buffer.append("<symbol> " + current_token + " </symbol>")
        self.tk.advance()
        current_token = self.tk.get_token()

        print(current_token)
        print(self.tk.token_count)
       
        if current_token == ")": 
            self.output_buffer.append("<expressionList>")
            self.output_buffer.append("</expressionList>")
            self.output_buffer.append("<symbol> " + ")" + " </symbol>")

            self.tk.advance()
            current_token = self.tk.get_token()
            print(current_token)
        else:
            print(current_token)
            print(self.tk.token_count)
            #HACK BECAUSE EXPRESSION IS NOT IMPLEMENTED FAKE EXPRESSION
            self.compile_expression_list()
            current_token = self.tk.current_token
           
            print(current_token)
            print(self.tk.token_count)
            if not (current_token == ")"): 
                raise Exception (") expected for do closure expression")
            self.output_buffer.append("<symbol> " + current_token + " </symbol>")  
            
            self.tk.advance()
            current_token = self.tk.get_token() 
           
            ###############################################

        if not current_token == ";": 
            raise Exception ("; Symbol expected for end of do command")
        self.output_buffer.append("<symbol> " + current_token + " </symbol>")  
        
        self.tk.advance()
        current_token = self.tk.get_token()   
        print("final do token:" + current_token) 
        self.output_buffer.append("</doStatement>")

    def compile_while(self, start_token): 
        
        print("compiling while")
        current_token = start_token

        print(current_token)
        
        self.output_buffer.append("<whileStatement>")
        self.output_buffer.append("<keyword> " + current_token + " </keyword>" )
        self.tk.advance()
        #data type (come back and cehck this later)
        current_token = self.tk.get_token()
       
        print(current_token)
        if not (current_token == "("): 
            raise Exception ("( expected for while expression")
        self.output_buffer.append("<symbol> " + current_token + " </symbol>")
        
        self.tk.advance()
        #data type (come back and cehck this later)
        current_token = self.tk.get_token()  
    
        #HACK BECAUSE EXPRESSION IS NOT IMPLEMENTED FAKE EXPRESSION
        self.compile_expression(current_token)
        current_token = self.tk.current_token
        ###############################################

        print(current_token)
        if not (current_token == ")"): 
            raise Exception (") expected for while expression")
        self.output_buffer.append("<symbol> " + current_token + " </symbol>")  
        
        self.tk.advance()
        current_token = self.tk.get_token() 

        print(current_token)
        if not (current_token == "{"): 
            raise Exception ("{ expected for start of while statement block")
        self.output_buffer.append("<symbol> " + current_token + " </symbol>")  

        self.tk.advance()
        current_token = self.tk.get_token() 

        self.compile_statements(current_token)
        current_token = self.tk.get_token() 
        print("post while statement token:" + current_token)
        
        print(current_token)
        if not (current_token == "}"): 
            raise Exception ("} terminator expected for while expression")
        self.output_buffer.append("<symbol> " + current_token + " </symbol>")  

        self.tk.advance()
        current_token = self.tk.get_token() 
        print("final while token:" + self.tk.get_token()) 
        self.output_buffer.append("</whileStatement>")


    def compile_return(self, start_token): 
        print("compiling return statement")
        current_token = start_token

        print(current_token)
        print(self.tk.token_count)
        
        self.output_buffer.append("<returnStatement>")
        self.output_buffer.append("<keyword> " + current_token + " </keyword>" )
        self.tk.advance()
        #data type (come back and cehck this later)
        current_token = self.tk.get_token()
        
        print(current_token)
        print(self.tk.token_count)

        print("entering return expression")
        self.compile_expression(current_token)
       
        current_token = self.tk.current_token

        print("leaving return expression")
        print("return token " + current_token )
        print(self.tk.token_count)

        if (current_token == ";"): 
            self.output_buffer.append("<symbol> " + current_token + " </symbol>")

        self.tk.advance()
        current_token = self.tk.get_token()   
        self.output_buffer.append("</returnStatement>")
        print("final return token:" + current_token) 
    
    def compile_if(self, start_token): 
        
        
        print("compiling if")
        current_token = start_token

        print(current_token)
        
        self.output_buffer.append("<ifStatement>")
        self.output_buffer.append("<keyword> " + current_token + " </keyword>" )
        self.tk.advance()
        #data type (come back and cehck this later)
        current_token = self.tk.get_token()
       
        print(current_token)
        if not (current_token == "("): 
            raise Exception ("( expected for if expression")
        self.output_buffer.append("<symbol> " + current_token + " </symbol>")
        
        self.tk.advance()
        #data type (come back and cehck this later)
        current_token = self.tk.get_token()  
    
        #HACK BECAUSE EXPRESSION IS NOT IMPLEMENTED FAKE EXPRESSION
        self.compile_expression(current_token)
        current_token = self.tk.current_token
        ###############################################

        print(current_token)
        if not (current_token == ")"): 
            raise Exception (") expected for if expression")
        self.output_buffer.append("<symbol> " + current_token + " </symbol>")  
        
        self.tk.advance()
        current_token = self.tk.get_token() 

        print(current_token)
        if not (current_token == "{"): 
            raise Exception ("{ expected for start of if statement block")
        self.output_buffer.append("<symbol> " + current_token + " </symbol>")  

        self.tk.advance()
        current_token = self.tk.get_token() 

        self.compile_statements(current_token)
        current_token = self.tk.get_token() 
        print("post if statement token:" + current_token)
        
        print(current_token)
        if not (current_token == "}"): 
            raise Exception ("} terminator expected for if expression")
        self.output_buffer.append("<symbol> " + current_token + " </symbol>")  

        self.tk.advance()
        current_token = self.tk.get_token() 

        #Check for else statement

        if current_token == "else": 
            print("entering else block under if ")
            self.output_buffer.append("<keyword> " + current_token + " </keyword>" )
            self.tk.advance()
            current_token = self.tk.get_token()

            print(current_token)
            if not (current_token == "{"): 
                raise Exception ("{ expected for start of if-else statement block")
            self.output_buffer.append("<symbol> " + current_token + " </symbol>")  

            self.tk.advance()
            current_token = self.tk.get_token() 

            self.compile_statements(current_token)
            current_token = self.tk.get_token() 
            print("post if-else statement token:" + current_token)

            print(current_token)
            if not (current_token == "}"): 
                raise Exception ("} expected for end of if-else statement block")
            self.output_buffer.append("<symbol> " + current_token + " </symbol>")  

            self.tk.advance()
            current_token = self.tk.get_token() 

        print("final if token:" + self.tk.get_token()) 
        self.output_buffer.append("</ifStatement>")

    #Leaves function without moving on the current_token = always exists at ; currently
    #Will process multiple terms
    def compile_expression(self, start_token): 
        
        if start_token == ";":
            return

        self.output_buffer.append("<expression>")
        current_token = start_token

        first_time_loop = True
        
        print("expression start token: " + current_token)
        start_bracket = False

        while(self.tk.has_more_tokens) and not (current_token == ";" or (current_token == "]" and not start_bracket) or (current_token == ")" and not start_bracket) or (current_token == ",") ): 
            
            #New logic added to fill in the expression block
            if not self.tk.token_type(self.tk.current_token) == "SYMBOL":
                print("compile term: " + self.tk.current_token)
                self.compile_term()
            
            elif self.tk.token_type(self.tk.current_token) == "SYMBOL":
                print("symbol term: " + self.tk.current_token)
                if self.tk.current_token == "(": 
                    self.compile_term()
                else:
                    first_time_loop = False
                    print("this is where the minus sign is going")
                    if self.math_transform.get(self.tk.current_token) is not None:
                        self.output_buffer.append("<symbol> " + self.math_transform.get(self.tk.current_token)+ " </symbol>")
                    else:
                        self.output_buffer.append("<symbol> " + self.tk.current_token+ " </symbol>") 
            


            self.tk.advance()
            current_token = self.tk.get_token()
            print(current_token)
            print(self.tk.token_count)
            
            if current_token == "[" or current_token == "(":
                start_bracket = not start_bracket

            print("expression token: " + current_token)
        
        print("Exit expression final token: " + current_token)
        
        self.output_buffer.append("</expression>")



    #Complex function to handle where we need to create an expression
    #We want to be able to call this function when the start_token = first value following expression start character
    #eg after ( or = )
    #Cases handled: Assignment, inside expression list, single operation like while and if 

    def compile_term(self): 
        
        self.output_buffer.append("<term>")

        #passed in from expression handle
        if self.tk.current_token == "(": 
            print("Starting term token: " + self.tk.current_token)
            self.output_buffer.append("<symbol> " + self.tk.current_token + " </symbol>")
            self.tk.advance()
            self.compile_expression(self.tk.current_token)

        elif self.tk.token_type(self.tk.current_token) == "STRING_CONST": 
            self.output_buffer.append("<stringConstant> " + self.tk.current_token.replace('"',"") + " </stringConstant>")
            
        elif self.tk.token_type(self.tk.current_token) == "INT_CONST": 
            self.output_buffer.append("<integerConstant> " + self.tk.current_token + " </integerConstant>")
        elif self.tk.token_type(self.tk.current_token) == "KEYWORD": 
            self.output_buffer.append("<keyword> " + self.tk.current_token + " </keyword>")            
        elif self.tk.token_type(self.tk.current_token) == "IDENTIFIER": 
            #Here we need to determine what comes next
            print(self.tk.current_token)
            print("IDENTIFER TERM")
            self.output_buffer.append("<identifier> " + self.tk.current_token + " </identifier>")
            self.tk.advance()
            #Now we could get either . [ or (
            if self.tk.current_token == "(": 
                self.output_buffer.append("<symbol> " + self.tk.current_token + " </symbol>")
                print("Calling expression list")
                self.compile_expression_list()
                self.output_buffer.append("<symbol> " + self.tk.current_token + " </symbol>") 
            elif self.tk.current_token == "[": 
                self.output_buffer.append("<symbol> " + self.tk.current_token + " </symbol>")               
                
                print("Calling expression list from [")
                self.tk.advance()

                self.compile_expression(self.tk.current_token)
                self.output_buffer.append("<symbol> " + self.tk.current_token + " </symbol>") 
            
            elif self.tk.current_token == ".":
                self.output_buffer.append("<symbol> " + self.tk.current_token + " </symbol>")
                while(self.tk.has_more_tokens and not (self.tk.current_token == "(")):
                    self.tk.advance()
                    if self.tk.token_type(self.tk.current_token) == "IDENTIFIER": 
                        self.output_buffer.append("<identifier> " + self.tk.current_token + " </identifier>")
                    if self.tk.current_token == ".": 
                        self.output_buffer.append("<symbol> " + self.tk.current_token + " </symbol>")
                
                
                self.output_buffer.append("<symbol> " + self.tk.current_token + " </symbol>")    
                self.tk.advance()
                print("compile expression list")
                self.compile_expression_list()
                self.output_buffer.append("<symbol> " + self.tk.current_token + " </symbol>")              
                
            else: 
                print("term: no special treatment")
                self.tk.current_token = self.tk.previous_token
                self.tk.token_count-=1
                print("term passing back " + self.tk.current_token)
                #self.output_buffer.append("<identifier> " + self.tk.previous_token + " </identifier>")

        
        
        self.output_buffer.append("</term>")



    def compile_expression_list(self):
        self.output_buffer.append("<expressionList>")
        print("expression list start token: " + self.tk.current_token)      
        found_next = True

        while(self.tk.has_more_tokens and found_next):

            self.compile_expression(self.tk.current_token)
            print ("exit compile expression list token: " + self.tk.current_token)

            if self.tk.current_token == ",":
                found_next = True
                self.output_buffer.append("<symbol> " + self.tk.current_token+ " </symbol>")
            else: 
                found_next = False 
            
            self.tk.advance()

        self.tk.current_token = self.tk.previous_token
        self.tk.token_count-=1

        self.output_buffer.append("</expressionList>")



    def close(self): 
        self.output_file.close()