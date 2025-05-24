import tkinter as tk
from tkinter import messagebox, scrolledtext
from cryptography.fernet import Fernet
import os

# ----------------- KEY HANDLING -----------------
def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)
    messagebox.showinfo("Success", "Key generated and saved as key.key")

def load_key():
    if not os.path.exists("key.key"):
        messagebox.showerror("Error", "Key not found! Please generate it first.")
        return None
    with open("key.key", "rb") as key_file:
        return key_file.read()

# -----------------FOR ENCRYPTION -----------------
def encrypt_message():
    key = load_key()
    if not key:
        return
    f = Fernet(key)
    message = input_text.get("1.0", tk.END).strip()
    if not message:
        messagebox.showwarning("Warning", "Input message is empty!")
        return
    encrypted = f.encrypt(message.encode())
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, encrypted.decode())
    output_text.config(state=tk.DISABLED)

# -----------------FOR DECRYPTION -----------------
def decrypt_message():
    key = load_key()
    if not key:
        return
    f = Fernet(key)
    encrypted_message = input_text.get("1.0", tk.END).strip()
    if not encrypted_message:
        messagebox.showwarning("Warning", "Encrypted message is empty!")
        return
    try:
        decrypted = f.decrypt(encrypted_message.encode())
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, decrypted.decode())
        output_text.config(state=tk.DISABLED)
    except Exception:
        messagebox.showerror("Error", "Invalid encrypted message or wrong key!")

# ----------------- GUI SETUP -----------------
root = tk.Tk()
root.title("Encryption-Decryption Tool")
root.geometry("700x500")
root.configure(bg="#f7f7f7")  # Light background

FONT_TITLE = ("Segoe UI", 14, "bold")
FONT_TEXT = ("Segoe UI", 11)
BTN_STYLE = {
    "font": ("Segoe UI", 11),
    "width": 16,
    "padx": 5,
    "pady": 5,
    "bg": "#74b9ff",
    "fg": "#2d3436"
}

# Title Label
tk.Label(root, text="Enter your message or encrypted text", font=FONT_TITLE, fg="#2d3436", bg="#f7f7f7").pack(pady=10)

# Input Text Area
input_text = scrolledtext.ScrolledText(root, width=70, height=6, font=FONT_TEXT, bg="white", fg="#2d3436", insertbackground="#2d3436")
input_text.pack(padx=20, pady=5)

# Buttons Frame
btn_frame = tk.Frame(root, bg="#f7f7f7")
btn_frame.pack(pady=15)

encrypt_btn = tk.Button(btn_frame, text="🔒 Encrypt", command=encrypt_message, **BTN_STYLE)
encrypt_btn.grid(row=0, column=0, padx=10)

decrypt_btn = tk.Button(btn_frame, text="🔓 Decrypt", command=decrypt_message, **BTN_STYLE)
decrypt_btn.grid(row=0, column=1, padx=10)

key_btn = tk.Button(btn_frame, text="🗝️ Generate Key", command=generate_key, **BTN_STYLE)
key_btn.grid(row=0, column=2, padx=10)

# Output Label
tk.Label(root, text="Output", font=FONT_TITLE, fg="#2d3436", bg="#f7f7f7").pack(pady=10)

# Output Text Area
output_text = scrolledtext.ScrolledText(root, width=70, height=6, font=FONT_TEXT, bg="white", fg="#2d3436", state=tk.DISABLED)
output_text.pack(padx=20, pady=5)

# Run App
root.mainloop()
