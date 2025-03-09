# Criar um sistema bancário com as operações: sacar, depositar e visualizar extrato.
# Mensagens, funções, variaveis em inglês para treinar o idioma.


# Declarando funções para realizar as operações
# Função de depósito
def deposit_money(value_deposit, bank_balance, bank_statement):
    if value_deposit > 0:  # Teste se o valor do deposito é positivo
        bank_balance += value_deposit  # Realizando o deposito
        # att o extrato
        bank_statement += f"Amount deposited: R${value_deposit:.2f}\n"
        print(
            # feedback para o usuario
            f"Amount deposited successfully. Current bank balance: R${bank_balance:.2f}")
    else:
        # feedback se o valor for negativo
        print("Invalid amount entered for deposit")
    # retorna esses valores para att das variaveis globais
    return bank_balance, bank_statement

# Função de saque


def withdraw_money(value_withdraw, bank_balance, bank_statement, withdraw_limit_value, withdrawal_number):
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
        bank_statement += f"Amount withdrawn: R${value_withdraw:.2f}\n"
        withdrawal_number += 1  # att qntd de saque realizado no dia
        # Feedback para o usuario
        print(f"Withdrawal successful. Current balance: R${bank_balance:.2f}")
        # retorna esses valores para att das variaveis globais
        return bank_balance, bank_statement, withdrawal_number

    return bank_balance, bank_statement, withdrawal_number


# Função da visualização do extrato bancário
# recebe saldo e extrato para exibir
def view_bank_statement(bank_balance, bank_statement):
    print("\n================ BANK STATEMENT ================")
    # Verifica se o extrato tá vazio ou não
    print("No movements were made." if not bank_statement else bank_statement)
    print(f"\nBank Balance: R$ {bank_balance:.2f}")  # exibe o saldo atual
    print("==========================================")


# Menu de controle das operações
menu = """
WELCOME TO THE BANKING SYSTEM MENU

[d] Deposit money
[w] Withdraw money
[v] View bank statement
[e] Exit

=> """
# Variavéis globais
bank_balance = 0
bank_statement = ""
withdrawal_number = 0

while True:

    option = input(menu)

    if option == "d":
        deposit_value = float(input("Enter the amount you wish to deposit: "))
        bank_balance, bank_statement = deposit_money(
            deposit_value, bank_balance, bank_statement)
    elif option == "w":
        withdraw_value = float(input("Enter the withdrawal amount: "))
        bank_balance, bank_statement, withdrawal_number = withdraw_money(
            withdraw_value, bank_balance, bank_statement, 500, withdrawal_number)
    elif option == "v":
        view_bank_statement(bank_balance, bank_statement)
    elif option == "e":
        break
    else:
        print("Invalid operation. Please enter a valid operation.")

# Dificuldades:
# Tive problemas com as váriaveis globais no sentido de conseguir mudá-lás após chamar a função
# Mas depois aprendi a realizar as mudanças de acordo com o retorno da função.
# No processo meu código ficou sem o return da linha 44, apenas depois do problema do retorno None da função
# Que percebi o erro de tratamento de retorno

# Aprendendo python aos poucos
