import os
from datetime import datetime
if not os.path.exists('users.txt'):
    with open('users.txt', 'w') as file:
        file.write(f'C0001,admin,1234\n')



# Creat customer_id
def auto_creat_customer_id():
    if not os.path.exists('customers.txt'):
        customer_id = 'C0002'
    else:
        with open('customers.txt', 'r') as file:
            for line in file:
                old_customer_id = line.split(',')[0]
            int_part = int(old_customer_id[1:])
        customer_id = (f'C{(int_part + 1):04}')    
    return customer_id

auto_creat_customer_id()


def auto_creat_account_no():
    if not os.path.exists('accounts.txt'):
        account_no = 10000
        return account_no
    else:
        with open('accounts.txt', 'r') as file:
            for line in file:
                account_no = line.split(',')[0]
        return int(account_no) + 1

def creat_account(customer_id, amount):
    account_no = auto_creat_account_no()
    balance = amount
    with open('accounts.txt', 'a') as file:
        file.write(f'{account_no},{customer_id},{balance}\n')
    return account_no


# Creat customer
def creat_customer():
    name = input('Enter Your Name: ')
    address = input('Enter Your Addess: ')
    customer_id = auto_creat_customer_id()

    amount = float(input('Enter Amount Open Balance'))
    account_no = creat_account(customer_id, amount)
    username = input('Enter Your username : ')
    password = input('Enter Your password : ')
    with open('users.txt', 'a') as file:
        file.write(f'{customer_id},{username},{password}\n')
    with open('customers.txt', 'a') as file:
        file.write(f'{customer_id},{name},{address},{account_no}\n')
# creat_customer()


    

def get_amount():
    while True:
        try:
            amount = float(input('Enter Amound: '))
            if amount > 0:
                return amount
            else:
                print('Enter Correct Amount.')        
        except ValueError:
            print('Enter Number only.')

def deposit(account_no):
    amount = get_amount()
    with open('accounts.txt', 'r') as file:
        to_write=[]
        for line in file:
            get_line = line.strip().split(',')
            balance = float(get_line[2])
            if int(get_line[0]) == account_no:
                new_balance = balance + amount 
                to_write.append(f'{get_line[0]},{get_line[1]},{new_balance}')
            else:
                to_write.append(f'{get_line[0]},{get_line[1]},{balance}')
    with open('accounts.txt', 'w') as file:
        for i in range(len(to_write)):
            file.write(f'{to_write[i]},\n')
    date_time=datetime.today().replace(microsecond=0)
    with open('transactions.txt','a') as file:
        file.write(f"{date_time},{account_no},Deposit,{amount},{new_balance}")
    print("Deposit successfull.\n")

def withdraw(account_no):
    amount = get_amount()
    with open('accounts.txt', 'r') as file:
        to_write=[]
        for line in file:
            get_line = line.strip().split(',')
            balance = float(get_line[2])
            if int(get_line[0]) == account_no:
                new_balance = balance - amount 
                to_write.append(f'{get_line[0]},{get_line[1]},{new_balance}')
            else:
                to_write.append(f'{get_line[0]},{get_line[1]},{balance}')
    with open('accounts.txt', 'w') as file:
        for i in range(len(to_write)):
            file.write(f'{to_write[i]},\n')
    date_time=datetime.today().replace(microsecond=0)
    with open('transactions.txt','a') as file:
        file.write(f"{date_time},{account_no},Withdraw,{amount},{new_balance}")
    print("Withdraw successfull.\n")

def balance(account_no):
    try:
        with open('accounts.txt', 'r') as file:
            for line in file:
                account = line.strip().split(',')
                if int(account[0])  == account_no:
                    balance = account[2]
        print(f'Your Balance Is: ${balance}')
    except UnboundLocalError:
        print("Account number is not correct...\nPlease try again")


def transaction(account_no):
    print(f"TRANSACTION HISTORY OF {account_no}\n")
    print("date\t\t\ttransactiontype\t\tamount\t\tbalance")
    with open('transactions.txt','r') as file:
        for line in file:
            transaction = line.strip().split(',')
            if int(transaction[1]) == account_no:
                print(f"{transaction[0]}\t{transaction[2]}\t\t\t{transaction[3]}\t{transaction[4]}\n")




def admin_menu():
    while True:
        print('\n----------WELCOME TO THE MINIBANK----------\n')
        print('1. Creat customer')
        print('2. Creat Accout')
        print('3. Deposit Money')
        print('4. Withdraw Money')
        print('5. Check Balance')
        print('6. Transaction History')
        print('7. Exit')
        choice = input('Enter Your selection: ')

        if choice == '1':
            creat_customer()

        elif choice == '3':
            deposit(int(input("Enter account number for deposit : ")))
        elif choice == '4':
            withdraw(int(input("Enter account number for withdraw : ")))
        elif choice == '5':
            balance(int(input("Enter account number for get balance : ")))
        elif choice == '6':
            transaction(int(input("Enter account number for get transaction history : ")))
        elif choice == '7':
            exit()
       

# menu

def user_menu(customer_id):
    with open('customers.txt','r') as file:
        for line in file:
            customer = line.strip().split(',')
            if customer_id == customer[0]:
                account_no = int(customer[3])
    while True:
        print('\n======MAIN MANU======')
        print('1. deposit')
        print('2. withraw')
        print('3. balance')
        print('4. Transaction History')
        print('5. exit')

        choice = input('choose an option (1-4):')
        if choice == '1':
            deposit(account_no)
        elif choice == '2':
            withdraw(account_no)
        elif choice == '3':
            balance(account_no)
        elif choice == '4':
            transaction(account_no)
        elif choice == '5':
            exit()
        else:
            print('❌Invalid choice... Try Again')
            
        




def login():
    username = input('Enter Your username : ')
    password = input('Enter Your password : ')
    with open('users.txt', 'r') as file:
        for line in file:
            user = line.strip().split(',')
            if username ==  user[1] and password == user[2]:
                if username =="admin":
                    print('\nAdmin Login successful...\n')
                    admin_menu()
                    break
                else:
                    customer_id  = user[0]
                    print('\nusser Login successful...\n')
                    user_menu(customer_id)
                    break

        else:
            print('\ninvalid username pass\n')
login()