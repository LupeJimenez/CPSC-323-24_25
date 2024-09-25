# Assignment 1 - Compilers CPSC 323
# Team Members: Lupita Jimenez, Lucero Matamoros, and Elena Marquez
# Date: 09/24/2024
# Description: This program is a lexical analyzer for the language RAT24F. 
# The lexer will read through the RAT24F source code file,
# identify the tokens, and output the tokens to a file USING FSM. 

import re  # Regular expression library

# TOKENS TYPES 
class TokenType:
    # Keywords
    KEYWORD = "KEYWORD"
    # Identifiers
    IDENTIFIER = "IDENTIFIER"
    # Operators 
    OPERATOR = "OPERATOR"
    # Integer
    INTEGER = "INTEGER"
    # Real 
    REAL = "REAL"
    # Separator
    SEPARATOR = "SEPARATOR"
    # Invalid
    INVALID = "INVALID"

class Token:  # Token class   
    def __init__(self, token_type, lexeme):  # Constructor
        self.token_type = token_type  # Token type
        self.lexeme = lexeme  # Lexeme
        
    def __str__(self):  # String representation of the token
        return f"{self.token_type} : {self.lexeme}"  # Return token type and lexeme
    
# Defining the keywords
keywords = ["Function", "Integer", "Boolean", "Real", "If", "Else", "Fi", "Return", "Put", "Get", "While", "True", "False"]

# FSM States
class State:
    START = "START"
    IDENTIFIER = "IDENTIFIER"
    INTEGER = "INTEGER"
    REAL = "REAL"
    OPERATOR = "OPERATOR"
    SEPARATOR = "SEPARATOR"
    COMMENT = "COMMENT"
    INVALID = "INVALID"

def is_separator(char):
    return char in ('(', ')', ';', ':', ',', '{', '}', '$')

def is_operator_char(char):
    return char in ('+', '-', '*', '/', '<', '>', '=', '!')

def is_keyword(lexeme):
    return lexeme in keywords

def contains_invalid_characters(lexeme):
    return '_' in lexeme or '"' in lexeme

def lexer(line):
    tokens = []
    current_lexeme = ''
    current_state = State.START

    for i in range(len(line)):
        ch = line[i]

        if current_state == State.START:
            if ch.isspace():
                continue
            elif is_separator(ch):
                tokens.append(Token(TokenType.SEPARATOR, ch))
            elif is_operator_char(ch):
                current_lexeme += ch
                current_state = State.OPERATOR
            elif ch.isalpha():
                current_lexeme += ch
                current_state = State.IDENTIFIER
            elif ch.isdigit():
                current_lexeme += ch
                current_state = State.INTEGER
            elif ch == '[' and i + 1 < len(line) and line[i + 1] == '*':
                current_state = State.COMMENT
            else:
                current_state = State.INVALID

        elif current_state == State.IDENTIFIER:
            if ch.isalnum() or ch == '_':
                current_lexeme += ch
            else:
                # Check if it's a keyword or a valid identifier
                if is_keyword(current_lexeme):
                    tokens.append(Token(TokenType.KEYWORD, current_lexeme))
                else:
                    tokens.append(Token(TokenType.IDENTIFIER, current_lexeme))
                current_lexeme = ''
                current_state = State.START
                i -= 1  # Re-evaluate this character

        elif current_state == State.INTEGER:
            if ch.isdigit():
                current_lexeme += ch
            elif ch == '.':
                current_lexeme += ch
                current_state = State.REAL
            else:
                tokens.append(Token(TokenType.INTEGER, current_lexeme))
                current_lexeme = ''
                current_state = State.START
                i -= 1  # Re-evaluate this character

        elif current_state == State.REAL:
            if ch.isdigit():
                current_lexeme += ch
            else:
                tokens.append(Token(TokenType.REAL, current_lexeme))
                current_lexeme = ''
                current_state = State.START
                i -= 1  # Re-evaluate this character

        elif current_state == State.OPERATOR:
            if ch == '=':
                current_lexeme += ch
                tokens.append(Token(TokenType.OPERATOR, current_lexeme))
                current_lexeme = ''
                current_state = State.START
            else:
                tokens.append(Token(TokenType.OPERATOR, current_lexeme))
                current_lexeme = ''
                current_state = State.START
                i -= 1  # Re-evaluate this character

        elif current_state == State.COMMENT:
            if ch == '*' and i + 1 < len(line) and line[i + 1] == ']':
                current_state = State.START  # End of comment
            continue  # Ignore characters in comments

        elif current_state == State.INVALID:
            current_lexeme += ch
            tokens.append(Token(TokenType.INVALID, current_lexeme))
            current_lexeme = ''
            current_state = State.START

    # Final state handling
    if current_lexeme:
        tokens.append(Token(TokenType.INVALID, current_lexeme))

    return tokens

def main():
    input_filename = input("Enter the input file name: ")
    output_filename = input_filename.rsplit('.', 1)[0] + '_output.txt'

    try:
        with open(input_filename, 'r') as file, open(output_filename, 'w') as output_file:
            for line in file:
                tokens = lexer(line)
                for token in tokens:
                    output_file.write(f"Token: {token.token_type}, Lexeme: {token.lexeme}\n")
        print(f"Output file '{output_filename}' created successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
