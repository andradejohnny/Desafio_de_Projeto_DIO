import textwrap

def menu():
    menu = """\n
    ---------- MENU ----------

    [d]  Depositar
    [s]  Sacar
    [e]  Extrato
    [nc] Nova Conta
    [nu] Novo Usuário
    [q] Sair
nu
    => """
    return input(textwrap.dedent(menu))

def depositar(saldo, valor, extrato, /): #Deve receber os argumentos apenas por posição
  if valor > 0:
    saldo += valor
    print("Deposito efetuado com sucesso!") 
    extrato += f"Depósito: R$ {valor:.2f}\n"
  else:
    print("Valor inválido!")

  return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saques = numero_saques >= limite_saques
    excedeu_saldo = valor > saldo
    excedeu_limite = valor> limite



    if excedeu_saldo:
            print("Erro de operação!!! -> Você não tem saldo suficiente.")

    elif excedeu_saques:
            print("Erro de operação!!! -> Ultrapassou o limite diário de saques!!!.")

    elif excedeu_limite:
             print("Erro de operação!!! -> O valor do saque ultrapassa o limite.")

    elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1
            print("\n Saque realizado com sucesso!")

    else:
            print("Erro de operação!!! -> Valor inválido.")
          
    return saldo, extrato

def exibir_extrato(saldo, /, *, extrato):
     print("\n================ EXTRATO ================")
     print("Não foram realizadas movimentações." if not extrato else extrato)
     print(f"\nSaldo: R$ {saldo:.2f}")
     print("==========================================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n Já existe um usuario cadastrado com esse CPF no sistema! ")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe seu endereço: ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco}) #estrutura de dicionario

    print("Usuario criado com sucesso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf] #compressão de listas com um filtro

    return usuarios_filtrados[0] if usuarios_filtrados else None #Verifica se usuarios Filtrados tem conteudo, se não for uma lista vazia retorna o primeiro usuario (funciona por ter a possibilidade de cadastrar somente um cpf)

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n Conta criada com sucesso! ")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\n  Usuario não encontrado, fluxo de criação de conta encerrado! ")
    return None



def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    usuarios = []
    contas = []

    while True:
      opcao = menu()

      if opcao == "d":
        print("Depósito")
        valor = float(input("informe o valor dos depósitos: "))

        saldo, extrato = depositar(saldo, valor, extrato) #Passa os dados dessas formas pois a função recebe os argumentos apenas por posição
      
      elif opcao == "s":
        print("Saque")
        valor = float(input("Informe o valor do saque: "))

        saldo, extrato = sacar(saldo=saldo, valor=valor, extrato=extrato, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES) #Passa os dados dessas formas pois a função recebe os argumentos apenas por nome

      elif opcao == "e":
          print("Extrato")
          exibir_extrato(saldo, extrato=extrato) #Passa os dados dessas formas pois a função recebe os argumentos por posição e por nome
            
      elif opcao == "q":
        break

      elif opcao == "nc":
          numero_conta = len(contas) + 1
          conta = criar_conta(AGENCIA, numero_conta, usuarios)

          if conta:
              contas.append(conta)
          
      elif opcao == "nu":
          criar_usuario(usuarios)

      else:
        print("Operação inválida, por favor selecione novamente a operação desejada!")
      
  

main()
