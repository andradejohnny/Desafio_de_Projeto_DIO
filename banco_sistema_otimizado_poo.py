import textwrap
from abc import ABC, abstractmethod, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        #Dados privados
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    # Método de classe que cria uma nova conta.
    # 'cls' refere-se à própria classe 'Conta'.
    # Retorna uma nova instância da classe 'Conta' com os parâmetros 'numero' e 'cliente'.
    @classmethod #-> Um método de classe é um método que está associado à classe em si, e não a uma instância específica da classe. Ele é chamado usando a própria classe e pode acessar e modificar o estado da classe. No caso, nova_conta é usado para criar uma nova instância da classe Conta.
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property #-> As propriedades são usadas para fornecer uma interface de acesso controlado a atributos privados. Elas permitem que você leia o valor de um atributo como se estivesse acessando uma variável, mas com a segurança de um método.
    def saldo(self): #Propriedade que retorna o saldo da conta.
        return self._saldo
    
    @property
    def numero(self): #Propriedade que retorna o número da conta.
        return self._numero
    
    @property
    def agencia(self): #Propriedade que retorna o número da agência.
        return self._agencia
    
    @property
    def cliente(self): #Propriedade que retorna o cliente associado à conta.
        return self._cliente
    
    @property
    def historico(self): #Propriedade que retorna o histórico da conta.
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
          print("Erro de operação!!! -> Você não tem saldo suficiente.")

        elif valor > 0:
          self._saldo -= valor
          print("\n Saque realizado com sucesso!")
          return True

        else:
          print("Erro de operação!!! -> Valor inválido.")

        return False
              
    def depositar(self, valor):
      if valor > 0:
            self._saldo += valor
            print("Deposito efetuado com sucesso!") 
      else:
            print("Valor inválido!")
            return False

      return True
    
class ContaCorrente(Conta): # A classe 'ContaCorrente' herda da classe 'Conta'.
    def __init__(self, numero, cliente, limite=500, limite_saques=3): 
        # Método inicializador da classe 'ContaCorrente'.
        # Define atributos adicionais além dos herdados de 'Conta'.
        super().__init__(numero, cliente) # Chama o inicializador da classe pai 'Conta' passando 'numero' e 'cliente'.
        self._limite = limite # Define o limite de saque diário. O padrão é 500.
        self._limite_saques = limite_saques # Define o número limite de saques diários. O padrão é 3.
    
    def sacar(self, valor): # Método que realiza um saque, com regras específicas para 'ContaCorrente'.
        
        
        # Conta o número de saques realizados até agora.
        # Filtra as transações no histórico para contar quantas são do tipo 'Saque'.
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__])

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor) # Se as verificações forem aprovadas, chama o método 'sacar' da classe pai 'Conta'.
        
        return False  #Retorna 'False' se o saque falhou.
    
    def __str__(self) -> str: 
        # Método especial que retorna uma string representando o objeto.
        # Usado para fornecer uma representação textual da conta corrente.
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico: # Define a classe 'Historico' que gerencia uma lista de transações associadas a uma conta.

    def __init__(self):
        self._transacoes = []  # Inicializa um atributo privado '_transacoes' como uma lista vazia, esta lista será usada para armazenar as transações da conta.

    @property
    def transacoes(self):  # Define uma propriedade 'transacoes' que permite acessar o atributo privado '_transacoes'.
        return self._transacoes  # Retorna a lista de transações, permite acesso controlado ao atributo '_transacoes' fora da classe.
    
    def adicionar_transacao(self, transacao): # Define um método 'adicionar_transacao' que adiciona uma nova transação à lista de transações.
        
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,  # Adiciona um dicionário à lista '_transacoes'.
                "valor": transacao.valor, # A chave 'valor' armazena o valor da transação acessando o atributo 'valor' do objeto 'transacao'.
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"), #módulo date time, pegando data atual do sistema e formatar
            }
        )

class Transacao(ABC): # Define a classe 'Transacao' como uma classe abstrata.
    @property
    @abstractmethod
    def valor(self): # Define uma propriedade abstrata chamada 'valor'.
        pass
    
    @abstractmethod
    def registrar(self, conta): # Define um método de classe abstrato chamado 'registrar', este método deve ser implementado em qualquer subclasse que herde de 'Transacao'.
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)



def menu():
    menu = """\n
    ---------- MENU ----------

    [d]  Depositar
    [s]  Sacar
    [e]  Extrato
    [nc] Nova Conta
    [nu] Novo Usuário
    [q] Sair

    => """
    return input(textwrap.dedent(menu))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n Cliente não possui conta! ")
        return
    
    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nliente não encontrado!")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\ná existe cliente com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("\n=== Cliente criado com sucesso! ===")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nliente não encontrado, fluxo de criação de conta encerrado!")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("\n=== Conta criada com sucesso! ===")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))



def main():
    clientes = []
    contas = []

    while True:
      opcao = menu()

      if opcao == "d":
        depositar(clientes)
      
      elif opcao == "s":
        sacar(clientes)

      elif opcao == "e":
          exibir_extrato(clientes)
            
      elif opcao == "q":
        break

      elif opcao == "nc":
          numero_conta = len(contas) + 1
          criar_conta(numero_conta, clientes, contas)
          
      elif opcao == "nu":
          criar_cliente(clientes)

      elif opcao == "lc":
          listar_contas(contas)

      else:
        print("Operação inválida, por favor selecione novamente a operação desejada!")
      
  

main()

