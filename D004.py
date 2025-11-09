from abc import ABC, abstractmethod

class PessoaFisica:
    def __init__(self, cpf, nome, data_nascimento):
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento
    
    @property
    def nome(self):
        return self._nome
    
    @property
    def cpf(self):
        return self._cpf
    
    @property
    def data_nascimento(self):
        return self._data_nascimento

class Cliente(PessoaFisica):
    def __init__(self,senha, endereco, contas, **kw):
        super().__init__(**kw)
        self._endereco = endereco
        self._contas = contas
        self._senha = senha
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
class Conta:
    def __init__(self,saldo, numero, agencia, cliente, historico):
        self._saldo = saldo
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = historico
    
    def saldo(self):
        return self._saldo
    
    def nova_conta(self, cliente, numero_conta):
        Conta(100, numero_conta, "001", cliente,"")


    def depositar(self,valor):
        if valor < 0:
            print("Valor inválido.")
            return
        self._saldo+=valor
        print("Saldo actualizador")
    
    def sacar(self, valor):
        if valor < 0:
            print("Valor inválido")
            return
        
        if valor > self._saldo:
            print("Valor inválido")
            return
        
        self._saldo-=valor
        print("Saque realizado com sucesso.")
    
    def transferencia_conta_conta(self, conta, valor):
        if valor >= self._saldo:
            print("Valor inválido.")
            return
        if valor < 0:
            print("Valor inválido.")
            return
        
        self._saldo-=valor
        conta._saldo+=valor
        print("Transferência realizada com sucesso.")

class ContaCorrente(Conta):
    def __init__(self, limite, limite_saques, **kw):
        super().__init__(**kw)
        self._limite = limite
        self._limite_saques = limite_saques

class Transacao(ABC):
    @abstractmethod
    def registrar(conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        sucesso = conta.depositar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)
        return sucesso

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        sucesso = conta.sacar(self.valor)
        if sucesso:
            conta.historico.adicionar_transacao(self)
        return sucesso

class Transferencia(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta_origem, conta_destino):
        sucesso = conta_origem.transferencia_conta_conta(conta_destino, self.valor)
        if sucesso:
            conta_origem.historico.adicionar_transacao(self)
        return sucesso
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

    def listar_transacoes(self):
        for t in self.transacoes:
            tipo = t.__class__.__name__
            print(f"{tipo} de R${t.valor:.2f}")

clientes = []

menu = '''

[c] - Cadastrar-se
[l] - Login
[s] - Sair

=> '''

def maneger_cliente(cliente):
    menu = '''

[p] - Perfil
[c] - contas
[a] - Adicionar conta
[t] - Transação
[s] - Sair

=> '''
    print(f'Olá, {cliente.nome}.')
    while True:
        opcao = input(menu)
        if opcao == "p":
            print("Seu perfil")
        elif opcao == "c":
            if len(cliente._contas) == 0:
                op = input("Você ainda não criou nehuma conta. Digite [a], para criar uma conta. => ")
                if op == "a":
                    opcao = "a"
            for conta in cliente._contas:
                print("======")
                print(f'Número conta: {conta._numero}\nSaldo: {conta._saldo}\nHistorico:\n {conta._historico.listar_transacoes} ')
                print("======")
        elif opcao == "t":
            while True:
                submenu = '''
[d] - Depositar
[s] - Sacar
[t] - Transferência de conta-conta'''
                print(submenu)
                op = input("=> ")
                if op == "d":
                    valor = float(input("Digite o valor, por favor: "))
                    deposito = Deposito(valor)
                    numero_conta = int(input("Digite o número da conta, por favor: "))
                    c = None
                    for conta in cliente._contas:
                        if conta._numero == numero_conta:
                            c = conta
                    cliente.realizar_transacao(c, deposito)
                    break
                elif op == "s":
                    valor = float(input("Digite o valor, por favor: "))
                    deposito = Saque(valor)
                    numero_conta = int(input("Digite o número da conta, por favor: "))
                    c = None
                    for conta in cliente._contas:
                        if conta._numero == numero_conta:
                            c = conta
                    cliente.realizar_transacao(c, deposito)
                    break

        elif opcao == "a":
            historico = Historico()
            conta = ContaCorrente(100*1000, 10, saldo=0, numero=len(cliente._contas)+1, agencia="001",cliente=cliente,historico=historico)
            cliente._contas.append(conta)
            print("Conta criado com sucesso.")
        if opcao == "s":
            print(f'Tchau, {cliente.nome}')
            break


while True:
    opcao = input(menu)
    if opcao == "c":
        while True:
            print("[s] - sair")
            cpf = int(input("Digite seu CPF, por favor: "))
            if cpf == "s": break
            for cliente in clientes:
                if cliente._cpf == cpf:
                    print("Cpf inválido.")
                    continue
            break
        
        nome = input("Digite seu nome, por favor: ")
        data_nascimento = input("Digite sua data de nascimento [dd-mm-aaaa], por favor: ")
        print("==Endereço==")
        provincia = input("Digite a sua provincia de residência, por favor: ")
        municipio = input("Digite o seu município de residência, por favor: ")
        bairro = input("Digite o seu bairro de residênia, por favor: ")
        rua = input("Digite a sua rua de residência, por favor: ")
        n_casa = input("Digite o número da sua cada de residência, por favor: ")
        print("======")
        def endereco(*args):
            return "-".join(args)
        
        _endereco = endereco(provincia, municipio, bairro, rua, n_casa)

        contas = []
        senha = ""
        while True:
            suposta_senha = str(input("Digite uma senha pra manter sua conta segura: "))
            if not suposta_senha:
                print("Por favor, digite uma senha.")
                continue
            if len(suposta_senha) < 8:
                print("Senha tem que ter mais de 8 caractéres.")
                continue
            for i in range(50):
                print()
            confirmacao_senha = input("Digte a senha que acabou de digitar acima, por favor: ")
            if confirmacao_senha == "s":
                break
            if suposta_senha != confirmacao_senha:
                print("Por favor, digite senhas iguais.")
                continue
            senha = suposta_senha
            print("Senha cadastrada com sucesso.")
            break

        c = Cliente(senha, _endereco, [], cpf=cpf, nome=nome, data_nascimento=data_nascimento)
        clientes.append(c)
        print("Conta cadastrada com sucesso.")
    elif opcao == "l":
        while True: 
            print(" [0] - sair ")
            cpf = int(input("Digite seu cpf, por favor: "))
            if cpf == 0:break
            c = None
            for cliente in clientes:
                if cpf == cliente._cpf:
                    c = cliente
            break
            
        if not c:
            print("Cliente não encontrado")
            continue
        senha = int(input("Digite sua senha, por favor: "))
        print(senha, cliente._senha)
        if senha != int(cliente._senha):
            print("Senha incorrecta.")
            continue
        print("Login efectuado com sucesso.")
        maneger_cliente(c)

    elif opcao == "s":
        break