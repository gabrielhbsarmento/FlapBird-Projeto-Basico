import pygame #biblioteca de criação de jogos
import os #biblioteca para interagir com pastas (no caso vai servir para as imgs)
import random #biblioteca que gera numeros aleatorios (Obstaculos do jogo)

# definindo constantes

# pygame.transform.sacle2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
# declaramos a variavel alocando ela com a imagem utilizando a biblioteca os
# e multiplicando a escala por 2

TELA_LARGURA = 500
TELA_ALTURA = 800

IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
IMAGEMS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),
]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 50)

#criando classes dos objetos

class Passaro:
    IMGS = IMAGEMS_PASSARO
    # ANIMAÇOES DE ROTAÇÃO
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    #CRIANDO A FUNÇAO QUE DA VIDA AO PASSARO

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    #CRIANDO A FUNÇÃO DE PULAR USANDO A FORMULA DO SO SORVETE ( EQUAÇÃO DO DESLOCAMENTO EM FISICA )

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
#Calculando deslocamento
      self.tempo += 1
      deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo
# delimitaçoes no deslocamento
      if deslocamento > 16:
          deslocamento = 16
      elif deslocamento < 0:
          deslocamento -= 2

      self.y += deslocamento

# angulo do parraro
      if deslocamento < 0 or self.y < (self.altura + 50):
          if self.angulo < self.ROTACAO_MAXIMA:
              self.angulo = self.ROTACAO_MAXIMA
      else:
         if self.angulo > -90:
             self.angulo -= self.VELOCIDADE_ROTACAO
    def desenhar(self, tela):

# fazendo a ultilização das imgs quando o passaro voar
      self.contagem_imagem +=1

      if self.contagem_imagem < self.TEMPO_ANIMACAO:
          self.imagem = self.IMGS[0]
      elif self.contagem_imagem < self.TEMPO_ANIMACAO*2:
          self.imagem = self.IMGS[1]
      elif self.contagem_imagem < self.TEMPO_ANIMACAO*3:
          self.imagem = self.IMGS[2]
      elif self.contagem_imagem < self.TEMPO_ANIMACAO*4:
          self.imagem = self.IMGS[1]
      elif self.contagem_imagem >= self.TEMPO_ANIMACAO*4 + 1:
          self.imagem = self.IMGS[0]
          self.contagem_imagem = 0

# caso o passaro estiver caindo
      if self.angulo <= -80:
          self.imagem = self.IMGS[1]
          self.contagem_imagem = self.TEMPO_ANIMACAO*2

# desenhando a imagem do passaro rotacionado
# cria basicamente a imagem do passaro com um retangulo imvisivel
# tem que definir ele com a posiçaõ que vai ficar ( posição x e y)

      imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
      pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
      retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)
      tela.blit(imagem_rotacionada, retangulo.topleft)

# evitando bug de colizão
# get mask ele pega o codigo acima e cria su quadradinhos para poder comparar
# na hora de colidir com o cano no caso 

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)
               
class Cano:
    # ANIMAÇOES DO CANO
    DISTANCIA = 200
    VELOCIDADE = 5

    # CRIANDO A FUNÇAO QUE DA VIDA AO Cano
    # DEFININDO PARAMETROS
    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True) # o flip ajuda a imverter a img de ponta a cabeça
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.definir_altura()

# definido altura com base na altura inical (self.altura)

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

# movendo o cano
    def mover(self):
        self.x -= self.VELOCIDADE

# desenhando a tela com o blit
    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

# colisao dos canos
# primeiro define os canos da base e o de topo]
# surface serve para desenhar a img
# round retorna valor aproximado do valor da variavel
# overlap ele usa para comparar pixel (no caso vai comparar
# cria a mascara do cano com o get mask
# pegando tbm a mask do passaro para fazer a condição com o mask do cano para colidir
    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))
# condicoes de v e f caso tenha uma colisao entre a base e o passaro ou topo e passaro
        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)

        if base_ponto or topo_ponto:
            return True
        else:
            return False

# definindo a classe chao
# objetivo: definir parametros , cria dois chaos , fazer condição para repetição de imagens para
# não ter que criar mais de  20 imgs do chão para rodar .
# para cria prescisa da largura  da img
# width pega o valor da largura  da img

class Chao:
    # parametros do chão
    VELOCIDADE = 5
    LARGURA = IMAGEM_CHAO.get_width()
    IMAGEM = IMAGEM_CHAO

# aplicando valor do chão
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

# criando função mover
# -= quer dizer que ele está andando para esquerda do x(negativo)
# += quer dizer que ele está andando para direita do x(positivo)
    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE
# condição de movimentação da tela
# se o valor do x1(chao1) for menor que 0 ele fica atras do x2(chao2)
# e se o valor de x2(chao2) for menor que 0 ele fica atras do x1(chao1)
        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA
#criando a tela do chao com o blit
# pegando a img o valor do chao1 , valor do chao2 e a posição y da tela
    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))

#criando função mestre que junta  e cria a tela do jogo

def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)
#colocando a fonte do jogo
#definindo pontuação: fonte, langura , valor da tela e etc

    texto = FONTE_PONTOS.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    tela.blit(texto, (TELA_LARGURA - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
#comando display ele atualiza tudo com o . update gerando a tela toda
    pygame.display.update()

# criando função mai
# criando todas a favriaveis acima  , porem , pegando as calsses
#definido as regras do game  ; ou seja ; movimentação , condição de pontuação e de derrota e afins
def main():
    passaros = [Passaro(230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        # atualiza o frame da tela com o tick (atualiza as telas no game)
        relogio.tick(30)

# interação com o usuário
# cria um evento para pegar definir a movimentação do passaro
# type recebe um valor do evento (no caso se for igual ao quit[clicar no x])
# keydown evendo de apretar um botao do teclado
# no caso define com o evento.key e associa ele a bara de espaço f=definindo condeção de pular no jogo
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()

        # mover as coisas

        # definindo movimentação do cano e do passaro
        for passaro in passaros:
            passaro.mover()
        chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            #pegando a class passaro e sua posição
            #criando condição de derrota
            # no caso se o valor do cano for maior que o valor do passaro ele nao passa e finaliza
            #criando condição de pontuação
            # no caso se o valor do passaro for maior que o cano ele passa, pontua e adiciona um cano
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
            cano.mover()
            # se o cano a largura dele for menor que zero
            # quer dizer que está fora da tela e po ser excluido adicionando num lista de canos para depois
            # ser excluido
            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)

        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))
        for cano in remover_canos:
            canos.remove(cano)

# definindo condição caso passe no chão ou no topo
# caso a posição do passaro no eixo y (valor dele) + altura do passaro for maior que o chao
# valor do chão no eixo y  ou passaro  no eixo y ser menor que 0 ou topo y
# o passaro apaga
        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)

        desenhar_tela(tela, passaros, canos, chao, pontos)

if __name__ == '__main__':
    main()