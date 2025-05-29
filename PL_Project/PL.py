#!/usr/bin/env python3
"""
Multi-Language Lexical Analyzer
ISO 9001:2015 Project Guidelines Implementation

This lexical analyzer supports C, Python, and Java tokenization
with comprehensive error handling and structured output.
"""

import re
import sys
import os
from enum import Enum
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass

class TokenType(Enum):
    """Enumeration of all possible token types"""
    # Language constructs
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    
    # Literals
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    CHAR = "CHAR"
    BOOLEAN = "BOOLEAN"
    
    # Operators
    ARITHMETIC_OP = "ARITHMETIC_OP"
    ASSIGNMENT_OP = "ASSIGNMENT_OP"
    ASSIGNMENT = "ASSIGNMENT"
    RELATIONAL_OP = "RELATIONAL_OP"
    LOGICAL_OP = "LOGICAL_OP"
    BITWISE_OP = "BITWISE_OP"
    UNARY_OP = "UNARY_OP"
    SHIFT_OP = "SHIFT_OP"
    
    # Punctuation
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    LBRACKET = "LBRACKET"
    RBRACKET = "RBRACKET"
    SEMICOLON = "SEMICOLON"
    COMMA = "COMMA"
    DOT = "DOT"
    COLON = "COLON"
    QUESTION = "QUESTION"
    
    # Special
    COMMENT = "COMMENT"
    WHITESPACE = "WHITESPACE"
    NEWLINE = "NEWLINE"
    ERROR = "ERROR"

@dataclass
class Token:
    """Represents a token with its type, value, and position"""
    type: TokenType
    value: str
    line: int
    column: int

class Language(Enum):
    """Supported programming languages"""
    C = 1
    PYTHON = 2
    JAVA = 3

class LexicalAnalyzer:
    """Multi-language lexical analyzer implementation"""
    
    def __init__(self):
        self.language = None
        self.tokens = []
        self.errors = []
        self.line_number = 1
        self.column_number = 1
        self.token_count = 0
        self.error_count = 0
        
        # Define language-specific keywords
        self.keywords = {
            Language.C: {
                'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
                'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if',
                'inline', 'int', 'long', 'register', 'restrict', 'return', 'short',
                'signed', 'sizeof', 'static', 'struct', 'switch', 'typedef', 'union',
                'unsigned', 'void', 'volatile', 'while', '_Bool', '_Complex', '_Imaginary'
            },
            Language.PYTHON: {
                'and', 'as', 'assert', 'break', 'class', 'continue', 'def', 'del',
                'elif', 'else', 'except', 'exec', 'finally', 'for', 'from', 'global',
                'if', 'import', 'in', 'is', 'lambda', 'not', 'or', 'pass', 'print',
                'raise', 'return', 'try', 'while', 'with', 'yield', 'True', 'False', 'None'
            },
            Language.JAVA: {
                'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char',
                'class', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum',
                'extends', 'final', 'finally', 'float', 'for', 'goto', 'if', 'implements',
                'import', 'instanceof', 'int', 'interface', 'long', 'native', 'new',
                'package', 'private', 'protected', 'public', 'return', 'short', 'static',
                'strictfp', 'super', 'switch', 'synchronized', 'this', 'throw', 'throws',
                'transient', 'try', 'void', 'volatile', 'while', 'true', 'false', 'null'
            }
        }
        
        # Define token patterns
        self.patterns = [
            # Comments
            (r'/\*[\s\S]*?\*/', TokenType.COMMENT),  # C/Java block comments
            (r'//.*', TokenType.COMMENT),            # C/Java line comments
            (r'#.*', TokenType.COMMENT),             # Python comments
            
            # String literals
            (r'"([^"\\]|\\.)*"', TokenType.STRING),
            (r"'([^'\\]|\\.)*'", TokenType.STRING),  # Python strings
            
            # Character literals (C/Java)
            (r"'([^'\\]|\\.)'", TokenType.CHAR),
            
            # Numeric literals
            (r'\d+\.\d*([eE][+-]?\d+)?', TokenType.FLOAT),  # Float with optional exponent
            (r'\d+[eE][+-]?\d+', TokenType.FLOAT),          # Scientific notation
            (r'\d+\.\d+', TokenType.FLOAT),                 # Simple float
            (r'\d+', TokenType.INTEGER),                    # Integer
            
            # Multi-character operators
            (r'\+\+|--', TokenType.UNARY_OP),
            (r'==|!=|<=|>=|<|>', TokenType.RELATIONAL_OP),
            (r'&&|\|\||!', TokenType.LOGICAL_OP),
            (r'<<|>>', TokenType.SHIFT_OP),
            (r'\+=|-=|\*=|/=|%=|&=|\|=|\^=|<<=|>>=', TokenType.ASSIGNMENT_OP),
            (r'&|\||\^|~', TokenType.BITWISE_OP),
            (r'\*\*|//', TokenType.ARITHMETIC_OP),  # Python-specific
            (r'\+|-|\*|/|%', TokenType.ARITHMETIC_OP),
            (r'=', TokenType.ASSIGNMENT),
            
            # Single character tokens
            (r'\(', TokenType.LPAREN),
            (r'\)', TokenType.RPAREN),
            (r'\{', TokenType.LBRACE),
            (r'\}', TokenType.RBRACE),
            (r'\[', TokenType.LBRACKET),
            (r'\]', TokenType.RBRACKET),
            (r';', TokenType.SEMICOLON),
            (r',', TokenType.COMMA),
            (r'\.', TokenType.DOT),
            (r':', TokenType.COLON),
            (r'\?', TokenType.QUESTION),
            
            # Identifiers and keywords
            (r'[a-zA-Z_][a-zA-Z0-9_]*', TokenType.IDENTIFIER),
            
            # Whitespace
            (r'[ \t]+', TokenType.WHITESPACE),
            (r'\n', TokenType.NEWLINE),
        ]
        
        # Compile patterns
        self.compiled_patterns = [(re.compile(pattern), token_type) 
                                for pattern, token_type in self.patterns]
    
    def select_language(self) -> bool:
        """Prompt user to select programming language"""
        print("=== MULTI-LANGUAGE LEXICAL ANALYZER ===")
        print("Select programming language:")
        print("1. C")
        print("2. Python")
        print("3. Java")
        
        try:
            choice = int(input("Enter your choice (1-3): "))
            if choice == 1:
                self.language = Language.C
            elif choice == 2:
                self.language = Language.PYTHON
            elif choice == 3:
                self.language = Language.JAVA
            else:
                print("ERROR: Invalid choice. Please select 1, 2, or 3.")
                return False
            return True
        except ValueError:
            print("ERROR: Invalid input. Please enter a number.")
            return False
    
    def get_input_source(self) -> Optional[str]:
        """Get input source from user choice"""
        print("\nInput mode:")
        print("1. Interactive input")
        print("2. File input")
        
        try:
            choice = int(input("Enter your choice (1-2): "))
            
            if choice == 1:
                print("\nEnter your code (press Enter twice to finish):")
                lines = []
                empty_lines = 0
                while True:
                    try:
                        line = input()
                        if line.strip() == "":
                            empty_lines += 1
                            if empty_lines >= 2:
                                break
                        else:
                            empty_lines = 0
                        lines.append(line)
                    except EOFError:
                        break
                return '\n'.join(lines)
                
            elif choice == 2:
                filename = input("Enter filename: ").strip()
                if not filename:
                    print("ERROR: No input file provided.")
                    return None
                
                try:
                    with open(filename, 'r', encoding='utf-8') as file:
                        return file.read()
                except FileNotFoundError:
                    print(f"ERROR: Could not open {filename}. Please make sure the file exists.")
                    return None
                except Exception as e:
                    print(f"ERROR: Failed to read file {filename}: {e}")
                    return None
            else:
                print("ERROR: Invalid input mode selection.")
                return None
                
        except ValueError:
            print("ERROR: Invalid input. Please enter a number.")
            return None
    
    def add_token(self, token_type: TokenType, value: str):
        """Add a token to the list"""
        token = Token(token_type, value, self.line_number, self.column_number)
        self.tokens.append(token)
        if token_type != TokenType.WHITESPACE and token_type != TokenType.NEWLINE:
            self.token_count += 1
    
    def add_error(self, message: str, value: str):
        """Add an error to the list"""
        error = f"ERROR: {message} '{value}' at line {self.line_number}"
        self.errors.append(error)
        self.error_count += 1
    
    def validate_token_for_language(self, token_type: TokenType, value: str) -> bool:
        """Validate if a token is appropriate for the selected language"""
        if self.language == Language.PYTHON:
            # Python-specific validations
            if token_type == TokenType.CHAR:
                self.add_error("Character literals not used in Python", value)
                return False
            if token_type == TokenType.SEMICOLON and value == ';':
                self.add_error("Semicolons not typically used in Python", value)
                return False
            if value in ['**', '//'] and token_type == TokenType.ARITHMETIC_OP:
                return True  # Python-specific operators
                
        elif self.language in [Language.C, Language.JAVA]:
            # C/Java-specific validations
            if value in ['**', '//'] and token_type == TokenType.ARITHMETIC_OP:
                self.add_error("Invalid operator for C/Java", value)
                return False
                
        return True
    
    def classify_identifier(self, value: str) -> TokenType:
        """Classify an identifier as keyword or regular identifier"""
        if self.language and value in self.keywords[self.language]:
            return TokenType.KEYWORD
        return TokenType.IDENTIFIER
    
    def tokenize(self, source_code: str):
        """Tokenize the source code"""
        self.tokens.clear()
        self.errors.clear()
        self.token_count = 0
        self.error_count = 0
        self.line_number = 1
        self.column_number = 1
        
        position = 0
        
        while position < len(source_code):
            matched = False
            
            for pattern, token_type in self.compiled_patterns:
                match = pattern.match(source_code, position)
                if match:
                    value = match.group(0)
                    
                    # Handle special cases
                    if token_type == TokenType.IDENTIFIER:
                        token_type = self.classify_identifier(value)
                    
                    # Validate comment styles for language
                    if token_type == TokenType.COMMENT:
                        if value.startswith('#') and self.language != Language.PYTHON:
                            self.add_error("Invalid comment style for C/Java", value)
                        elif (value.startswith('//') or value.startswith('/*')) and self.language == Language.PYTHON:
                            self.add_error("Invalid comment style for Python", value)
                    
                    # Validate other tokens for language compatibility
                    if self.validate_token_for_language(token_type, value):
                        self.add_token(token_type, value)
                    
                    # Update position tracking
                    if token_type == TokenType.NEWLINE:
                        self.line_number += 1
                        self.column_number = 1
                    else:
                        self.column_number += len(value)
                    
                    position = match.end()
                    matched = True
                    break
            
            if not matched:
                # Handle invalid characters
                char = source_code[position]
                
                # Check for invalid number formats
                if char.isdigit():
                    # Look for malformed numbers like 12.3.4
                    end_pos = position
                    while end_pos < len(source_code) and (source_code[end_pos].isdigit() or source_code[end_pos] == '.'):
                        end_pos += 1
                    potential_number = source_code[position:end_pos]
                    if potential_number.count('.') > 1:
                        self.add_error("Invalid number format", potential_number)
                        position = end_pos
                    else:
                        self.add_error("Unknown symbol", char)
                        position += 1
                else:
                    self.add_error("Unknown symbol", char)
                    position += 1
                
                self.column_number += 1
    
    def print_results(self):
        """Print tokenization results in structured format"""
        language_names = {Language.C: "C", Language.PYTHON: "Python", Language.JAVA: "Java"}
        
        print(f"\n=== LEXICAL ANALYSIS for {language_names[self.language]} ===")
        print(f"{'TOKEN TYPE':<15} | {'TOKEN VALUE':<20} | {'LINE'}")
        print("=" * 50)
        
        for token in self.tokens:
            if token.type not in [TokenType.WHITESPACE, TokenType.NEWLINE]:
                print(f"{token.type.value:<15} | {token.value:<20} | {token.line}")
        
        # Print errors
        if self.errors:
            print(f"\n=== ERRORS FOUND ===")
            for error in self.errors:
                print(error)
        
        # Print statistics
        self.print_statistics()
    
    def print_statistics(self):
        """Print analysis statistics"""
        print(f"\n=== LEXICAL ANALYSIS SUMMARY ===")
        print(f"Total tokens recognized: {self.token_count}")
        print(f"Total errors found: {self.error_count}")
        print(f"Lines processed: {self.line_number}")

def main():
    """Main function to run the lexical analyzer"""
    analyzer = LexicalAnalyzer()
    
    # Language selection
    if not analyzer.select_language():
        return 1
    
    # Input source selection
    source_code = analyzer.get_input_source()
    if source_code is None:
        return 1
    
    # Perform lexical analysis
    analyzer.tokenize(source_code)
    
    # Display results
    analyzer.print_results()
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)