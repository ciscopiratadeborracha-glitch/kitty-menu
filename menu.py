import curses
import os
import subprocess
import sys
import time

MENU_DIR = os.path.expanduser("~/kitty-menu")

def comando(cmd):
    return subprocess.run(
        cmd,
        cwd=MENU_DIR,
        capture_output=True,
        text=True
    )

def atualizar_agora(tela):
    tela.clear()
    tela.addstr(2, 2, "Atualizando...")
    tela.refresh()

    resultado = comando(["git", "pull", "origin", "main"])

    tela.clear()
    tela.addstr(2, 2, "Resultado da atualização:")
    tela.addstr(4, 2, resultado.stdout[:70])
    tela.addstr(5, 2, resultado.stderr[:70])
    tela.addstr(7, 2, "Reiniciando menu...")
    tela.refresh()
    time.sleep(2)

    os.execv(sys.executable, [sys.executable] + sys.argv)

def procurar_atualizacao(tela):
    tela.clear()
    tela.addstr(2, 2, "Procurando atualização...")
    tela.refresh()

    comando(["git", "fetch", "origin", "main"])

    local = comando(["git", "rev-parse", "HEAD"]).stdout.strip()
    remoto = comando(["git", "rev-parse", "origin/main"]).stdout.strip()

    if local == remoto:
        mensagem(tela, "Seu menu já está atualizado.")
        return

    log = comando([
        "git", "log",
        "--oneline",
        "HEAD..origin/main"
    ]).stdout.strip()

    tela.clear()
    tela.addstr(1, 2, "NOVA ATUALIZAÇÃO ENCONTRADA")
    tela.addstr(2, 2, "===========================")

    linha = 4
    for item in log.splitlines()[:5]:
        tela.addstr(linha, 2, "- " + item[:65])
        linha += 1

    tela.addstr(linha + 1, 2, "Deseja atualizar agora?")
    tela.addstr(linha + 3, 2, "> Sim")
    tela.addstr(linha + 4, 2, "  Não")
    tela.refresh()

    escolha = 0

    while True:
        tecla = tela.getch()

        if tecla == curses.KEY_UP or tecla == curses.KEY_DOWN:
            escolha = 1 - escolha

        elif tecla in [10, 13, curses.KEY_ENTER]:
            if escolha == 0:
                atualizar_agora(tela)
            else:
                return

        tela.addstr(linha + 3, 2, ("> " if escolha == 0 else "  ") + "Sim")
        tela.addstr(linha + 4, 2, ("> " if escolha == 1 else "  ") + "Não")
        tela.refresh()

def mensagem(tela, texto):
    tela.clear()
    tela.addstr(2, 2, texto)
    tela.addstr(4, 2, "Pressione ENTER para voltar.")
    tela.refresh()

    while tela.getch() not in [10, 13, curses.KEY_ENTER]:
        pass

def desenhar(tela, titulo, opcoes, selecionado):
    tela.clear()
    tela.addstr(1, 2, titulo)
    tela.addstr(2, 2, "=" * len(titulo))

    for i, opcao in enumerate(opcoes):
        marcador = ">" if i == selecionado else " "
        tela.addstr(4 + i, 2, f"{marcador} {opcao}")

    tela.addstr(9, 2, "Use as setas ↑ ↓ e ENTER")
    tela.refresh()

def escolher(tela, titulo, opcoes):
    selecionado = 0

    while True:
        desenhar(tela, titulo, opcoes, selecionado)
        tecla = tela.getch()

        if tecla == curses.KEY_UP:
            selecionado = (selecionado - 1) % len(opcoes)

        elif tecla == curses.KEY_DOWN:
            selecionado = (selecionado + 1) % len(opcoes)

        elif tecla in [10, 13, curses.KEY_ENTER]:
            return selecionado

def main(tela):
    curses.curs_set(0)
    tela.keypad(True)

    while True:
        opcao = escolher(tela, "KITTY MENU", ["Configuração", "Sair"])

        if opcao == 0:
            config = escolher(tela, "CONFIGURAÇÃO", ["Procurar atualização", "Voltar"])

            if config == 0:
                procurar_atualizacao(tela)

        elif opcao == 1:
            break

curses.wrapper(main)
