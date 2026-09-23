import pygame

BOTAO_TOQUE_ESQUERDA = pygame.Rect(10, 520, 70, 70)
BOTAO_TOQUE_DIREITA = pygame.Rect(90, 520, 70, 70)

BOTAO_TOQUE_ATAQUE = pygame.Rect(270, 520, 80, 80)
FONTE_BOTAO = None


sprites_raio = {}
atacando = False
tempo_inicio_ataque = 0
DURACAO_ATAQUE = 300

OBSTACULOS = [
    pygame.Rect(0, 0, 360, 20),
    pygame.Rect(0, 260, 360, 20),
    pygame.Rect(0, 0, 20, 640),
    pygame.Rect(340, 0, 20, 640),
]

# --- CONFIGURAÇÕES E VARIAVEIS ---
LARGURA_BASE = 360
ALTURA_BASE = 640

# --- VARIAVEIS DO PERSONAGEM ---
# Posição inicial no centro da tela
player_x = 0
player_y = 500
VELOCIDADE = 3

# --- SPRITES E DIREÇÃO DO PERSONAGEM ---
sprites_idle = {}
direcao_atual = 1 # Direção Inicial do personagem



cenario = None


def carregar_assets():
    global cenario, sprites_idle
    nome_imagem_cenario = 'fase1.jpg'
    pygame.font.init()
    if not pygame.font.get_init():
        pygame.font.init()

    FONTE_BOTAO = pygame.font.SysFont('Arial', 20, bold=True)

    try:
        img_esq = pygame.image.load('raio_esquerda.png').convert_alpha()
        sprites_raio['esquerda'] = pygame.transform.smoothscale(img_esq, (100, 100))

        img_dir = pygame.image.load('raio_direita.png').convert_alpha()
        sprites_raio['direita'] = pygame.transform.smoothscale(img_dir, (100, 100))

    except Exception as e:
        print("erro")

    try:
        #Carrega a imagem da pasta raiz
        imagem_bruta = pygame.image.load(nome_imagem_cenario).convert()
        cenario = pygame.transform.smoothscale(imagem_bruta, (LARGURA_BASE, ALTURA_BASE))
        print("Cenário carregado com sucesso!")

    except Exception as erro:
        cenario = None
        print("Erro ao carregar o cenário: {erro}")

    # 2. Carrega as Sprites das Direções
    

    for i in range(1, 9):
        nome_arquivo = f'Idle{i}.png'
        try:
            img = pygame.image.load(nome_arquivo).convert_alpha()

            sprites_idle[i] = pygame.transform.smoothscale(img, (100, 100))
            print(f"Sprite Idle{i}.png carregada!")
        except Exception as e:
            print("Erro")


def atualizar(eventos):

    global player_x, player_y, direcao_atual
    global atacando, tempo_inicio_ataque

    pygame.event.pump()
    tempo_atual = pygame.time.get_ticks()

    toque_esqueda = False
    toque_direita = False
    toque_ataque = False

    for evento in eventos:
        if evento.type in(pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
            pos_mouse = pygame.mouse.get_pos()
            largura_janela, altura_janela = pygame.display.get_surface().get_size()
            pos_x_base = pos_mouse[0] * (LARGURA_BASE / largura_janela)
            pos_y_base = pos_mouse[1] * (ALTURA_BASE / altura_janela)
            pos_toque = (pos_x_base, pos_y_base)

            if BOTAO_TOQUE_ATAQUE.collidepoint(pos_toque) and not atacando:
                toque_ataque = True
        if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE and not atacando:
            toque_ataque = True
    if toque_ataque and not atacando:
        atacando = True
        tempo_inicio_ataque = tempo_atual


    if atacando:
        if tempo_atual - tempo_inicio_ataque > DURACAO_ATAQUE:
            atacando = False


    if not atacando:
        toque_esqueda = False
        toque_direita = False
        if pygame.mouse.get_pressed()[0]:
            pos_mouse = pygame.mouse.get_pos()
            largura_janela, altura_janela = pygame.display.get_surface().get_size()
            pos_x_base = pos_mouse[0] * (LARGURA_BASE / largura_janela)
            pos_y_base = pos_mouse[1] * (ALTURA_BASE / altura_janela)
            pos_toque = (pos_x_base, pos_y_base)
            if BOTAO_TOQUE_ESQUERDA.collidepoint(pos_toque):
                toque_esqueda = True
            elif BOTAO_TOQUE_DIREITA.collidepoint(pos_toque):
                toque_direita = True

    #Captura o estado de todas as teclas do teclado
        teclas = pygame.key.get_pressed()

        # Movimentação horizontal (A / D ou setas Esquerda/Direita)
        esquerda = teclas[pygame.K_a] or teclas[pygame.K_LEFT] or toque_esqueda
        direita = teclas[pygame.K_d] or teclas[pygame.K_RIGHT] or toque_direita    
        cima = teclas[pygame.K_w] or teclas[pygame.K_UP]
        baixo = teclas[pygame.K_s] or teclas[pygame.K_DOWN]

        player_rect = pygame.Rect(player_x, player_y, 100, 100)

        dx = 0
        if esquerda:
            dx -= VELOCIDADE
        if direita:
            dx += VELOCIDADE

        if dx != 0:
            player_rect.x += dx
            colidiu = False
            for obstaculo in OBSTACULOS:
                if player_rect.colliderect(obstaculo):
                    colidiu = True
                    break
            if not colidiu:
                player_x += dx
            else:
                player_rect.x = player_x



        dy = 0
        if cima:
            dy -= VELOCIDADE
        if baixo:
            dy += VELOCIDADE

        if dy != 0:
            player_rect.y += dy
            colidiu = False
            for obstaculo in OBSTACULOS:
                if player_rect.colliderect(obstaculo):
                    colidiu = True
                    break
            if not colidiu:
                player_y += dy

        if baixo and not (esquerda or direita or cima):
            direcao_atual = 5
        elif cima and not (esquerda or direita or baixo):
            direcao_atual = 2
        elif esquerda and not(cima or baixo or direita):
            direcao_atual = 8
        elif direita and not (cima or baixo or esquerda):
            direcao_atual = 1
        elif cima and esquerda:
            direcao_atual = 4
        elif cima and direita:
            direcao_atual = 3
        elif baixo and esquerda:
            direcao_atual = 7
        elif baixo and direita:
            direcao_atual = 6

    player_x = max(0, min(player_x, LARGURA_BASE - 100))
    player_y = max(0, min(player_y, ALTURA_BASE - 100))


def desenhar_botoes_toque(superficie):
    cor_botao = (255, 255, 255, 100)
    global FONTE_BOTAO

    if FONTE_BOTAO is None:
        pygame.font.init()
        FONTE_BOTAO = pygame.font.SysFont('Arial', 18, bold=True)

    txt_esq = FONTE_BOTAO.render("<", True, (255, 255, 255))
    txt_dir = FONTE_BOTAO.render(">", True, (255, 255, 255))
    txt_atq = FONTE_BOTAO.render("Raio", True, (255, 200, 0))

    if FONTE_BOTAO is None:
        if not pygame.font.get_init():
            pygame.font.init()
        FONTE_BOTAO = pygame.font.SysFont('Arial', 20, bold=True)
    pygame.draw.rect(superficie, (0, 230, 255), BOTAO_TOQUE_ESQUERDA, width=2, border_radius=10)
    txt_esq = FONTE_BOTAO.render("<", True, (255, 255, 255))
    superficie.blit(txt_esq, (BOTAO_TOQUE_ESQUERDA.centerx - txt_esq.get_width()//2, BOTAO_TOQUE_ESQUERDA.centery - txt_esq.get_height()//2))

    pygame.draw.rect(superficie, (0, 230, 255), BOTAO_TOQUE_DIREITA, width=2, border_radius=10)
    txt_esq = FONTE_BOTAO.render(">", True, (255, 255, 255))
    superficie.blit(txt_dir, (BOTAO_TOQUE_DIREITA.centerx - txt_dir.get_width()//2, BOTAO_TOQUE_DIREITA.centery - txt_dir.get_height()//2))

    pygame.draw.rect(superficie, (255, 200, 0), BOTAO_TOQUE_ATAQUE, width=2, border_radius=15)
    FONTE_BOTAO.render("RAIO", True, (255, 200, 0))
    superficie.blit(txt_atq, (BOTAO_TOQUE_ATAQUE.centerx - txt_atq.get_width()//2, BOTAO_TOQUE_ATAQUE.centery - txt_atq.get_height()//2))

def desenhar(superficie):
    if cenario:
        superficie.blit(cenario, (0, 0))
    else:
        superficie.fill((30, 30, 30))

    if atacando:
        lado = 'esquerda' if direcao_atual in [8] else 'direita'

        if lado in sprites_raio:
            superficie.blit(sprites_raio[lado], (player_x, player_y))

        else:
            pygame.draw.rect(superficie, (255, 255, 0), (player_x, player_y, 100, 100))
    else:
        if direcao_atual in sprites_idle:
            superficie.blit(sprites_idle[direcao_atual], (player_x, player_y))

        else:
            pygame.draw.rect(superficie, (0, 230, 255), (player_x, player_y, 100, 100))

    desenhar_botoes_toque(superficie)
    #for obstaculo in OBSTACULOS:
        #pygame.draw.rect(superficie, (255, 0, 0), obstaculo, width=1)