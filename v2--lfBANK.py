# Criar um sistema bancário com as operações: sacar, depositar e visualizar extrato.
# Mensagens, funções, variaveis em inglês para treinar o idioma.
# O desafio após o módulo de coleções é modelar o banco de dados por funções, o que fiz já na primeira versão
# Pelo qual motivo já tinha sido apresentado no módulo
# No entanto, vou atender os requisitos da v2 tais como: paramêtros especiais, novas funções e criatividade!


# Para deixar as transações mais realistas vou importar a data e hora

from datetime import datetime
# Declarando funções para realizar as operações
# Função de depósito


def login_system(*, cpf, password, users):
    for user in users:
        if user["cpf"] == cpf and user["password"] == password:
            print(f"WELCOME {user['name'].upper()}")
            return True

    print("User not registered!")
    return False


# Passagem apenas por posição
def deposit_money(accounts, num_account, value_deposit, /):
    if value_deposit > 0:  # Teste se o valor do deposito é positivo
        for account in accounts:
            if account["numero_conta"] == num_account:
                # Realizando o deposito
                account["bank_balance"] += value_deposit
                # att transações
                data = datetime.now().strftime("%d/%m/%Y %H:%M")
                transaction = {"tipo": "Deposit",
                               "valor": value_deposit, "horario_data": data}
                account["transactions"].append(transaction)
                # feedback para o usuario
                print(
                    f"Amount deposited successfully. Current bank balance: R${account['bank_balance']:.2f}")
    else:
        # feedback se o valor for negativo
        print("Invalid amount entered for deposit")


# Função de saque


def withdraw_money(*, accounts, num_account, value_withdraw, withdraw_limit_value, withdrawal_number):
    WITHDRAWAL_LIMIT = 3  # limite de saque diário
    account = None
    for acc in accounts:
        if acc["numero_conta"] == num_account:
            account = acc
    if account:
        # Testando condições para realizar o saque
        if value_withdraw > withdraw_limit_value:  # Maior que o limite do saque
            print("Withdrawal amount is greater than the withdrawal limit - R$500")
        elif withdrawal_number >= WITHDRAWAL_LIMIT:  # Se realizou o limite diário
            print("Your daily withdrawal limit has already been reached")
        # Se o saque é maior que o saldo atual
        elif value_withdraw > account["bank_balance"]:
            print("Withdrawal amount reported is greater than your current balance")
        else:  # Caso contrário realizar a operação de saque
            account["bank_balance"] -= value_withdraw
            # Att extrato
            data = datetime.now().strftime("%d/%m/%Y %H:%M")
            transaction = {"tipo": "withdraw",
                           "valor": value_withdraw, "horario_data": data}
            account["transactions"].append(transaction)
            withdrawal_number += 1  # att qntd de saque realizado no dia
            # Feedback para o usuario
            print(
                f"Withdrawal successful. Current balance: R${account['bank_balance']:.2f}")
            # retorna esses valores para att das variaveis globais
            return withdrawal_number
    else:
        print("Account not folder!")
    return withdrawal_number


# Função da visualização do extrato bancário
# recebe saldo e extrato para exibir
def view_bank_statement(num_account, accounts, /, *, transactions):
    print("\n================ BANK STATEMENT ================")
    conta = None
    for a in accounts:
        if a["numero_conta"] == num_account:
            conta = a
            break

    if not conta:
        print("Account not found!")
        return

    if not transactions:
        print("No transactions found.")
    else:
        for t in transactions:
            print(f"{t['horario_data']}: {t['tipo']} = R${t['valor']:.2f}")

    print(f"\nBalance: R$ {conta['bank_balance']:.2f}")
    print("==========================================")

# nessa v2 deve-se criar as funções criar usuário e criar conta corrente


def create_user(users, account, AGENCIA, num_conta):
    name = input("Full name: ")
    date = input("birth date: ")
    cpf = input("CPF: ")

    if check_cpf(cpf, users):
        print("Cannot register user, user already registered")
        return users

    end = input("Home address: ")
    password = input("Password for login: ")

    print("User successfully registered!")
    user = {"name": name, "date": date, "cpf": cpf,
            "end": end, "password": password, "accounts": []}
    conta, num_conta = create_account(cpf, account, AGENCIA, num_conta)
    user["accounts"].append(conta)
    users.append(user)

    return users, num_conta


def check_cpf(cpf, users):
    for user in users:
        if user["cpf"] == cpf:
            return True
    return False


def create_account(cpf, account, AGENCIA, num_conta):
    new_account = {"Agencia": AGENCIA, "numero_conta": num_conta,
                   "usuario": cpf, "bank_balance": 0, "transactions": []}
    account.append(new_account)
    num_conta += 1

    print("Your account has also been created, make transactions using your password!")

    return account, num_conta


def list_users(users):
    print("\n================ LIST USERS ================")
    # Verifica se tem usuários existentes, caso contrário mostra a lista de usuários
    if not users:
        print("Nenhum usuário cadastrado")
    else:
        for user in users:
            print(
                f"nome:{user['name']}, data de nascimento: {user['date']} - CPF: {user['cpf']}")


def list_accounts(accounts):
    print("\n================ LIST ACCOUNTS ================")
    if not accounts:
        print("Nenhuma conta cadastrado")
    else:
        for account in accounts:
            print(
                f"AGENCIA:{account['Agencia']}, número da conta: {account['numero_conta']} - CPF do titular: {account['usuario']}")


# Variavéis globais
withdrawal_number = 0
withdraw_limit_value = 500

# Novas varíáveis para as novas funções
users = []
accounts = []
num_account = 1
AGENCIA = "0001"

# Menu Inicial de Login
while True:

    login = """
WELCOME TO THE BANKING SYSTEM

[l] Login
[n] New User
[e] exit system

    """
    login_option = input(login)

    if login_option == "l":
        cpf = input("CPF USER: ")
        senha = input("PASSWORD USER: ")
        if login_system(cpf=cpf, password=senha, users=users):
            logged = True
            while logged:
                cpf_enter = cpf  # guardar cpf de login e menu de opções
                menu = """
    WELCOME TO THE BANKING SYSTEM MENU

    [d] Deposit money
    [w] Withdraw money
    [v] View bank statement
    [na] New account
    [la] List Account
    [e] Exit

    => """
                while True:

                    option = input(menu)

                    if option == "d":
                        deposit_value = float(
                            input("Enter the amount you wish to deposit: "))
                        deposit_money(accounts, num_account,
                                      deposit_value)
                    elif option == "w":
                        withdraw_value = float(
                            input("Enter the withdrawal amount: "))
                        withdrawal_number = withdraw_money(accounts=accounts, num_account=num_account,
                                                           value_withdraw=withdraw_value,
                                                           withdraw_limit_value=withdraw_limit_value,
                                                           withdrawal_number=withdrawal_number)
                    elif option == "v":
                        num_account_view = input(
                            "Informe o número para visualizar o extrato")
                        for account in accounts:
                            if account["numero_conta"] == num_account_view:
                                view_bank_statement(
                                    num_account_view, accounts, transactions=account["transactions"])
                    elif option == "na":
                        account, num_account = create_account(cpf_enter, accounts,
                                                              AGENCIA, num_account)

                        for user in users:
                            if user["cpf"] == cpf_enter:
                                user["accounts"].append(account)

                    elif option == "la":
                        list_accounts(accounts)
                    elif option == "e":
                        break
                    else:
                        print("Invalid operation. Please enter a valid operation.")
    elif login_option == "n":
        users, num_account = create_user(users, accounts, AGENCIA, num_account)
    elif login_option == "e":
        logged = False
        break

# Aprendendo python aos poucos
