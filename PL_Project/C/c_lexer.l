%{
#include <stdio.h>
#include <string.h>

void print_token(const char *label, const char *text) {
    char buffer[1024];
    int j = 0;
    for (int i = 0; text[i] != '\0' && j < 1023; i++) {
        if (text[i] == '\n') {
            buffer[j++] = '\\';
            buffer[j++] = 'n';
        } else if (text[i] == '\t') {
            buffer[j++] = '\\';
            buffer[j++] = 't';
        } else {
            buffer[j++] = text[i];
        }
    }
    buffer[j] = '\0';
    printf("%-30s : %s\n", label, buffer);
}

%}

%option noyywrap



%%
"#include"[ \t]*"<"[a-zA-Z0-9_/.]+">"   {printf("%-30s : %s\n", "PREPROCESSOR DIRECTIVE", yytext); }
"/*"([^*]|\*+[^*/])*\*+"/"              { printf("%-30s : %s\n", "COMMENT", yytext); }
"//".*                                  { printf("%-30s : %s\n", "COMMENT", yytext); }

\'([^\'\\\n]|\\.)*\n                    { yytext[yyleng - 1] = '\0'; print_token("ERROR: UNTERMINATED_CHAR", yytext); unput('\n'); }
\'([^\'\\]|\\.)\'                       { printf("%-30s : %s\n", "CHAR", yytext); }
\'([^\'\\\n]|\\.){2,}\'                 { print_token("ERROR: INVALID_CHAR", yytext); unput('\n'); }

\"([^\"\\\n]|\\.)*[\n]                  { yytext[yyleng - 1] = '\0'; print_token("ERROR: UNTERMINATED_STRING", yytext); unput('\n'); }
\"([^\"\\\n]|\\.)*\"                    { printf("%-30s : %s\n", "STRING", yytext); }


[0-9]+\.[0-9]+\.[0-9]+                  { printf("%-30s : %s\n", "ERROR: INVALID_NUMBER", yytext); }  
[0-9]+\.\.[0-9]+                        { printf("%-30s : %s\n", "ERROR: INVALID_NUMBER", yytext); } 
[0-9]+\.\.                              { printf("%-30s : %s\n", "ERROR: INVALID_NUMBER", yytext); } 
\.\.[0-9]+                              { printf("%-30s : %s\n", "ERROR: INVALID_NUMBER", yytext); } 
\.[0-9]*\.[0-9]+                        { printf("%-30s : %s\n", "ERROR: INVALID_NUMBER", yytext); } 
[0-9]*\.[0-9]*\.                        { printf("%-30s : %s\n", "ERROR: INVALID_NUMBER", yytext); }  

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

[a-zA-Z_][a-zA-Z0-9_]*          {
    if (strcmp(yytext, "int") == 0 || strcmp(yytext, "return") == 0 || strcmp(yytext, "if") == 0)
        printf("%-30s : %s\n", "KEYWORD", yytext);
    else
        printf("%-30s : %s\n", "IDENTIFIER", yytext);
}


[ \t\n]+    ;
\r         ;
[@#$`~]                                 { printf("%-30s : %s\n", "ERROR: UNKNOWN_SYMBOL", yytext); }
.                                       { printf("%-30s : %s\n", "ERROR: UNKNOWN_SYMBOL", yytext); }

%%


int main() {
    yylex();
    return 0;
}