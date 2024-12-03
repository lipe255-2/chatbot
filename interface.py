import tkinter as tk
from tkinter import scrolledtext, Frame
import threading
from crewai import Task, Crew
from agentes import identificador, juridico, tecnico, supervisor
from tarefas import identificacao, solucao_tecnica, solucao_juridica, supervisar

# Inicializa a estrutura de agentes e tarefas
crew = Crew(
    agents=[identificador, tecnico, juridico, supervisor],
    tasks=[identificacao, solucao_tecnica, solucao_juridica, supervisar],
    verbose=2
)

# Função para enviar mensagem
def send_message():
    user_message = user_input.get().strip()
    if user_message:
        display_message("Você", user_message, is_user=True)
        user_input.delete(0, tk.END)
        chat_frame.update_idletasks()

        # Feedback visual enquanto a resposta é gerada
        display_message("IA", "Gerando resposta...", is_user=False)

        # Thread para evitar travar a interface
        threading.Thread(target=get_ia_response, args=(user_message,)).start()

def get_ia_response(user_message):
    bot_response = crew.kickoff(inputs={"problema": user_message})
    display_message("IA", bot_response, is_user=False)

def display_message(sender, message, is_user=False):
    bubble = Frame(chat_frame, bg="#4CAF50" if is_user else "#f0f0f0", pady=5, padx=10, bd=5)
    bubble.pack(anchor="e" if is_user else "w", pady=5, padx=10, fill="x")
    label = tk.Label(
        bubble,
        text=f"{sender}: {message}",
        bg=bubble["bg"],
        fg="white" if is_user else "black",
        font=("Arial", 12),
        wraplength=400,
        justify="left"
    )
    label.pack(fill="x")

    # Faz o scroll automático para a última mensagem
    chat_canvas.yview_moveto(1)

def clear_chat():
    for widget in chat_frame.winfo_children():
        widget.destroy()

# Criação da janela principal
window = tk.Tk()
window.title("Chat com IA - Estilo de Cartões")
window.geometry("500x650")
window.config(bg="#333333")

# Cabeçalho
header = tk.Label(
    window, text="Conversa com IA", bg="#282828", fg="#ffffff",
    font=("Helvetica", 18, "bold"), pady=10
)
header.pack(fill=tk.X)

# Área de chat com rolagem
chat_canvas = tk.Canvas(window, bg="#333333", bd=0, highlightthickness=0)
chat_frame = tk.Frame(chat_canvas, bg="#333333")
scrollbar = tk.Scrollbar(window, orient="vertical", command=chat_canvas.yview)
chat_canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
chat_canvas.pack(fill="both", expand=True)
chat_canvas.create_window((0, 0), window=chat_frame, anchor="nw")

chat_frame.bind("<Configure>", lambda e: chat_canvas.configure(scrollregion=chat_canvas.bbox("all")))

# Caixa de entrada e botões
bottom_bar = tk.Frame(window, bg="#282828", pady=10)
bottom_bar.pack(fill=tk.X, side="bottom")

user_input = tk.Entry(bottom_bar, font=("Arial", 14), bg="#444444", fg="white", insertbackground="white", relief="flat")
user_input.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=5)

send_button = tk.Button(
    bottom_bar, text="Enviar", command=send_message, bg="#4CAF50",
    fg="white", font=("Arial", 12, "bold"), relief="flat", cursor="hand2"
)
send_button.pack(side="left", padx=(0, 5))

clear_button = tk.Button(
    bottom_bar, text="Limpar", command=clear_chat, bg="#f44336",
    fg="white", font=("Arial", 12, "bold"), relief="flat", cursor="hand2"
)
clear_button.pack(side="left", padx=(0, 10))

# Evento de teclado para enviar com "Enter"
window.bind("<Return>", lambda event: send_message())

# Loop principal
window.mainloop()