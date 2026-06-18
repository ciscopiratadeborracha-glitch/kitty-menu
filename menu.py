import curses
import os
import shutil
import subprocess
import sys

APPS = [
    {"nome": "Firefox", "cmd": "firefox", "instalar": "sudo apt install firefox -y"},
    {"nome": "VS Code", "cmd": "code", "flatpak": "com.visualstudio.code", "instalar": "flatpak install flathub com.visualstudio.code -y"},
    {"nome": "VLC", "cmd": "vlc", "instalar": "sudo apt install vlc -y"},
    {"nome": "Discord", "cmd": "discord", "flatpak": "com.discordapp.Discord", "instalar": "flatpak install flathub com.discordapp.Discord -y"},
    {"nome": "Telegram", "cmd": "telegram-desktop", "flatpak": "org.telegram.desktop", "instalar": "flatpak install flathub org.telegram.desktop -y"},
    {"nome": "Steam", "cmd": "steam", "flatpak": "com.valvesoftware.Steam", "instalar": "flatpak install flathub com.valvesoftware.Steam -y"},
]

def rodar(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def app_instalado(app):
    if shutil.which(app["cmd"]):
        return True

    if "flatpak" in app and shutil.which("flatpak"):
        r = rodar(f"flatpak list --app | grep {app['flatpak']}")
        return r.returncode == 0

    return False

def abrir_app(app):
    if shutil.which(app["cmd"]):
        os.system(f"nohup {app['cmd']} >/dev/null 2>&1 &")
    elif "flatpak" in app:
        os.system(f"nohup flatpak run {app['flatpak']} >/dev/null 2>&1 &")

def mensagem(tela, texto):
    tela.clear()
    tela.addstr(2, 2, texto)
    tela.addstr(4, 2, "Pressione ENTER para voltar.")
    tela.refresh()

    while tela.getch() not in [10, 13, curses.KEY_ENTER]:
        pass

def confirmar(tela, titulo, pergunta):
    escolha = 0
    opcoes = ["Sim", "Não"]

    while True:
        desenhar(tela, titulo, opcoes, escolha)
        tela.addstr(12, 2, pergunta[:70])
        tela.refresh()

        tecla = tela.getch()

        if tecla == curses.KEY_UP:
            escolha = (escolha - 1) % len(opcoes)
        elif tecla == curses.KEY_DOWN:
            escolha = (escolha + 1) % len(opcoes)
        elif tecla in [10, 13, curses.KEY_ENTER]:
            return escolha == 0

def instalar_app(tela, app):
    if app_instalado(app):
        mensagem(tela, f"{app['nome']} já está instalado.")
        return

    if confirmar(tela, app["nome"], f"{app['nome']} não está instalado. Deseja instalar?"):
        curses.endwin()
        os.system(app["instalar"])
        input("\nPressione ENTER para voltar ao menu...")

def atualizar(tela):
    curses.endwin()
    os.system("cd ~/kitty-menu && git pull origin main")
    input("\nPressione ENTER para voltar ao menu...")
    os.execv(sys.executable, [sys.executable] + sys.argv)

def desenhar(tela, titulo, opcoes, selecionado):
    tela.clear()
    tela.addstr(1, 2, "═══════════════════════════════")
    tela.addstr(2, 2, "          カウアン")
    tela.addstr(3, 2, "═══════════════════════════════")

    tela.addstr(5, 2, titulo)
    tela.addstr(6, 2, "─" * len(titulo))

    for i, opcao in enumerate(opcoes):
        marcador = ">" if i == selecionado else " "
        tela.addstr(8 + i, 2, f"{marcador} {opcao}")

    tela.addstr(18, 2, "↑ ↓ para navegar | ENTER para selecionar")
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

def menu_aplicativos(tela):
    opcoes = [app["nome"] for app in APPS] + ["Voltar"]

    while True:
        escolha = escolher(tela, "APLICATIVOS", opcoes)

        if escolha == len(opcoes) - 1:
            break

        instalar_app(tela, APPS[escolha])

def menu_instalado(tela):
    while True:
        instalados = [app for app in APPS if app_instalado(app)]
        opcoes = [app["nome"] for app in instalados] + ["Voltar"]

        escolha = escolher(tela, "INSTALADO", opcoes)

        if escolha == len(opcoes) - 1:
            break

        abrir_app(instalados[escolha])
        mensagem(tela, f"Abrindo {instalados[escolha]['nome']}...")

def menu_configuracao(tela):
    while True:
        escolha = escolher(tela, "CONFIGURAÇÃO", ["Procurar atualização", "Voltar"])

        if escolha == 0:
            atualizar(tela)
        elif escolha == 1:
            break

def main(tela):
    curses.curs_set(0)
    tela.keypad(True)

    while True:
        escolha = escolher(tela, "MENU", ["Aplicativos", "Instalado", "Configuração", "Sair"])

        if escolha == 0:
            menu_aplicativos(tela)
        elif escolha == 1:
            menu_instalado(tela)
        elif escolha == 2:
            menu_configuracao(tela)
        elif escolha == 3:
            break

curses.wrapper(main)
