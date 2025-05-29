import subprocess
import os
import sys
import tempfile

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def analyze_only_lexer(source_code, lexer_exe, output_filename="output.txt"):
    with tempfile.TemporaryDirectory() as tmpdir:
        source_file_path = os.path.join(tmpdir, "input.code")

        with open(source_file_path, "w") as f:
            f.write(source_code)

        try:
            with open(source_file_path, "r") as source_file:
                lexer_proc = subprocess.run(
                    [lexer_exe],
                    stdin=source_file,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
            lexer_output = "\n".join(line.strip() for line in lexer_proc.stdout.splitlines() if line.strip())

        except FileNotFoundError:
            lexer_output = "Lexer executable not found. Please build your lexer."
        except subprocess.TimeoutExpired:
            lexer_output = "Lexer timed out."

        with open(output_filename, "w") as out_file:
            out_file.write("=== Input Source Code ===\n")
            out_file.write(source_code + "\n\n")
            out_file.write("=== Lexical Tokenization Output ===\n")
            out_file.write(lexer_output + "\n")

        print(f"\nOutput saved to {output_filename}")

def main():
    while True:
        clear()
        print("Select language:")
        print("1. C\n2. Java\n3. Python")
        lang = input("Enter choice (1-3): ").strip()

        lexer_map = {
            "1": "C\\c_lexer.exe",
            "2": "Java\\java_lexer.exe",
            "3": "python\\py_lexer.exe"
        }
        lexer = lexer_map.get(lang)

        if not lexer:
            clear()
            print("Invalid language choice")
            input("Press Enter to try again...")
            continue

        while True:
            clear()
            print("Input mode:\n0. Go Back\n1. Manual\n2. File")
            mode = input("Enter choice (0-2): ").strip()
            
            if mode == '0':
                break

            if mode == "1":
                print("\nEnter code (end input with Ctrl+Z then Enter):")
                try:
                    user_input = sys.stdin.read()
                    analyze_only_lexer(user_input, lexer)
                except KeyboardInterrupt:
                    clear()
                    print("Cancelled.")
                    break

            elif mode == "2":
                filename = input("Enter filename (or 'x' to exit): ").strip()
                if filename.lower() == 'x':
                    break
                if filename.lower() == '':
                    clear()
                    input("ERROR: No input file provided.")
                    continue
                    
                try:
                    with open(filename, 'r') as f:
                        code = f.read()
                        analyze_only_lexer(code, lexer)
                except FileNotFoundError:
                    clear()
                    input(f"Could not open {filename}.txt. Please make sure the file exists.")
                    continue

            else:
                clear()
                input("ERROR: Invalid input mode. Please try again.")
                continue

            again = input("\nWant to analyze again? (Y/N): ").strip().lower()
            if again != 'y':
                clear()
                print("Thank you for using this multilanguage lexical analyzer.")
                exit()
            else:
                main()
                

if __name__ == "__main__":
    main()
