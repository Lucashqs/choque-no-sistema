import sys
import pygame
import random

pygame.init()

LARGURA = 360
ALTURA = 640

TELA = pygame.display.set_mode((LARGURA, ALTURA))

pygame.display.set_caption("CHOQUE NO SISTEMA")

COR_FUNDO = (15, 15, 30)
COR_CHOQUE = (0, 230, 255)
COR_TEXTO = (255, 255, 255)
COR_BOTAO = (30, 40, 70)

pygame.font.init()

FONTE_TITULO = pygame.font.SysFont("sans-serif", 36, bold=True)
FONTE_BOTAO = pygame.font.SysFont("sans-serif", 24)

BOTAO_NOVO_JOGO = pygame.Rect(50, 280, 260, 50)
BOTAO_CARREGAR = pygame.Rect(50, 350, 260, 50)
BOTAO_OPCOES = pygame.Rect(50, 420, 260, 50)

RELOGIO = pygame.time.Clock()

RODANDO = True

def desenhar_raios(superficie):
    if random.randint(0, 100) < 30:
        x_inicio = random.randint(20, LARGURA - 20)
        y_inicio = random.randint(10, 150)

        pontos = [(x_inicio, y_inicio)]

        for _ in range(4):
            x_inicio += random.randint(-20, 20)
            y_inicio += random.randint(15, 35)
            pontos.append((x_inicio, y_inicio))

        if len(pontos) > 1:
            pygame.draw.lines(superficie, (255, 255, 255), False, pontos, 3)
            pygame.draw.lines(superficie, COR_CHOQUE, False, pontos, 1)

try:
    pygame.mixer.init()
    pygame.mixer.music.load('musica_menu1.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    print("Música do menu carrega com sucesso!")
except Exception as e:
    print(f"Aviso: Não foi possivél carregar a música. Detalhes: {e}")



try:
    img_fundo = pygame.image.load('fundo_menu.jpg').convert()
    img_fundo = pygame.transform.scale(img_fundo, (LARGURA, ALTURA))
    tem_fundo = True
    print('Imagem de fundo carregada com sucesso!')
except Exception as e:
    tem_fundo = False
    print(f"Falha ao carregar 'fundo_menu.jpg'. Usando cor padrão. Detalhes: {e}")

while RODANDO:

    if tem_fundo:
        TELA.blit(img_fundo, (0, 0))
    else:
        TELA.fill(COR_FUNDO)
    desenhar_raios(TELA)

    texto_titulo = FONTE_TITULO.render("CHOQUE NO", True, COR_CHOQUE)
    texto_subtitulo = FONTE_TITULO.render("SISTEMA", True, COR_CHOQUE)

    TELA.blit(texto_titulo, (LARGURA // 2 - texto_titulo.get_width() // 2, 80))
    TELA.blit(texto_subtitulo, (LARGURA // 2 - texto_subtitulo.get_width() // 2, 130))

    botoes = [
        (BOTAO_NOVO_JOGO, "Novo Jogo"),
        (BOTAO_CARREGAR, "Carregar"),
        (BOTAO_OPCOES, "Opcoes")
    ]

    for retangulo, texto in botoes:
        pygame.draw.rect(TELA, COR_BOTAO, retangulo, border_radius=10)

        pygame.draw.rect(TELA, COR_CHOQUE, retangulo, width=2, border_radius=10)

        txt_surface  = FONTE_BOTAO.render(texto, True, COR_TEXTO)
        txt_x = retangulo.x + (retangulo.width - txt_surface.get_width()) // 2
        txt_y = retangulo.y + (retangulo.height - txt_surface.get_height()) // 2
        TELA.blit(txt_surface, (txt_x, txt_y))

        

    POS_TOQUE = (0, 0)
    TOCOU = False


    if TOCOU and retangulo.collidepoint(POS_TOQUE):
        if texto == "Novo Jogo":
            print("Iniciando novo jogo...")
    
        elif texto == "Carregar":
            print("Carregando jogo salvo...")
        elif texto == "Opcoes":
            print("Abrindo tela de opcoes")
    
    


    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            RODANDO = False

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                POS_TOQUE = evento.pos
                TOCOU = True
    pygame.display.flip()
    RELOGIO.tick(60)

pygame.quit()
sys.exit()
