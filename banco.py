
menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

  opcao = input(menu)
  
  if opcao == "d":
    print("Depósito")
    valor = float(input("informe o valor dos depósitos: "))
    if valor > 0:
        saldo += valor
        print("Deposito efetuado com sucesso!") 
        extrato += f"Depósito: R$ {valor:.2f}\n"
    else:
        print("Valor inválido!")


  elif opcao == "s":
    print("Saque")
    valor = float(input("Informe o valor do saque: "))


    excedeu_saques = numero_saques >= LIMITE_SAQUES

    if valor > saldo:
      print("Erro de operação!!! -> Você não tem saldo suficiente.")

    elif numero_saques >= LIMITE_SAQUES:
      print("Erro de operação!!! -> Ultrapassou o limite diário de saques!!!.")

    elif valor > limite:
      print("Erro de operação!!! -> O valor do saque ultrapassa o limite.")

    elif valor > 0:
      saldo -= valor
      extrato += f"Saque: R$ {valor:.2f}\n"
      numero_saques += 1

    else:
      print("Erro de operação!!! -> Valor inválido.")

  elif opcao == "e":
    print("Extrato")
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")
  
  elif opcao == "q":
    break

  else:
    print("Operação inválida, por favor selecione novamente a operação desejada!")
  
  