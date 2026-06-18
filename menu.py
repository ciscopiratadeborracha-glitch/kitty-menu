import curses
import os
import shutil
import subprocess
import sys
import time

MENU_DIR = os.path.expanduser("~/kitty-menu")
VERSION_FILE = os.path.join(MENU_DIR, "VERSION")
CHANGELOG_FILE = os.path.join(MENU_DIR, "CHANGELOG.txt")

APPS = [
    {"nome": "Firefox", "cmd": "firefox", "instalar": "sudo apt install firefox -y"},
    {"nome": "VS Code", "cmd": "code", "flatpak": "com.visualstudio.code", "instalar": "flatpak install flathub com.visualstudio.code -y"},
    {"nome": "VLC", "cmd": "vlc", "instalar": "sudo apt install vlc -y"},
    {"nome": "Discord", "cmd": "discord", "flatpak": "com.discordapp.Discord", "instalar": "flatpak install flathub com.discordapp.Discord -y"},
    {"nome": "Telegram", "cmd": "telegram-desktop", "flatpak": "org.telegram.desktop", "instalar": "flatpak install flathub org.telegram.desktop -y"},
    {"nome": "Steam", "cmd": "steam", "flatpak": "com.valvesoftware.Steam", "instalar": "flatpak install flathub com.valvesoftware.Steam -y"},
]

JOGOS = [
    {"nome": "SuperTuxKart", "cmd": "supertuxkart", "instalar": "sudo apt install supertuxkart -y"},
    {"nome": "Minetest", "cmd": "minetest", "instalar": "sudo apt install minetest -y"},
    {"nome": "OpenTTD", "cmd": "openttd", "instalar": "sudo apt install openttd -y"},
    {"nome": "0 A.D.", "cmd": "0ad", "instalar": "sudo apt install 0ad -y"},
    {"nome": "RetroArch", "cmd": "retroarch", "instalar": "sudo apt install retroarch -y"},
]

def rodar(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def instalado(item):
    if shutil.which(item["cmd"]):
        return True

    if "flatpak" in item and shutil.which("flatpak"):
        r = rodar(f"flatpak list --app | grep {item['flatpak']}")
        return r.returncode == 0

    return False

def abrir_item(item):
    if shutil.which(item["cmd"]):
        os.system(f"nohup {item['cmd']} >/dev/null 2>&1 &")
    elif "flatpak" in item:
        os.system(f"nohup flatpak run {item['flatpak']} >/dev/null 2>&1 &")

def ler_versao():
    try:
        with open(VERSION_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    except:
        return "1.0.0"

def mensagem(tela, texto):
    tela.clear()
    tela.addstr(2, 2, texto[:70])
    tela.addstr(4, 2, "Pressione ENTER para voltar.")
    tela.refresh()

    while tela.getch() not in [10, 13, curses.KEY_ENTER]:
        pass

def confirmar(tela, titulo, pergunta):
    escolha = 0
    opcoes = ["Sim", "Não"]

    while True:
        tela.clear()
        tela.addstr(1, 2, titulo)
        tela.addstr(2, 2, "=" * len(titulo))
        tela.addstr(4, 2, pergunta[:70])

        for i, opcao in enumerate(opcoes):
            marcador = ">" if i == escolha else " "
            tela.addstr(6 + i, 2, f"{marcador} {opcao}")

        tela.addstr(10, 2, "↑ ↓ para navegar | ENTER para selecionar")
        tela.refresh()

        tecla = tela.getch()

        if tecla == curses.KEY_UP:
            escolha = (escolha - 1) % len(opcoes)
        elif tecla == curses.KEY_DOWN:
            escolha = (escolha + 1) % len(opcoes)
        elif tecla in [10, 13, curses.KEY_ENTER]:
            return escolha == 0

def instalar_item(tela, item):
    if instalado(item):
        mensagem(tela, f"{item['nome']} já está instalado.")
        return

    if confirmar(tela, item["nome"], f"{item['nome']} não está instalado. Deseja instalar?"):
        curses.endwin()
        os.system(item["instalar"])
        input("\nPressione ENTER para voltar ao menu...")

def atualizar(tela):
    tela.clear()
    tela.addstr(2, 2, "Procurando atualização...")
    tela.refresh()

    rodar(f"cd {MENU_DIR} && git fetch origin main")

    local = rodar(f"cd {MENU_DIR} && git rev-parse HEAD").stdout.strip()
    remoto = rodar(f"cd {MENU_DIR} && git rev-parse origin/main").stdout.strip()

    if local == remoto:
        mensagem(tela, "Seu sistema já está atualizado.")
        return

    log = rodar(f"cd {MENU_DIR} && git log --oneline HEAD..origin/main").stdout.strip()

    tela.clear()
    tela.addstr(1, 2, "NOVA ATUALIZAÇÃO ENCONTRADA")
    tela.addstr(2, 2, "===========================")

    linha = 4
    for item in log.splitlines()[:6]:
        tela.addstr(linha, 2, "- " + item[:65])
        linha += 1

    tela.refresh()

    if confirmar(tela, "ATUALIZAÇÃO", "Deseja instalar essa atualização agora?"):
        curses.endwin()
        os.system(f"cd {MENU_DIR} && git pull origin main")
        input("\nAtualização concluída. Pressione ENTER para reiniciar o menu...")
        os.execv(sys.executable, [sys.executable] + sys.argv)

def mostrar_arquivo(tela, titulo, caminho):
    tela.clear()
    tela.addstr(1, 2, titulo)
    tela.addstr(2, 2, "=" * len(titulo))

    try:
        with open(caminho, "r", encoding="utf-8") as f:
            linhas = f.readlines()
    except:
        linhas = ["Arquivo não encontrado."]

    for i, linha in enumerate(linhas[:12]):
        tela.addstr(4 + i, 2, linha.strip()[:70])

    tela.addstr(18, 2, "Pressione ENTER para voltar.")
    tela.refresh()

    while tela.getch() not in [10, 13, curses.KEY_ENTER]:
        pass

def sistema_info(tela):
    curses.endwin()
    os.system("clear")
    os.system("fastfetch")
    input("\nPressione ENTER para voltar ao menu...")

def atualizar_sistema(tela):
    curses.endwin()
    os.system("sudo apt update && sudo apt upgrade -y")
    input("\nPressione ENTER para voltar ao menu...")

def abrir_pasta(nome, caminho):
    caminho = os.path.expanduser(caminho)
    os.system(f"xdg-open '{caminho}' >/dev/null 2>&1 &")

def desenhar(tela, titulo, opcoes, selecionado):
    tela.clear()

    tela.addstr(1, 2, "╔══════════════════════════════════════╗")
    tela.addstr(2, 2, "║              カウアン               ║")
    tela.addstr(3, 2, f"║            Sistema v{ler_versao():<8}          ║")
    tela.addstr(4, 2, "╚══════════════════════════════════════╝")

    tela.addstr(6, 2, titulo)
    tela.addstr(7, 2, "─" * len(titulo))

    for i, opcao in enumerate(opcoes):
        marcador = ">" if i == selecionado else " "
        tela.addstr(9 + i, 2, f"{marcador} {opcao}")

    tela.addstr(20, 2, "↑ ↓ para navegar | ENTER para selecionar")
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

        instalar_item(tela, APPS[escolha])

def menu_instalado(tela):
    while True:
        itens = [item for item in APPS + JOGOS if instalado(item)]
        opcoes = [item["nome"] for item in itens] + ["Voltar"]

        escolha = escolher(tela, "INSTALADO", opcoes)

        if escolha == len(opcoes) - 1:
            break

        abrir_item(itens[escolha])
        mensagem(tela, f"Abrindo {itens[escolha]['nome']}...")

def menu_arquivos(tela):
    pastas = [
        ("Downloads", "~/Downloads"),
        ("Documentos", "~/Documentos"),
        ("Imagens", "~/Imagens"),
        ("Vídeos", "~/Vídeos"),
        ("Pasta pessoal", "~"),
    ]

    opcoes = [p[0] for p in pastas] + ["Voltar"]

    while True:
        escolha = escolher(tela, "ARQUIVOS", opcoes)

        if escolha == len(opcoes) - 1:
            break

        abrir_pasta(pastas[escolha][0], pastas[escolha][1])
        mensagem(tela, f"Abrindo {pastas[escolha][0]}...")

def menu_jogos(tela):
    opcoes = [jogo["nome"] for jogo in JOGOS] + ["Voltar"]

    while True:
        escolha = escolher(tela, "JOGOS", opcoes)

        if escolha == len(opcoes) - 1:
            break

        instalar_item(tela, JOGOS[escolha])

def menu_sistema(tela):
    while True:
        escolha = escolher(
            tela,
            "SISTEMA",
            [
                "Informações do sistema",
                "Atualizar sistema",
                "Reiniciar",
                "Desligar",
                "Sobre",
                "Voltar"
            ]
        )

        if escolha == 0:
            sistema_info(tela)
        elif escolha == 1:
            atualizar_sistema(tela)
        elif escolha == 2:
            if confirmar(tela, "REINICIAR", "Deseja reiniciar o computador?"):
                os.system("systemctl reboot")
        elif escolha == 3:
            if confirmar(tela, "DESLIGAR", "Deseja desligar o computador?"):
                os.system("systemctl poweroff")
        elif escolha == 4:
            mensagem(tela, f"カウアン v{ler_versao()} - Menu personalizado para Kitty.")
        elif escolha == 5:
            break

def menu_configuracao(tela):
    while True:
        escolha = escolher(
            tela,
            "CONFIGURAÇÃO",
            [
                "Procurar atualização",
                "Versão atual",
                "Histórico de atualizações",
                "Voltar"
            ]
        )

        if escolha == 0:
            atualizar(tela)
        elif escolha == 1:
            mostrar_arquivo(tela, "VERSÃO ATUAL", VERSION_FILE)
        elif escolha == 2:
            mostrar_arquivo(tela, "HISTÓRICO", CHANGELOG_FILE)
        elif escolha == 3:
            break

def main(tela):
    curses.curs_set(0)
    tela.keypad(True)

    while True:
        escolha = escolher(
            tela,
            "MENU",
            [
                "Aplicativos",
                "Instalado",
                "Arquivos",
                "Jogos",
                "Sistema",
                "Configuração",
                "Sair"
            ]
        )

        if escolha == 0:
            menu_aplicativos(tela)
        elif escolha == 1:
            menu_instalado(tela)
        elif escolha == 2:
            menu_arquivos(tela)
        elif escolha == 3:
            menu_jogos(tela)
        elif escolha == 4:
            menu_sistema(tela)
        elif escolha == 5:
            menu_configuracao(tela)
        elif escolha == 6:
            break

curses.wrapper(main)
