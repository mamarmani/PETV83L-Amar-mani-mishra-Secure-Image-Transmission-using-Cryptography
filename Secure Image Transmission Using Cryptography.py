import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
from cryptography.fernet import Fernet, InvalidToken
import io
import os

class ImageCryptoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🔐 Secure Image Transmission using Cryptography")
        self.root.configure(bg="#0f0f0f")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{int(screen_width*0.65)}x{int(screen_height*0.75)}")

        self.image_data = None
        self.image_path = None
        self.key = None
        self.image_visible = False
        self.decrypted_image_pil = None

        self.setup_gui()

    def setup_gui(self):
        tk.Label(self.root, text="🔐 SECURE IMAGE TRANSMISSION",
                 font=("Consolas", 20, "bold"), bg="#0f0f0f", fg="#00ff00", pady=15).pack(fill="x")

        main_frame = tk.Frame(self.root, bg="#0f0f0f")
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        button_frame = tk.Frame(main_frame, bg="#1f1f1f", padx=15, pady=15)
        button_frame.pack(side="left", fill="y")

        self.create_button(button_frame, "🖼️ Select Image", self.load_image)
        self.create_button(button_frame, "🔒 Encrypt Image", self.encrypt_image)
        self.create_button(button_frame, "📁 Select Encrypted File", self.load_encrypted_file)
        self.create_button(button_frame, "🔓 Decrypt Image", self.decrypt_image)

        display_wrapper = tk.Frame(main_frame, bg="#0f0f0f")
        display_wrapper.pack(side="right", expand=True, fill="both", padx=20)

        tk.Label(display_wrapper, text="📸 Image Preview", font=("Consolas", 14, "bold"),
                 bg="#0f0f0f", fg="#00ff00").pack(anchor="nw")

        self.display_frame = tk.Frame(display_wrapper, bg="#1a1a1a", width=500, height=500)
        self.display_frame.pack(pady=(10, 5), fill="both", expand=True)
        self.display_frame.pack_propagate(False)

        self.canvas = tk.Label(self.display_frame, bg="#1a1a1a")
        self.canvas.pack(expand=True)

        self.info_frame = tk.Frame(self.display_frame, bg="#1a1a1a")
        self.info_frame.pack(pady=10)

        self.file_row = tk.Frame(self.info_frame, bg="#1a1a1a")
        self.file_row.pack(anchor="center")
        self.file_row.pack_forget()

        self.file_label = tk.Label(self.file_row, text="", bg="#1a1a1a", fg="#00ff00",
                                   font=("Consolas", 10), wraplength=480, justify="center")
        self.file_label.pack()

        self.key_row = tk.Frame(self.info_frame, bg="#1a1a1a")
        self.key_row.pack(anchor="center")
        self.key_row.pack_forget()

        tk.Label(self.key_row, text="Encryption Key:", bg="#1a1a1a", fg="#00ff00",
                 font=("Consolas", 10, "bold")).pack(side="left")
        self.key_entry = tk.Entry(self.key_row, width=60, font=("Consolas", 10),
                                  fg="#00ff00", bg="#000000", insertbackground="#00ff00", borderwidth=1)
        self.key_entry.pack(side="left", padx=5)
        self.key_entry.config(state='readonly')

        tk.Button(self.key_row, text="📋 Copy", command=self.copy_key,
                  bg="#111111", fg="#00ff00", font=("Consolas", 9, "bold"),
                  activebackground="#00ff00", activeforeground="#000000",
                  relief="flat").pack(side="left")

        self.save_button = tk.Button(display_wrapper, text="💾 Save Decrypted Image",
                                     command=self.save_decrypted_image,
                                     font=("Consolas", 10, "bold"), bg="#111111", fg="#00ff00",
                                     width=30, activebackground="#00ff00", activeforeground="#000000")
        self.save_button.pack()
        self.save_button.pack_forget()

        tk.Label(self.root, text="👨‍💻 Amar Mani Mishra | Reg No: 12301362   ||   👨‍💻 Abhishek Gupta | Reg No: 12318144",
                 font=("Consolas", 10), bg="#0f0f0f", fg="#008000", pady=8).pack(fill="x", side="bottom")

    def create_button(self, parent, text, command):
        btn = tk.Button(parent, text=text, command=command, width=25, bg="#111111", fg="#00ff00",
                        font=("Consolas", 10, "bold"), pady=6, relief="flat", cursor="hand2",
                        activebackground="#00ff00", activeforeground="#000000")
        btn.pack(pady=10, fill="x")
        btn.bind("<Enter>", lambda e: btn.config(bg="#00aa00", fg="#000000"))
        btn.bind("<Leave>", lambda e: btn.config(bg="#111111", fg="#00ff00"))

    def copy_key(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.key_entry.get())
        self.root.update()
        self.key_row.pack_forget()

    def load_image(self):
        self.key_row.pack_forget()
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if path:
            self.image_path = path
            with open(path, "rb") as f:
                self.image_data = f.read()
            img = Image.open(path)
            img.thumbnail((480, 480))
            self.tk_image = ImageTk.PhotoImage(img)
            self.canvas.config(image=self.tk_image)
            self.image_visible = True
            self.save_button.pack_forget()
            self.key_entry.config(state='normal')
            self.key_entry.delete(0, tk.END)
            self.key_entry.config(state='readonly')
            self.file_label.config(text="")

    def encrypt_image(self):
        if not self.image_data:
            messagebox.showerror("Error", "No image loaded")
            return

        self.key = Fernet.generate_key()
        cipher = Fernet(self.key)
        encrypted_data = cipher.encrypt(self.image_data)
        self.image_data = encrypted_data

        base = os.path.splitext(self.image_path)[0] + "_encrypted"
        filename = base + ".bin"
        count = 1
        while os.path.exists(filename):
            filename = f"{base}_{count}.bin"
            count += 1

        with open(filename, "wb") as f:
            f.write(self.image_data)

        self.canvas.config(image='')
        self.tk_image = None
        self.image_visible = False
        self.save_button.pack_forget()

        self.file_label.config(text=f"Encrypted File: {filename}")
        self.file_row.pack(anchor="center")
        self.key_entry.config(state='normal')
        self.key_entry.delete(0, tk.END)
        self.key_entry.insert(0, self.key.decode())
        self.key_entry.config(state='readonly')
        self.key_row.pack(anchor="center")

    def decrypt_image(self):
        self.key_row.pack_forget()
        self.file_row.pack_forget()
        if not self.image_data:
            messagebox.showerror("Error", "No encrypted image loaded")
            return

        if self.image_visible:
            self.canvas.config(image='')
            self.tk_image = None
            self.image_visible = False
            self.save_button.pack_forget()
            return

        key = simpledialog.askstring("Input", "Enter the encryption key:")
        try:
            cipher = Fernet(key.encode())
            decrypted_data = cipher.decrypt(self.image_data)
            image = Image.open(io.BytesIO(decrypted_data))
            image.thumbnail((480, 480))
            self.tk_image = ImageTk.PhotoImage(image)
            self.canvas.config(image=self.tk_image)
            self.image_visible = True
            self.decrypted_image_pil = image
            self.save_button.pack()
        except (InvalidToken, Exception) as e:
            messagebox.showerror("Error", f"Decryption failed:\n{str(e)}")

    def load_encrypted_file(self):
        self.key_row.pack_forget()
        self.file_row.pack_forget()
        path = filedialog.askopenfilename(filetypes=[("Encrypted files", "*.bin")])
        if path:
            self.image_path = path
            with open(path, "rb") as f:
                self.image_data = f.read()
            self.tk_image = None
            self.canvas.config(image='', text="Encrypted file selected")
            self.file_label.config(text=f"Selected File: {path}")
            self.file_row.pack(anchor="center")
            self.image_visible = False
            self.decrypted_image_pil = None
            self.save_button.pack_forget()

    def save_decrypted_image(self):
        if not self.decrypted_image_pil:
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[
            ("PNG Image", "*.png"),
            ("JPEG Image", "*.jpg"),
            ("All Files", "*.*")
        ])
        if save_path:
            self.decrypted_image_pil.save(save_path)
            messagebox.showinfo("Saved", f"Decrypted image saved to:\n{save_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCryptoApp(root)
    root.mainloop()
