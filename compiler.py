# import lexems_to_csv as lex;
import pandas as pd
import numpy as np

import preprocess
from automata.fa.dfa import DFA
import re
import automata_read as auto
import csv
import networkx as net;
import matplotlib.pyplot as plt

# there is a problem in pygraphiz library on windows
try:
    import pygraphviz
except Exception as e:
    print("IMPORTING Error");
 
ext = 0 ;


def build_graph(curr_node , last_node):
        g.add_node(curr_node );
        g.add_edge(last_node , curr_node );



g = net.DiGraph();
last_call_node = "prog_si" ;
g.add_node("prog_si");





text = """program test;
var d : array [ 0 .. 5 ] of array [1..4] of integer ; abc , b , c , ahmedAbed : integer ; n , test : real ;
begin
a := ac + b ;
a := (a*5.3)+ 4.5 ;
if a :< b then
a := 'aASGAFD' ;
b := ( a * 6 ) + 4 ;
c := ahmed ;
while ( a + ( x * c ) ) >= ( ahmed - abed ) do
f := 5 ;
end ."""














# to prevent white space problem , for instance : x=5 and  x = 5 ;


text = preprocess.normalize_spaces(text);

tokens = re.split(r'\s+', text);



try:
    tokens_list = auto.read_dfa(tokens);
    print(tokens_list);
except Exception as e:
    print("Lexical Error" , e);
    exit(1);
    
    
token_pointer = 0;

def progSI2024():

    global token_pointer;

    if tokens_list[token_pointer][0] == "program":
        token_pointer += 1

        if tokens_list[token_pointer][1] == "nom prog":
            token_pointer += 1

            if tokens_list[token_pointer][0] == ";":
                token_pointer += 1
                last_call_node = 'progSI2024';
                corps();

                if tokens_list[token_pointer][0] == ".":
                    token_pointer += 1
                else:
                    print("Missing '.' at the end of the program")
            else:
                print("Missing ';' after program name")
        else:
            print("Invalid program name")
    else:
        print("Program declaration Error !! ")


def corps():
    global token_pointer
    global last_call_node 
    global ext

    ext+=1;
    curr_node = "corps" + str(ext) ;
    build_graph(curr_node , last_call_node);

    if tokens_list[token_pointer][0] not in ["const" , "var"]:
        last_call_node = curr_node;
        instr_comp()
    else :
        last_call_node = curr_node;
        partie_definition_constante()
        print("partie_definition_CONST() TERMINE ! ")

        last_call_node = curr_node;
        partie_definition_variable()
        print("partie_definition_variable() TERMINE ! ")

        last_call_node = curr_node;
        instr_comp()




    print("La Partie corp est bien definie ! ")


def partie_definition_constante():
    global token_pointer
    global last_call_node 
    global ext
    
    ext+=1;
    curr_node = "partie_def_const" + str(ext);
    build_graph(curr_node , last_call_node)

    if tokens_list[token_pointer][0] == "const":
        token_pointer += 1
        last_call_node = curr_node;
        definition_constante()

        if tokens_list[token_pointer - 1 ][0] == ";":
            print("partie definition constante bien definie !! ")
        else:
            print(" ';' missing !!")
    else:
        last_call_node = curr_node;
        vide()



# else:
#     return ;


def definition_constante():
    global token_pointer
    global last_call_node 
    global ext
    
    ext+=1;
    curr_node = "def_const" + str(ext);
    build_graph(curr_node , last_call_node);

    if tokens_list[token_pointer][1] == "identifier" or tokens_list[token_pointer][1] == "nom prog":
        token_pointer += 1

        if tokens_list[token_pointer][0] == "=":

            token_pointer += 1

            if tokens_list[token_pointer][1] == "integer" or tokens_list[token_pointer][1] == "real" or tokens_list[token_pointer][1] == "string":
                token_pointer += 1

                if tokens_list[token_pointer][0] == ";":
                    token_pointer += 1
                    last_call_node = curr_node;
                    definition_constante()
                else:
                    print("Missing ';' in definition constant")
            else:
                print("Invalid constant type")
        else:
            print("Missing '=' in definition constant")
            exit(0)
    else:
        return
#*************************************************************************************************************
#*****************************************  PARTIE VAR  ********************************************************************
def partie_definition_variable():
    global token_pointer
    global last_call_node 
    global ext

    ext+=1;

    curr_node = "partie_def_var" + str(ext);
    build_graph(curr_node , last_call_node);

    if tokens_list[token_pointer][0] == "var":

        token_pointer += 1
        last_call_node = curr_node;
        definition_variables()

        if tokens_list[token_pointer - 1 ][0] == ";":
            print("Partie definition variable bien definie !! ")
        else:
            print("';' missing !!")
    else:
        last_call_node = curr_node;
        vide()





def definition_variable():
    global token_pointer
    global last_call_node 
    global ext

    ext+=1;
    curr_node = "def_var" + str(ext);
    build_graph(curr_node , last_call_node);

    if tokens_list[token_pointer][1] == "identifier" or tokens_list[token_pointer][1] == "nom prog" :
        last_call_node = curr_node;
        groupe_variable()
        if tokens_list[token_pointer][0] == ":":
            token_pointer += 1

            if tokens_list[token_pointer][0] == "integer" or tokens_list[token_pointer][0] == "real" or tokens_list[token_pointer][0] == "char" or tokens_list[token_pointer][0] == "string" :
                token_pointer += 1
                if tokens_list[token_pointer][0] == ";":
                    token_pointer += 1
                    last_call_node =  curr_node;
                    definition_variable()
                else:
                    print("Missing ';' in definition variables")
            elif tokens_list[token_pointer][0] == "array" :
                last_call_node =  curr_node;
                tableau()
                if tokens_list[token_pointer][0] == ";":
                    token_pointer += 1
                    last_call_node =  curr_node;
                    definition_variable()
                else:
                    print("Missing ';' in definition variables")

            else:
                print("Invalid variable type")
        else:
            print("Missing ':' in definition variables")
    else:
        return


def definition_variables():
    global token_pointer
    global last_call_node 
    global ext

    ext+=1;

    curr_node = "def_vars";
    build_graph(curr_node , last_call_node);

    last_call_node = "def_vars";
    definition_variable()
    if tokens_list[token_pointer][0] == ";":
        token_pointer+=1;
        last_call_node = "def_vars";
        definition_variables();
    else :
        last_call_node = "def_vars";
        definition_variable()




def groupe_variable():

    global token_pointer
    global last_call_node 
    global ext

    ext+=1;
    curr_node = "groupe_var" + str(ext);
    build_graph(curr_node , last_call_node);


    if tokens_list[token_pointer][1] == "identifier" or tokens_list[token_pointer][1] == "nom prog" :
        token_pointer += 1
        if tokens_list[token_pointer][0] == ",":
            token_pointer += 1
            last_call_node = curr_node;
            groupe_variable()
        else:
            return
    else:
        print("Invalid variable identifier")


def tableau():
    global token_pointer
    global last_call_node 
    global ext

    ext+=1;

    curr_node = "tableau" + str(ext);
    build_graph(curr_node , last_call_node);

    if tokens_list[token_pointer][0] == "array":
        token_pointer+=1

        if tokens_list[token_pointer][0] == "[" and tokens_list[token_pointer + 1][1] == "integer" and tokens_list[token_pointer +2 ][0] == ".." and tokens_list[token_pointer + 3][1] == "integer" and  tokens_list[token_pointer + 4][0] == "]" and tokens_list[token_pointer + 5][0] =="of":
            token_pointer+=6
            if tokens_list[token_pointer][0] == "integer" or tokens_list[token_pointer][0] == "real" or tokens_list[token_pointer][0] == "char" or tokens_list[token_pointer][0] == "string" :
                token_pointer+=1
            elif tokens_list[token_pointer][0] == "array" :
                last_call_node = curr_node;
                tableau()

            else:
                print("invalid array type !")

        else :
            print("Invalid array declaration !")
            exit(7)



    else:
        print("type inxist !")



def vide():
    pass


#*************************************************************************************************************
#*****************************************PARTIE INSTRUCTION********************************************************************

def instr_comp():
    global token_pointer
    global last_call_node 
    global ext


    ext+=1;
    curr_node = "instr_comp" + str(ext);
    build_graph(curr_node , last_call_node);

    if tokens_list[token_pointer][0] == "begin":
        token_pointer += 1
        last_call_node = curr_node;
        instructions()
        print(tokens_list[token_pointer][0])

        if tokens_list[token_pointer][0] == "end":
            token_pointer += 1
        else:
            print("Missing 'end' in instruction compound")
    else:
        print("Invalid instruction comp")



def instructions():
    global token_pointer
    global last_call_node 
    global ext

    ext+=1 ;

    curr_node = "instructions" + str(ext);

    build_graph(curr_node , last_call_node);


    last_call_node = curr_node;
    instruction()
    if tokens_list[token_pointer][0] == ";":
        token_pointer += 1
        last_call_node = curr_node;
        instructions()
    else:
        return


def instruction():
    global token_pointer
    global last_call_node 
    global ext

    ext+=1;

    curr_node = "instruction" + str(ext);
    build_graph(curr_node , last_call_node);

    if tokens_list[token_pointer][1] == "identifier" or tokens_list[token_pointer][1] == "nom prog":
        last_call_node = curr_node;
        instruction_affectation()
    elif tokens_list[token_pointer][0] == "if":
        token_pointer += 1
        last_call_node = curr_node;
        instruction_if()
    elif tokens_list[token_pointer][0] == "while":
        token_pointer += 1
        last_call_node = curr_node;
        instruction_while()
    else:
        last_call_node = curr_node;
        vide()


def instruction_affectation():
    global token_pointer
    global last_call_node 
    global ext

    ext+=1;
    curr_node = "instruction_affectation" + str(ext);

    build_graph(curr_node , last_call_node);

    if tokens_list[token_pointer][1] == "identifier" or tokens_list[token_pointer][1] == "nom prog":
        token_pointer += 1
        if tokens_list[token_pointer][0] == ":=":
            token_pointer += 1
            last_call_node = curr_node;
            expression()
        else:
            print("Missing ':=' in assignment instruction")
    else:
        print("Invalid identifier in assignment instruction")


def expression():
    global token_pointer
    global last_call_node 
    global ext;

    ext+=1;

    curr_node = "expression"  + str(ext);
    build_graph(curr_node , last_call_node);

    if tokens_list[token_pointer][0] == '(':
        token_pointer += 1
        last_call_node = curr_node;
        expression()
        if tokens_list[token_pointer][0] == ')':
            token_pointer += 1
            last_call_node = curr_node;
            expression_prime()
    elif tokens_list[token_pointer][1] == "identifier" or tokens_list[token_pointer][1] =="nom prog":
            token_pointer += 1
            last_call_node = curr_node;
            expression_prime()
    elif tokens_list[token_pointer][1] == "integer" or tokens_list[token_pointer][1] == "real" or tokens_list[token_pointer][1] == "string"  :
            token_pointer += 1
            last_call_node = curr_node;
            expression_prime()




def expression_prime():
    global token_pointer
    global last_call_node 
    global ext
    
    ext+=1;
    curr_node = "expression_prime" + str(ext);
    build_graph(curr_node , last_call_node);
    # Implement the code for the <Term> non-terminal
    if tokens_list[token_pointer][0] in ['+', '*' , '-']:
        token_pointer += 1

        last_call_node = curr_node;
        expression()

        last_call_node = curr_node;
        expression_prime()
    else:
        last_call_node = curr_node;
        vide()





def instruction_if():
    global token_pointer
    global last_call_node 
    global ext

    ext+=1;

    curr_node = "instruction_if" + str(ext);
    build_graph(curr_node , last_call_node);
    
    last_call_node = curr_node;
    condition()

    if tokens_list[token_pointer][0] == "then":
        token_pointer += 1
        last_call_node = curr_node;
        instruction()
    else:
        print("Missing 'then' in if statement")


def condition():
    global token_pointer
    global last_call_node 
    global ext

    ext+=1
    curr_node = "condition" + str(ext);
    build_graph(curr_node , last_call_node);
    
    last_call_node = curr_node;
    expression()
    if tokens_list[token_pointer][0]+tokens_list[token_pointer + 1][0]  in ['>=', '<=', '<>']:
        token_pointer += 2
        last_call_node = curr_node;
        expression()
    elif tokens_list[token_pointer][0] in ['<', '>']:
        token_pointer += 1
        last_call_node = curr_node;
        expression()
    elif tokens_list[token_pointer][0] == "(":
        token_pointer += 1
        last_call_node = curr_node;
        condition()
        if tokens_list[token_pointer][0] == ")":
            token_pointer += 1
            return


def instruction_while():
    global token_pointer
    global last_call_node 
    global ext;

    ext+=1;
    curr_node = "instruction_while"+ str(ext);
    build_graph(curr_node , last_call_node);

    last_call_node = curr_node;
    condition()

    if tokens_list[token_pointer][0] == "do":
        token_pointer += 1 ;
        last_call_node = curr_node;
        instruction()
    else:
        print("Missing 'do' in while loop")



progSI2024()
try:
    pos = net.nx_agraph.graphviz_layout(g, prog="dot")
    net.draw(g, pos, with_labels=True, font_weight='bold', arrowsize = 10, connectionstyle="arc3,rad=0.1" , font_size = 4 , node_size = 60);
except Exception as e : 
    print(" <<<< THERE IS NO LIBRARY NAMED Pygraphviz >>> ")
# Draw the graph
plt.figure(figsize=(5000, 5000))
plt.show();


