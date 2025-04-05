# Toda modelagem inicial do sistema bancário utilizado POO.
from abc import ABC, abstractmethod
from datetime import datetime

# Essa classe foi criada na necessidade de usar o login e não usar varíaveis globais para guardar clientes e contas


class Banco:
    def __init__(self):
        self._clientes = []
        self._contas = []

    @property
    def clientes(self):
        return self._clientes

    @property
    def contas(self):
        return self._contas

    def buscar_cliente(self, cpf):
        for c in self.clientes:
            if (c.cpf == cpf):
                return c
        return False

    def cadastrar_cliente(self, cliente):
        self._clientes.append(cliente)

    def cadastrar_conta(self, conta):
        self._contas.append(conta)
        conta.cliente.adicionar_conta(conta)


class Cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, endereco, cpf, nome, data_nascimento):
        super().__init__(endereco)
        self._cpf = cpf
        self._nome = nome
        self._data_nascimento = data_nascimento

    @property
    def cpf(self):
        return self._cpf

    @property
    def nome(self):
        return self._nome


class Conta:
    def __init__(self, numero_conta, cliente):
        self._saldo = 0
        self._numero_conta = numero_conta
        self._AGENCIA = "0001"
        self._cliente = cliente
        self._historico = Historico()
        self._data_abertura = datetime.now()

    @classmethod
    def nova_conta(cls, cliente, numero_conta):
        return cls(numero_conta, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero_conta(self):
        return self._numero_conta

    @property
    def agencia(self):
        return self._AGENCIA

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self._saldo
        if (valor > saldo):
            print("---- Você não tem saldo suficiente ----")

        elif (valor > 0):
            self._saldo -= valor
            print("==== Saque realizado com sucesso! ====")
            return True

        else:
            print("---- Número Informado é inválido para transação! ----")

        return False

    def depositar(self, valor):

        if (valor > 0):
            self._saldo += valor
            print("==== Valor depositado com Sucesso! ====")
            return True

        print("---- Número Informado é inválido para transação! ----")
        return False


class ContaCorrente(Conta):
    def __init__(self, numero_conta, cliente, limite=500, limite_saques=3):
        super().__init__(numero_conta, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self.qnt_saques_realizados = 0

    def sacar(self, valor):
        if (valor > self.limite):
            print("---- Valor maior que o limite do saque! ----")

        elif (self.qnt_saques_realizados >= self.limite_saques):
            print("---- O limite de saque diário já foi atingido! ----")
        else:
            self.qnt_saques_realizados += 1
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self._AGENCIA}
            C/C:\t\t{self._numero_conta}
            Titular:\t{self.cliente._nome}
            Saldo: \t\t  R${self._saldo}
        """


class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):

        self.transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M")})


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        return self._valor

    @abstractmethod
    def registrar_transacao(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        super().__init__()
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar_transacao(self, conta):
        if conta.sacar(self._valor):
            conta.historico.adicionar_transacao(self)
            return True
        return False


class Deposito(Transacao):
    def __init__(self, valor):
        super().__init__()
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar_transacao(self, conta):
        if conta.depositar(self._valor):
            conta.historico.adicionar_transacao(self)
            return True
        return False

### Funções de amostragem de menus ###


def login_banco():
    login = """
[e] Entrar
[c] Cadastrar
[s] Sair

==> """
    return login


def menu_operacores():
    menu = """
[d] Depositar dinheiro
[s] Sacar dinheiro
[v] Visualizar extrato bancário
[c] Criar nova conta
[l] Listar contas
[e] Exit

=> """

    return menu

# Funções do menu de login


def cadastrar_cliente(banco):
    print("\n====== CADASTRO DE CLIENTE ======\n")
    cpf = input("CPF:")

    if (banco.buscar_cliente(cpf)):
        print("------ Cliente já cadastrado ------")
        return
    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento (dd/mm/aaaa): ")
    endereco = input(
        "Endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(endereco, cpf, nome, data_nascimento)
    banco.cadastrar_cliente(cliente)
    print("\n##### Cliente Cadastrado com sucesso #####")


def fazer_login(banco):
    cpf = input("\nInforme o CPF: \n==> ")
    cliente = banco.buscar_cliente(cpf)
    if cliente:
        print(f"======= BEM VINDO {cliente.nome.upper()} =======")
        return True

    print("##### CLIENTE NÃO CADASTRADO! #####")
    return False


def main():
    banco = Banco()
    while True:
        login_opcao = input(login_banco())
        if (login_opcao == "e"):
            if fazer_login(banco):
                logged = True
                while logged:
                    opcao_operacao = input(menu_operacores())

                    if (opcao_operacao == "d"):
                        pass
                    elif (opcao_operacao == "s"):
                        pass
                    elif (opcao_operacao == "v"):
                        pass
                    elif (opcao_operacao == "c"):
                        pass
                    elif (opcao_operacao == "l"):
                        pass
                    elif (opcao_operacao == "e"):
                        logged = False
        elif (login_opcao == "c"):
            cadastrar_cliente(banco)
        elif (login_opcao == "s"):
            exit("----- FINALIZANDO O PROGRAMA! -----")


main()
