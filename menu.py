import os
import time

def limpar():
    os.system("clear")

def procurar_atualizacao():
    limpar()
    print("================================")
    print("      PROCURAR ATUALIZAÇÃO")
    print("================================")
    print()
    print("Nenhum servidor configurado.")
    print("Em breve o sistema verificará atualizações online.")
    print()
    input("Pressione ENTER para voltar...")

def configuracao():
    while True:
        limpar()

        print("================================")
        print("        CONFIGURAÇÃO")
        print("================================")
        print()
        print("1 - Procurar atualização")
        print("0 - Voltar")
        print()

        opcao = input("Escolha: ")

        if opcao == "1":
            procurar_atualizacao()

        elif opcao == "0":
            break

def menu():
    while True:
        limpar()

        print("================================")
        print("         KITTY MENU")
        print("================================")
        print()
        print("1 - Configuração")
        print("0 - Sair")
        print()

        opcao = input("Escolha: ")

        if opcao == "1":
            configuracao()

        elif opcao == "0":
            print("Saindo...")
            time.sleep(1)
            break

menu()
