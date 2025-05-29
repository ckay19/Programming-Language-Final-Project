%{
#include <stdio.h>
#include <string.h>
%}
%option noyywrap

%%
"#"[ \t]*[^\n]*                         { printf("%-30s : %s\n", "COMMENT", yytext); }

\"\"\"([^\"\\]|\\.|\\n)*?\"\"\"         { printf("%-30s : %s\n", "MULTILINE_STRING", yytext); }
\'\'\'([^\'\\]|\\.|\\n)*?\'\'\'         { printf("%-30s : %s\n", "MULTILINE_STRING", yytext); }

\"([^\"\\\n]|\\.)*\n                    { yytext[yyleng - 1] = '\0'; printf("%-30s : %s\n", "ERROR: UNTERMINATED_STRING", yytext); unput('\n'); }
\'([^\'\\\n]|\\.)*\n                    { yytext[yyleng - 1] = '\0'; printf("%-30s : %s\n", "ERROR: UNTERMINATED_STRING", yytext); unput('\n'); }

\"([^\"\\\n]|\\.)*\"                    { printf("%-30s : %s\n", "STRING", yytext); }
\'([^\'\\\n]|\\.)\'                     { printf("%-30s : %s\n", "STRING", yytext); }

[0-9]+\.[0-9]+\.[0-9]+                  { printf("%-30s : %s\n", "ERROR: INVALID_NUMBER", yytext); }  
[0-9]+\.\.[0-9]+                        { printf("%-30s : %s\n", "ERROR: INVALID_NUMBER", yytext); } 
[0-9]+\.\.                              { printf("%-30s : %s\n", "ERROR: INVALID_NUMBER", yytext); } 
\.\.[0-9]+                              { printf("%-30s : %s\n", "ERROR: INVALID_NUMBER", yytext); } 
\.[0-9]*\.[0-9]+                        { printf("%-30s : %s\n", "ERROR: INVALID_NUMBER", yytext); } 
[0-9]*\.[0-9]*\.                        { printf("%-30s : %s\n", "ERROR: INVALID_NUMBER", yytext); }  

[0-9]+\.[0-9]*([eE][-+]?[0-9]+)?        { printf("%-30s : %s\n", "FLOAT", yytext); }
[0-9]+([eE][-+]?[0-9]+)?                { printf("%-30s : %s\n", "INTEGER", yytext); }

"=="|"!="|"<="|">="|"<"|">"             { printf("%-30s : %s\n", "REL_OP", yytext); }
"\+\="|"-="|"*="|"/="|"%="              { printf("%-30s : %s\n", "AUG_ASSIGN", yytext); }
"//"|"**"|"+"|"-"|"*"|"/"|"%"           { printf("%-30s : %s\n", "ARITH_OP", yytext); }

"="                                     { printf("%-30s : %s\n", "ASSIGNMENT", yytext); }

"and"|"or"|"not"                        { printf("%-30s : %s\n", "LOGICAL_OP", yytext); }

"if"|"elif"|"else"|"while"|"for"|"in"|"def"|"return"|"pass"|"break"|"continue"|"class"|"import"|"from"|"as"|"with"|"try"|"except"|"finally"|"raise"|"True"|"False"|"None"|"global"|"nonlocal"|"assert" {
    printf("%-30s : %s\n", "KEYWORD", yytext);
}

[a-zA-Z_][a-zA-Z0-9_]*                  { printf("%-30s : %s\n", "IDENTIFIER", yytext); }

[(){}\[\]]                              { printf("%-30s : %s\n", "BRACKET", yytext); }
[:,.;]                                  { printf("%-30s : %s\n", "PUNCT", yytext); }

[ \t]+                                  { /* skip whitespace */ }
\n                                      { /* ignore newline */ }
\r                                      ;

@[a-zA-Z_][a-zA-Z0-9_]*                 { printf("%-30s : %s\n", "ERROR: ILLEGAL_SYMBOL", yytext); }

[^ \t\n[:alnum:]_\"\'\.\[\]\{\}\(\)\:\;\,\#\=\+\-\*/%<>!] {
    printf("%-30s : %s\n", "ERROR: UNKNOWN_CHARACTER", yytext);
}

.                                       { printf("%-30s : %s\n", "ERROR: UNKNOWN_CHARACTER", yytext); }

%%

int main() {
    yylex();
    return 0;
}
