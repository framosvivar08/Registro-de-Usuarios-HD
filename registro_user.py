import tkinter as tk
from tkinter import ttk, BooleanVar, Checkbutton
from tkcalendar import DateEntry
import pandas as pd
import os
from datetime import date

#Diccionaro Establecimientos
def obtener_establecimiento():
    return{
        1:"CESFAM Thomas Fenton",
        2:"CESFAM Mateo Bencur",
        3:"CESFAM Juan Damianovic",
        4:"CESFAM 18 Septiembre",
        5:"CESFAM Carlos Ibañez",
        6:"CECOSF Rio Seco",
        7:"CECOSF Sandra Vargas",
        8:"CECOSF Fortaleciendo Vidas",
        9:"CESFAM Juan Lozic",
        10:"Hospital Augusto Essmann",
        11:"Hospital Cristina Calderon",
        12:"Hospital Marco Antonio Chamorro",
        13:"Hospital Clinico de Magallanes",
        14:"Posta Rio Verde",
        15:"Posta Punta Delgada"

    }

#Diccionario Plataformas
def obtener_plataforma():
    return{
        1:"SIC",
        2:"DART",
        3:"Telesalud",
        4:"Telecomité Oncología",
        5:"Atención Remota"

    }

#Diccionario Roles
def obtener_roles():
    return{
        1: ["Nefrología", "Dermatología", "Diabetes", "Geriatría", "Reumatología", "TTM", "Patología Oral", "Todas/Some"],
        2: ["Administrativo", "TTM"],
        3: ["Triagista", "Gestor de Casos", "Administrativo"],
        4: ["Presentador", "Gestor", "Resolutor"],
        5: ["Administrativo", "Profesional"]
    }

#guardar en excel
def guardar_excel(datos, ruta_archivo=None):

    if ruta_archivo is None:
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        ruta_archivo = os.path.join(ruta_base, "user.xlsx")
    
    if os.path.exists(ruta_archivo):
        df = pd.read_excel(ruta_archivo)
        df = pd.concat([df, pd.DataFrame([datos])], ignore_index=True) 
    else:
        df = pd.DataFrame([datos])
        
    df.to_excel(ruta_archivo, index=False)
    print(f"Datos guardados en {ruta_archivo}")

#buscar rut
def buscar_rut(self, event=None):
    
    #ruta_user = "C:/Users/framo/OneDrive/Escritorio/registro usuario/user.xlsx"
    
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_user = os.path.join(ruta_base, "user.xlsx")

    rut = entry_rut.get().strip()
    
    if not os.path.exists(ruta_user):
        label_status. config(text="No hay base de datos disponible.")
        return
    
    if not rut:
        label_status.config(text="Por favor, ingrese un RUT")
        return
    
    df = pd.read_excel(ruta_user, dtype={'RUT': str})
    registro = df[df['RUT'] == rut]
    
    if not registro.empty:
        entry_name.delete(0, tk.END)
        entry_name.insert(0, registro.iloc[0]['Nombre'])

        entry_ap_pat.delete(0, tk.END)
        entry_ap_pat.insert(0,registro.iloc[0]['Apellido paterno'])

        entry_ap_mat.delete(0,tk.END)
        entry_ap_mat.insert(0, registro.iloc[0]['Apellido materno'])

        entry_tlf.delete(0, tk.END)
        entry_tlf.insert(0, registro.iloc[0]['Telefono'])

        entry_mail.delete(0, tk.END)
        entry_mail.insert(0, registro.iloc[0]['mail'])

        entry_fn.delete(0, tk.END)
        entry_fn.insert(0, registro.iloc[0]['nacimiento'])
           
    else:
        label_status.config(text="No hay registro del usuario.")

#limpiar campos
def limpiar_campos():
    entry_rut.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_ap_pat.delete(0, tk.END)
    entry_ap_mat.delete(0, tk.END)
    entry_tlf.delete(0, tk.END)
    entry_mail.delete(0, tk.END)
    entry_fn.delete(0, tk.END)
    entry_estab.delete(0, tk.END)
    combo_plataforma.set("")
    create_date.set_date(date.today())

#Registro de usuario    
def registrar_user():
    
    rut =entry_rut.get().strip()
    nombre = entry_name.get().strip()
    ap_pat = entry_ap_pat.get().strip()
    ap_mat = entry_ap_mat.get().strip()
    telefono = entry_tlf.get().strip()
    mail = entry_mail.get().strip()
    birth =entry_fn.get().strip()
    establecimiento = entry_estab.get().strip()
    plataforma = combo_plataforma.get()
    create_user = create_date.get()
    selected_roles = [checkbox.cget("text") for checkbox, var in role_checkboxes if var.get()]

    if plataforma =="DART":
        nombre_user_dart = entry_user_dart.get().strip()
    else:
        nombre_user_dart=None

    if rut :
        
        datos ={"RUT": rut, "Nombre": nombre, "Apellido paterno": ap_pat, "Apellido materno": ap_mat,"Telefono": 
        telefono,"mail": mail,"nacimiento": birth,"establecimiento": establecimiento, "Plataforma": plataforma,"Roles": ",".join(selected_roles)  ,"fecha creacion": create_user,"nombre usuario": nombre_user_dart}
                
        #ruta_user = "C:/Users/framo/OneDrive/Escritorio/registro usuario/user.xlsx"
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        ruta_user = os.path.join(ruta_base, "user.xlsx")


        guardar_excel(datos, ruta_user)

        label_status.config (text ="Registro completado exitosamente.")
        limpiar_campos()
    
    else:
        label_status.config (text ="Error en el registro")

#carga plataformas
plataformas = obtener_plataforma()

#cargar  establecimientos
establecimiento = obtener_establecimiento()

#cargar archvio roles
roles = obtener_roles()

#configuracion ventana
ventana = tk.Tk()
ventana.title("Registro de funcionarios")
ventana.geometry("380x600")

role_checkboxes = []
#Label RUT 
label_rut =tk.Label(ventana, text="RUT:")
label_rut.grid(row=0, column=0, padx=10,pady=5)
entry_rut = tk.Entry(ventana)
entry_rut.grid(row=0,column=1,padx=10,pady=5)

entry_rut.bind("<Return>", buscar_rut)

#Label Nombre
label_nombre =tk.Label(ventana, text="Nombre:")
label_nombre.grid(row=1, column=0, padx=10,pady=5)
entry_name = tk.Entry(ventana)
entry_name.grid(row=1,column=1,padx=10,pady=5)
#label apellido paterno
label_ap_pat =tk.Label(ventana, text="Apellido paterno:")
label_ap_pat.grid(row=2, column=0, padx=10,pady=5)
entry_ap_pat = tk.Entry(ventana)
entry_ap_pat.grid(row=2,column=1,padx=10,pady=5)
#label apellido materno
label_ap_mat =tk.Label(ventana, text="Apellido materno:")
label_ap_mat.grid(row=3, column=0, padx=10,pady=5)
entry_ap_mat = tk.Entry(ventana)
entry_ap_mat.grid(row=3,column=1,padx=10,pady=5)
#Label Telefono
label_tlf = tk.Label(ventana, text="Teléfono:")
label_tlf.grid(row=4, column=0, padx=10, pady=5)
entry_tlf =tk.Entry(ventana)
entry_tlf.grid(row=4, column=1,padx=10,pady=5)
#label mail
label_mail = tk.Label(ventana, text="Mail:")
label_mail.grid(row=5, column=0, padx=10, pady=5)
entry_mail = tk.Entry(ventana)
entry_mail.grid(row=5, column=1, padx=10, pady=5)

#label nacimiento
label_fn = tk.Label(ventana, text="Fecha de Nacimiento")
label_fn.grid(row=6, column=0, padx=10, pady=5)
entry_fn = tk.Entry(ventana, width=20)
entry_fn.grid(row=6, column=1, padx=10, pady=5)

#Setear fecha de nacimiento
def setear_fecha(event):
    fecha = entry_fn.get().strip()
    
    # Si el texto es mayor a 10 caracteres, recortar
    if len(fecha) > 10:
        entry_fn.delete(10, tk.END)
        return

    # Si la longitud de la fecha es 2 o 5, agregar el '/'
    if len(fecha) == 2 or len(fecha) == 5:
        entry_fn.insert(len(fecha), '/')
entry_fn.bind("<KeyRelease>", setear_fecha)

#label Establecimiento
label_estab = tk.Label(ventana, text="Establecimiento:")
label_estab.grid(row=7, column=0, padx=10, pady=5)
entry_estab = ttk.Combobox(ventana, values=list(establecimiento.values()),width=30)
entry_estab.grid(row=7, column=1, padx=10,pady=5)

#Label Plataforma
label_plataforma =tk.Label(ventana, text="Plataforma:")
label_plataforma.grid(row=8, column=0, padx=10,pady=5)
combo_plataforma = ttk.Combobox(ventana, values=list(plataformas.values()))
combo_plataforma.grid(row=8, column=1, padx=10,pady=5)

#Label usuario DART
label_user_dart = tk.Label(ventana, text="Nombre de usuario:")
entry_user_dart = tk.Entry(ventana)

# Configuración inicial de la variable para última fila
last_row = 9

def actualizar_roles(event):
    global last_row  # Variable para rastrear la última fila ocupada

    # Eliminar los checkboxes previos
    for checkbox, _ in role_checkboxes:
        checkbox.grid_forget()
    role_checkboxes.clear()

    # Obtener la plataforma seleccionada
    selected_plataform = combo_plataforma.get()
    plataforma_id = next((key for key, value in plataformas.items() if value == selected_plataform), None)

    # Si hay roles para la plataforma seleccionada
    if plataforma_id and plataforma_id in roles:
        label_roles.grid(row=9, column=0, columnspan=2, sticky='w', padx=10, pady=5)
        
        for idx, role in enumerate(roles[plataforma_id]):
            var = BooleanVar()
            checkbox = Checkbutton(ventana, text=role, variable=var)
            checkbox.grid(row=9 + idx, column=1, columnspan=2, sticky='w', padx=10)
            role_checkboxes.append((checkbox, var))
        
        # Actualizar la última fila ocupada
        last_row = 9 + len(roles[plataforma_id])
    else:
        label_roles.grid_forget()
        last_row = 9  # Si no hay roles, los widgets vuelven a la posición inicial

    if selected_plataform=="DART":
        label_user_dart.grid(row=last_row,column=0, padx=10, pady=5)
        entry_user_dart.grid(row=last_row,column=1,padx=10, pady=5)
        last_row+=1
    else:
        label_user_dart.grid_forget()
        entry_user_dart.grid_forget()

    reposicionar_widgets_dinamicamente()

def reposicionar_widgets_dinamicamente():
    """Función para reposicionar widgets dinámicamente según `last_row`."""
    label_create.grid(row=last_row, column=0, padx=10, pady=5)
    create_date.grid(row=last_row, column=1, padx=10, pady=5)
    btn_save.grid(row=last_row + 1, column=0, columnspan=2, pady=5)
    label_status.grid(row=last_row + 2, column=0, columnspan=2, pady=6)

# Widgets posteriores que se reposicionan dinámicamente
label_roles = tk.Label(ventana, text="Roles Disponibles:")
label_create = tk.Label(ventana, text="Fecha de creación")
create_date = DateEntry(ventana, width=18, background="darkblue", foreground="white", borderwidth=2)
create_date.set_date(date.today())
btn_save = tk.Button(ventana, text="Guardar usuario", command=registrar_user)
label_status = tk.Label(ventana, text="", fg="green")

reposicionar_widgets_dinamicamente()

# Vinculación del evento
combo_plataforma.bind("<<ComboboxSelected>>", actualizar_roles)

ventana.mainloop()