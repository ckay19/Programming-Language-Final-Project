%{
#include <stdio.h>
#include <string.h>
%}

%option noyywrap

%%
"/*"([^*]|\*+[^*/])*\*+"/"              { printf("%-30s : %s\n", "COMMENT", yytext); }
"//".*                                  { printf("%-30s : %s\n", "COMMENT", yytext); }

\"([^\"\\\n]|\\.)*\"                    { printf("%-30s : %s\n", "STRING", yytext); }
\"([^\"\\\n]|\\.)*\n                    { yytext[yyleng - 1] = '\0'; printf("%-30s : %s\n", "ERROR: UNCLOSED_STRING", yytext); unput('\n'); }

\'([^\'\\\n]|\\.)\'                     { printf("%-30s : %s\n", "CHAR", yytext); }
\'([^\'\\\n]|\\.)*\n                    { yytext[yyleng - 1] = '\0'; printf("%-30s : %s\n", "ERROR: UNCLOSED_CHAR", yytext); unput('\n'); }
\'([^\'\\\n]|\\.){2,}\'                 { printf("%-30s : %s\n", "ERROR_INVALID_CHAR", yytext); unput('\n'); }

[0-9]+\.[0-9]+\.[0-9]+                  { printf("%-30s : %s\n", "ERROR: INVALID_FLOAT", yytext); }
[0-9]+\.\.[0-9]+                        { printf("%-30s : %s\n", "ERROR: INVALID_FLOAT", yytext); }
[0-9]+\.\.                              { printf("%-30s : %s\n", "ERROR: INVALID_FLOAT", yytext); }
\.\.[0-9]+                              { printf("%-30s : %s\n", "ERROR: INVALID_FLOAT", yytext); }
\.[0-9]*\.[0-9]+                        { printf("%-30s : %s\n", "ERROR: INVALID_FLOAT", yytext); }
[0-9]*\.[0-9]*\.                        { printf("%-30s : %s\n", "ERROR: INVALID_FLOAT", yytext); }

[0-9]+\.[0-9]+([eE][+-]?[0-9]+)?        { printf("%-30s : %s\n", "FLOAT", yytext); }
[0-9]+([eE][+-]?[0-9]+)                 { printf("%-30s : %s\n", "FLOAT", yytext); }
[0-9]+                                  { printf("%-30s : %s\n", "INTEGER", yytext); }

"++"|"--"                               { printf("%-30s : %s\n", "UNARY_OP", yytext); }
"=="|"!="|"<="|">="|"<"|">"             { printf("%-30s : %s\n", "REL_OP", yytext); }
"&&"|"||"|"!"                           { printf("%-30s : %s\n", "LOGICAL_OP", yytext); }
"<<"|">>"                               { printf("%-30s : %s\n", "SHIFT_OP", yytext); }
"\+="|"-="|"*="|"/="|"%="               { printf("%-30s : %s\n", "ASSIGN_OP", yytext); }
"&"|"|"|"^"|"~"                         { printf("%-30s : %s\n", "BITWISE_OP", yytext); }
"+"|"-"|"*"|"/"|"%"                     { printf("%-30s : %s\n", "ARITH_OP", yytext); }
"="                                     { printf("%-30s : %s\n", "ASSIGNMENT", yytext); }

"("                                     { printf("%-30s : %s\n", "LPAREN", yytext); }
")"                                     { printf("%-30s : %s\n", "RPAREN", yytext); }
"{"                                     { printf("%-30s : %s\n", "LBRACE", yytext); }
"}"                                     { printf("%-30s : %s\n", "RBRACE", yytext); }
"["                                     { printf("%-30s : %s\n", "LBRACKET", yytext); }
"]"                                     { printf("%-30s : %s\n", "RBRACKET", yytext); }
";"                                     { printf("%-30s : %s\n", "SEMICOLON", yytext); }
","                                     { printf("%-30s : %s\n", "COMMA", yytext); }
"."                                     { printf("%-30s : %s\n", "DOT", yytext); }
":"                                     { printf("%-30s : %s\n", "COLON", yytext); }
"\?"                                    { printf("%-30s : %s\n", "QUESTION", yytext); }

[a-zA-Z_][a-zA-Z0-9_]*                  {
    if (strcmp(yytext, "class") == 0 || strcmp(yytext, "public") == 0 || strcmp(yytext, "static") == 0)
        printf("%-30s : %s\n", "KEYWORD", yytext);
    else
        printf("%-30s : %s\n", "IDENTIFIER", yytext);
}

[ \t\n]+                                { /* skip whitespace */ }
\r                                      ;
[@#$`~]                                 { printf("%-30s : %s\n", "ERROR: ILLEGAL_SYMBOL", yytext); }
.                                       { printf("%-30s : %s\n", "ERROR: INVALID_CHARACTER", yytext); }
%%


int main() {
    yylex();
    return 0;
}
