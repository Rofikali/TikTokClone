import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from io import BytesIO

# Pillow >= 10.0 fix
from PIL import Image
RESAMPLE = Image.Resampling.LANCZOS

class ImageResizer:
    def __init__(self, path):
        self.path = path
        self.image = Image.open(path)
        self.filename = os.path.basename(path)

    def resize(self, width=None, height=None):
        if width and height:
            self.image = self.image.resize((int(width), int(height)), RESAMPLE)

    def compress_to_size(self, target_size_bytes, output_path):
        format = self.image.format or 'JPEG'
        quality = 95
        step = 5

        while True:
            buffer = BytesIO()
            self.image.save(buffer, format=format, quality=quality)
            size = buffer.tell()

            if size <= target_size_bytes or quality <= 10:
                with open(output_path, 'wb') as f:
                    f.write(buffer.getvalue())
                return size
            quality -= step

class ResizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Batch Image Resizer & Compressor")
        self.geometry("600x500")
        self.resizers = []
        self.preview_image = None
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self)
        frame.pack(pady=10)

        tk.Button(frame, text="Select Images", command=self.load_images).grid(row=0, column=0, padx=5)
        self.file_listbox = tk.Listbox(self, width=70, height=5)
        self.file_listbox.pack()

        self.canvas = tk.Canvas(self, width=200, height=150, bg='white')
        self.canvas.pack(pady=5)

        tk.Label(self, text="Target Size:").pack()
        self.size_entry = tk.Entry(self)
        self.size_entry.pack()

        self.unit_var = tk.StringVar(value='KB')
        tk.OptionMenu(self, self.unit_var, 'Bytes', 'KB', 'MB').pack(pady=5)

        tk.Label(self, text="Width (px):").pack()
        self.width_entry = tk.Entry(self)
        self.width_entry.pack()

        tk.Label(self, text="Height (px):").pack()
        self.height_entry = tk.Entry(self)
        self.height_entry.pack()

        tk.Button(self, text="Resize and Save All", command=self.process_all).pack(pady=15)

        self.progress = ttk.Progressbar(self, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=5)

    def load_images(self):
        paths = filedialog.askopenfilenames(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
        if paths:
            self.resizers = [ImageResizer(path) for path in paths]
            self.file_listbox.delete(0, tk.END)
            for r in self.resizers:
                self.file_listbox.insert(tk.END, r.filename)
            self.preview_first_image()

    def preview_first_image(self):
        if self.resizers:
            img = self.resizers[0].image.copy()
            img.thumbnail((200, 150))
            self.preview_image = ImageTk.PhotoImage(img)
            self.canvas.create_image(100, 75, image=self.preview_image)

    def process_all(self):
        if not self.resizers:
            messagebox.showwarning("No Images", "Please load images first.")
            return

        try:
            width = int(self.width_entry.get()) if self.width_entry.get() else None
            height = int(self.height_entry.get()) if self.height_entry.get() else None
            size = float(self.size_entry.get())
            unit = self.unit_var.get()

            if unit == 'KB':
                target_size = int(size * 1024)
            elif unit == 'MB':
                target_size = int(size * 1024 * 1024)
            else:
                target_size = int(size)

            save_dir = filedialog.askdirectory()
            if not save_dir:
                return

            self.progress["maximum"] = len(self.resizers)
            self.progress["value"] = 0

            for i, resizer in enumerate(self.resizers):
                resizer.resize(width, height)
                output_path = os.path.join(save_dir, f"resized_{resizer.filename}")
                resizer.compress_to_size(target_size, output_path)
                self.progress["value"] = i + 1
                self.update_idletasks()

            messagebox.showinfo("Done", f"All images processed and saved to:\n{save_dir}")

        except Exception as e:
            messagebox.showerror("Error", str(e))

# Optional drag-and-drop support
try:
    from tkinterdnd2 import TkinterDnD, DND_FILES

    class DragDropApp(ResizerApp, TkinterDnD.Tk):
        def __init__(self):
            TkinterDnD.Tk.__init__(self)
            ResizerApp.__init__(self)
            self.drop_target_register(DND_FILES)
            self.dnd_bind('<<Drop>>', self.drop_files)

        def drop_files(self, event):
            files = self.tk.splitlist(event.data)
            self.resizers = [ImageResizer(f) for f in files]
            self.file_listbox.delete(0, tk.END)
            for r in self.resizers:
                self.file_listbox.insert(tk.END, r.filename)
            self.preview_first_image()

    app = DragDropApp()

except ImportError:
    print("Drag-and-drop not available. Install with: pip install tkinterdnd2")
    app = ResizerApp()

app.mainloop()
