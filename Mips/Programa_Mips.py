import tkinter as tk
from tkinter import ttk, messagebox

def register_to_bin(reg):
    if reg.startswith("$") and reg[1:].isdigit():
        num = int(reg[1:])
        if 0 <= num <= 7:
            return f"{num:03b}"
    return None

def immediate_to_bin(imm, bits=6):
    if imm.isdigit():
        num = int(imm)
        if 0 <= num < (1 << bits):
            return f"{num:0{bits}b}"
    return None

def assemble():
    instr = entry.get().strip()
    parts = instr.replace(",", "").split()
    
    opcode_dict = {"addi": "1000", "andi": "0110", "ori": "1010", "sw": "1100", "lw": "1011", "beq": "1101", "slti": "1001", "j": "0111", "add": "1111", "sub": "1111", "and": "1111", "or": "1111", "nand": "1111", "nor": "1111", "xnor": "1111", "slt": "1111"}
    funct_dict = {"add": "000", "sub": "001", "and": "010", "or": "011", "nand": "100", "nor": "101", "xnor": "110", "slt": "111"}
    instr_name = parts[0].lower()
    
    if instr_name not in opcode_dict:
        messagebox.showerror("Erro", "Instrução inválida!")
        return
    
    opcode = opcode_dict[instr_name]
    binary_code = ""
    
    try:
        if instr_name in ["sw", "lw"]:
            rt = register_to_bin(parts[1])
            offset, rs = parts[2].split("(")
            rs = rs.replace(")", "")
            rs = register_to_bin(rs)
            imm = immediate_to_bin(offset)
        elif instr_name == "beq":
            rs, rt, imm = register_to_bin(parts[1]), register_to_bin(parts[2]), immediate_to_bin(parts[3])
        elif instr_name == "j":
            imm = immediate_to_bin(parts[1], bits=12)
        elif instr_name in funct_dict:
            rd, rs, rt, funct = register_to_bin(parts[1]), register_to_bin(parts[2]), register_to_bin(parts[3]), funct_dict[instr_name]
        else:
            rt, rs, imm = register_to_bin(parts[1]), register_to_bin(parts[2]), immediate_to_bin(parts[3])
        
        if None in locals().values():
            raise ValueError
        
        binary_code = opcode + rs + rt + (rd if 'rd' in locals() else '') + (funct if 'funct' in locals() else '') + (imm if 'imm' in locals() else '')
        hex_code = f"{int(binary_code, 2):04X}"
        result_label.config(text=f"Código de Máquina: {hex_code}")
    except:
        messagebox.showerror("Erro", "Formato inválido! Verifique a sintaxe.")

# Criando a interface gráfica
root = tk.Tk()
root.title("MIPS Assembler")
root.geometry("400x200")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

frame = ttk.Frame(root, padding=10)
frame.pack(expand=True)

label = ttk.Label(frame, text="Digite a instrução:", font=("Arial", 12))
label.pack()

entry = ttk.Entry(frame, width=35, font=("Arial", 12))
entry.pack(pady=5)

button = ttk.Button(frame, text="Converter", command=assemble)
button.pack(pady=5)

result_label = ttk.Label(frame, text="Código de Máquina: ", font=("Arial", 12, "bold"))
result_label.pack(pady=5)

root.mainloop()
