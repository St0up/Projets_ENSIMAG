#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TP TL1: implémentation des automates
"""

import sys

###############
# Cadre général

V = set(('.', 'e', 'E', '+', '-')
        + tuple(str(i) for i in range(10)))

class Error(Exception):
    pass

INPUT_STREAM = sys.stdin
END = '\n' # WARNING: test_tp modifies the value of END.

# Initialisation: on vérifie que END n'est pas dans V
def init_char():
    if END in V:
        raise Error('character ' + repr(END) + ' in V')

# Accès au caractère suivant dans l'entrée
def next_char():
    global INPUT_STREAM
    ch = INPUT_STREAM.read(1)
    # print("@", repr(ch))  # decommenting this line may help debugging
    if ch in V or ch == END:
        return ch
    raise Error('character ' + repr(ch) + ' unsupported')


############
# Question 1 : fonctions nonzerodigit et digit

def nonzerodigit(char):
    assert(len(char) <= 1)
    return '1' <= char <= '9'

def digit(char):
    assert(len(char) <= 1)
    return '0' <= char <= '9'


############
# Question 2 : integer et pointfloat sans valeur

def integer_Q2():
    init_char()
    return integer_Q2_state_0()


def integer_Q2_state_0():
    ch = next_char()
    rep = nonzerodigit(ch)
    if rep == END:
        return False
    if not(nonzerodigit(ch)):
        if not(digit(ch)):
            return False
        return integer_Q2_state_1()
    return integer_Q2_state_2()


def integer_Q2_state_1():
    ch = next_char()
    rep1 = nonzerodigit(ch)
    rep2 = digit(ch)
    if rep1 == True :
        return False
    elif ch == END:
        return True
    elif rep2:
        return integer_Q2_state_1()
    else:
        return False

def integer_Q2_state_2():
    ch = next_char()
    rep = digit(ch)
    if ch == END:
        return True
    elif rep:
        return integer_Q2_state_2()
    else:
        return False

#pointfloat_Q2

def pointfloat_Q2():
    init_char()
    return pointfloat_Q2_state_0()

def pointfloat_Q2_state_0():
    ch = next_char()
    rep = digit(ch)
    if ch == ".":
        return pointfloat_Q2_state_1()
    elif rep == True:
        return pointfloat_Q2_state_2()
    else:
        return False

def pointfloat_Q2_state_1():
    ch = next_char()
    rep = digit(ch)
    if rep == True:
        return pointfloat_Q2_state_3()
    else:
        return False

def pointfloat_Q2_state_2():
    ch = next_char()
    rep = digit(ch)
    if ch == ".":
        return pointfloat_Q2_state_3()
    elif rep == True:
        return pointfloat_Q2_state_2()
    else:
        return False


def pointfloat_Q2_state_3():
    ch = next_char()
    rep = digit(ch)
    if rep == True:
        return pointfloat_Q2_state_3()
    elif ch == END:
        return True
    else:
        return False

############
# Question 5 : integer avec calcul de la valeur
# si mot accepté, renvoyer (True, valeur)
# si mot refusé, renvoyer (False, None)

# Variables globales pour se transmettre les valeurs entre états
int_value = 0
exp_value = 0

def integer():
    global int_value
    int_value = 0
    init_char()
    return integer_state_0()


def integer_state_0():
    global int_value
    ch = next_char()
    rep = nonzerodigit(ch)
    if rep == END:
        return False, None
    if not(nonzerodigit(ch)):
        if not(digit(ch)):
            return False, None
        int_value = int_value*10+int(ch)
        return integer_state_1()
    int_value = int_value*10+int(ch)
    return integer_state_2()


def integer_state_1():
    global int_value
    ch = next_char()
    rep1 = nonzerodigit(ch)
    rep2 = digit(ch)
    if rep1 == True :
        return False, None
    elif ch == END:
        return True, int_value
    elif rep2:
        int_value = int_value*10+int(ch)
        return integer_state_1()
    else:
        return False, None


def integer_state_2():
    global int_value
    ch = next_char()
    rep = digit(ch)
    if ch == END:
        return True, int_value
    elif rep:
        int_value = int_value*10+int(ch)
        return integer_state_2()
    else:
        return False, None

############
# Question 7 : pointfloat avec calcul de la valeur

def pointfloat():
    global int_value
    global exp_value
    init_char()
    int_value = 0.
    exp_value = 0
    return pointfloat_state_0()

def pointfloat_state_0():
    global int_value
    global exp_value
    ch = next_char()
    rep = digit(ch)
    if ch == ".":
        exp_value = 0
        return pointfloat_state_1()
    elif rep == True:
        int_value = int_value*10+int(ch)
        return pointfloat_state_2()
    else:
        return False, None

def pointfloat_state_1():
    global int_value
    global exp_value
    ch = next_char()
    rep = digit(ch)
    if rep == True:
        exp_value += 1
        int_value = int_value*10+int(ch)
        return pointfloat_state_3()
    else:
        return False, None

def pointfloat_state_2():
    global int_value
    ch = next_char()
    rep = digit(ch)
    if ch == ".":
        return pointfloat_state_3()
    elif rep == True:
        int_value = int_value*10+int(ch)
        return pointfloat_state_2()
    else:
        return False, None


def pointfloat_state_3():
    global int_value
    global exp_value
    ch = next_char()
    rep = digit(ch)
    if rep == True:
        int_value = int_value*10+int(ch)
        exp_value += 1
        return pointfloat_state_3()
    elif ch == END:
        print(int_value, exp_value)
        return True, int_value*10**(-exp_value)
    else:
        return False, None


############
# Question 8 : exponent, exponentfloat et number

#exponent

int_value = 0
signe = 1

def exponent():
    global int_value
    global signe
    signe = 1
    int_value = 0
    init_char()
    return exponent_0()

def exponent_0():
    ch = next_char()
    if ch != 'e' and ch != 'E':
        return False, None
    else:
        return exponent_1()

def exponent_1():
    global int_value
    global signe
    ch = next_char()
    rep = digit(ch)
    if rep:
        int_value = int_value*10 + int(ch)
        return exponent_3()
    elif ch == '-':
        signe = -1
        return exponent_2()
    elif ch == '+':
        return exponent_2()
    else:
        return False, None

def exponent_2():
    global int_value
    ch = next_char()
    rep = digit(ch)
    if rep:
        int_value = int_value*10 + int(ch)
        return exponent_3()
    else:
        return False, None

def exponent_3():
    global int_value
    global signe
    ch = next_char()
    rep = digit(ch)
    if ch == END:
        return True, signe*int_value
    elif rep:
        int_value = int_value*10 + int(ch)
        return exponent_3()
    else:
        return False, None


# La valeur du signe de l'exposant : 1 si +, -1 si -
sign_value = 1
puis_val = 0
exp_value = 0

def exponentfloat():
    global int_value
    global sign_value
    global exp_value
    global puis_value
    puis_value = 0
    int_value = 0
    exp_value = 0
    sign_value = 1
    init_char()
    return exponentfloat_0()

def exponentfloat_0():
    global int_value
    ch = next_char()
    rep = nonzerodigit(ch)
    if ch == '0':
        return exponentfloat_1()
    elif rep:
        int_value = int_value*10 + int(ch)
        return exponentfloat_2()
    elif ch == '.':
        return exponentfloat_3()
    else:
        return False, None

def exponentfloat_1():
    global int_value
    ch = next_char()
    rep = nonzerodigit(ch)
    if ch == '0':
        return exponentfloat_1()
    elif rep:
        int_value = int_value*10 + int(ch)
        return exponentfloat_4()
    elif ch == '.':
        return exponentfloat_5()
    elif ch == 'e' or ch == 'E':
        return exponentfloat_6()
    else:
        return False, None

def exponentfloat_2():
    global int_value
    ch = next_char()
    rep = digit(ch)
    if rep:
        int_value = int_value*10 + int(ch)
        return exponentfloat_2()
    elif ch == '.':
        return exponentfloat_5()
    elif ch == 'e' or ch == 'E':
        return exponentfloat_6()
    else:
        return False, None

def exponentfloat_3():
    global int_value
    global exp_value
    exp_value += 1
    ch = next_char()
    rep = digit(ch)
    if rep:
        int_value = int_value*10 + int(ch)
        return exponentfloat_5()
    else:
        return False, None

def exponentfloat_4():
    global int_value
    ch = next_char()
    rep = digit(ch)
    if rep:
        int_value = int_value*10 + int(ch)
        return exponentfloat_4()
    elif ch == '.':
        return exponentfloat_5()
    else:
        return False, None

def exponentfloat_5():
    global int_value
    global exp_value
    ch = next_char()
    rep = digit(ch)
    if rep:
        exp_value += 1
        int_value = int_value*10 + int(ch)
        return exponentfloat_5()
    elif ch == 'e' or ch == 'E':
        return exponentfloat_6()
    else:
        return False, None

def exponentfloat_6():
    global puis_value
    global sign_value
    ch = next_char()
    rep = digit(ch)
    if rep:
        puis_value = puis_value*10 + int(ch)
        return exponentfloat_8()
    elif ch == '-':
        sign_value = -1
        return exponentfloat_7()
    elif ch == '+':
        sign_value = 1
        return exponentfloat_7()
    else:
        return False, None

def exponentfloat_7():
    global puis_value
    ch = next_char()
    rep = digit(ch)
    if rep:
        puis_value = int(ch)
        return exponentfloat_8()
    else:
        return False, None

def exponentfloat_8():
    global int_value
    global puis_value
    global exp_value
    global sign_value
    ch = next_char()
    rep = digit(ch)
    if rep:
        puis_value = puis_value*10 + int(ch)
        return exponentfloat_8()
    elif ch == END:
        return True, int_value*(10**-exp_value)*(10**(sign_value*puis_value))
    else:
        return False, None

#################
# Automate Number

def number():
    global int_value
    global sign_value
    global exp_value
    global puis_value
    puis_value = 0
    int_value = 0
    exp_value = 0
    sign_value = 1
    init_char()
    return number_0()

def number_0():
    global int_value
    ch = next_char()
    rep = nonzerodigit(ch)
    if ch == '0':
        return number_1()
    elif rep:
        int_value = int(ch)
        return number_2()
    elif ch == '.':
        return number_3()
    else:
        return False, None

def number_1():
    global int_value
    ch = next_char()
    rep = nonzerodigit(ch)
    if ch == '0':
        return number_1()
    elif rep:
        int_value = int(ch)
        return number_5()
    elif ch == '.':
        return number_4()
    elif ch == 'e' or ch == 'E':
        return number_6()
    elif ch == END or ch == ' ':
        return True, 0
    else:
        return False, None

def number_2():
    global int_value
    ch = next_char()
    rep = digit(ch)
    if rep:
        int_value = int_value*10 + int(ch)
        return number_2()
    elif ch == '.':
        return number_4()
    elif ch == 'e' or ch == 'E':
        return number_6()
    elif ch == END or ch == ' ':
        return True, int_value
    else:
        return False, None

def number_3():
    global int_value
    global exp_value
    exp_value += 1
    ch = next_char()
    rep = digit(ch)
    if rep:
        int_value = int_value*10 + int(ch)
        return number_4()
    else:
        return False, None

def number_4():
    global int_value
    global exp_value
    ch = next_char()
    rep = digit(ch)
    if rep:
        exp_value += 1
        int_value = int_value*10 + int(ch)
        return number_4()
    elif ch == 'e' or ch == 'E':
        return number_6()
    elif ch == END or ch == ' ':
        return True, int_value*(10**-exp_value)
    else:
        return False, None

def number_5():
    global int_value
    ch = next_char()
    rep = digit(ch)
    if rep:
        int_value = int_value*10 + int(ch)
        return number_5()
    elif ch == '.':
        return number_4()
    elif ch == 'E' or ch == 'e':
        return number_6()
    else:
        return False, None


def number_6():
    global puis_value
    global sign_value
    ch = next_char()
    rep = digit(ch)
    if rep:
        puis_value = int(ch)
        return number_8()
    elif ch == '-':
        sign_value = -1
        return number_7()
    elif ch == '+':
        return number_7()
    else:
        return False, None

def number_7():
    global puis_value
    ch = next_char()
    rep = digit(ch)
    if rep:
        puis_value = int(ch)
        return number_8()
    else:
        return False, None

def number_8():
    print('ici')
    global puis_value
    ch = next_char()
    rep = digit(ch)
    if rep:
        puis_value = puis_value*10 + int(ch)
        return number_8()
    elif ch == END or ch == ' ':
        return True, int_value*(10**-exp_value)*(10**(sign_value*puis_value))
    else:
        return False, None

########################
#####    Projet    #####
########################


V = set(('.', 'e', 'E', '+', '-', '*', '/', '(', ')', ' ')
        + tuple(str(i) for i in range(10)))


############
# Question 10 : eval_exp

def eval_exp():
    ch = next_char()
    if ch == '+':
        next_char()
        n1 = eval_exp()
        n2 = eval_exp()
        return n1 + n2
    elif ch == '*':
        next_char()
        n1 = eval_exp()
        n2 = eval_exp()
        return n1 * n2
    elif ch == '-':
        next_char()
        n1 = eval_exp()
        n2 = eval_exp()
        return n1 - n2
    elif ch == '/':
        next_char()
        n1 = eval_exp()
        n2 = eval_exp()
        return n1 / n2
    else:
        valeur = number()
        print(valeur)
        return valeur[1]


############
# Question 12 : eval_exp corrigé

current_char = ''

# Accès au caractère suivant de l'entrée sans avancer
def peek_char():
    global current_char
    if current_char == '':
        current_char = INPUT_STREAM.read(1)
    ch = current_char
    # print("@", repr(ch))  # decommenting this line may help debugging
    if ch in V or ch in END:
        return ch
    raise Error('character ' + repr(ch) + ' unsupported')

def consume_char():
    global current_char
    current_char = ''

def eval_exp_v2():
    ch = peek_char()
    if ch == '+':
        consume_char()
        n1 = eval_exp_v2()
        n2 = eval_exp_v2()
        return n1 + n2
    elif ch == '*':
        consume_char()
        n1 = eval_exp_v2()
        n2 = eval_exp_v2()
        return n1 * n2
    elif ch == '-':
        consume_char()
        n1 = eval_exp_v2()
        n2 = eval_exp_v2()
        return n1 - n2
    elif ch == '/':
        consume_char()
        n1 = eval_exp_v2()
        n2 = eval_exp_v2()
        return n1 / n2
    elif ch == ' ':
        consume_char()
        return eval_exp_v2()
    else:
        valeur = number_v2()
        print(valeur)
        return valeur[1]

def number_v2():
    global int_value
    global sign_value
    global exp_value
    global puis_value
    puis_value = 0
    int_value = 0
    exp_value = 0
    sign_value = 1
    init_char()
    return number_0_v2()

def number_0_v2():
    global int_value
    ch = peek_char()
    consume_char()
    rep = nonzerodigit(ch)
    if ch == '0':
        return number_1()
    elif rep:
        int_value = int(ch)
        return number_2()
    elif ch == '.':
        return number_3()
    else:
        return False, None


############
# Question 14 : automate pour Lex

operator = set(['+', '-', '*', '/'])

def FA_Lex():
    ch = peek_char()
    if ch == '(' or ch == ')':
        consume_char()
        return ch
    elif ch in ['+', '-', '*', '/']:
        consume_char()
        return ch
    else:
        return number_v2()

############
# Question 15 : automate pour Lex avec token

# Token
NUM, ADD, SOUS, MUL, DIV, OPAR, FPAR = range(7)
token_value = 0


def FA_Lex_w_token():
    ch = peek_char()
    if ch == '+':
        consume_char()
        return 1
    elif ch == '-':
        consume_char()
        return 2
    elif ch == '*':
        consume_char()
        return 3
    elif ch == '/':
        consume_char()
        return 4
    elif ch == '(':
        consume_char()
        return 5
    elif ch == ')':
        consume_char()
        return 6
    else:
        return 0


# Fonction de test
if __name__ == "__main__":
    print("@ Test interactif de l'automate")
    print("@ Vous pouvez changer l'automate testé en modifiant la fonction appelée à la ligne 'ok = ... '.")
    print("@ Tapez une entrée:")
    try:
        # ok = pointfloat_Q2() # changer ici pour tester un autre automate sans valeur
        # ok, val = number() # changer ici pour tester un autre automate avec valeur
        ok, val = True, eval_exp_v2() # changer ici pour tester eval_exp et eval_exp_v2
        if ok:
            # print("Accepted!")
            print("value:", val) # décommenter ici pour afficher la valeur (question 4 et +)
        else:
            # print("Rejected!")
            print("value so far:", int_value) # décommenter ici pour afficher la valeur en cas de rejet
    except Error as e:
        print("Error:", e)
