from automata.base.automaton import Automaton
from automata.fa.dfa import DFA
import numpy as np
import automata.base.exceptions as exceptions
import re

letters = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]

digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

punct = [",", "(", ")", ";", "[", "]"]
#  , :=

arithmetic_operators = ['+', "*", "-"]

logic_operators = ["<", ">", "="]


state_names = {f"q{i}" for i in range(82)}


# middle of the identifiers

keys_states = {
    "q27",
    "q11",
    "q30",
    "q20",
    "q34",
    "q40",
    "q45",
    "q48",
    "q53",
    "q55",
    "q14",
    "q59",
    "q64",
    "q66",
    "q70",
    "q81",
}

# all are final states

identifier_state = {"q2"};

logic_operators_states = {"q71", "q72", "q73", "q74", "q75", "q77"};
# all are final states
# q77 is defined as assignment
arithmetic_operators_states = {"q6"};

string_states = {"q4", "q3"};
string_final = {"q4"};
# final state is q4

integer_state = {"q65"};

real_state = {"q66", "q67"};
real_final = {"q67"};
# final state is q67

punc_states = {"q78","q5","q79","q76"};
punc_final = {"q5","q79","q78" , "q76"}

nom_prog = {"q1"};

ident_states = state_names.difference(
    keys_states,
    logic_operators_states,
    arithmetic_operators_states,
    string_states,
    integer_state,
    punc_states,
    real_state,
    nom_prog,
    identifier_state,
)


def generate_states(state, transition_symbol=letters + digits, except_char=None):
    """
    state : 'q0' , ...
    transition symbol : letters or symbols
    """
    result = {}
    if type(state) == list and len(state) > 1:
        couples = list(zip(state, transition_symbol))
        for state, symbol in couples:
            result[symbol] = state
    else:
        if except_char is not None:
            for char in except_char:
                if char in transition_symbol:
                    transition_symbol.remove(char)

        for symbol in transition_symbol:
            result[symbol] = state
    # print(f'{result} of state {state} , trans symbols {transition_symbol}')
    return result


def read_dfa(words):
    dfa = DFA(
        states=state_names,
        input_symbols={
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            " ",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
            ",",
            "(",
            ")",
            ";",
            "[",
            "]",
            ".",
            "<",
            ">",
            "=",
            ":",
            "+",
            "*",
            "-",
            "_",
            "'",
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
        },
        transitions={
            "q0": {
                **generate_states("q1", letters),
                **generate_states("q3", "'"),
                **generate_states("q5", punct),
                **generate_states("q65", digits),
                **generate_states("q6", arithmetic_operators),
                **generate_states("q71", "="),
                **generate_states("q72", "<"),
                **generate_states("q74", ">"),
                **generate_states("q76", ":"),
                **generate_states(
                    [
                        "q7",
                        "q13",
                        "q21",
                        "q28",
                        "q31",
                        "q35",
                        "q41",
                        "q46",
                        "q49",
                        "q54",
                        "q56",
                        "q60",
                        "q80",
                        "q78"
                    ],
                    ["c", "i", "p", "v", "r", "s", "b", "e", "a", "o", "t", "w", "d","."],
                ),
            },

            "q80":{
                **generate_states("q81", "o")
            },

            "q81":{
              #'do' final state
            },

            "q78": {
                **generate_states("q79", "."),
            },

            "q79": {
            },
            "q1": {
                **generate_states("q1", letters ),
                **generate_states("q2", digits + ['_']),
                # '0': 'q2', '1': 'q2', '2': 'q2', '3': 'q2', '4': 'q2', '5': 'q2', '6': 'q2', '7': 'q2', '8': 'q2', '9': 'q2', '+': 'q2' ,
            },
            "q2": {
                **generate_states("q2", letters),
                **generate_states("q2", digits + ["_"]),
                # '0': 'q2', '1': 'q2', '2': 'q2', '3': 'q2', '4': 'q2', '5': 'q2', '6': 'q2', '7': 'q2', '8': 'q2', '9': 'q2', '_': 'q2',
            },
            "q3": {
                **generate_states("q3", letters),
                **generate_states("q3", digits),
                **generate_states("q3", [" "]),
                **generate_states("q4", "'"),
            },
            "q4": {
                # 'string' final state
            },
            "q5": {},
            "q6": {},
            "q7": {
                **generate_states(["q8", "q68"], ["o", "h"]),
                **generate_states("q1", letters + digits + ['_'] , except_char=["o", "h"]),
            },
            "q68": {
                **generate_states("q69", "a"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["a"]),
            },
            "q69": {
                **generate_states("q70", "r"),
                **generate_states("q1", letters + digits + ['_'],except_char=["r"]),
            },
            "q70": {
                # 'char' final state
            },
            "q71": {
                # '=' final state
            },
            "q72": {
                # < final state
                **generate_states("q73", [">", "="]),
            },
            "q73": {
                # <> or <= final state
            },
            "q74": {
                # > final state
                **generate_states("q75", "="),
            },
            "q75": {
                # >= final state
            },
            "q76": {
                **generate_states("q77", "="),
            },
            "q77": {
                # := final state
            },
            "q8": {
                **generate_states("q9", "n"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["n"]),
            },
            "q9": {
                **generate_states("q10", "s"),
                **generate_states("q1",letters + digits + ['_'] ,  except_char=["s"]),
            },
            "q10": {
                **generate_states("q11", "t"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["t"]),
            },
            "q11": {},
            "q12": {},
            "q13": {
                **generate_states("q14", "f"),
                **generate_states("q15", "n"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["f", "n"]),
            },
            "q14": {},
            "q15": {
                **generate_states("q16", "t"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["t"]),
            },
            "q16": {
                **generate_states("q17", "e"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["e"]),
            },
            "q17": {
                **generate_states("q18", "g"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["g"]),
            },
            "q18": {
                **generate_states("q19", "e"),
                **generate_states("q1",letters + digits + ['_'] ,  except_char=["e"]),
            },
            "q19": {
                **generate_states("q20", "r"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["r"]),
            },
            "q20": {},
            "q21": {
                **generate_states("q22", "r"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["r"]),
            },
            "q22": {
                **generate_states("q23", "o"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["o"]),
            },
            "q23": {
                **generate_states("q24", "g"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["g"]),
            },
            "q24": {
                **generate_states("q25", "r"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["r"]),
            },
            "q25": {
                **generate_states("q26", "a"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["a"]),
            },
            "q26": {
                **generate_states("q27", "m"),
                **generate_states("q1",letters + digits + ['_'] ,  except_char=["m"]),
            },
            "q27": {},
            "q28": {
                **generate_states("q29", "a"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["a"]),
            },
            "q29": {
                **generate_states("q30", "r"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["r"]),
            },
            "q30": {},
            "q31": {
                **generate_states("q32", "e"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["e"]),
            },
            "q32": {
                **generate_states("q33", "a"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["a"]),
            },
            "q33": {
                **generate_states("q34", "l"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["l"]),
            },
            "q34": {},
            "q35": {
                **generate_states("q36", "t"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["t"]),
            },
            "q36": {
                **generate_states("q37", "r"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["r"]),
            },
            "q37": {
                **generate_states("q38", "i"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["i"]),
            },
            "q38": {
                **generate_states("q39", "n"),
                **generate_states("q1",letters + digits + ['_'] ,  except_char=["n"]),
            },
            "q39": {
                **generate_states("q40", "g"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["g"]),
            },
            "q40": {},
            "q41": {
                **generate_states("q42", "e"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["e"]),
            },
            "q42": {
                **generate_states("q43", "g"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["g"]),
            },
            "q43": {
                **generate_states("q44", "i"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["i"]),
            },
            "q44": {
                **generate_states("q45", "n"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["n"]),
            },
            "q45": {},
            "q46": {
                **generate_states("q47", "n"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["n"]),
            },
            "q47": {
                **generate_states("q48", "d"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["d"]),
            },
            "q48": {},
            "q49": {
                **generate_states("q50", "r"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["r"]),
            },
            "q50": {
                **generate_states("q51", "r"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["r"]),
            },
            "q51": {
                **generate_states("q52", "a"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["a"]),
            },
            "q52": {
                **generate_states("q53", "y"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["y"]),
            },
            "q53": {},
            "q54": {
                **generate_states("q55", "f"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["f"]),
            },
            "q55": {},
            "q56": {
                **generate_states("q57", "h"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["h"]),
            },
            "q57": {
                **generate_states("q58", "e"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["e"]),
            },
            "q58": {
                **generate_states("q59", "n"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["n"]),
            },
            "q59": {},
            "q60": {
                **generate_states("q61", "h"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["h"]),
            },
            "q61": {
                **generate_states("q62", "i"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["i"]),
            },
            "q62": {
                **generate_states("q63", "l"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["l"]),
            },
            "q63": {
                **generate_states("q64", "e"),
                **generate_states("q1", letters + digits + ['_'] , except_char=["e"]),
            },
            "q64": {},
            "q65": {**generate_states("q65", digits), **generate_states("q66", ".")},
            "q66": {**generate_states("q67", digits)},
            "q67": {**generate_states("q67", digits)},
        },
        initial_state="q0",
        # add con , beg as final
        final_states={
            "q1",
            "q2",
            "q6",
            "q65",
            "q67",
            "q4",
            "q5",
            "q27",
            "q30",
            "q20",
            "q34",
            "q10",
            "q11",
            "q40",
            "q45",
            "q48",
            "q53",
            "q55",
            "q14",
            "q59",
            "q64",
            "q4",
            "q67",
            "q71",
            "q72",
            "q73",
            "q74",
            "q75",
            "q77",
            "q70",
            "q78",
            "q76",
            "q79",
            "q81",
        }.union(ident_states),
        allow_partial=True,
    )

    token_dict = []
    for w in words:
        try:
            end_state = dfa.read_input(w)
            if end_state in keys_states:
                token_dict.append([w, "key word"])
            elif end_state in punc_final :
                token_dict.append([w, "punctuation"])
            elif end_state == "q77":
                token_dict.append([w, "assignment"])
            elif end_state in logic_operators_states:
                token_dict.append([w, "logic operator"])
            elif end_state in arithmetic_operators_states:
                token_dict.append([w, "arithmetic operator"])
            elif end_state in ["q65"]:
                token_dict.append([w, "integer"])
            elif end_state == "q2" or end_state in ident_states:
                token_dict.append([w, "identifier"])
            elif end_state == "q1":
                token_dict.append([w, "nom prog"])
            elif end_state in real_final:
                token_dict.append([w, "real"])
            elif end_state in string_final:
                token_dict.append([w, "string"])

        except exceptions.RejectionException as e:
            stopping_state = re.findall(string=e.__str__(), pattern='\(\w+\)')[0][1:-1];

            # print(f'{stopping_state}, {len(w)}')
            print(f'{stopping_state} from {w}')
            if stopping_state == 'None':
                raise Exception("Lexical Error : illegal character ! \n");
            elif stopping_state in string_states.difference(string_final):
                print("String problem");
                raise Exception("Lexical Error : incorrect string declaration ! \n")
            elif stopping_state in real_state.difference(real_final):
                raise Exception("Lexical Error : incorrect real declaration ! \n")
            elif stopping_state in punc_states.difference(punc_final):
                raise Exception("Lexical Error : incorrect punctuation ! \n");

        except Exception as e:
            print(e)

    return token_dict


# tokens = read_dfa(
#     [
#         "program",
#         "name",
#         "..",
#         "const",
#         "a_dfd_50",
#         "=",
#         "50",
#         ";",
#         "var",
#         "a",
#         ",",
#         "c",
#         ":",
#         "integer",
#     ]
# )
# print(tokens)


token_pointer = 0


# def progSI2024():
#     global token_pointer

#     try:
#         assert tokens[token_pointer][0] == "program"
#         token_pointer += 1

#         assert tokens[token_pointer][1] == "identifier"
#         token_pointer += 1

#         assert tokens[token_pointer][0] == ";"
#         token_pointer += 1

#         corps()
#         # assert tokens[token_pointer][0] == ".";

#     except Exception:
#         print("Program declaration Error !! ")


# # progSI2024();
# def corps():
#     partie_definition_constante()
#     # partie_definition_variable();
#     # instr_comp()


# def partie_definition_constante():
#     try:
#         if tokens[token_pointer][0] == "const":
#             token_pointer += 1

#             definition_constante()

#             assert tokens[token_pointer][0] == ";"

#     except:
#         print("partie definition constante error !! ")

#     # else:
#     #     return ;


# def definition_constante():
#     try:
#         assert tokens[token_pointer][1] == "identifier"
#         token_pointer += 1
#         assert tokens[token_pointer][0] == "="
#         token_pointer += 1
#         if (
#             tokens[token_pointer][1] == "integer"
#             or tokens[token_pointer][1] == "real"
#             or tokens[token_pointer][1] == "string"
#         ):
#             token_pointer += 1
#         if tokens[token_pointer][0] == ";":
#             token_pointer += 1
#             definition_constante()

#     except Exception as e:
#         print("definition constant Error !! ")

# # progSI2024()


# # differntiate const and char  , >= , .. ,