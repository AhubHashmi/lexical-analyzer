import re
import tkinter as tk
from tkinter import messagebox

TOKENS = {
   "for": ("keyword", "for"),
   "import": ("keyword", "import"),
   "()": ("punctuator", "()"),
   "(": ("(", "_"),
   ")": (")", "_"),
   "int": ("data_type", "int"),
   ";": (";", "_"),
   ",": (",", "_"),
   "{": ("{", "_"),
   "}": ("}", "_"),
   "++": ("inc_opt", "++"),
   "--": ("dec_opt", "--"),
   "<=": ("rel_opt", "<="),
   ">=": ("rel_opt", ">="),
   "==": ("rel_opt", "=="),
   "!=": ("rel_opt", "!="),
   "<": ("rel_opt", "<"),
   ">": ("rel_opt", ">"),
   "+=": ("rel_opt", "+="),
   "-=": ("rel_opt", "-="),
   "*=": ("rel_opt", "*="),
   "/=": ("rel_opt", "/="),
   "=": ("assign_opt", "="),
   "+": ("arith_opt", "+"),
   "-": ("arith_opt", "-"),
   "*": ("arith_opt", "*"),
   "/": ("arith_opt", "/"),
   "[": ("[", "_"),
   "]": ("]", "_"),
   "print": ("keyword", "print"),
   "range": ("range", "_"),
   "in": ("in", "_"),
   "anynumber": ("Numeric_val", "givennumber"),
   ";": ("Punctuator", ";"),
   ",": ("Punctuator", ","),
   "::": ("namespace_provider", "::"),
   ":": ("Scope_resolution_Operator", ":"),
   "?": ("Ternary_Conditional_operator", "?"),
   "//": ("Single_Line_comment", "//"),
   "/*": ("Multi_Line_comment_opener", "/*"),
   "*/": ("Multi_Line_comment_closer", "*/"),
   "%": ("format_specifier", "%"),
   "&": ("address-of_operator/bitwise_AND_operator/Reference_Declaration", "&"),
   "!": ("Logical_Operator", "!"),
   "|": ("Punctuator", "|"),
   "^": ("Bitwise_Operator", "^"),
   "||": ("Logical_operator", "||"),
   "class":("Keyword", "class"),
   "def":("Keyword", "def"),
   ".":("Punctuator", "."),
   "break":("keyword", "break"),
   "pass":("keyword", "pass"),
   "global":("keyword", "global"),
   "is":("keyword", "is"),
   "lambda":("keyword", "lambda"),
   "elif":("keyword", "elif"),
   "else":("keyword", "else"),
   "finally":("keyword", "finally"),
   "exec":("keyword", "exec"),
   "except":("keyword", "except"),
   "not":("keyword", "not"),
   "or":("keyword", "or"),
   "assert":("keyword", "assert"),
   "as":("keyword", "as"),
   "del":("keyword", "del"),
   "raise":("keyword", "raise"),
   "return":("keyword", "return"),
   "try":("keyword", "try"),
   "while":("keyword", "while"),
   "with":("keyword", "with"),
   "yield":("keyword", "yield"),
   "@":("punctuator", "@"),
   "$":("punctuator", "$"),
   "&":("punctuator", "&"),
   "float":("datatype", "float"),
   "char":("datatype", "char"),
   "int":("datatype", "int"),
   "self":("class_inst", "self"),
}

def tokenize_program():
    user_input = text_input.get("1.0", "end-1c")
    lines = user_input.split('\n')

    tokens_listbox.delete(0, tk.END)

    inside_string = False
    inside_include = False
    inside_angle_brackets = False
    inside_multi_line_comment = False

    for line_no, line in enumerate(lines, start=1):
        if inside_multi_line_comment:
            if "*/" in line:
                inside_multi_line_comment = False
                tokens_listbox.insert(tk.END, f"Line {line_no}:\n  {line}\n    Class Part: multi-line comment\n    Value Part: {line.strip()}")
                tokens_listbox.insert(tk.END, "")
            else:
                tokens_listbox.insert(tk.END, f"Line {line_no}:\n  {line}\n    Class Part: multi-line comment\n    Value Part: {line.strip()}")
                tokens_listbox.insert(tk.END, "")
            continue

        if line.strip().startswith("#"):
            if "#" in line and "<" in line and ">" in line:
                tokens_listbox.insert(tk.END, f"Line {line_no}:\n  {line}\n    Class Part: library\n    Value Part: {line.strip()}")
            else:
                tokens_listbox.insert(tk.END, f"Line {line_no}:\n  {line}\n    Class Part: single-line comment\n    Value Part: {line.strip()}")
            tokens_listbox.insert(tk.END, "")
            continue

        if "/*" in line:
            inside_multi_line_comment = True
            tokens_listbox.insert(tk.END, f"Line {line_no}:\n  {line}\n    Class Part: multi-line comment\n    Value Part: {line.strip()}")
            tokens_listbox.insert(tk.END, "")
            continue

        line_tokens = []
        words = re.findall(r"[\w']+|\".*?\"|\d+\.\d+|\d+|[(),;=+\-*/<>\[\]#]+", line)

        for word in words:
            if word == "\"":
               inside_string = not inside_string
            elif word == "#":
              inside_include = True
              token_class, token_value = "Special_Char", "#"
              line_tokens.append((word, token_class, token_value))
              inside_include = False

            elif inside_include:
             if word == "<":
               inside_angle_brackets = True
               inside_include = False
               library_name = ""
             else:
              token_class, token_value = "library_includer", "include"
              line_tokens.append((word, token_class, token_value))
              inside_include = False

            elif inside_angle_brackets:
            
              if word == ">":
                inside_angle_brackets = False
                token_class, token_value = "library", library_name
                line_tokens.append(("<" + library_name + ">", token_class, token_value))
              else:
                library_name += word

            elif word.startswith("'") and word.endswith("'"):
                line_tokens.append((word, "char_const", word.strip("'")))
            elif word.startswith("\"") and word.endswith("\""):
                line_tokens.append((word, "string", word.strip("\"")))
            elif re.match(r"^\d+\.\d+$", word):
                line_tokens.append((word, "float_const", word))
            elif word in TOKENS:
                token_class, token_value = TOKENS[word]
                line_tokens.append((word, token_class, token_value))
                if word == "class":
                    if words.index(word) + 1 < len(words):
                        next_word = words[words.index(word) + 1]
                        if re.match(r"^[a-zA-Z_]\w*$", next_word):
                            class_name = next_word
                            line_tokens.append((next_word, "Identifier", next_word))
                            words[words.index(word) + 1] = ""
                elif word == "def":
                    if words.index(word) + 1 < len(words):
                        next_word = words[words.index(word) + 1]
                        if re.match(r"^[a-zA-Z_]\w*$", next_word):
                            method_name = next_word
                            line_tokens.append((next_word, "function/method", "function/method"))
                            words[words.index(word) + 1] = ""
                elif word == "(":
                    if re.match(r"^\(\w+\)$", word):
                        method_name = word[1:-1]
                        line_tokens.append(("(", "function/method", "function/method"))
                        line_tokens.append((method_name, "method_name", method_name))
                        line_tokens.append((")", "function/method", "function/method"))
            else:
                if re.match(r"^\d+$", word):
                    line_tokens.append((word, "Numeric_val", word))
                else:
                    line_tokens.append((word, "variable_name", word))
            # Syntax error handling logic
            if inside_string or inside_include or inside_angle_brackets:
                tokens_listbox.insert(tk.END, "Syntactically incorrect")
                tokens_listbox.insert(tk.END, "")
                break

        if not (inside_string or inside_include or inside_angle_brackets):
            tokens_listbox.insert(tk.END, f"Line {line_no}:")
            for token, token_class, token_value in line_tokens:
                if token_class == "string":
                    tokens_listbox.insert(tk.END, f"  {token}\n    Class Part: {token_class}\n    Value Part: {token_value}")
                else:
                    tokens_listbox.insert(tk.END, f"  {token}\n    Class Part: {token_class}\n    Value Part: {token_value}")
            tokens_listbox.insert(tk.END, "")


app = tk.Tk()
app.title("Lexical Analyzer")
app.geometry("600x400")

title_label = tk.Label(app, text="Lexical Analyzer", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

text_input = tk.Text(app, height=8, width=60, font=("Courier New", 12))
text_input.pack(padx=20, pady=(0, 10))

tokenize_button = tk.Button(app, text="Tokenize", command=tokenize_program, bg="#4caf50", fg="white",
                            font=("Helvetica", 12, "bold"), padx=20, pady=10)
tokenize_button.pack()

tokens_listbox = tk.Listbox(app, font=("Courier New", 10))
tokens_listbox.pack(fill=tk.BOTH, expand=True)

app.mainloop()
