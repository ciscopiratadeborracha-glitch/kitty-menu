import curses
import os
import subprocess
import sys
import time

PASTA_MENU = os.path.expanduser("~/kitty-menu")

def procurar_atualizacao(tela):
    tela.clear()
    tela.addstr(1, 2, "PROCURAR ATUALIZAÇÃO")
    tela.addstr(3, 2, "Verificando atualizações...")
    tela.refresh()

    try:
        os.chdir(PASTA_MENU)

        subprocess.run(["git", "fetch"], check=True)

        local = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
        remoto = subprocess.check_output(["git", "rev-parse", "origin/main"]).decode().strip()

        if local == remoto:
            tela.addstr(5, 2, "Seu menu já está atualizado.")
            tela.addstr(7, 2, "Pressione ENTER para voltar.")
            tela.refresh()
            esperar_enter(tela)
        else:
            tela.addstr(5, 2, "Atualização encontrada!")
            tela.addstr(6, 2, "Atualizando...")
            tela.refresh()

            subprocess.run(["git", "pull"], check=True)

            tela.addstr(8, 2, "Atualização concluída!")
            tela.addstr(9, 2, "Reiniciando menu...")
            tela.refresh()
            time.sleep(2)

            os.execv(sys.executable, [sys.executable] + sys.argv)

    except Exception as erro:
        tela.addstr(5, 2, "Erro ao procurar atualização:")
        tela.addstr(6, 2, str(erro))
        tela.addstr(8, 2, "Pressione ENTER para voltar.")
        tela.refresh()
        esperar_enter(tela)

def esperar_enter(tela):
    while True:
        tecla = tela.getch()
        if tecla in [10, 13, curses.KEY_ENTER]:
            break

def desenhar_menu(tela, titulo, opcoes, selecionado):
    tela.clear()

    tela.addstr(1, 2, "================================")
    tela.addstr(2, 2, f"        {titulo}")
    tela.addstr(3, 2, "================================")

    for i, opcao in enumerate(opcoes):
        y = 5 + i

        if i == selecionado:
            tela.addstr(y, 2, f"> {opcao}")
        else:
            tela.addstr(y, 2, f"  {opcao}")

    tela.addstr(10, 2, "Use ↑ ↓ ou W/S para mover")
    tela.addstr(11, 2, "ENTER para escolher")
    tela.refresh()

def menu_configuracao(tela):
    opcoes = ["Procurar atualização", "Voltar"]
    selecionado = 0

    while True:
        desenhar_menu(tela, "CONFIGURAÇÃO", opcoes, selecionado)

        tecla = tela.getch()

        if tecla in [curses.KEY_UP, ord("w"), ord("W")]:
            selecionado -= 1
            if selecionado < 0:
                selecionado = len(opcoes) - 1

        elif tecla in [curses.KEY_DOWN, ord("s"), ord("S")]:
            selecionado += 1
            if selecionado >= len(opcoes):
                selecionado = 0

        elif tecla in [10, 13, curses.KEY_ENTER]:
            if selecionado == 0:
                procurar_atualizacao(tela)
            elif selecionado == 1:
                break

def menu_principal(tela):
    curses.curs_set(0)
    tela.keypad(True)

    opcoes = ["Configuração", "Sair"]
    selecionado = 0

    while True:
        desenhar_menu(tela, "KITTY MENU", opcoes, selecionado)

        tecla = tela.getch()

        if tecla in [curses.KEY_UP, ord("w"), ord("W")]:
            selecionado -= 1
            if selecionado < 0:
                selecionado = len(opcoes) - 1

        elif tecla in [curses.KEY_DOWN, ord("s"), ord("S")]:
            selecionado += 1
            if selecionado >= len(opcoes):
                selecionado = 0

        elif tecla in [10, 13, curses.KEY_ENTER]:
            if selecionado == 0:
                menu_configuracao(tela)
            elif selecionado == 1:
                break

curses.wrapper(menu_principal)
