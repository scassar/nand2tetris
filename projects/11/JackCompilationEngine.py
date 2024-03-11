# My implementation of the Nand2Tetris Compiler
# Author: Shaun Cassar
# Code: CompilationEngine

# Class reponsible for 3 main things: 
# 1) Read a token
# 2) Determine if the token needs to kick off a specific grammer/statement
# 3) Process tokens as required
# 4) Write to XML to capture parsed tokens and report back errors and quit

# Future Enhancements: Add more Error checking (even though not required for this course)

from JackHelper import * 
from VMWriter import *
from SymbolTable import *

class JackCompilationEngine: 
    
    def __init__(self, output_file, tokenizer): 
         
        self.tk = tokenizer
        self.file = output_file
        self.writer = VMWriter(output_file+".vm")
        self.symbol_table = SymbolTable()
        self.if_label_count = 0
        self.while_label_count = 0
        self.class_name = ""

    # Function will check the currect token matches a particular data type   
    def handle_error_type(self, function, compare_token): 
        if not self.tk.token_type(self.tk.current_token) in compare_token:
            raise Exception(f"Expecting token type of type {compare_token} in {function}")
    
    # Function will check the currect token matches an expected symbol.
    def handle_error_symbol(self, function, compare_token, message): 
        if not self.tk.current_token == compare_token:
            if not message == "": 
                    raise Exception(f"Expected token {compare_token} in {function} {message}")
            else: 
                raise Exception(f"Expected token {compare_token} in {function}")
    
    #Main driver for CompilationEngine. All remaining Functions as per course spec.
    def process(self): 
        self.tk.advance()
        if self.tk.token_type(self.tk.current_token) == "KEYWORD": 
            if self.tk.current_token == "class": 
                self.compile_class()

    def compile_class(self): 

        self.tk.advance() 
        self.class_name = self.tk.current_token 
        self.tk.advance()
        self.handle_error_symbol("class", "{","expected for class command")
 
        while(self.tk.has_more_tokens()):
            self.tk.advance()
            if self.tk.current_token == "function":
                self.compile_subroutine("function")
            if self.tk.current_token == "method":
                self.compile_subroutine("method")
            if self.tk.current_token == "constructor":
                self.compile_subroutine("constructor")
            elif self.tk.current_token == "static" or self.tk.current_token == "field": 
                self.compile_class_var_dec()

    def compile_param(self, type):
        
        self.tk.advance()
        symbol_kind = "argument"
        symbol_type = ""
        symbol_name = ""
        args=0
        set_type = True
        enter_loop = False
        
        if type == "method": 
            self.symbol_table.define('this', 'this',symbol_kind)

        #Not the most elegant solution. May come back to refactor one day rather than requiring loops to assign
        while self.tk.has_more_tokens() and not (self.tk.current_token == ")"): 
            enter_loop = True
            
            if self.tk.token_type(self.tk.current_token) == "IDENTIFIER":
 
                if set_type: 
                    symbol_type = self.tk.current_token
                else: 

                    symbol_name = self.tk.current_token
                set_type = not set_type

            elif self.tk.token_type(self.tk.current_token) == "KEYWORD":
 
                if set_type: 

                    symbol_type = self.tk.current_token
                else:

                    symbol_name = self.tk.current_token
                set_type = not set_type

            elif self.tk.token_type(self.tk.current_token) == "SYMBOL":

                self.symbol_table.define(symbol_name, symbol_type, symbol_kind)
                set_type = True
                symbol_name = ""
                symbol_type = ""
                args+=10
 
            else: 
                raise Exception("incorrect expected value in param list")

            self.tk.advance()

        if enter_loop: 
            self.symbol_table.define(symbol_name, symbol_type, symbol_kind)
            
        return args

    def compile_subroutine(self, type): 
            
            #Reset and start subroutine
            function_nargs = 0
            n_params = 0
            self.symbol_table.reset()
            self.while_label_count = 0
            self.if_label_count = 0
           
            self.tk.advance()
            subroutine_return_type = self.tk.current_token
            self.tk.advance()

            if not (self.tk.token_type(self.tk.current_token) == "IDENTIFIER"): 
                raise Exception ("Identifier expected for subroutine")
 
            subroutine_name = self.tk.current_token
            self.tk.advance()

            if not (self.tk.current_token == "("): 
                raise Exception ("( expected before parameter list")
            
            self.compile_param(type)

            if not self.tk.current_token == ")": 
                raise Exception (" ) expected after parameter list")
 
            self.tk.advance()

            if not self.tk.current_token == "{": 
                raise Exception (" { expected after to contain function body")
 
            self.tk.advance()
            while self.tk.has_more_tokens() and self.tk.current_token == "var": 
                self.compile_var_dec()
                self.tk.advance() 
            self.writer.write_function(self.class_name+"."+subroutine_name, self.symbol_table.var_count("local"))

            if type =='constructor':
                size = self.symbol_table.var_count('field')
                self.writer.write_push('constant',size)
                self.writer.write_call('Memory.alloc',1) 
                self.writer.write_pop('pointer',0)
            elif type=='method':
                self.writer.write_push('argument',0) 
                self.writer.write_pop('pointer',0)  

            self.compile_statements()
            
            self.handle_error_symbol("subroutine", "}", "expected symbol at the end of statements")
    
    def compile_class_var_dec(self): 
            
            current_data_type = ""
            class_var_kind = self.tk.current_token
            
            self.tk.advance()
            
            self.handle_error_type("class var dec",["IDENTIFIER","KEYWORD"])

            class_var_type = self.tk.current_token    
            self.tk.advance()

            self.handle_error_type("class","IDENTIFIER")

            class_var_name = self.tk.current_token
            self.symbol_table.define(class_var_name,class_var_type,class_var_kind)
            self.tk.advance()

            if self.tk.current_token == ",":
                while(self.tk.has_more_tokens() and not self.tk.current_token == ";"):
                        self.tk.advance()
                        class_var_name = self.tk.current_token
                        self.symbol_table.define(class_var_name,class_var_type,class_var_kind)
                        self.tk.advance()
                      
            self.handle_error_symbol("class var dec", ";","at end of variable statement")
   
    def compile_var_dec(self): 
            self.tk.advance()
            
            self.handle_error_type("variable",["IDENTIFIER","KEYWORD"])
            local_variable_kind = "local"

            local_variable_type = self.tk.current_token
                
            self.tk.advance()
            self.handle_error_type("variable","IDENTIFIER")
 
            local_variable_name = self.tk.current_token
            self.symbol_table.define(local_variable_name,local_variable_type, local_variable_kind)
            self.tk.advance()

            if self.tk.current_token == ",":
                while(self.tk.has_more_tokens() and not self.tk.current_token == ";"):
                        self.tk.advance()
                        local_variable_name = self.tk.current_token
                        self.tk.advance()          
                        self.symbol_table.define(local_variable_name,local_variable_type, local_variable_kind)     
            
            self.handle_error_symbol("variable", ";","at end of variable statement")
 
    def compile_statements(self):
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

    def compile_let(self): 
        
        self.tk.advance()
        self.handle_error_type("let","IDENTIFIER")
        variable_name = self.tk.current_token
        variable_type = self.symbol_table.type_of(variable_name)
        variable_kind = self.symbol_table.kind_of(variable_name)
        variable_index = self.symbol_table.index_of(variable_name)

        if variable_kind == "field": 
            variable_kind = "this"
        
        self.tk.advance()
        
        if self.tk.current_token == "[": 
 
            self.tk.advance()
            self.compile_expression()
            current_token = self.tk.get_token()
            self.writer.write_push(variable_kind, variable_index)
            self.writer.write_arithmetic("add")

            self.handle_error_symbol("let", "]","expected for let command")
 
            self.tk.advance()
            current_token = self.tk.get_token() 

            self.handle_error_symbol("let", "=","expected for let command")
            
            self.tk.advance()

            self.compile_expression()
            self.writer.write_pop('temp',0)
            self.writer.write_pop('pointer',1)
            self.writer.write_push('temp',0)
            self.writer.write_pop('that',0)
            self.handle_error_symbol("let", ";","expected for end of let command")
 
        else:
            self.handle_error_symbol("let", "=","expected for let command")
            self.tk.advance()
            self.compile_expression()
            self.handle_error_symbol("let", ";","expected for end of let command")
            self.writer.write_pop(variable_kind, variable_index)
        self.tk.advance()

    def compile_do(self): 
        self.tk.advance()
        
        self.handle_error_type("do","IDENTIFIER")
        expression_args = 0
        return_args = 0
        subroutine_name = self.tk.current_token
        
        self.tk.advance()

        if self.tk.current_token == ".": 
            #We must determine if the call is for a class, or an object. Check the symbol table for reference
            subroutine_type = self.symbol_table.type_of(subroutine_name)
            if subroutine_type != None:  #Its a class that has been defined

                subroutine_kind = self.symbol_table.kind_of(subroutine_name)
                subroutine_index = self.symbol_table.index_of(subroutine_name)
                
                subroutine_name = self.symbol_table.type_of(subroutine_name)

                expression_args+=1

                if subroutine_kind == "field":
                    subroutine_kind = "this"
                self.writer.write_push(subroutine_kind,subroutine_index)
 
            subroutine_name = subroutine_name+self.tk.current_token

            self.tk.advance()

            self.handle_error_type("do","IDENTIFIER")
 
            subroutine_name = subroutine_name+self.tk.current_token
            self.tk.advance()

        else: #Calling method that belongs to the current class
            subroutine_name = self.class_name+"."+subroutine_name
            self.writer.write_push("pointer",0)
            expression_args+=1

        self.handle_error_symbol("do", "("," symbol expected for do command to execute function")
 
        self.tk.advance()
       
        if self.tk.current_token == ")": 
 
            self.tk.advance()

        else:
            return_args = self.compile_expression_list()
            self.handle_error_symbol("do", ")"," expected for do closure expression")
 
            self.tk.advance()
        
        self.handle_error_symbol("do", ";"," Symbol expected for end of do command")
 
        self.writer.write_call(subroutine_name, expression_args+return_args)
        
        self.writer.write_pop("temp", 0)
        self.tk.advance()

    def compile_while(self): 
        
        self.tk.advance()

        self.handle_error_symbol("while", "("," expected for while expression")
 
        self.tk.advance()
        start_while_count = str(self.while_label_count)
        end_while_count = str(self.while_label_count)
        self.while_label_count+=1 

        self.writer.write_label("WHILE_EXP"+start_while_count)

        self.compile_expression()

        self.writer.write_arithmetic('not')

        self.writer.write_if("WHILE_END"+end_while_count)

        self.handle_error_symbol("while", ")"," expected for while expression")
 
        self.tk.advance()

        self.handle_error_symbol("while", "{"," expected for start of while statement block")
 
        self.tk.advance()
        self.compile_statements()
        self.writer.write_goto("WHILE_EXP"+start_while_count)
        self.writer.write_label("WHILE_END"+end_while_count)
        self.handle_error_symbol("while", "}"," terminator expected for while expression")
 
        self.tk.advance()
 
    def compile_return(self): 
 
        self.tk.advance()
        
        if not (self.tk.current_token == ";"): 
            self.compile_expression()
            self.writer.write_return()
        else:    
 
            self.writer.write_push("constant", 0)
            self.writer.write_return()
       
        self.tk.advance()
 
    def compile_if(self): 
 
        self.tk.advance()
        
        self.handle_error_symbol("if", "("," expected for if expression")
        self.tk.advance()
        start_if_count = str(self.if_label_count)
        end_if_count = str(self.if_label_count)
        self.if_label_count+=1 

        self.compile_expression()

        self.writer.write_if("IF_TRUE"+start_if_count)
        self.writer.write_goto("IF_FALSE" + end_if_count)
        self.writer.write_label("IF_TRUE"+start_if_count)
        
        self.handle_error_symbol("if", ")"," expected for if expression")
        self.tk.advance()
        self.handle_error_symbol("if", "{"," expected for start of if statement block")
        self.tk.advance()

        self.compile_statements()

        self.handle_error_symbol("if", "}"," terminator expected for if expression")

        self.tk.advance()
        
        if self.tk.current_token == "else": 
            self.writer.write_goto("IF_END"+ end_if_count)
        if self.tk.current_token == "else": 
            self.writer.write_label("IF_FALSE" + end_if_count)
 
            self.tk.advance()
            self.handle_error_symbol("if-else", "{"," expected for start of if-else statement block")
            self.tk.advance()
            
            self.compile_statements()
            self.handle_error_symbol("if-else", "}"," expected for end of if-else statement block")
 
            self.tk.advance()
            self.writer.write_label("IF_END"+ end_if_count)
        else:
            self.writer.write_label("IF_FALSE" + end_if_count)
 
    def compile_expression(self): 
 
        expression_term = None
       
        if self.tk.current_token == "(": 
            self.tk.advance()
            self.compile_expression()
            self.tk.advance()

        else: 
            self.compile_term()

        while(self.tk.has_more_tokens and self.tk.current_token in ".+-*/&|<>="): 
                 
            expression_term = self.tk.current_token 
            self.tk.advance()
            self.compile_term()

            if expression_term is not None:
                if expression_term == "*": 
                    self.writer.write_call("Math.multiply", 2)
                elif expression_term == "/":
                    self.writer.write_call("Math.divide", 2)
                else:
                    self.writer.write_arithmetic(math_transform_vm[expression_term])
                    
    def compile_term(self): 

        if self.tk.token_type(self.tk.current_token) == "STRING_CONST": 
            fixed_string = self.tk.current_token.replace('"',"")
            string_length = len(fixed_string)
            self.writer.write_push("constant", string_length)
            self.writer.write_call("String.new", 1)
            for letter in fixed_string: 
                value = ord(letter)
                self.writer.write_push("constant", value)
                self.writer.write_call("String.appendChar",2)       
        elif self.tk.token_type(self.tk.current_token) == "INT_CONST": 
            self.writer.write_push("constant", self.tk.current_token)         
        elif self.tk.token_type(self.tk.current_token) == "KEYWORD": 
            if self.tk.current_token in ["null", "false"]: 
                self.writer.write_push("constant", 0)
            elif self.tk.current_token == "true":
                self.writer.write_push("constant", 0)
                self.writer.write_arithmetic("not") 
            elif self.tk.current_token == "this":
                self.writer.write_push("pointer", 0) 
        elif self.tk.token_type(self.tk.current_token) == "SYMBOL":
            if self.tk.current_token == "(": 
                self.tk.advance()
                self.compile_expression()
                self.handle_error_symbol("compile-term", ")"," expected in return from term")  
            elif self.tk.current_token in ["-","~"]: 
                token = self.tk.current_token
                self.tk.advance()
                self.compile_term()
                if token == "-":
                    self.writer.write_arithmetic("neg")
                elif token == "~":
                    self.writer.write_arithmetic("not")
                return

        elif self.tk.token_type(self.tk.current_token) == "IDENTIFIER": 
            
            variable_start_name = self.tk.current_token
            variable_type = self.symbol_table.type_of(self.tk.current_token)
            variable_kind = self.symbol_table.kind_of(self.tk.current_token)
            variable_index = self.symbol_table.index_of(self.tk.current_token)
            
            if variable_kind == "field": 
                variable_kind = "this"
            look_ahead = self.tk.get_lookahead()
            
            if look_ahead == "(": 
                n_args = 1
                self.tk.advance()
                self.tk.advance()
                n_args_return = self.compile_expression_list()
                n_args = n_args+n_args_return
                self.writer.write_push("pointer", 0)
                self.writer.write_call(self.class_name+"."+variable_start_name, n_args)
            
            elif look_ahead == "[": 
                self.tk.advance()
 
                self.tk.advance()
                self.compile_expression()
                self.handle_error_symbol("compile-term", "]"," Missing ] in array element from term") 
                self.writer.write_push(variable_kind,variable_index)
                self.writer.write_arithmetic("add")
                self.writer.write_pop('pointer',1)
                self.writer.write_push('that',0)
                
            elif look_ahead == ".":
                n_args = 0
                if variable_type is not None: #variable is a class
                    n_args+=1
                    if variable_kind != 'field': 
                        self.writer.write_push(variable_kind, variable_index)
                    else: 
                        self.writer.write_push('this', variable_index)
                    variable_start_name = variable_type

                self.tk.advance()
                variable_start_name = variable_start_name + self.tk.current_token
                self.tk.advance()
                self.handle_error_type("term","IDENTIFIER")
 
                variable_start_name = variable_start_name + self.tk.current_token
                self.tk.advance()
                self.tk.advance()
                
                n_args_return = self.compile_expression_list()
                n_args = n_args + n_args_return

                self.writer.write_call(variable_start_name, n_args)
 
            else: 
                self.writer.write_push(variable_kind, variable_index) 
       
        self.tk.advance()

    def compile_expression_list(self):
        
        found_next = True
        total_args = 0
        if self.tk.current_token == ")": 
            return 0

        while(self.tk.has_more_tokens and found_next):

            total_args+=1
            self.compile_expression()

            if self.tk.current_token == ",":
                found_next = True
            else: 
                found_next = False 
            
            self.tk.advance()

        #Given the structure, this will return the character after ) (;) - rollback one character in this case
        self.tk.current_token = self.tk.previous_token
        self.tk.token_count-=1
        return total_args

    def close(self): 
        self.output_file.close()
        self.writer.close()