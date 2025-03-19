# Criar um sistema bancário com as operações: sacar, depositar e visualizar extrato.
# Mensagens, funções, variaveis em inglês para treinar o idioma.
# O desafio após o módulo de coleções é modelar o banco de dados por funções, o que fiz já na primeira versão
# Pelo qual motivo já tinha sido apresentado no módulo
# No entanto, vou atender os requisitos da v2 tais como: paramêtros especiais, novas funções e criatividade!


# Para deixar as transações mais realistas vou importar a data e hora

from datetime import datetime
# Declarando funções para realizar as operações
# Função de depósito


def deposit_money(value_deposit, bank_balance, transactions, /):  # Passagem apenas por posição
    if value_deposit > 0:  # Teste se o valor do deposito é positivo
        bank_balance += value_deposit  # Realizando o deposito
        # att transações
        data = datetime.now().strftime("%d/%m/%Y %H:%M")
        transaction = {"tipo": "Deposit",
                       "valor": value_deposit, "horario_data": data}
        transactions.append(transaction)

        print(
            # feedback para o usuario
            f"Amount deposited successfully. Current bank balance: R${bank_balance:.2f}")
    else:
        # feedback se o valor for negativo
        print("Invalid amount entered for deposit")
    # retorna esses valores para att das variaveis globais
    return bank_balance, transactions

# Função de saque


def withdraw_money(*, value_withdraw, bank_balance, transactions, withdraw_limit_value, withdrawal_number):
    WITHDRAWAL_LIMIT = 3  # limite de saque diário

    # Testando condições para realizar o saque
    if value_withdraw > withdraw_limit_value:  # Maior que o limite do saque
        print("Withdrawal amount is greater than the withdrawal limit - R$500")
    elif withdrawal_number >= WITHDRAWAL_LIMIT:  # Se realizou o limite diário
        print("Your daily withdrawal limit has already been reached")
    elif value_withdraw > bank_balance:  # Se o saque é maior que o saldo atual
        print("Withdrawal amount reported is greater than your current balance")
    else:  # Caso contrário realizar a operação de saque
        bank_balance -= value_withdraw  # Att saldo
        # Att extrato
        data = datetime.now().strftime("%d/%m/%Y %H:%M")
        transaction = {"tipo": "withdraw",
                       "valor": value_withdraw, "horario_data": data}
        transactions.append(transaction)
        withdrawal_number += 1  # att qntd de saque realizado no dia
        # Feedback para o usuario
        print(f"Withdrawal successful. Current balance: R${bank_balance:.2f}")
        # retorna esses valores para att das variaveis globais
        return bank_balance, transactions, withdrawal_number

    return bank_balance, transactions, withdrawal_number


# Função da visualização do extrato bancário
# recebe saldo e extrato para exibir
def view_bank_statement(bank_balance, /, *, transactions):
    print("\n================ BANK STATEMENT ================")
    # Verifica se transações estão vazias
    if not transactions:
        print("No movements were made.")
    else:
        for t in transactions:
            print(
                f"{t['horario_data']}: {t['tipo']} = R${t['valor']}")
            # exibe o saldo atual
    print(f"\nBank Balance: R$ {bank_balance:.2f}")
    print("==========================================")

# nessa v2 deve-se criar as funções criar usuário e criar conta corrente


def create_user(users):
    name_user = input("Informe o nome completo do usuário: ")
    date_user = input("Informe a data de nascimento do usuário: ")
    cpf_user = input("Informe o cpf do usuário: ")
    if check_cpf(cpf_user, users):
        print("Não foi é possível cadastrar usuário, usuário já cadastrado")
        return users

    end_user = input(
        """Informe o endereço (logradouro, bairro, cidade/sigla do estado)
    Exemplo: Rua José Amarantes, 447, Gerintim, Xique-Xique/BA""")

    user = {"name_user": name_user, "date_user": date_user, "cpf_user": cpf_user,
            "end_user": end_user}
    users.append(user)

    print("Usuário cadastrado com sucesso!")

    return users


def check_cpf(cpf, users):
    for user in users:
        if user["cpf_user"] == cpf:
            return user["cpf_user"]
    return False


def create_account(account, users, AGENCIA, num_conta):
    cpf_user = input("Informe o cpf do usuário para criar a conta")
    if check_cpf(cpf_user, users):
        new_account = {"Agencia": AGENCIA, "numero_conta": num_conta,
                       "usuario": check_cpf(cpf_user, users)}
        account.append(new_account)
        num_conta += 1

        print("Conta criada com sucesso!")
    else:
        print("Usuário não cadastrado no sistema")

    return account, num_conta


def list_users(users):
    print("\n================ LIST USERS ================")
    # Verifica se tem usuários existentes, caso contrário mostra a lista de usuários
    if not users:
        print("Nenhum usuário cadastrado")
    else:
        for user in users:
            print(
                f"nome:{user["name_user"]}, data de nascimento: {user["date_user"]} - CPF: {user["cpf_user"]}")


def list_accounts(accounts):
    print("\n================ LIST ACCOUNTS ================")
    if not accounts:
        print("Nenhuma conta cadastrado")
    else:
        for account in accounts:
            print(
                f"AGENCIA:{account["Agencia"]}, número da conta: {account["date_user"]} - CPF do titular: {account["usuario"]}")


# Menu de controle das operações
menu = """
WELCOME TO THE BANKING SYSTEM MENU

[d] Deposit money
[w] Withdraw money
[v] View bank statement
[nu] New user
[na] New account
[lu] List Users
[la] List Account
[e] Exit

=> """
# Variavéis globais
bank_balance = 0
bank_statement = ""
withdrawal_number = 0
withdraw_limit_value = 500

# Novas varíáveis para as novas funções
users = []
accounts = []
transactions = []
num_account = 1
AGENCIA = "0001"

while True:

    option = input(menu)

    if option == "d":
        deposit_value = float(input("Enter the amount you wish to deposit: "))
        bank_balance, transactions = deposit_money(
            deposit_value, bank_balance, transactions)
    elif option == "w":
        withdraw_value = float(input("Enter the withdrawal amount: "))
        bank_balance, transactions, withdrawal_number = withdraw_money(
            value_withdraw=withdraw_value,
            bank_balance=bank_balance,
            transactions=transactions,
            withdraw_limit_value=withdraw_limit_value,
            withdrawal_number=withdrawal_number)
    elif option == "v":
        view_bank_statement(bank_balance, transactions=transactions)
    elif option == "nu":
        users = create_user(users)
    elif option == "na":
        accounts, num_account = create_account(
            accounts, users, AGENCIA, num_account)
    elif option == "lu":
        list_users(users)
    elif option == "la":
        list_accounts(accounts)
    elif option == "e":
        break
    else:
        print("Invalid operation. Please enter a valid operation.")


# Aprendendo python aos poucos
