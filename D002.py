from datetime import datetime



menuCliente = '''

[c] - Criar utilizador
[l] - Listar utilizadores
[d] - Deletar utilizadore
[a] - Actualizar utilizador
[e] - Entrar 

'''

LIMITE_SAQUES = 3
clientes = []

def createUsers():
    global clientes
    print("CADASTRO DE UTILIZADOR".center(50, "#"))
    Nome = input("Digite seu nome: ").strip()
    Nascimento = input("Digite sua data de nascimento [DD-MM-AAAA]: ").strip()
    Cpf = int(input("Digite o seu CPF: ").strip())
    # Address
    print("Endereço: ")
    Logradouro = input("Logradouro: ").strip()
    Bairro = input("Bairro: ").strip()
    Cidade = input("Cidade: ").strip()

    Endereco = f'{Logradouro} {Bairro} {Cidade}'

    cliente = {
        "nome": Nome,
        "nascimento": Nascimento,
        "cpf": Cpf,
        "endereco": Endereco
    }

    clientes.append(cliente)

def readUsers():
    global clientes
    print("LISTAGEM DE UTILIZADORES".center(50, "#"))
    for cliente in clientes:
        print(cliente)

def deleteUser():
    print("LISTAGEM DE UTILIZADORES".center(50, "#"))
    for cliente in clientes:
        print(cliente)
    try:
        Cpf = int(input("Digite o cpf do utilizador que deseja actualizar: "))
    except: 
        print("Valor inválido.")
        return
    cliente = None
    for c in clientes:
        if c["cpf"] == Cpf:
            cliente = c
    
    if cliente == None:
        print("Utilizador não existente.")
        return
    clientes.remove(cliente)
    print("Utilizador removido com sucesso.")

def updateUser():
    print("LISTAGEM DE UTILIZADORES".center(50, "#"))
    for cliente in clientes:
        print(cliente)
    try:
        Cpf = int(input("Digite o cpf do utilizador que deseja actualizar: "))
    except: 
        print("Valor inválido.")
        return
    cliente = None
    for c in clientes:
        if c["cpf"] == Cpf:
            cliente = c
    
    if cliente == None:
        print("Utilizador não existente.")
        return

    Nome = input("Digite seu nome: ").strip()
    Nascimento = input("Digite sua data de nascimento [DD-MM-AAAA]: ").strip()
    # Address
    print("Endereço: ")
    Logradouro = input("Logradouro: ").strip()
    Bairro = input("Bairro: ").strip()
    Cidade = input("Cidade: ").strip()

    Endereco = f'{Logradouro} {Bairro} {Cidade}'

    if (not Logradouro) and (not Bairro) and (not Cidade):
        Endereco = ''

    cliente = {
        "nome": Nome,
        "nascimento": Nascimento,
        "cpf": Cpf,
        "endereco": Endereco
    }
    for c in clientes:
        if c["cpf"] == Cpf:
            if Nome:
                c["nome"] = Nome
            if Nascimento:
                c["nascimento"] = Nascimento
            if Endereco:
                c["endereco"] = Endereco
            print("Cliente actualziado: ", c)
    
    print("Utilizador actualizado com sucesso.")


def managerUser():
    global clientes
    cpf = int(input("Digite o seu CPF para entrar: "))
    cliente = None
    for c in clientes:
        if c["cpf"] == cpf:
            cliente = c
    cliente["contas"] = []
    contas = cliente["contas"]
    
    if cliente == None:
        print("Utilizador não existente.")
        return
    menu = "[p] - Perfil\n[l] - Listar contas\n[c] - Criar conta\n[d] - Eliminar conta\n[e] - Entrar na conta\n"

    while True:
        opcao = input(menu)
        
        if opcao == "p":
            print(cliente)
        elif opcao == "l":
            print("LISTAGEM DE CONTAS".center(50, "#"))
            for conta in contas:
                print(conta)
            continue
        elif opcao == "c":
            numero_conta = len(cliente["contas"])+1
            conta = {
                "saldo": 0,
                "limite": 500,
                "extrato": "",
                "depositos": [],
                "saques": [],
                "numero_saques": 0,
                "numero_conta": numero_conta
            }

            cliente["contas"].append(conta)

            print("Conta criada com sucesso.")

            continue
        elif opcao == "d":
            print("LISTAGEM DE CONTAS".center(50, "#"))
            for conta in contas:
                print(conta)
            r = int(input("Digite o numero_conta: ").strip())
            conta = None
            for c in contas:
                if r == c["numero_conta"]:
                    conta = c
            cliente["contas"].remove(conta)
            print("Conta removida com sucesso.")
            continue
        elif opcao == "e":
            print("Entrando na conta")
            managerAccount(cliente=cliente)
            continue
        else:
            print("Opção em inválida.")
            continue


def managerAccount(cliente):
    numero_conta = int(input("Digite o número da conta para entrar: "))
    conta = None
    for c in cliente["contas"]:
        if c["numero_conta"] == numero_conta:
            conta = c
    
    if conta == None:
        print("Conta não existente.")
        return
    
    def depoisitar(deposito):
        saldo = conta["saldo"]
        #Validações
        if( deposito < 0 ):
            print("Impossível depositar um valor negativo")

        #Lógica
        saldo_anterior = conta["saldo"]
        conta["saldo"] += deposito

        #Sucesso
        print("Depósito realizado com sucesso.")
        print(f"Saldo anterior: R$ {saldo_anterior:.2f}")
        print(f"Saldo actual: R$ {conta["saldo"]:.2f}")

        #Extrato
        data = datetime.now()
        deposito = f'Valor depositado: {deposito}\nData: {data}\nEstado: Sucesso\n'
        conta["depositos"].append(deposito)

    def sacar(saque):
        numero_saques = conta["numero_saques"]
        saldo = conta["saldo"]
        #Validações
        if ( saque < 0) :
            print("Impossível realizar um saque de um valor negativo.")
            return 
        if (numero_saques > LIMITE_SAQUES):
            print("Atingiu o limite de saques impossível realizar um saque.")
            return 
        if( saque > saldo):
            print(f"Saque não pode ser maior que o saldo.\nSaldo: R$ {saldo:.2f} ")
            return 

        #Lógica
        saldo_anterior = saldo
        conta["saldo"] -= saque
        conta["numero_saques"] += 1

        #Sucesso
        print("Saque realizado com sucesso.")
        print(f"Saldo anterior: R$ {saldo_anterior:.2f}")
        print(f"Saldo actual: R$ {conta["saldo"]:.2f}")

        #Extrato
        data = datetime.now()
        saq = f'Valor sacado: R$ {saque:.2f}\nData: {data}\nEstado: Sucesso\n'
        conta["saques"].append(saq)

    def exibir_extrato():
        #Separador
        separador = "-".center(50,"=")
        saques = conta["saques"]
        depositos = conta["depositos"]

        #Depositos
        d = "\n".join(depositos) if len(depositos) > 0 else "Sem depositos na conta."

        #Saques
        s = "\n".join(saques) if len(saques) > 0 else "Sem saques na conta."

        #Extrado
        extrato = f'''
{"EXTRATO".center(50,"#")}
{separador}
DEPOSITOS:

{d}
{separador}
SAQUES:

{s}
{separador}
SALDO: R$ {conta["saldo"]:.2f}
'''
        
        print(extrato)

   
    menu = '''

[d] - Depositar
[s] - Sacar
[e] - Extrado
[end] - Sair 

'''
    while True:
        print(menu)
        opcao = str(input("Escolha: "))

        if opcao == "d":
            while True:
                deposito = float(input("Valor a depositar: "))
                depoisitar(deposito)
                question = str(input("Deseja realizar outro depósito? [s/n]: ")).lower()
                if question == 'n':
                    break
            continue
            break
        elif opcao == "s":
            while True:
                    saque = float(input("Valor do saque: "))
                    sacar(saque)
                    question = str(input("Deseja realizar outro saque? [s/n]: ")).lower()
                    if question == 'n':
                        break
            continue
        elif opcao == "e":
            exibir_extrato()
            continue
        elif opcao == "end":
            break
        else:
            print("Opção inválida.")
        

# 1 Utilizador -> n Contas
# 1 Contar -> 1 Utilizador

while True:
    print(menuCliente)
    opcao = input().strip()
    if opcao == "c":
        createUsers()
        continue
    elif opcao == "l":
        readUsers()
        continue
    elif opcao == "d":
        deleteUser()
        continue
    
    elif opcao == "a":
        updateUser()
        continue
    elif opcao == "e":
        managerUser()
        continue
    else:
        print("Opção inválida!")
        continue