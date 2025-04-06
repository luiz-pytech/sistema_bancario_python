# Toda modelagem inicial do sistema bancário utilizado POO.
from abc import ABC, abstractmethod
from datetime import datetime
import random

# Essa classe BANCO foi criada na necessidade de usar o login e não usar varíaveis globais para guardar clientes e contas


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

    def buscar_contas(self, numero_conta):
        for conta in self.contas:
            if (conta.numero_conta == numero_conta):
                return conta
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
        transacao.registrar_transacao(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

    @property
    def contas(self):
        return self._contas


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
            print("✅✅✅ Saque realizado com sucesso! ✅✅✅")
            return True

        else:
            print("---- Número Informado é inválido para transação! ----")

        return False

    def depositar(self, valor):

        if (valor > 0):
            self._saldo += valor
            print("✅✅✅ Valor depositado com Sucesso! ✅✅✅")
            return True

        print("---- Número Informado é inválido para transação! ----")
        return False

    def pix(self, valor, conta_destino):
        if (valor > self.saldo):
            print("---- Você não tem saldo suficiente ----")
            return False

        if (valor > 0):
            self._saldo -= valor
            conta_destino._saldo += valor
            print("✅✅✅ Pix realizado com sucesso! ✅✅✅")
            return True

        print("---- Número Informado é inválido para transação! ----")
        return False


class ContaCorrente(Conta):
    def __init__(self, numero_conta, cliente, limite=500, limite_saques=3, limite_pix=1000):
        super().__init__(numero_conta, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
        self.qnt_saques_realizados = 0
        self.limite_pix = limite_pix

    def sacar(self, valor):
        if (valor > self.limite):
            print("---- Valor maior que o limite do saque! ----")

        elif (self.qnt_saques_realizados >= self.limite_saques):
            print("---- O limite de saque diário já foi atingido! ----")
        else:
            self.qnt_saques_realizados += 1
            return super().sacar(valor)

        return False

    def pix(self, valor, conta_destino):
        if (valor > self.limite_pix):
            print("---- Valor maior que o limite do saque! ----")
            return False

        return super().pix(valor, conta_destino)

    def __str__(self):
        return f"""\
            Agência:\t{self._AGENCIA}
            C/C:\t\t{self._numero_conta}
            Titular:\t{self.cliente.nome}
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


class Pix(Transacao):
    def __init__(self, valor, conta_destino):
        super().__init__()
        self._valor = valor
        self._conta_destino = conta_destino

    @property
    def valor(self):
        return self._valor

    @property
    def conta_destino(self):
        return self._conta_destino

    def registrar_transacao(self, conta_envio):
        if conta_envio.pix(self._valor, self._conta_destino):
            conta_envio.historico.adicionar_transacao(self)
            self.conta_destino.historico.adicionar_transacao(self)
            return True
        return False

### Funções de amostragem de menus ###


def login_banco():
    login = """
┌──────────────────────────┐
│        LF BANK           │
├──────────────────────────┤
│ [e] Entrar na conta      │
│ [c] Criar conta          │
│ [s] Sair do sistema      │
└──────────────────────────┘
=> """
    return login


def menu_operacoes():
    menu = """
┌──────────────────────────┐
│    MENU PRINCIPAL        │
├──────────────────────────┤
│ [d] Depositar            │
│ [s] Sacar                │
│ [v] Ver extrato          │
│ [p] Transferir via PIX   │
│ [c] Nova conta           │
│ [l] Minhas contas        │
│ [e] Sair da conta        │
└──────────────────────────┘
=> """

    return menu

# Funções do menu de login


def cadastrar_cliente(banco):
    print("\n╔════════════════════════════╗")
    print("║    CADASTRO DE CLIENTE     ║")
    print("╚════════════════════════════╝")
    cpf = input("CPF:")

    if (banco.buscar_cliente(cpf)):
        print("\n⚠️⚠️⚠️ Cliente já cadastrado ⚠️⚠️⚠️")
        return
    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento (dd/mm/aaaa): ")
    endereco = input(
        "Endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(endereco, cpf, nome, data_nascimento)
    banco.cadastrar_cliente(cliente)
    print("\n✅✅✅ CLIENTE CADASTRADO COM SUCESSO ✅✅✅")
    print("SEJA BEM-VINDO AO LF BANK!")


def fazer_login(banco):
    cpf = input("\nInforme o CPF: \n==> ")
    cliente = banco.buscar_cliente(cpf)
    if cliente:
        print(f"\n ✨ Olá, {cliente.nome.upper()} ✨")
        return cliente

    print("⚠️⚠️⚠️ CLIENTE NÃO CADASTRADO! ⚠️⚠️⚠️")
    return False


# Operações do menu interno do BANCO (depositar, sacar, visualizar extrato)

def depositar_dinheiro(cliente):
    if not cliente._contas:
        print(
            f"⚠️⚠️⚠️ {cliente._nome} você não tem conta cadastrada, é necessário criar uma conta! ⚠️⚠️⚠️")
        return
    else:
        print("\n╔════════════════════════════╗")
        print("║        DEPÓSITO            ║")
        print("╚════════════════════════════╝")
        conta = cliente.contas[0]
        if len(cliente.contas) > 1:
            i = 1
            for conta in cliente._contas:
                print(
                    f"[{i}] - Número da conta: {conta.numero_conta} -- Saldo R$: {conta.saldo}")
                i += 1
        # Conta para realizar a transacao
        num_conta_transacao = int(input(
            "\nInforme o número da conta pra transacao: \n ==> ")) - 1
        conta = cliente._contas[num_conta_transacao]
        if (num_conta_transacao < 0 or num_conta_transacao > len(cliente._contas)):
            print("⚠️⚠️⚠️ Número de conta inválido! ⚠️⚠️⚠️")
            return

    valor_deposito = float(input("\nInforme o valor para depósito: \n==>"))
    transacao = Deposito(valor_deposito)
    if (cliente.realizar_transacao(conta, transacao)):
        print("✅✅✅ DEPÓSITO REALIZADO COM SUCESSO! ✅✅✅")


def sacar_dinheiro(cliente):

    if not cliente._contas:
        print(
            f"⚠️⚠️⚠️ {cliente._nome} você não tem conta cadastrada, é necessário criar uma conta! ⚠️⚠️⚠️")
        return
    else:
        print("\n╔════════════════════════════╗")
        print("║          SAQUE             ║")
        print("╚════════════════════════════╝")
        conta = cliente.contas[0]
        if len(cliente.contas) > 1:
            i = 1
            for conta in cliente._contas:
                print(
                    f"[{i}] - Número da conta: {conta.numero_conta} -- Saldo R$: {conta.saldo}")
                i += 1
    # Conta para realizar a transacao
        num_conta_transacao = int(input(
            "\nInforme o número da conta pra transacao: \n ==> ")) - 1
        conta = cliente._contas[num_conta_transacao]
        if (num_conta_transacao < 0 or num_conta_transacao > len(cliente._contas)):
            print("⚠️⚠️⚠️ Número de conta inválido! ⚠️⚠️⚠️")
            return

    valor_saque = float(input("\nInforme o valor para saque: \n==> "))

    transacao = Saque(valor_saque)
    if (cliente.realizar_transacao(conta, transacao)):
        print("✅✅✅ Saque realizado com sucesso ✅✅✅")


def visualizar_extrato(cliente):
    if not cliente.contas:
        print(
            f"⚠️⚠️⚠️ {cliente._nome} você não tem conta cadastrada, é necessário criar uma conta! ⚠️⚠️⚠️")
        return
    elif len(cliente.contas) == 1:
        conta = cliente.contas[0]
    elif len(cliente.contas) > 1:
        i = 1
        for conta in cliente.contas:
            print(
                f"[{i}] - Número da conta: {conta.numero_conta} -- Saldo R$: {conta.saldo}")
            i = i + 1
        # Conta para realizar a transacao
        num_conta_transacao = int(input(
            "\nInforme o número da conta pra transacao: \n ==> ")) - 1
        conta = cliente._contas[num_conta_transacao]
        if (num_conta_transacao < 0 or num_conta_transacao > len(cliente._contas)):
            print("⚠️⚠️⚠️ Número de conta inválido! ⚠️⚠️⚠️")
            return

    print("\n╔════════════════════════════════════╗")
    print("║            EXTRATO                 ║")
    print("╠════════════════════════════════════╣")
    extrato = ""
    transacoes = conta.historico.transacoes
    if not transacoes:
        extrato = "  Nenhuma transação realizada."
    else:
        for t in transacoes:
            extrato += (f"\n{t['data']} - {t['tipo']}: R${t['valor']:.2f}")
    print(extrato)
    print(f"\nSaldo: R$ {conta.saldo:.2f}")
    print("\n\n╚════════════════════════════════════╝")


def criar_nova_conta(cliente, banco):
    conta = ContaCorrente.nova_conta(cliente, str(random.randint(1000, 9999)))
    banco.cadastrar_conta(conta)

    print("✅✅✅ NOVA CONTA CADASTRADA COM SUCESSO ✅✅✅")


def listar_contas(cliente):
    if not cliente.contas:
        print(
            f"⚠️⚠️⚠️ {cliente._nome} você não tem conta cadastrada, é necessário criar uma conta! ⚠️⚠️⚠️")
        return
    else:
        print("\n╔════════════════════════════╗")
        print("║     SUAS CONTAS            ║")
        print("╠════════════════════════════╣")
        for conta in cliente.contas:
            print(f"  ➤ Conta: {conta.numero_conta}")
            print(f"    Agência: {conta.agencia}")
            print(f"    Saldo: R$ {conta.saldo:.2f}")
            print("╟────────────────────────────╢")
        print("╚════════════════════════════╝")


def enviar_pix(cliente, banco):
    # numero da conta de destino
    numero_conta = str(input("Informe o numero da conta de destino: \n==> "))
    conta_destino = banco.buscar_contas(
        numero_conta)  # recuperando conta destino
    if not conta_destino:
        print("⚠️⚠️⚠️ CONTA NÃO EXISTENTE! ⚠️⚠️⚠️")  # Testando existência
    else:
        if not cliente._contas:
            print(
                f"⚠️⚠️⚠️ {cliente._nome} você não tem conta cadastrada, é necessário criar uma conta! ⚠️⚠️⚠️")
            return
        else:
            print("\n╔════════════════════════════╗")
            print("║    TRANSFERÊNCIA PIX       ║")
            print("╚════════════════════════════╝")
            print("Seleciona a conta para fazer sua operação: \n")
            if len(cliente.contas) > 1:
                i = 1
                for conta in cliente._contas:
                    print(
                        f"[{i}] - Número da conta: {conta.numero_conta} -- Saldo R$: {conta.saldo}")
                    i += 1
            num_conta_transacao = int(input(
                "\n==> ")) - 1
            conta_envio = cliente._contas[num_conta_transacao]
            if (num_conta_transacao < 0 or num_conta_transacao > len(cliente._contas)):
                print("⚠️⚠️⚠️ Número de conta inválido! ⚠️⚠️⚠️")
                return

    valor_pix = float(input("Informe o valor: \n==> "))
    transacao = Pix(valor_pix, conta_destino)
    if (cliente.realizar_transacao(conta_envio, transacao)):
        print("✅✅✅ Pix realizado com sucesso! ✅✅✅")


def main():
    banco = Banco()

    # Cliente 1
    cliente1 = PessoaFisica(
        endereco="Rua A, 123 - Centro - São Paulo/SP",
        cpf="12345678901",
        nome="João Silva",
        data_nascimento="15/05/1980"
    )

    # Cliente 2
    cliente2 = PessoaFisica(
        endereco="Av. B, 456 - Jardim - Rio de Janeiro/RJ",
        cpf="98765432109",
        nome="Maria Oliveira",
        data_nascimento="20/11/1990"
    )

    banco.cadastrar_cliente(cliente1)
    banco.cadastrar_cliente(cliente2)
    conta1 = ContaCorrente(
        numero_conta="1001",
        cliente=cliente1
    )

    # Conta para Maria
    conta2 = ContaCorrente(
        numero_conta="1002",
        cliente=cliente2,
        limite=1000  # Limite especial
    )
    conta3 = ContaCorrente(
        numero_conta="1003",
        cliente=cliente2,
        limite=200
    )

    banco.cadastrar_conta(conta1)
    banco.cadastrar_conta(conta2)
    banco.cadastrar_conta(conta3)

    while True:
        login_opcao = input(login_banco()).lower()
        if (login_opcao == "e"):
            cliente_logged = fazer_login(banco)
            if cliente_logged:
                logged = True
                while logged:
                    opcao_operacao = input(menu_operacoes()).lower()

                    if (opcao_operacao == "d"):
                        depositar_dinheiro(cliente_logged)
                    elif (opcao_operacao == "s"):
                        sacar_dinheiro(cliente_logged)
                    elif (opcao_operacao == "v"):
                        visualizar_extrato(cliente_logged)
                    elif (opcao_operacao == "c"):
                        criar_nova_conta(cliente_logged, banco)
                    elif (opcao_operacao == "l"):
                        listar_contas(cliente_logged)
                    elif (opcao_operacao == "p"):
                        enviar_pix(cliente_logged, banco)
                    elif (opcao_operacao == "e"):
                        logged = False
        elif (login_opcao == "c"):
            cadastrar_cliente(banco)
        elif (login_opcao == "s"):
            exit("----- FINALIZANDO O PROGRAMA! -----")


main()
