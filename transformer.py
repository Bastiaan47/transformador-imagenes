#hecho por Drakhnar
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import os
import threading
import sv_ttk 

class ModernConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cambiador de Formatos e img")
        self.root.geometry("800x550")
        sv_ttk.set_theme("dark")  
        self.files_to_convert = []
        self.output_folder = ""
        self.target_format = tk.StringVar(value="PNG")
        
        #UI 
        main_frame = ttk.Frame(root, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        lbl_title = ttk.Label(main_frame, text="Convertidor de Imágenes", font=("Segoe UI", 20, "bold"))
        lbl_title.pack(pady=(0, 20), anchor=tk.W)
        btn_files = ttk.Button(main_frame, text="Seleccionar Imágene(es)", command=self.select_files, style="Accent.TButton", width=25)
        btn_files.pack(anchor=tk.W, pady=5)
        self.lbl_files_count = ttk.Label(main_frame, text="No hay archivos seleccionados", foreground="gray")
        self.lbl_files_count.pack(anchor=tk.W, pady=(0, 10))
        lbl_format = ttk.Label(main_frame, text="Seleccionar formato de Salida:")
        lbl_format.pack(anchor=tk.W, pady=(10, 5))
        formats = ["PNG", "JPEG", "WEBP", "BMP", "TIFF", "ICO", "PDF", "GIF"]
        self.combo_format = ttk.Combobox(main_frame, textvariable=self.target_format, values=formats, state="readonly", width=18)
        self.combo_format.pack(anchor=tk.W)
        btn_convert = ttk.Button(main_frame, text="Convertir Ahora", command=self.start_conversion_thread, style="Accent.TButton", width=25)
        btn_convert.pack(anchor=tk.W, pady=20)
        self.progress = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress.pack(fill=tk.X, pady=10)
        self.lbl_status = ttk.Label(main_frame, text="...", font=("Segoe UI", 9))
        self.lbl_status.pack()

    def select_files(self):
        file_types = [
            ("Imágenes", "*.jpg *.jpeg *.png *.webp *.bmp *.tiff *.tif *.ico *.gif"),
            ("Todos los archivos", "*")
        ]
        
        files = filedialog.askopenfilenames(
            parent=self.root, 
            title="Seleccionar  imágenes", 
            filetypes=file_types
        )
        
        if files:
            self.files_to_convert = files
            self.lbl_files_count.config(text=f"✅ {len(files)} archivos cargados", foreground="#4cc9f0")

    def start_conversion_thread(self):
        if not self.files_to_convert:
            messagebox.showwarning("Faltan archivos", parent=self.root)
            return
        
        self.output_folder = filedialog.askdirectory(parent=self.root, title="Selecciona carpeta de destino")
        if not self.output_folder:
            return

        threading.Thread(target=self.convert_images).start()

    def convert_images(self):
        target_fmt = self.target_format.get().lower()
        pil_format = target_fmt
        if target_fmt == "jpg": pil_format = "jpeg"
        
        total = len(self.files_to_convert)
        self.progress["maximum"] = total
        success_count = 0
        
        self.lbl_status.config(text="transformando imagen(es)...")
        self.root.update_idletasks()
        
        for index, file_path in enumerate(self.files_to_convert):
            try:
                filename = os.path.basename(file_path)
                name_only = os.path.splitext(filename)[0]
                save_path = os.path.join(self.output_folder, f"{name_only}.{target_fmt}")
                
                with Image.open(file_path) as img:

                    if pil_format in ["jpeg", "bmp"] and img.mode in ("RGBA", "LA"):
                        background = Image.new("RGB", img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[-1])
                        img = background
                    elif pil_format != "jpeg" and img.mode == "P":
                         img = img.convert("RGBA")


                    if pil_format == "jpeg":
                        img.save(save_path, format="JPEG", quality=100, subsampling=0, optimize=True)
                    elif pil_format == "webp":
                        img.save(save_path, format="WEBP", quality=100, lossless=True, method=6)
                    elif pil_format == "png":
                        img.save(save_path, format="PNG", optimize=True)
                    elif pil_format == "ico":
                        if img.size[0] > 256 or img.size[1] > 256:
                            img.thumbnail((256, 256))
                        img.save(save_path, format="ICO")
                    else:
                        img.save(save_path, format=pil_format.upper())

                success_count += 1
                
            except Exception as e:
                print(f"Error con {filename}: {e}")
            
            self.progress["value"] = index + 1
            self.lbl_status.config(text=f"Convirtiendo {index+1} de {total}...")
            self.root.update_idletasks()

        self.lbl_status.config(text="¡Proceso Terminado!")
        messagebox.showinfo("Éxito", f"Se completó la conversión.\n{success_count} imágenes guardadas en:\n{self.output_folder}", parent=self.root)
        self.progress["value"] = 0
        self.files_to_convert = []
        self.lbl_files_count.config(text="No hay archivos seleccionados", foreground="gray")

if __name__ == "__main__":
    root = tk.Tk()

    try:
        root.tk.call('tk', 'scaling', 1.5) 
    except:
        pass
        
    app = ModernConverterApp(root)
    root.mainloop()