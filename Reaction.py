# Balance reaction
import tkinter as tk
from tkinter import messagebox
from chempy import Reaction, balance_stoichiometry

# Hide
BM = {}
MOL_Reac = []
MOL_Prod = []
React = {}
Produc = {}

# ==============
# Ask User
# ==============
def Ask_user():
    answ = messagebox.askyesno(
        "ASK",
        "Do you want Generate Reaction"
    )
    if answ:
        Ask_button.config(text='BACK ALL', bg='red')
        Frame_heavey.pack()
        Comp_BM.set('')
        Opt_compound_BM.pack()
        Btn_Next.pack()          
        much_rop.pack_forget()
        frame_option_rap.pack_forget()
        reaction.pack_forget()
        frame_basis.pack_forget()
    else:
        Ask_button.config(text='NEXT', bg='white')
        Btn_Next.pack_forget()
        reaction.pack_forget()
        Frame_heavey.pack_forget()
        much_rop.pack_forget()
        frame_option_rap.pack_forget()
        frame_basis.pack_forget()
        Btn_basis.pack_forget()
        Opt_compound_BM.pack_forget()

def heavy_compound():         
    much_rop.pack()
    Comp_BM.set("")
    Opt_compound_BM.pack_forget()
    Btn_Next.pack_forget()
    Frame_heavey.pack_forget()

    for frame_option in frame_option_rap.winfo_children(): 
        frame_option.destroy()  #<--- Reset Frame
    MOL_Reac.clear() #<--- Reset Reactant
    MOL_Prod.clear() #<--- Reset Product

#    Ent_comp_reac.set("")
#    Ent_comp_produc.set("")
 
# Validasi input
    try:
        n_reac= int(Ent_comp_reac.get())
        n_prod = int(Ent_comp_produc.get())
    except ValueError:
        messagebox.showerror('Error', 'Input must be numbers')
        return
    if n_reac == 0 or n_prod == 0: 
        messagebox.showerror('Error','Cannot be filled 0')
        return
    elif n_reac <= 0 or n_prod <= 0:
        messagebox.showerror('Error', 'The amount of reactant and product cannot be less than 0')
    choice = BM.keys()
    if len(choice) == 0:
        messagebox.showerror('ERROR', 'Not have compound!')
        return

    for reac in range(n_reac): #<--- Looping for ammount reactant
        var = tk.StringVar()
        var.set("")
        tk.Label(frame_option_rap, text=f"Reactant: {reac+1}").pack()
        MOL_Reac.append(var)
        tk.OptionMenu(frame_option_rap, var, *choice).pack()
    for prod in range(n_prod): #<--- Looping for ammount product
        var = tk.StringVar()
        var.set("")
        tk.Label(frame_option_rap, text=f'Product: {prod+1}').pack()
        MOL_Prod.append(var)
        tk.OptionMenu(frame_option_rap, var, *choice).pack()
    
    tk.Button(frame_option_rap, text='Generate', command=generate_reaction, bg='lightgreen').pack(pady=5)
    frame_option_rap.pack(pady=2)

# ==============
# Reaction
# ==============
def generate_reaction():
    React.clear()
    Produc.clear()
    for var in MOL_Reac:
        comp = var.get()
        if comp in React:
            React[comp] +=1
        else:
            React[comp] = 1
    
    for var in MOL_Prod:
        comp = var.get()
        if comp in Produc:
            Produc[comp] += 1
        else:
            Produc[comp] =1 

    if len(React) == 0 or len(Produc) == 0:
        messagebox.showerror('Error', 'Reactant and Product do not exist')
        return
    
    try:
        reactant, produc = balance_stoichiometry(React, Produc)
        r = Reaction(reactant, produc) 
        show_reaction.set(str(r))
        # Cofficient reaction

        coef_Reactant.set(list(reactant.items()))
        coef_Product.set(list(produc.items()))
    except Exception as e:
        messagebox.showerror("Erorrr",e)
    reaction.pack()

# ==============
# Update mol option
# ==============
def update_BM():
    menu_BM = Opt_BM['menu']
    menu_BM.delete(0,'end')
    for x, y in BM.items():
        label_text=f'{x}: {y}'
        menu_BM.add_command(
            label=label_text,
            command=lambda k=x: Comp_BM.set(f"{k}: {BM[k]}") #<--- Hidden value
        )

# ==============
# Calculate Mol
# ==============
def entry_CaB():      #<--- CaB (Compound and BM)
    name_compound = Ent_comp.get().upper()
    b_BM = Ent_Cal_Comp.get()

    if Ent_comp.get() == '' or Ent_Cal_Comp.get() == '':
        messagebox.showerror(
            'ERROR',
            'SOMETHING IS NOT FILLED IN'
        )     
        return
    try:
        b_BM= float(b_BM)
    except:
        messagebox.showerror('ERROR', 'MUST BE IN NUMBERS')

    # Choice Compound 
    BM[name_compound] = b_BM
    update_BM()
    messagebox.showinfo('Success input compound', f'\n{name_compound}: {b_BM: .2f}')

    # Auto Delete
    Ent_comp.set("")
    Ent_Cal_Comp.set("")
        
# ===============================
# GUI 
# ===============================

# ===============================
# FRAME
# ===============================
window = tk.Tk()
window.geometry('400x600')
window.title('Balance reaction')
frame_option_rap = tk.Frame(window) #<--- rap (Reactant and Product)
reaction = tk.Frame(window)
frame_basis = tk.Frame(window)
Opt_compound_BM = tk.Frame(window)
Frame_heavey = tk.Frame(window)
much_rop = tk.Frame(window)

# ===============================
# BUTTON
# ===============================
Btn_basis = tk.Frame(window)
Btn_Next = tk.Frame(window)    

# GUI input compound and heavy compound
Ent_comp = tk.StringVar()
tk.Label(Frame_heavey, text='Compound').pack(pady=3)
tk.Entry(Frame_heavey, textvariable=Ent_comp, width=30).pack(pady=5)
Ent_Cal_Comp = tk.StringVar()
tk.Label(Frame_heavey, text='Heavy compound').pack(pady=3)
tk.Entry(Frame_heavey, textvariable=Ent_Cal_Comp, width=30).pack(pady=5)
tk.Button(Frame_heavey, text='SAVE', width=12, command=entry_CaB).pack()

# GENERATE REACTION
Ent_comp_reac = tk.StringVar()
tk.Label(much_rop, text='Reactant', font=('Arial', 12, 'bold')).pack(pady=3)
tk.Entry(much_rop, textvariable=Ent_comp_reac, width=30).pack(pady=5)

Ent_comp_produc = tk.StringVar()
tk.Label(much_rop, text='Product', font=('Arial', 12, 'bold')).pack(pady=3)
tk.Entry(much_rop, textvariable=Ent_comp_produc, width=30).pack(pady=5)

tk.Button(Btn_Next, text='Next', width=12, command=heavy_compound).pack()
tk.Button(much_rop, text='CALCULTE', width=12, command=heavy_compound).pack()

Comp_BM = tk.StringVar()
Opt_BM = tk.OptionMenu(Opt_compound_BM, Comp_BM, '') # <-- Dropdown option hide reactant
Opt_BM.pack() # <-- Show dropdown hide reactant 

# ==============
# Basis
# ==============
tk.Button(Btn_basis, text='NEXT', width=12, command=heavy_compound).pack()
tk.Label(frame_basis, text='Heavey compound', font=('Arial', 12, 'bold')).pack(pady=2)
ent_basis = tk.StringVar()

# ==============
# Show generete reaction
# ==============
show_reaction = tk.StringVar()
tk.Label(reaction, text='REACTION', font=('Arial', 10,'bold')).pack(pady=10)
tk.Label(reaction,textvariable=show_reaction, font=('Arial', 13)).pack()

# Coefficient
tk.Label(reaction, text='Coefficient reactant').pack()
coef_Reactant = tk.StringVar()
tk.Label(reaction, textvariable=coef_Reactant).pack()
tk.Label(reaction, text='Coefficient product').pack()
coef_Product = tk.StringVar()
tk.Label(reaction,textvariable=coef_Product).pack()

# ==============
# Output
# ==============
Ask_button = tk.Button(window, text='NEXT', width=12,command=Ask_user)
Ask_button.pack()
window.mainloop()
