import tkinter as tk
from tkinter import messagebox
import json
import os

ARQUIVO = "agenda.json"

def carregar_agenda():
    if not os.path.exists(ARQUIVO):
        return []
    with open(ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_agenda(agenda):
    with open(ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(agenda, f, indent=4, ensure_ascii=False)

janela = tk.Tk()
janela.title("Agenda de Contatos")
janela.geometry("500x600")

tk.Label(janela, text="ID").pack()
entry_id = tk.Entry(janela)
entry_id.pack()

tk.Label(janela, text="Nome").pack()
entry_nome = tk.Entry(janela)
entry_nome.pack()

tk.Label(janela, text="Telefone").pack()
entry_telefone = tk.Entry(janela)
entry_telefone.pack()

tk.Label(janela, text="Email").pack()
entry_email = tk.Entry(janela)
entry_email.pack()

tk.Label(janela, text="Buscar por Nome").pack()
entry_busca = tk.Entry(janela)
entry_busca.pack()

lista = tk.Listbox(janela, width=70, height=15)
lista.pack(pady=10)

def cadastrarContato():
    agenda = carregar_agenda()
    id_contato = entry_id.get().strip()
    nome = entry_nome.get().strip()
    
    if not id_contato or not nome:
        messagebox.showerror("Erro", "ID e Nome são obrigatórios")
        return
    
    if any(c["id"] == id_contato for c in agenda):
        messagebox.showerror("Erro", "ID já existe. Escolha outro.")
        return
    
    contato = {
        "id": id_contato,
        "nome": nome,
        "telefone": entry_telefone.get().strip(),
        "email": entry_email.get().strip()
    }
    agenda.append(contato)
    salvar_agenda(agenda)
    messagebox.showinfo("Sucesso", "Contato cadastrado!")
    
    entry_id.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    listarContato()

def listarContato():
    lista.delete(0, tk.END)
    agenda = carregar_agenda()
    if not agenda:
        lista.insert(tk.END, "Nenhum contato cadastrado.")
        return
    for c in agenda:
        lista.insert(tk.END, f"ID: {c['id']} | Nome: {c['nome']} | Tel: {c['telefone']} | Email: {c['email']}")

def deletarContato():
    selecionado = lista.curselection()
    if not selecionado:
        messagebox.showerror("Erro", "Selecione um contato para deletar")
        return
    
    if not messagebox.askyesno("Confirmação", "Tem certeza que deseja deletar?"):
        return
    
    indice = selecionado[0]
    agenda = carregar_agenda()
    if indice < len(agenda):
        agenda.pop(indice)
        salvar_agenda(agenda)
        listarContato()
        messagebox.showinfo("Sucesso", "Contato deletado!")

def buscarContato():
    nome_busca = entry_busca.get().strip().lower()
    if not nome_busca:
        messagebox.showerror("Erro", "Digite um nome para buscar")
        return
    
    lista.delete(0, tk.END)
    agenda = carregar_agenda()
    encontrados = [c for c in agenda if nome_busca in c["nome"].lower()]
    
    if not encontrados:
        lista.insert(tk.END, "Nenhum contato encontrado.")
        return
    
    for c in encontrados:
        lista.insert(tk.END, f"ID: {c['id']} | Nome: {c['nome']} | Tel: {c['telefone']} | Email: {c['email']}")
    
    entry_busca.delete(0, tk.END)

tk.Button(janela, text="Cadastrar", command=cadastrarContato).pack(pady=5)
tk.Button(janela, text="Listar Todos", command=listarContato).pack(pady=5)
tk.Button(janela, text="Buscar", command=buscarContato).pack(pady=5)
tk.Button(janela, text="Deletar", command=deletarContato).pack(pady=5)
tk.Button(janela, text="Sair", command=janela.quit).pack(pady=5)

listarContato()

janela.mainloop()