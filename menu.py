import os
import time
import subprocess
import sys

PASTA_MENU = os.path.expanduser("~/kitty-menu")

def limpar():
    os.system("clear")

def procurar_atualizacao():
    limpar()
    print("================================")
    print("      PROCURAR ATUALIZAÇÃO")
    print("================================")
    print()

    try:
        os.chdir(PASTA_MENU)

        print("Verificando atualizações...")
        subprocess.run(["git", "fetch"], check=True)

        local = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
        remoto = subprocess.check_output(["git", "rev-parse", "origin/main"]).decode().strip()

        if local == remoto:
            print()
            print("Seu menu já está atualizado.")
            input("\nPressione ENTER para voltar...")
        else:
            print()
            print("Atualização encontrada!")
            print("Atualizando...")
            subprocess.run(["git", "pull"], check=True)

            print()
            print("Atualização concluída!")
            print("Reiniciando o menu...")
            time.sleep(2)
            os.execv(sys.executable, [sys.executable] + sys.argv)

    except Exception as erro:
        print()
        print("Erro ao procurar atualização:")
        print(erro)
        input("\nPressione ENTER para voltar...")

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
