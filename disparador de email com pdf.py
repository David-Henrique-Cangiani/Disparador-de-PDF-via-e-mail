import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import smtplib
import unicodedata
from email.message import EmailMessage

# =======================
# Config SMTP
# =======================
SMTP_SERVER = "smtp.seudominio.com"
SMTP_PORT = 587

# Flag / credenciais armazenadas após login bem-sucedido
cred_valid = False
smtp_credentials = {"email": "", "senha": ""}

# =======================
# Funções auxiliares
# =======================
def normalizar_nome(nome):
    """Remove acentos e caracteres especiais, troca espaços por pontos"""
    nome = unicodedata.normalize('NFD', nome)
    nome = nome.encode('ascii', 'ignore').decode('utf-8')
    nome = re.sub(r'[^a-zA-Z\s]', '', nome)
    nome = nome.lower().strip().replace(" ", ".")
    return nome

def obter_email(nome_arquivo):
    """
    Gera um e-mail genérico a partir do nome do arquivo:

    - Usa apenas o primeiro nome do arquivo, ignorando números ou extensão.
    - Pode gerar endereços fixos caso definidos em emails_fixos (opcional).
    - Caso contrário, gera e-mail genérico baseado no nome do arquivo.
    """
    nome = nome_arquivo.lower()
    # Remove extensão
    base = os.path.splitext(nome_arquivo)[0]
    # Remove números iniciais e caracteres especiais
    base = re.sub(r'^\d+[_\-\s]*', '', base)
    # Pega apenas o primeiro nome
    primeiro_nome = base.split('_')[0]
    # Normaliza para formato e-mail
    return f"{normalizar_nome(primeiro_nome)}@seudominio.com"

# =======================
# Funções de login e envio
# =======================
def check_login(show_success=True):
    """Tenta autenticar no SMTP"""
    global cred_valid, smtp_credentials

    email = email_entry.get().strip()
    senha = senha_entry.get()

    if not email or not senha:
        messagebox.showwarning("Atenção", "Preencha e-mail e senha antes de conectar.")
        return False

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(email, senha)

        cred_valid = True
        smtp_credentials["email"] = email
        smtp_credentials["senha"] = senha
        email_entry.config(state='disabled')
        senha_entry.config(state='disabled')
        login_btn.config(state='disabled')

        if show_success:
            messagebox.showinfo("Conectado", "Login bem-sucedido. Você pode enviar e-mails agora.")

        tela_principal()
        return True
    except smtplib.SMTPAuthenticationError:
        cred_valid = False
        messagebox.showerror("Erro de autenticação", "E-mail ou senha inválidos.")
        return False
    except Exception as e:
        cred_valid = False
        messagebox.showerror("Erro de conexão", f"Não foi possível conectar:\n{e}")
        return False

def enviar_emails(sender_email, senha, arquivos_emails, assunto, corpo):
    """Envia os arquivos PDF por e-mail."""
    global cred_valid, smtp_credentials
    if not sender_email or not senha:
        messagebox.showwarning("Atenção", "Informe e-mail e senha antes de enviar.")
        return
    if (not cred_valid) or (smtp_credentials.get("email") != sender_email) or (smtp_credentials.get("senha") != senha):
        ok = check_login(show_success=False)
        if not ok:
            return

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(sender_email, senha)

            for arquivo, destinatario in arquivos_emails.items():
                if not destinatario:
                    log_area.insert(tk.END, f"⚠️ Sem e-mail encontrado para: {os.path.basename(arquivo)}\n")
                    log_area.see(tk.END)
                    continue

                msg = EmailMessage()
                msg['From'] = sender_email
                msg['To'] = destinatario
                msg['Subject'] = assunto
                msg.set_content(corpo)

                with open(arquivo, 'rb') as f:
                    pdf_data = f.read()
                msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename=os.path.basename(arquivo))

                server.send_message(msg)
                log_area.insert(tk.END, f"✅ Enviado: {os.path.basename(arquivo)} → {destinatario}\n")
                log_area.see(tk.END)

        messagebox.showinfo("Sucesso", "Todos os e-mails foram enviados!")

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro durante o envio: {str(e)}")

# =======================
# Interface Tkinter
# =======================
def selecionar_pasta():
    folder = filedialog.askdirectory(title="Selecione a pasta dos PDFs")
    if folder:
        pasta_var.set(folder)
        listar_pdfs(folder)

def listar_pdfs(folder):
    arquivos = [f for f in os.listdir(folder) if f.lower().endswith('.pdf')]
    arquivos_emails.clear()
    log_area.delete('1.0', tk.END)
    for arquivo in arquivos:
        email = obter_email(arquivo)
        arquivos_emails[os.path.join(folder, arquivo)] = email
        log_area.insert(tk.END, f"{arquivo} → {email if email else '⚠️ Não encontrado'}\n")
    log_area.see(tk.END)

def tela_principal():
    login_frame.pack_forget()
    main_frame.pack(fill='both', expand=True)

# =======================
root = tk.Tk()
root.title("Envio de PDFs por E-mail")

root.state('zoomed')
root.configure(bg="#E8F0FE")

arquivos_emails = {}

# Frame de login
login_frame = tk.Frame(root, bg="#E8F0FE")
login_frame.pack(fill='both', expand=True)

tk.Label(login_frame, text="E-mail de envio:", bg="#E8F0FE", fg="#0B3D91", font=("Arial", 14)).pack(pady=(50,5))
email_entry = tk.Entry(login_frame, font=("Arial", 14), width=30)
email_entry.pack(pady=5)

tk.Label(login_frame, text="Senha:", bg="#E8F0FE", fg="#0B3D91", font=("Arial", 14)).pack(pady=5)
senha_entry = tk.Entry(login_frame, font=("Arial", 14), width=30, show="*")
senha_entry.pack(pady=5)

login_btn = tk.Button(login_frame, text="Conectar", font=("Arial", 14), bg="#0B3D91", fg="white", relief="flat", command=check_login)
login_btn.pack(pady=20, ipadx=10, ipady=5)

# Frame principal
main_frame = tk.Frame(root, bg="#E8F0FE")

tk.Label(main_frame, text="Selecione a pasta com os PDFs", bg="#E8F0FE", fg="#0B3D91", font=("Arial", 14)).pack(pady=10)
pasta_var = tk.StringVar()
tk.Button(main_frame, text="Selecionar pasta", font=("Arial", 14), bg="#0B3D91", fg="white", relief="flat", command=selecionar_pasta).pack(pady=5, ipadx=10, ipady=5)

tk.Label(main_frame, text="Pré-visualização dos arquivos e e-mails", bg="#E8F0FE", fg="#0B3D91", font=("Arial", 14)).pack(pady=10)
log_area = scrolledtext.ScrolledText(main_frame, width=100, height=20, font=("Arial", 12), wrap='word')
log_area.pack(fill='both', expand=True, padx=10, pady=10)

tk.Label(main_frame, text="Assunto:", bg="#E8F0FE", fg="#0B3D91", font=("Arial", 14)).pack(pady=5)
assunto_entry = tk.Entry(main_frame, width=60, font=("Arial", 14))
assunto_entry.pack(pady=5)

tk.Label(main_frame, text="Corpo da mensagem:", bg="#E8F0FE", fg="#0B3D91", font=("Arial", 14)).pack(pady=5)
mensagem_text = tk.Text(main_frame, width=60, height=6, font=("Arial", 12), wrap='word')
mensagem_text.pack(fill='both', expand=True, padx=10, pady=10)

enviar_btn = tk.Button(main_frame, text="Enviar e-mails", font=("Arial", 14), bg="#0B3D91", fg="white", relief="flat",
                       command=lambda: enviar_emails(email_entry.get(), senha_entry.get(), arquivos_emails,
                                                    assunto_entry.get(), mensagem_text.get("1.0", tk.END)))
enviar_btn.pack(side='bottom', pady=20, ipadx=10, ipady=5)

root.mainloop()
