import qr_code_creator
import tkinter as tk

def create_qr():
    link = url.get()
    name = qr_name.get()
    qr_code_creator.create_qrcode(str(link), str(name))
    lbl_result["text"] = "Imagen generada"
    

window = tk.Tk()
window.title("Generador QR Sindicato")
window.resizable(width=False, height=False)

frm_entry = tk.Frame(master=window)
url = tk.Entry(master=frm_entry, width=40)
lbl_url = tk.Label(master=frm_entry, text="Ingrese URL")
qr_name = tk.Entry(master=frm_entry, width=20)
lbl_name = tk.Label(master=frm_entry, text="Ingrese el nombre de la imagen")

url.grid(row=1, column=0)
lbl_url.grid(row=0, column=0)
lbl_name.grid(row=2, column=0)
qr_name.grid(row=3, column=0)

btn_generate = tk.Button(
    master=window,
    text = "Convertir",
    command=create_qr
)
lbl_result = tk.Label(master=window, text="")

frm_entry.grid(row=0, column=0, padx=10)
btn_generate.grid(row=4, column=0, pady=15)
lbl_result.grid(row=5, column=0, padx=15)

window.mainloop()