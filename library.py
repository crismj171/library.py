import datetime
from collections import deque

livros = {}
usuarios = {}
pilha_acoes = []

def cadastro_livro():
    id = input("ID do livro: ")
    titulo = input("Título: ")
    autor = input("Autor: ")

    if id in livros:
        print("Livro já cadastrado")
    else:
        livros[id] = [(titulo, autor), True, deque()]
        print("Cadastro finalizado")

def cadastro_usuario():
    cpf = input("CPF: ")
    nome = input("Nome: ")

    if cpf in usuarios:
        print("Usuário já cadastrado")
    else:
        usuarios[cpf] = [nome, [], 0]
        print("Cadastro finalizado")

def emprestar():
    cpf = input("CPF: ")
    id = input("ID do livro: ")

    if cpf not in usuarios:
        print("Usuário inexistente")
        return
    if id not in livros:
        print("Livro inexistente")
        return

    livro = livros[id]
    if livro[1] == True:
        livro[1] = False
        data = datetime.date.today()
        usuarios[cpf][1].append([id, data])
        print("Sob empréstimo.")
        pilha_acoes.append(f"O usuário de CPF {cpf} emprestou o livro de ID {id} em {data}")
    else:
        print("Indisponível. Em fila para empréstimo.")
        livro[2].append(cpf)
        pilha_acoes.append(f"O usuário de CPF {cpf} entrou na fila de espera para o livro de ID {id}")

def devolver():
    cpf = input("CPF: ")
    id = input("ID do livro: ")

    if cpf not in usuarios:
        print("Usuário inexistente")
        return
    if id not in livros:
        print("Livro inexistente")
        return

    u = usuarios[cpf]
    l = livros[id]

    registro_emprestimo = None
    for emprestimo in u[1]:
        if emprestimo[0] == id:
            registro_emprestimo = emprestimo
            break

    if registro_emprestimo is None:
        print("Empréstimo inexistente")
        return

    hoje = datetime.date.today()
    dias = (hoje - registro_emprestimo[1]).days

    if dias > 30:
        multa = (dias - 30) * 3
        u[2] += multa
        print(f"Atraso de {dias-30} dias. Multa de R$ {multa}")
    else:
        print("Livro devolvido dentro do prazo")

    u[1].remove(registro_emprestimo)
    pilha_acoes.append(f"{cpf} devolveu {id} em {hoje}")

    if l[2]:
        prox = l[2].popleft()
        usuarios[prox][1].append([id, hoje])
        print("Em empréstimo para o usuário:", usuarios[prox][0])
        l[1] = False
        pilha_acoes.append(f"O livro de ID {id} foi emprestado automaticamente para o usuário de CPF {prox}")
    else:
        l[1] = True
        print("Devolvido com sucesso")

def ver_user():
    cpf = input("Insira o CPF do usuário: ")
    if cpf not in usuarios:
        print("Usuário não cadastrado.")
        return
    u = usuarios[cpf]
    print(f"\nNome: {u[0]}")
    print(f"Multa: R$ {u[2]}")
    print("Empréstimos atuais:")
    if u[1]:
        for e in u[1]:
            print(f"- Livro {e[0]} desde {e[1]}")
    else:
        print("Nenhum livro emprestado.")

def ver_livros():
    if not livros:
        print("Nenhum livro cadastrado.")
        return
    print("\nLista de livros:")
    for id, dados in livros.items():
        status = "Disponível" if dados[1] else "Indisponível"
        print(f"ID: {id} | Título: {dados[0][0]} | Autor: {dados[0][1]} | Status: {status}")

def ver_historico():
    if pilha_acoes:
        print("\nHistórico de ações:")
        for a in reversed(pilha_acoes):
            print(a)
    else:
        print("Não existe nenhum registro no histórico.")

def demonstracao_emprestimo():
    cpf = input("CPF do usuário: ")
    id = input("ID do livro: ")

    if cpf not in usuarios:
        print("Usuário inexistente")
        return
    if id not in livros:
        print("Livro inexistente")
        return

    livro = livros[id]
    if livro[1] == True:
        livro[1] = False
        data = datetime.date.today() - datetime.timedelta(days=40)
        usuarios[cpf][1].append([id, data])
        print("Empréstimo simulado há 40 dias para gerar multa na devolução.")
        pilha_acoes.append(f"(Demonstração) O usuário de CPF {cpf} emprestou o livro de ID {id} em {data}")
    else:
        print("Indisponível. Em fila para empréstimo.")
        livro[2].append(cpf)
        pilha_acoes.append(f"(Demonstração) O usuário de CPF {cpf} entrou na fila de espera para o livro de ID {id}")

def transferir_livro():
    cpf_origem = input("CPF do usuário que está com o livro: ")
    cpf_destino = input("CPF do usuário que vai receber o livro: ")
    id = input("ID do livro a ser transferido: ")

    if cpf_origem not in usuarios:
        print("Usuário de origem inexistente")
        return
    if cpf_destino not in usuarios:
        print("Usuário de destino inexistente")
        return
    if id not in livros:
        print("Livro inexistente")
        return

    livro = livros[id]

    if livro[2]:
        print("Há usuários na fila de espera. Transferência não permitida.")
        return

    emprestimos_origem = usuarios[cpf_origem][1]
    registro = None
    for emp in emprestimos_origem:
        if emp[0] == id:
            registro = emp
            break

    if registro is None:
        print("O usuário de origem não possui este livro emprestado.")
        return

    usuarios[cpf_origem][1].remove(registro)
    usuarios[cpf_destino][1].append([id, registro[1]])

    print("Transferência realizada com sucesso.")
    pilha_acoes.append(f"O livro de ID {id} foi transferido de {cpf_origem} para {cpf_destino}")

while True:
    print("\n1. Cadastrar livro")
    print("2. Cadastrar usuário")
    print("3. Registrar empréstimo")
    print("4. Registrar devolução")
    print("5. Verificar usuário")
    print("6. Verificar histórico")
    print("7. Verificar livros")
    print("8. Demonstração de multa de empréstimo")
    print("9. Transferir livro entre usuários")
    print("10. Sair")
    op = input("Opção: ")

    if op == '1':
        cadastro_livro()
    elif op == '2':
        cadastro_usuario()
    elif op == '3':
        emprestar()
    elif op == '4':
        devolver()
    elif op == '5':
        ver_user()
    elif op == '6':
        ver_historico()
    elif op == '7':
        ver_livros()
    elif op == '8':
        demonstracao_emprestimo()
    elif op == '9':
        transferir_livro()
    elif op == '10':
        break
    else:
        print("A opção selecionada é inválida.")
