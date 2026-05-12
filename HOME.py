import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import psycopg2
from psycopg2 import Error

from db import init_pool
from db import get_conn

import textwrap
from datetime import datetime



#CHAMAR A CONEXÃO COM O BANCO DE DADOS ---------------------------
init_pool()

def select_pedido():
    try:
        listapedidos = "SELECT id_pedido,nome_cliente,status_pedido,descricao_pedido, TO_CHAR(prazo_entrega, 'DD/MM/YYYY') AS prazo_entrega FROM pedido INNER JOIN cliente ON pedido.id_cliente = cliente.id_cliente " \
        "WHERE status_pedido IN ('Em produção','aguardando aceitação') ORDER BY CASE WHEN status_pedido='Em produção' THEN 1 WHEN status_pedido='aguardando aceitação' THEN 2 ELSE 3 END, prazo_entrega ASC;"
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(listapedidos)
                pedidos = cur.fetchall()

                numlinhas=0
                for pedido in pedidos:
                    numlinhas=numlinhas+1
                    tag = 'linhapar' if numlinhas%2==0 else 'linhaimpar'
                    treehome.insert("","end", values=pedido, tags=(tag))
                return pedido
    
    except Exception as e:
        print("Erro na função select_pedido:", e)


def atualizarhome():

    for item in treehome.get_children():
        treehome.delete(item)

    select_pedido()



#----------------------------------------------     D E L E T E        -------------------------------------
# DELETE PEDIDO ----------------         -------------------------

def deletar_pedido():
    selecionado = treehome.focus()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione um pedido para deletar")
        return

    ondedeletar = treehome.item(selecionado, 'values')
    id_pedido_delete = ondedeletar[0]
    confirm = messagebox.askyesno("Confirmação", f"Deletar o pedido {ondedeletar[0]} de {ondedeletar[1]}?")
    if not confirm:
        return
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM pedido WHERE id_pedido = %s", (id_pedido_delete, ))
        conn.commit()

    messagebox.showinfo("Sucesso", "Pedido deletado com sucesso!")
    atualizarhome()


# DELETE CLIENTE      --------------------          ----------------



# DELETE FORNECEDOR --------------- -------      --------------   ---------------





#CRIANDO HOME PAGE -----------------------------------------------
home=tk.Tk()
home.title("ORDENS DE SERVIÇO")
home.geometry("900x618")

style=ttk.Style()
style.configure("Treeview", rowheight=59)


#---------------------------------- TREE HOME

treehome=ttk.Treeview(home, selectmode='browse', column=('id_pedido','cliente','status_pedido','descricao_pedido','prazo_entrega'), show='headings')

treehome.column("id_pedido", width=5, minwidth=5)
treehome.heading("#1", text="Codigo")

treehome.column("cliente", width=150, minwidth=50)
treehome.heading("#2", text="Cliente")

treehome.column("status_pedido", width=60, minwidth=60)
treehome.heading("#3", text="Situação")
treehome.tag_configure('data_atrasada', foreground='red')

treehome.column("descricao_pedido", width=300, minwidth=50)
treehome.heading("#4", text="Descrição")

treehome.column("prazo_entrega", width=50, minwidth=50)
treehome.heading("#5", text="Prazo de entrega")

'''scrollbar = ttk.Scrollbar(treehome, orient=tk.VERTICAL, command=treehome.yview)
treehome.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side='right')'''

treehome.pack(fill="both", expand=True)



menu_clique_direito = tk.Menu(treehome, tearoff=0)
menu_clique_direito.add_command(label="Atualizar", command=atualizarhome)
menu_clique_direito.add_separator()
menu_clique_direito.add_command(label="Deletar", command=deletar_pedido)





def set_confirmado():
    selecionado = treehome.focus()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione um pedido para atualizar")
        return

    ondealterar = treehome.item(selecionado, 'values')
    id_do_pedido = ondealterar[0]
    confirm = messagebox.askyesno("Confirmação", f"Alterar o pedido {ondealterar[0]} de {ondealterar[1]}?")
    if not confirm:
         return
    
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE pedido SET status_pedido = 'Em produção' WHERE id_pedido = %s ", (id_do_pedido, ))

        conn.commit()
    atualizarhome()

def set_finalizado():
    selecionado = treehome.focus()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione um pedido para atualizar")
        return

    ondealterar = treehome.item(selecionado, 'values')
    id_do_pedido = ondealterar[0]
    confirm = messagebox.askyesno("Confirmação", f"Alterar o pedido {ondealterar[0]} de {ondealterar[1]}?")
    if not confirm:
         return
    
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE pedido SET status_pedido = 'Finalizado' WHERE id_pedido = %s ", (id_do_pedido, ))

        conn.commit()
    atualizarhome()

def set_aguardando():
    selecionado = treehome.focus()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione um pedido para atualizar")
        return

    ondealterar = treehome.item(selecionado, 'values')
    id_do_pedido = ondealterar[0]
    confirm = messagebox.askyesno("Confirmação", f"Alterar o pedido {ondealterar[0]} de {ondealterar[1]}?")
    if not confirm:
         return
    
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE pedido SET status_pedido = 'aguardando aceitação' WHERE id_pedido = %s ", (id_do_pedido, ))

        conn.commit()
    atualizarhome()

def set_cancelado():
    selecionado = treehome.focus()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione um pedido para atualizar")
        return

    ondealterar = treehome.item(selecionado, 'values')
    id_do_pedido = ondealterar[0]
    confirm = messagebox.askyesno("Confirmação", f"Alterar o pedido {ondealterar[0]} de {ondealterar[1]}?")
    if not confirm:
         return
    
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE pedido SET status_pedido = 'Cancelado' WHERE id_pedido = %s ", (id_do_pedido, ))

        conn.commit()
    atualizarhome()

menu_alterar_situacao = tk.Menu(menu_clique_direito, tearoff=0)
menu_alterar_situacao.add_command(label="Finalizado", command=set_finalizado)
menu_alterar_situacao.add_command(label="Em produção", command=set_confirmado)
menu_alterar_situacao.add_command(label="Aguardando confirmação", command=set_aguardando)
menu_alterar_situacao.add_command(label="Cancelado", command=set_cancelado)

menu_clique_direito.add_cascade(label="Alterar situação", menu=menu_alterar_situacao)




atualizarhome()
def mostrar_menu(event):
    menu_clique_direito.tk_popup(event.x_root, event.y_root)
home.bind("<Button-3>", mostrar_menu)

                #IMPRIMINDO AS ORDENS DE SERVIÇO NA TABELA DA JANELA HOME -------------------------

treehome.tag_configure('linhapar', background='#e0e0e0')
treehome.tag_configure('linhaimpar', background="#9c9c9c")



# MENU DE DETALHES DO PEDIDO -------------------

def mostrar_detalhes():
    selecionado = treehome.focus()
    if not selecionado:
        return

    id_pedido = treehome.item(selecionado, 'values')[0]

    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM pedido WHERE id_pedido = %s", (id_pedido,))
                dados = cur.fetchone()
                colunas = [desc[0] for desc in cur.description]
    except Exception as e:
        print("Erro ao buscar detalhes:", e)
        return

    detalhes_janela = tk.Toplevel()
    detalhes_janela.title(f"Detalhes do Pedido {id_pedido}")

    for i, (col, valor) in enumerate(zip(colunas, dados)):
        tk.Label(detalhes_janela, text=f"{col}:", font=("Arial", 10, "bold")).grid(row=i, column=0, sticky="w", padx=5, pady=2)
        tk.Label(detalhes_janela, text=f"{valor}", font=("Arial", 10)).grid(row=i, column=1, sticky="w", padx=5, pady=2)

menu_clique_direito.add_separator()
menu_clique_direito.add_command(label="Detalhes", command=mostrar_detalhes)
#FUNÇÕES DO PROGRAMA ---------------------------------------------
                                             #CADASTRO DE CLIENTES
def novocliente():

    janelanovocliente=tk.Toplevel(home)
    janelanovocliente.title("Cadastro de cliente")
    janelanovocliente.geometry("340x350")

    frame_form = tk.Frame(janelanovocliente)
    frame_form.grid(row=4, column=0, pady=10)

    label_nome = tk.Label(frame_form, text="Nome:")
    label_nome.grid(row=0, column=0, padx=5, pady=5)
    campo_nome = tk.Entry(frame_form, width=30)
    campo_nome.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

    label_email = tk.Label(frame_form, text="Email:")
    label_email.grid(row=1, column=0, padx=5, pady=5)
    campo_email = tk.Entry(frame_form, width=30)
    campo_email.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

    label_whatsapp = tk.Label(frame_form, text="Whatsapp:")
    label_whatsapp.grid(row=2, column=0, padx=5, pady=5)
    campo_whatsapp = tk.Entry(frame_form, width=30)
    campo_whatsapp.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

    label_telefone = tk.Label(frame_form, text="Telefone:")
    label_telefone.grid(row=3, column=0, padx=5, pady=5)
    campo_telefone = tk.Entry(frame_form, width=30)
    campo_telefone.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

    label_CPF = tk.Label(frame_form, text="CPF:")
    label_CPF.grid(row=4, column=0, padx=5, pady=5)
    campo_CPF = tk.Entry(frame_form, width=30)
    campo_CPF.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")    

    label_CNPJ = tk.Label(frame_form, text="CNPJ:")
    label_CNPJ.grid(row=5, column=0, padx=5, pady=5)
    campo_CNPJ = tk.Entry(frame_form, width=30)
    campo_CNPJ.grid(row=5, column=1, padx=5, pady=5, sticky="nsew")

    
    frame_radio = tk.Frame(janelanovocliente)
    frame_radio.grid(row=6, column=0, pady=0)

    opcao_sexo = tk.StringVar(value="M")
    label_sexo = tk.Label(frame_radio, text="Sexo:")
    label_sexo.grid(row=6, column=0, padx=0, pady=0, sticky="w")
    tk.Radiobutton(frame_radio, text="M", value="M", variable=opcao_sexo).grid(row=6, column=1, padx=0, pady=0, sticky="w")
    tk.Radiobutton(frame_radio, text="F", value="F", variable=opcao_sexo).grid(row=6, column=2, padx=0, pady=0, sticky="w")
    tk.Radiobutton(frame_radio, text="N/A", value="O", variable=opcao_sexo).grid(row=6, column=3, padx=0, pady=0, sticky="w")

    label_endereco = tk.Label(frame_form, text="Endereço:")
    label_endereco.grid(row=7, column=0, padx=5, pady=5)
    campo_endereco = tk.Text(frame_form, width=30, height=3)
    campo_endereco.grid(row=7, column=1, padx=5, pady=1)



    def insertcliente():

        try:

            get_maior_id_cliente = "SELECT MAX(id_cliente) AS maior_id_cliente FROM cliente"
            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(get_maior_id_cliente)
                    maior_id_cliente = cur.fetchone()[0] or 0
                    id_novo_cliente = int(maior_id_cliente)+1

                    cpf = campo_CPF.get().strip() or None
                    cnpj = campo_CNPJ.get().strip() or None
                    email = campo_email.get().strip() or None
                    endereco = campo_endereco.get("1.0", "end-1c") or None
                    telefone = campo_telefone.get().strip() or None

                    dadosdoinsertcliente=[id_novo_cliente, campo_nome.get(), telefone, email, campo_whatsapp.get(), opcao_sexo.get(), cpf, cnpj, endereco ]
                    print(dadosdoinsertcliente)
                    insertnovocliente = "INSERT INTO cliente (id_cliente, nome_cliente, fone_cliente, email_cliente, whats_cliente, sexo_cliente, cpf_cliente, cnpj_cliente, end_cliente) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cur.execute(insertnovocliente,tuple(dadosdoinsertcliente))

                    conn.commit()
                    messagebox.showinfo("Feito!",f"Cliente inserido com sucesso")
                    janelanovocliente.destroy()


        except Exception as e:
            messagebox.showerror("Algo deu errado",f"verifique os dados")
        

  
            
    frame_botoes = tk.Frame(janelanovocliente)
    frame_botoes.grid(row=7, column=0, pady=10)

    botaook = tk.Button(frame_botoes, text="OK", width=8, height=1, command=insertcliente)
    botaook.grid(row=0, column=0, padx=10, pady=0, sticky='w')

    botaocancelar = tk.Button(frame_botoes, text="Cancelar", width=8, height=1, command=janelanovocliente.destroy)
    botaocancelar.grid(row=0, column=1, padx=10, pady=0, sticky='e')


    janelanovocliente.mainloop()

                                             #CADASTRO DE FORNECEDORES
def novofornecedor():

    janelanovofornecedor=tk.Toplevel(home)
    janelanovofornecedor.title("Cadastro de fornecedor")
    janelanovofornecedor.geometry("350x280")
    
    frame_form = tk.Frame(janelanovofornecedor)
    frame_form.pack(padx=10, pady=10, fill='both', expand=True)

    label_cnpj = tk.Label(frame_form, text="CNPJ:")
    label_cnpj.grid(row=0, column=0, padx=5, pady=5)
    campo_cnpj = tk.Entry(frame_form, width=30)
    campo_cnpj.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

    label_nome = tk.Label(frame_form, text="Nome:")
    label_nome.grid(row=1, column=0, padx=5, pady=5)
    campo_nome = tk.Entry(frame_form, width=30)
    campo_nome.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

    label_email = tk.Label(frame_form, text="Email:")
    label_email.grid(row=2, column=0, padx=5, pady=5)
    campo_email = tk.Entry(frame_form, width=30)
    campo_email.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

    label_tipo = tk.Label(frame_form, text="Tipo:")
    label_tipo.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")
    opcoes_fornecedortipo=["Tecidos","Madeira","Serviços","Couro","Tintas"]
    fornecedor_tipo=ttk.Combobox(frame_form,values=opcoes_fornecedortipo)
    fornecedor_tipo.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

    label_telefone = tk.Label(frame_form, text="Telefone:")
    label_telefone.grid(row=4, column=0, padx=5, pady=5)
    campo_telefone = tk.Entry(frame_form, width=30)
    campo_telefone.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")

    label_endereco = tk.Label(frame_form, text="Endereço:")
    label_endereco.grid(row=5, column=0, padx=5, pady=5)
    campo_endereco = tk.Text(frame_form, width=30, height=3)
    campo_endereco.grid(row=5, column=1, padx=5, pady=1)

    def insertfornecedor():
        
        try:

            get_maior_id_fornecedor = "SELECT MAX(id_forn) AS maior_id_fornecedor FROM fornecedor;"
            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(get_maior_id_fornecedor)

                    maior_id_fornecedor = cur.fetchone()[0] or 0
                    id_novo_fornecedor = int(maior_id_fornecedor)+1

                    email = campo_email.get().strip() or None
                    endereco = campo_endereco.get("1.0", "end-1c") or None

                    dadosdoinsertfornecedor=[id_novo_fornecedor, campo_cnpj.get(), campo_nome.get(), fornecedor_tipo.get(), email, campo_telefone.get(), endereco]
                
                    insertnovofornecedor = "INSERT INTO fornecedor (id_forn, cnpj_forn, nome_forn, tipo_forn, email_forn, fone_forn, end_forn) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                    cur.execute(insertnovofornecedor,tuple(dadosdoinsertfornecedor))

                    conn.commit()
                    messagebox.showinfo("Feito!",f"Fornecedor inserido com sucesso")
                    janelanovofornecedor.destroy()

        except Exception as e:
            messagebox.showerror("Algo deu errado",f"verifique os dados")
            janelanovofornecedor.mainloop()
    

    frame_botoes = tk.Frame(janelanovofornecedor)
    frame_botoes.pack(pady=1)

    botaocancelar = tk.Button(frame_botoes, text="Cancelar", width=8, command=janelanovofornecedor.destroy)
    botaocancelar.grid(row=6, column=0, padx=5, pady=3, sticky="w")

    botaook = tk.Button(frame_botoes, text="OK", width=15, command=insertfornecedor)
    botaook.grid(row=6, column=1, padx=5, pady=3, sticky="e")





                                             #CADASTRO DE ORÇAMENTO ----------- NOVOS PEDIDOS
listadeclientesdofiltro=[] 
def novoorcamento():    

    janelanovopedido=tk.Toplevel(home)
    janelanovopedido.title("Cadastro de pedidos")
    janelanovopedido.geometry("370x270")
 
    label_tipo_cliente = tk.Label(janelanovopedido, text="Tipo de cliente:")
    label_tipo_cliente.grid(row=0, column=0, padx=5, pady=5)
    opcoes_cliente_tipo=["CPF","CNPJ"]
    cliente_tipo=ttk.Combobox(janelanovopedido,values = opcoes_cliente_tipo)
    cliente_tipo.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
    cliente_tipo.current(0)
  
    label_cliente = tk.Label(janelanovopedido, text="Cliente:")
    label_cliente.grid(row=1, column=0, padx=5, pady=5)
    opcoes_cliente=tk.StringVar()
    cliente=ttk.Combobox(janelanovopedido, textvariable=opcoes_cliente)
    cliente.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

    label_valor = tk.Label(janelanovopedido, text="Valor | R$:")
    label_valor.grid(row=2, column=0, padx=5, pady=5)
    campo_valor = tk.Entry(janelanovopedido, width=30)
    campo_valor.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

    label_prazo = tk.Label(janelanovopedido, text="Prazo de entrega:")
    label_prazo.grid(row=3, column=0, padx=5, pady=5)
    campo_prazo = tk.Entry(janelanovopedido, width=30)
    campo_prazo.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")

    label_descricao = tk.Label(janelanovopedido, text="Descrição:")
    label_descricao.grid(row=4, column=0, padx=5, pady=5)
    campo_descricao = tk.Text(janelanovopedido, width=30, height=5)
    campo_descricao.grid(row=4, column=1, padx=5, pady=5, sticky="nsew")




    def buscando_cliente(event=None):
        global listadeclientesdofiltro
        
        tipo=cliente_tipo.get()
        cliente.set("")
        try:
            if "CPF" in tipo:
                select = "SELECT nome_cliente FROM cliente WHERE cpf_cliente IS not null ORDER BY nome_cliente"
            else:
                select = "SELECT nome_cliente FROM cliente WHERE cnpj_cliente IS not null ORDER BY nome_cliente"

            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(select)
                    retornoselect=cur.fetchall()

                    listadeclientesdofiltro = [nome[0] for nome in retornoselect]
                    listadeclientesdacombo = [nome[0] for nome in retornoselect]
                    cliente["values"] = listadeclientesdacombo

        except Exception as e:
             messagebox.showerror("Erro",f"Algo deu errado ao buscar clientes")

    def formatar_data(event):
        texto = campo_prazo.get().replace("/", "") 
        novo_texto = ""
        
        for i, c in enumerate(texto):
            novo_texto += c
            if i == 1 or i == 3:
                novo_texto += "/"
        campo_prazo.delete(0, tk.END)
        campo_prazo.insert(0, novo_texto[:10]) 

    def enviar():
        texto = campo_prazo.get()
        if len(texto) != 10:
            messagebox.showerror("Erro", "Data incompleta! Use DD/MM/AAAA")
            return
        try:
            data_obj = datetime.strptime(texto, "%d/%m/%Y").date()
            print("Data válida")
        except ValueError:
            messagebox.showinfo("Erro", f"Data inválida, use dd/mm/aaaa: {data_obj}")

    def filtra_por_letra(event=None):
        texto_digitado = cliente.get().lower()
        filtrados = [nome for nome in listadeclientesdofiltro if texto_digitado in nome.lower()]
        cliente["values"] = filtrados
        cliente.event_generate('<Down>')


    def insertpedido():
        nome_combo=cliente.get()
        try:

            get_maior_id_pedido = "SELECT MAX(id_pedido) AS maior_id_pedido FROM pedido"
            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(get_maior_id_pedido)
            
                    maior_id_pedido = cur.fetchone()[0] or 0
                    id_novo_pedido = int(maior_id_pedido)+1

                    get_data_pedido = "SELECT CURRENT_DATE"
                    cur.execute(get_data_pedido)
                    datapedido = cur.fetchone()[0]

                    texto_data_prazo = campo_prazo.get().strip()
                    data_prazo= datetime.strptime(texto_data_prazo,"%d/%m/%Y").date()
                    enviar()

                    get_id_cliente = "SELECT id_cliente FROM cliente WHERE nome_cliente = %s"
                    cur.execute(get_id_cliente,(nome_combo,))
                    id_cliente=cur.fetchone()[0]

                    descricao = campo_descricao.get("1.0", "end-1c") or None

                    status="aguardando aceitação"

                    dadosdoinsertpedido=[id_novo_pedido, id_cliente, campo_valor.get(), data_prazo, datapedido, descricao, status ]

                    insertnovopedido = "INSERT INTO pedido (id_pedido, id_cliente, valor_pedido, prazo_entrega, data_pedido, descricao_pedido, status_pedido) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                    cur.execute(insertnovopedido,tuple(dadosdoinsertpedido))
                    print(dadosdoinsertpedido)
                    conn.commit()

                    with get_conn() as conn:
                        with conn.cursor() as cur:
                            get_maior_id_pagamento = "SELECT MAX(id_pagamento) AS maior_id_pagamento FROM pagamento"
                            cur.execute(get_maior_id_pagamento)
                    
                            maior_id_pagamento = cur.fetchone()[0] or 0
                            id_novo_pagamento = int(maior_id_pagamento)+1

                            get_id_cliente = "SELECT id_cliente FROM cliente WHERE nome_cliente = %s"
                            cur.execute(get_id_cliente,(nome_combo,))
                            id_cliente=cur.fetchone()[0]

                            valor = campo_valor.get()
                            valor = float(valor)

                            status_pagamento='P'

                            dadosdoinsertpagamento=[id_novo_pagamento, id_novo_pedido, valor, datapedido, status_pagamento]

                            insertnovopagamento = "INSERT INTO pagamento (id_pagamento, id_pedido, valor_pagamento, data_pagamento, status_pagamento) VALUES (%s,%s,%s,%s,%s)"
                            cur.execute(insertnovopagamento,tuple(dadosdoinsertpagamento))

                            conn.commit()

            
            messagebox.showinfo("Feito!",f"Pedido cadastrado com sucesso")
            janelanovopedido.destroy()
            atualizarhome()


        except Exception as e:
            messagebox.showerror("Algo deu errado",f"verifique os dados")

    cliente.bind("<KeyRelease>", filtra_por_letra)
    cliente_tipo.bind("<<ComboboxSelected>>", buscando_cliente)

    campo_prazo.bind("<KeyRelease>", formatar_data)

    botaocancelar = tk.Button(janelanovopedido, text="Cancelar", width=8, height=1, command=janelanovopedido.destroy)
    botaocancelar.grid(row=5, column=0, padx=3, pady=3, sticky="e")

    botaook = tk.Button(janelanovopedido, text="OK", width=8, height=1, command=insertpedido)
    botaook.grid(row=5, column=1, padx=3, pady=3, sticky="e")



    buscando_cliente()
    janelanovopedido.mainloop()

                                             #CADASTRO DE COMPRA/AQUISIÇÃO

listadefornecedoresdofiltro=[]

def novacompra():
    
    janelanovacompra=tk.Toplevel(home)
    janelanovacompra.title("Registro de compra")
    janelanovacompra.geometry("360x250")
    
    label_fornecedor = tk.Label(janelanovacompra, text="fornecedor:")
    label_fornecedor.grid(row=0, column=0, padx=5, pady=5)
    opcoes_fornecedores=tk.StringVar()
    fornecedor=ttk.Combobox(janelanovacompra, textvariable=opcoes_fornecedores)
    fornecedor.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

    label_tipo_compra = tk.Label(janelanovacompra, text="Tipo de compra:")
    label_tipo_compra.grid(row=1, column=0, padx=5, pady=5)
    opcoes_tipo_compra=["Material","Serviço","mobiliário","Maquinário","Outros"]
    tipo_compra=ttk.Combobox(janelanovacompra,values = opcoes_tipo_compra)
    tipo_compra.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

    label_valor = tk.Label(janelanovacompra, text="Valor | R$:")
    label_valor.grid(row=2, column=0, padx=5, pady=5)
    campo_valor = tk.Entry(janelanovacompra, width=30)
    campo_valor.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
    

    label_observacao = tk.Label(janelanovacompra, text="Observação:")
    label_observacao.grid(row=3, column=0, padx=5, pady=5)
    campo_observacao = tk.Text(janelanovacompra, width=30, height=5)
    campo_observacao.grid(row=3, column=1, padx=5, pady=5, sticky="nsew")


    def buscando_fornecedor(event=None):
        global listadefornecedoresdofiltro
        
        try:
            select = "SELECT nome_forn FROM fornecedor ORDER BY nome_forn"

            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(select)
                    retornoselect=cur.fetchall()

                    listadefornecedoresdofiltro = [nome[0] for nome in retornoselect]
                    listadefornecedoresdacombo = [nome[0] for nome in retornoselect]
                    fornecedor["values"] = listadefornecedoresdacombo

        except Exception as e:
             messagebox.showerror("Erro",f"Algo deu errado ao buscar os fornecedores no seu banco de dados")

    def filtra_por_letra(event=None):
        texto_digitado = fornecedor.get().lower()
        filtrados = [nome for nome in listadefornecedoresdofiltro if texto_digitado in nome.lower()]
        fornecedor["values"] = filtrados
        fornecedor.event_generate('<Down>')


    def insertcompra():
        nome_combo=fornecedor.get()
        try:
            #ALIMENTANDO A TABELA COMPRA COM OS DADOS DA COMPRA

            get_maior_id_compra = "SELECT MAX(id_compra) AS maior_id_compra FROM compra"
            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(get_maior_id_compra)
            
                    maior_id_compra = cur.fetchone()[0] or 0
                    id_nova_compra = int(maior_id_compra)+1

                    get_data_compra = "SELECT CURRENT_DATE"
                    cur.execute(get_data_compra)
                    datacompra = cur.fetchone()[0]

                    get_id_fornecedor = "SELECT id_forn FROM fornecedor WHERE nome_forn = %s"
                    cur.execute(get_id_fornecedor,(nome_combo,))
                    id_fornecedor=cur.fetchone()[0]

                    valor = campo_valor.get()
                    valor = float(valor)

                    descricao = campo_observacao.get("1.0", "end-1c") or None

                    dadosdoinsertcompra=[id_nova_compra, id_fornecedor, valor, descricao, datacompra ]

                    insertnovacompra = "INSERT INTO compra (id_compra, id_forn, valor_compra, descricao_compra, data_compra) VALUES (%s,%s,%s,%s,%s)"
                    cur.execute(insertnovacompra,tuple(dadosdoinsertcompra))
                    print(dadosdoinsertcompra)
                    conn.commit()

            #ALIMENTANDO A TABELA PAGAMENTOS COM O VALOR DA COMPRA
            
            get_maior_id_pagamento = "SELECT MAX(id_pagamento) AS maior_id_pagamento FROM pagamento"
            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(get_maior_id_pagamento)
            
                    maior_id_pagamento = cur.fetchone()[0] or 0
                    id_novo_pagamento = int(maior_id_pagamento)+1

                    get_id_fornecedor = "SELECT id_forn FROM fornecedor WHERE nome_forn = %s"
                    cur.execute(get_id_fornecedor,(nome_combo,))
                    id_fornecedor=cur.fetchone()[0]

                    valor = campo_valor.get()
                    valor = float(valor)
                    valor = -valor

                    status_pagamento='P'

                    dadosdoinsertpagamento=[id_novo_pagamento, id_fornecedor, valor, datacompra, status_pagamento]

                    insertnovopagamento = "INSERT INTO pagamento (id_pagamento, id_forn, valor_pagamento, data_pagamento, status_pagamento) VALUES (%s,%s,%s,%s,%s)"
                    cur.execute(insertnovopagamento,tuple(dadosdoinsertpagamento))
                    print(dadosdoinsertpagamento)
                    
                    conn.commit()
                    janelanovacompra.destroy()

        except Exception as e:
            print("ERRO REAL:", e)
            messagebox.showerror("Algo deu errado", f"Erro real:\n{e}")


    fornecedor.bind("<KeyRelease>", filtra_por_letra)
    fornecedor.bind("<<ComboboxSelected>>", buscando_fornecedor)

    botaook = tk.Button(janelanovacompra, text="OK", width=8, height=1, command=insertcompra)
    botaook.grid(row=4, column=0, padx=3, pady=3)

    botaocancelar = tk.Button(janelanovacompra, text="Cancelar", width=8, height=1, command=janelanovacompra.destroy)
    botaocancelar.grid(row=4, column=1, padx=3, pady=3)

    buscando_fornecedor()
    janelanovacompra.mainloop()

    
                                             #LISTANDO CLIENTES 
def listarclientes():
    
    janelalistaclientes=tk.Toplevel(home)
    janelalistaclientes.title("Lista de clientes")
    janelalistaclientes.geometry("1200x800")

    treeclientes=ttk.Treeview(janelalistaclientes, selectmode='browse', column=('id_cliente','nome_cliente','fone_cliente','email_cliente','whats_cliente','sexo_cliente','cpf_cliente','cnpj_cliente','end_cliente'), show='headings')

    treeclientes.column("id_cliente", width=5, minwidth=5)
    treeclientes.heading("#1", text="ID")

    treeclientes.column("nome_cliente", width=150, minwidth=150)
    treeclientes.heading("#2", text="Nome")

    treeclientes.column("fone_cliente", width=80, minwidth=50)
    treeclientes.heading("#3", text="Telefone")

    treeclientes.column("email_cliente", width=160, minwidth=20)
    treeclientes.heading("#4", text="Email")

    treeclientes.column("whats_cliente", width=80, minwidth=50)
    treeclientes.heading("#5", text="Whatsapp")

    treeclientes.column("sexo_cliente", width=13, minwidth=13)
    treeclientes.heading("#6", text="Sexo")

    treeclientes.column("cpf_cliente", width=100, minwidth=50)
    treeclientes.heading("#7", text="CPF")

    treeclientes.column("cnpj_cliente", width=100, minwidth=50)
    treeclientes.heading("#8", text="CNPJ")

    treeclientes.column("end_cliente", width=300, minwidth=50)
    treeclientes.heading("#9", text="Endereço")

    '''scrollbar = ttk.Scrollbar(home, orient=tk.VERTICAL, command=treeclientes.yview)
    treeclientes.configure(yscrollcommand=scrollbar.set)

   
    scrollbar.pack()'''
    
    treeclientes.pack(fill="both", expand=True)

    treeclientes.tag_configure('linhapar', background='#e0e0e0')
    treeclientes.tag_configure('linhaimpar', background="#9c9c9c")

    def atualizarclientes():

        for item in treeclientes.get_children():
            treeclientes.delete(item)
        select_cliente()

        
    def deletar_cliente():
        selecionado = treeclientes.focus()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um cliente para deletar")
        
        ondedeletar = treeclientes.item(selecionado, 'values')
        id_cliente_delete = ondedeletar[0]
        confirm = messagebox.askyesno("Confirmação", f"Deletar o cliente: {ondedeletar[0]}, {ondedeletar[1]}?")
        if not confirm:
            return
    
        with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM cliente WHERE id_cliente = %s", (id_cliente_delete, ))
    
                    conn.commit()
                    messagebox.showinfo("Sucesso", "Cliente deletado com sucesso!")
                    atualizarclientes()


    menu_clique_direito = tk.Menu(treeclientes, tearoff=0)
    #menu_clique_direito.add_command(label="Editar", command=editar_pedido)
    menu_clique_direito.add_command(label="Deletar", command=deletar_cliente)
    menu_clique_direito.add_separator()
    menu_clique_direito.add_command(label="Voltar", command=janelalistaclientes.quit)

    def mostrar_menu(event):
        menu_clique_direito.tk_popup(event.x_root, event.y_root)
    treeclientes.bind("<Button-3>", mostrar_menu)
   

    def select_cliente():
        try:
            selectcliente = "SELECT id_cliente,nome_cliente,fone_cliente,email_cliente,whats_cliente,sexo_cliente,cpf_cliente,cnpj_cliente,end_cliente FROM cliente"
            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(selectcliente)
                    clientes = cur.fetchall()

                    numlinhas=0
                    for cliente in clientes:
                            numlinhas=numlinhas+1
                            tag = 'linhapar' if numlinhas%2==0 else 'linhaimpar'
                            
                            endereco_original = cliente[8]
                            endereco_quebrado = "\n".join(textwrap.wrap(endereco_original, width=40))

                            cliente_modificado = list(cliente)
                            cliente_modificado[8] = endereco_quebrado


                            treeclientes.insert("", "end", values=cliente_modificado, tags=(tag,))

                    return cliente
                
        except Exception as e:
                mensagem_vazio = tk.Label(janelalistaclientes, text="Não há clientes ainda", font=("Arial", 14))
                mensagem_vazio.pack(pady=20)

    select_cliente()


    janelalistaclientes.mainloop()

                                            # LISTANDO PEDIDOS FINALIZADOS


def listar_pedidos_finalizados():
    
    janelalistapedidosfinalizados=tk.Toplevel(home)
    janelalistapedidosfinalizados.title("Lista de Pedidos Finalizados")
    janelalistapedidosfinalizados.geometry("800x500")
    
    treepedidosfinalizados=ttk.Treeview(janelalistapedidosfinalizados, selectmode='browse', column=('id_pedido','nome_cliente','valor_pedido','data_pedido','descricao_pedido'), show='headings')

    treepedidosfinalizados.column("id_pedido", width=2, minwidth=2)
    treepedidosfinalizados.heading("#1", text="Código")

    treepedidosfinalizados.column("nome_cliente", width=120, minwidth=50)
    treepedidosfinalizados.heading("#2", text="Cliente")

    treepedidosfinalizados.column("valor_pedido", width=20, minwidth=20)
    treepedidosfinalizados.heading("#3", text="Valor")

    treepedidosfinalizados.column("data_pedido", width=20, minwidth=20)
    treepedidosfinalizados.heading("#4", text="Data do pedido")

    treepedidosfinalizados.column("descricao_pedido", width=250, minwidth=50)
    treepedidosfinalizados.heading("#5", text="Descrição")

    '''scrollbar = ttk.Scrollbar(janelalistapedidosfinalizados, orient=tk.VERTICAL, command=treepedidosfinalizados.yview)
    treepedidosfinalizados.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack()'''
    
    treepedidosfinalizados.pack(fill="both", expand=True)
    
    def finalizado_to_confirmado():
        selecionado = treepedidosfinalizados.focus()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um pedido para atualizar")
            return

        ondealterar = treepedidosfinalizados.item(selecionado, 'values')
        id_do_pedido = ondealterar[0]
        confirm = messagebox.askyesno("Confirmação", f"Alterar o pedido {ondealterar[0]} de {ondealterar[1]}?")
        if not confirm:
            return
        
        with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute("UPDATE pedido SET status_pedido = 'Em produção' WHERE id_pedido = %s ", (id_do_pedido, ))

                conn.commit()
                atualizarhome()
                atualizarpedidosfinalizados()

    menu_clique_direito = tk.Menu(treepedidosfinalizados, tearoff=0)

    menu_clique_direito.add_command(label="Voltar para produção", command=finalizado_to_confirmado)

    def mostrar_menu(event):
        menu_clique_direito.tk_popup(event.x_root, event.y_root)
    treepedidosfinalizados.bind("<Button-3>", mostrar_menu)

    def atualizarpedidosfinalizados():

        for item in treepedidosfinalizados.get_children():
            treepedidosfinalizados.delete(item)
        select_pedidos_finalizados()


                            #IMPRIMINDO OS DADOS DOS PEDIDOS FINALIZADOS


    treepedidosfinalizados.tag_configure('linhapar', background='#e0e0e0')
    treepedidosfinalizados.tag_configure('linhaimpar', background="#9c9c9c")

    def select_pedidos_finalizados():
        try:
            comando_select_pedidos_finalizados = "SELECT id_pedido,nome_cliente, valor_pedido, TO_CHAR(data_pedido, 'DD/MM/YYYY') AS data_pedido,descricao_pedido FROM pedido INNER JOIN cliente " \
            "ON pedido.id_cliente = cliente.id_cliente WHERE status_pedido IN ('Finalizado') ORDER BY data_pedido ASC;"
            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(comando_select_pedidos_finalizados)
                    pedidos_finalizados = cur.fetchall()

                    numlinhas=0
                    for pedido_finalizado in pedidos_finalizados:
                            numlinhas=numlinhas+1
                            tag = 'linhapar' if numlinhas%2==0 else 'linhaimpar'
                            
                            descricao_original = pedido_finalizado[4]
                            endereco_quebrado = "\n".join(textwrap.wrap(descricao_original, width=40))

                            descricao_modificado = list(pedido_finalizado)
                            descricao_modificado[4] = endereco_quebrado


                            treepedidosfinalizados.insert("", "end", values=descricao_modificado, tags=(tag,))

                    return pedido_finalizado
                
        except Exception as e:
            mensagem_vazio = tk.Label(janelalistapedidosfinalizados, text="Não há pedidos finalizados ainda", font=("Arial", 14))
            mensagem_vazio.pack(pady=20,side='top')

    select_pedidos_finalizados()



                                            # LISTANDO PEDIDOS CANCELADOS -------------------------------------------


def listar_pedidos_cancelados():
    
    janelalistapedidoscancelados=tk.Toplevel(home)
    janelalistapedidoscancelados.title("Lista de Pedidos Cancelados")
    janelalistapedidoscancelados.geometry("800x500")
    
    treepedidoscancelados=ttk.Treeview(janelalistapedidoscancelados, selectmode='browse', column=('id_pedido','nome_cliente','valor_pedido','data_pedido','descricao_pedido'), show='headings')

    treepedidoscancelados.column("id_pedido", width=2, minwidth=2)
    treepedidoscancelados.heading("#1", text="Código")

    treepedidoscancelados.column("nome_cliente", width=120, minwidth=50)
    treepedidoscancelados.heading("#2", text="Cliente")

    treepedidoscancelados.column("valor_pedido", width=20, minwidth=20)
    treepedidoscancelados.heading("#3", text="Valor")

    treepedidoscancelados.column("data_pedido", width=20, minwidth=20)
    treepedidoscancelados.heading("#4", text="Data do pedido")

    treepedidoscancelados.column("descricao_pedido", width=250, minwidth=50)
    treepedidoscancelados.heading("#5", text="Descrição")

    '''scrollbar = ttk.Scrollbar(janelalistapedidoscancelados, orient=tk.VERTICAL, command=treepedidoscancelados.yview)
    treepedidoscancelados.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack()'''

    treepedidoscancelados.pack(fill="both", expand=True)

    def atualizarpedidoscancelados():

        for item in treepedidoscancelados.get_children():
            treepedidoscancelados.delete(item)
        select_pedidos_cancelados()

    def cancelado_to_confirmado():
        selecionado = treepedidoscancelados.focus()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um pedido para atualizar")
            return

        ondealterar = treepedidoscancelados.item(selecionado, 'values')
        id_do_pedido = ondealterar[0]
        confirm = messagebox.askyesno("Confirmação", f"Alterar o pedido {ondealterar[0]} de {ondealterar[1]}?")
        if not confirm:
            return
        
        with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute("UPDATE pedido SET status_pedido = 'Em produção' WHERE id_pedido = %s ", (id_do_pedido, ))

                conn.commit()
        atualizarhome()
        atualizarpedidoscancelados()

    menu_clique_direito = tk.Menu(treepedidoscancelados, tearoff=0)

    menu_clique_direito.add_command(label="Reativar pedido", command=cancelado_to_confirmado)

    def mostrar_menu(event):
        menu_clique_direito.tk_popup(event.x_root, event.y_root)
    treepedidoscancelados.bind("<Button-3>", mostrar_menu)



                            #IMPRIMINDO OS DADOS DOS PEDIDOS CANCELADOS --------------


    treepedidoscancelados.tag_configure('linhapar', background='#e0e0e0')
    treepedidoscancelados.tag_configure('linhaimpar', background="#9c9c9c")

    def select_pedidos_cancelados():
        try:
            comando_select_pedidos_cancelados = "SELECT id_pedido,nome_cliente, valor_pedido, TO_CHAR(data_pedido, 'DD/MM/YYYY') AS data_pedido,descricao_pedido FROM pedido INNER JOIN cliente " \
            "ON pedido.id_cliente = cliente.id_cliente WHERE status_pedido IN ('Cancelado') ORDER BY data_pedido ASC;"
            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(comando_select_pedidos_cancelados)
                    pedidos_cancelados = cur.fetchall()

                    numlinhas=0
                    for pedido_cancelado in pedidos_cancelados:
                            numlinhas=numlinhas+1
                            tag = 'linhapar' if numlinhas%2==0 else 'linhaimpar'
                            
                            descricao_original = pedido_cancelado[4]
                            endereco_quebrado = "\n".join(textwrap.wrap(descricao_original, width=40))

                            descricao_modificado = list(pedido_cancelado)
                            descricao_modificado[4] = endereco_quebrado


                            treepedidoscancelados.insert("", "end", values=descricao_modificado, tags=(tag,))

                    return pedido_cancelado
                
        except Exception as e:
                mensagem_vazio = tk.Label(janelalistapedidoscancelados, text="Não há pedidos cancelados ainda", font=("Arial", 14))
                mensagem_vazio.pack(pady=20)

    select_pedidos_cancelados()


                                             #LISTANDO FORNECEDORES

def listarfornecedores():
    
    janelalistafornecedor=tk.Toplevel(home)
    janelalistafornecedor.title("Lista de fornecedores")
    janelalistafornecedor.geometry("800x500")
    
    treefornecedores=ttk.Treeview(janelalistafornecedor, selectmode='browse', column=('id_fornecedor','nome_forn','cnpj_forn','email_forn','fone_forn','tipo_forn','end_forn'), show='headings')

    treefornecedores.column("id_fornecedor", width=20, minwidth=20)
    treefornecedores.heading("#1", text="ID")

    treefornecedores.column("nome_forn", width=120, minwidth=50)
    treefornecedores.heading("#2", text="Fornecedor")

    treefornecedores.column("cnpj_forn", width=100, minwidth=20)
    treefornecedores.heading("#3", text="CNPJ")

    treefornecedores.column("email_forn", width=140, minwidth=50)
    treefornecedores.heading("#4", text="Email")

    treefornecedores.column("fone_forn", width=80, minwidth=50)
    treefornecedores.heading("#5", text="Telefone")

    treefornecedores.column("tipo_forn", width=100, minwidth=50)
    treefornecedores.heading("#6", text="Tipo")

    treefornecedores.column("end_forn", width=220, minwidth=50)
    treefornecedores.heading("#7", text="Endereço")

    '''scrollbar = ttk.Scrollbar(janelalistafornecedor, orient=tk.VERTICAL, command=treefornecedores.yview)
    treefornecedores.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack()'''

    treefornecedores.pack(fill="both", expand=True)

    def atualizarfornecedores():

        for item in treefornecedores.get_children():
            treefornecedores.delete(item)
        select_fornecedores()

        
    def deletar_fornecedor():
        selecionado = treefornecedores.focus()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um fornecedor para deletar")
            
        ondedeletar = treefornecedores.item(selecionado, 'values')
        id_fornecedor_delete = ondedeletar[0]
        confirm = messagebox.askyesno("Confirmação", f"Deletar o fornecedor: {ondedeletar[0]}, {ondedeletar[1]}?")
        if not confirm:
            return
    
        with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM fornecedor WHERE id_forn = %s", (id_fornecedor_delete, ))
                    conn.commit()
        messagebox.showinfo("Feito", "Fornecedor deletado com sucesso!")
        atualizarfornecedores()


    menu_clique_direito = tk.Menu(treefornecedores, tearoff=0)
    #menu_clique_direito.add_command(label="Editar", command=editar_fornecedor)
    menu_clique_direito.add_command(label="Deletar", command=deletar_fornecedor)
    menu_clique_direito.add_separator()
    menu_clique_direito.add_command(label="Voltar", command=janelalistafornecedor.quit)

    def mostrar_menu(event):
        menu_clique_direito.tk_popup(event.x_root, event.y_root)
    treefornecedores.bind("<Button-3>", mostrar_menu)

                    #IMPRIMINDO DADOS DE FORNECEDORES NA TABELA DA JANELA FORNECEDORES -------------------------


    treefornecedores.tag_configure('linhapar', background='#e0e0e0')
    treefornecedores.tag_configure('linhaimpar', background="#9c9c9c")

    def select_fornecedores():
        try:
            selectfornecedor = "SELECT id_forn,nome_forn,cnpj_forn,email_forn,fone_forn,tipo_forn,end_forn FROM fornecedor"
            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(selectfornecedor)
                    fornecedores = cur.fetchall()

                    numlinhas=0
                    for fornecedor in fornecedores:
                            numlinhas=numlinhas+1
                            tag = 'linhapar' if numlinhas%2==0 else 'linhaimpar'
                            
                            endereco_original = fornecedor[6]
                            endereco_quebrado = "\n".join(textwrap.wrap(endereco_original, width=40))

                            fornecedor_modificado = list(fornecedor)
                            fornecedor_modificado[6] = endereco_quebrado


                            treefornecedores.insert("", "end", values=fornecedor_modificado, tags=(tag,))

            return fornecedor
        
        except Exception as e:
                mensagem_vazio = tk.Label(janelalistafornecedor, text="Não há fornecedores ainda", font=("Arial", 14))
                mensagem_vazio.pack(pady=20)

    select_fornecedores()

#  LISTANDO PAGAMENTOS ENTRA E SAI ----------------------
def listarpagamentos():
    
    janelalistapagamentos=tk.Toplevel(home)
    janelalistapagamentos.title("Movimentações financeiras")
    janelalistapagamentos.geometry("800x500")
    
    treepagamentos=ttk.Treeview(janelalistapagamentos, selectmode='browse', column=('id_pagamento','Data','Nome','valor','status'), show='headings')

    treepagamentos.column("id_pagamento", width=20, minwidth=20)
    treepagamentos.heading("#1", text="ID")

    treepagamentos.column("Data", width=120, minwidth=50)
    treepagamentos.heading("#2", text="Data")

    treepagamentos.column("Nome", width=100, minwidth=20)
    treepagamentos.heading("#3", text="Nome")

    treepagamentos.column("valor", width=140, minwidth=50)
    treepagamentos.heading("#4", text="Valor")

    treepagamentos.column("status", width=140, minwidth=50)
    treepagamentos.heading("#5", text="Status")

    treepagamentos.pack(fill="both", expand=True)

    treepagamentos.tag_configure('positivo', background='#E8FFE8')
    treepagamentos.tag_configure('negativo', background='#FFE8E8')

    def select_pagamentos():
        try:
            selectpagamentos = "SELECT p.id_pagamento,p.data_pagamento, CASE WHEN p.id_forn IS NULL THEN c.nome_cliente ELSE f.nome_forn END AS nome, p.valor_pagamento, p.status_pagamento" \
            " FROM pagamento p LEFT JOIN pedido ped ON ped.id_pedido = p.id_pedido LEFT JOIN cliente c ON c.id_cliente = ped.id_cliente LEFT JOIN fornecedor f ON f.id_forn = p.id_forn"  
            "ORDER BY p.id_pagamento DESC;"
            with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute(selectpagamentos)
                    pagamentos = cur.fetchall()

                    for pagamento in pagamentos:
                            valor = pagamento[3]
                            tag = 'positivo' if valor >= 0 else 'negativo'
                            treepagamentos.insert("", "end", values=pagamento, tags=(tag,))
                    return pagamento
        except:
            print("erro")


    def atualizapagamentos():

        for item in treepagamentos.get_children():
            treepagamentos.delete(item)

        select_pagamentos()

    def set_p():
        selecionado = treepagamentos.focus()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um pedido para atualizar")
            return

        ondealterar = treepagamentos.item(selecionado, 'values')
        id_pagamento = ondealterar[0]
        confirm = messagebox.askyesno("Confirmação", f"Marcar como PAGO?")
        if not confirm:
            return
        
        with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute("UPDATE pagamento SET status_pagamento = 'P' WHERE id_pagamento = %s ", (id_pagamento, ))

                conn.commit()
        atualizapagamentos()

    def set_n():
        selecionado = treepagamentos.focus()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um pedido para atualizar")
            return

        ondealterar = treepagamentos.item(selecionado, 'values')
        id_pagamento = ondealterar[0]
        confirm = messagebox.askyesno("Confirmação", f"Marcar como NÃO PAGO?")
        if not confirm:
            return
        
        with get_conn() as conn:
                with conn.cursor() as cur:
                    cur.execute("UPDATE pagamento SET status_pagamento = 'N' WHERE id_pagamento = %s ", (id_pagamento, ))

                conn.commit()
        atualizapagamentos()


 

    menu_clique_pagamentos = tk.Menu(janelalistapagamentos, tearoff=0)
    #menu_clique_direito.add_command(label="Editar", command=editar_fornecedor)
    menu_clique_pagamentos.add_command(label="Pago", command=set_p)
    menu_clique_pagamentos.add_command(label="Não Pago", command=set_n)

    def mostrar_menu_pagamento(event):
        menu_clique_pagamentos.tk_popup(event.x_root, event.y_root)
    treepagamentos.bind("<Button-3>", mostrar_menu_pagamento)

    select_pagamentos()
    janelalistapagamentos.mainloop()



#CRIANDO MENU ----------------------------------------------------
menubar=tk.Menu(home)


#CRIANDO MENU ----------ITENS DO MENU-----------------------------
menucadastro=tk.Menu(menubar,tearoff=0)

menucadastro.add_command(label="Novo cliente",command=novocliente)
menucadastro.add_command(label="Pedido",command=novoorcamento)
menucadastro.add_command(label="Novo fornecedor",command=novofornecedor)
menucadastro.add_command(label="Nova aquisição",command=novacompra)

menubar.add_cascade(label="Cadastro",menu=menucadastro)

#MENU EXIBIR --
menuexibir=tk.Menu(menubar,tearoff=0)

menuexibir.add_command(label="Clientes",command=listarclientes)

menuexibir.add_command(label="Fornecedores",command=listarfornecedores)
menuexibir.add_command(label="Movimentações financeiras",command=listarpagamentos)

menubar.add_cascade(label="Exibir",menu=menuexibir)

#MENU HISTÓRICO ----------------------- 
menuhistorico=tk.Menu(menubar,tearoff=0)

menuhistorico.add_command(label="Finalizados",command=listar_pedidos_finalizados)
menuhistorico.add_command(label="Cancelados",command=listar_pedidos_cancelados)

menubar.add_cascade(label="Histórico de serviços",menu=menuhistorico)


#   A T U A L I Z A N D O    A P Ó S    M U D A N Ç A S   ----------------------


home.config(menu=menubar)
#IMPEDINDO O PROGRAMA DE FECHAR SOZINHO ---------------------------
home.mainloop()