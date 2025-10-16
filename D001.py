from datetime import datetime

menu = '''

[d] - Depositar
[s] - Sacar
[e] - Extrado
[end] - Sair 

'''

saldo = 0
limite = 500
extrato = ""
depositos = []
saques = []
numero_saques = 0
LIMITE_SAQUES = 3

def isString( s) -> bool:
    validation = str(type(s)) == "<class 'str'>"
    return validation
   
while True:
    print(menu)
    opcao = str(input("Escolha: "))

    if(not isString(opcao)):
       break

    if opcao == "d":
    #====================
        deposito = float(input("Valor a depositar: "))
        #Validações
        if( deposito < 0 ):
            print("Impossível depositar um valor negativo")
            continue

        #Lógica
        saldo_anterior = saldo
        saldo += deposito

        #Sucesso
        print("Depósito realizado com sucesso.")
        print(f"Saldo anterior: R$ {saldo_anterior:.2f}")
        print(f"Saldo actual: R$ {saldo:.2f}")

        #Extrato
        data = datetime.now()
        deposito = f'Valor depositado: {deposito}\nData: {data}\nEstado: Sucesso\n'
        depositos.append(deposito)


    elif opcao == "s":
    #====================
        saque = float(input("Valor do saque: "))

        #Validações
        if ( saque < 0) :
            print("Impossível realizar um saque de um valor negativo.")
            continue
        if (numero_saques > LIMITE_SAQUES):
            print("Atingiu o limite de saques impossível realizar um saque.")
            continue
        if( saque > saldo):
            print(f"Saque não pode ser maior que o saldo.\nSaldo: R$ {saldo:.2f} ")
            continue

        #Lógica
        saldo_anterior = saldo
        saldo -= saque
        numero_saques += 1

        #Sucesso
        print("Saque realizado com sucesso.")
        print(f"Saldo anterior: R$ {saldo_anterior:.2f}")
        print(f"Saldo actual: R$ {saldo:.2f}")

        #Extrato
        data = datetime.now()
        saq = f'Valor sacado: R$ {saque:.2f}\nData: {data}\nEstado: Sucesso\n'
        saques.append(saq)


    elif opcao == "e":
    #================
        #Separador
        separador = "-".center(50,"=")

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
SALDO: R$ {saldo:.2f}
'''
        
        print(extrato)
    elif opcao == "end":
        break
    else:
        print("Opção inválida.")
        