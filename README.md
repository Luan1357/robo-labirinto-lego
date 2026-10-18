# Robô Navegador de Labirinto: LEGO SPIKE

## Descrição do projeto

Este projeto consiste em um robô autônomo, montado com o kit LEGO SPIKE Prime (Mindstorms), capaz de percorrer um labirinto sem intervenção humana. A navegação é dividida em duas fases: uma fase de **ida**, em que o robô avança pelo labirinto utilizando o sensor de distância para detectar paredes e obstáculos à frente e decidir quando virar, e uma fase de **volta**, em que o robô refaz o caminho até o ponto de partida.

Para marcar pontos de decisão no percurso (como cruzamentos ou pontos de retorno), foram utilizadas fitas coloridas fixadas no chão do labirinto. O sensor de cor do robô identifica essas marcações e aciona a lógica correspondente, como iniciar a fase de volta ou registrar um ponto de referência do trajeto.

As curvas do robô são executadas com o auxílio do giroscópio embutido, que fornece a correção do ângulo de rotação em tempo real. Isso garante que cada curva (90°, 180° etc.) seja realizada com precisão, evitando o acúmulo de erro de trajetória que ocorreria se o robô dependesse apenas do tempo ou da rotação dos motores.

## Disciplina

Princípios de Robótica, PUCPR, 2025

## Tecnologias utilizadas

- Python (LEGO SPIKE Prime / Mindstorms)
- Sensor de distância (ultrassônico)
- Sensor de cor
- Giroscópio (sensor inercial embutido no hub)

## Estrutura do repositório

- `labirinto.py`: código-fonte do programa de navegação autônoma, extraído do projeto LEGO SPIKE (`.llsp3`).

## Contexto acadêmico

Projeto desenvolvido por **Luan Alfredo Lugarini**, estudante de Engenharia da Computação na PUCPR.
