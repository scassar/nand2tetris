# My implementation of the Nand2Tetris Compiler in nand2tetris
# Author: Shaun Cassar
# JackHelper.py (Contains useful helper functions for the CompilationEngine)

math_transform = {"<": "&lt;", 
                  ">": "&gt;", 
                  '"': "&quot;",
                  "&":"&amp;"}

math_transform_vm={ '=':'eq',
                    '+':'add',
                    '-':'sub',
                    '&':'and',
                    '|':'or',
                    '~':'not',
                    '<':'lt',
                    '>':'gt'}

def write_xml_header(keyword, value): 
    if value == "start":
        return f"<{keyword}>"
    else:
        return f"</{keyword}>"


def write_xml(keyword, value): 
    return f"<{keyword}> {value} </{keyword}>"
