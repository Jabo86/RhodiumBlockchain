# Leggi il file
with open('rhodium_gui_fixed.py', 'r') as f:
    lines = f.readlines()

# Trova e correggi la sezione problematica
for i in range(len(lines)):
    if "if block:" in lines[i] and i+3 < len(lines):
        # Le prossime 3 righe devono essere indentate
        lines[i+1] = "                " + lines[i+1].lstrip()
        lines[i+2] = "                " + lines[i+2].lstrip() 
        lines[i+3] = "                " + lines[i+3].lstrip()
        break

# Scrivi il file corretto
with open('rhodium_gui_fixed.py', 'w') as f:
    f.writelines(lines)

print("✅ Indentazione sistemata!")
