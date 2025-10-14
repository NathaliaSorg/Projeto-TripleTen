# Desafio de Modelagem Preditiva

O desafio consiste em construir um modelo preditivo para os preços de negociação de energia elétrica no mercado futuro para as várias maturidades.

Este esforço deve envolver a análise de dados dos decks Newave como variável do preditor, especialmente no mercado de longo prazo (A+2, A+3 e A+4).

## Mercado de Energia

O mercado de energia brasileiro pode ser separado em dois: o primeiro é o Ambiente de Contratação Regulado (ACR), nele contratos regulados são realizados para fornecer energia para as distribuidoras e consumidores cativos; o segundo é o Ambiente de Contratação Livre (ACL), no qual os clientes livres (grandes consumidores), comercializadoras e geradores negociam livremente os contratos de energia. 

Na operação do sistema, o despacho de energia (quanto cada usina vai produzir) é decidido pelo Operador Nacional do Sistema Elétrico (ONS) e, com base na decisão de despacho e nos custos de geração de cada usina, a Câmara de Comercialização de Energia Elétrica (CCEE) calcula o preço a curto prazo, chamado Preço de Liquidação de Diferenças (PLD). Este preço é usado para liquidar as diferenças entre volumes contratados e efetivamente despachados.

## Newave

Na decisão do despacho de energia, o operador deve escolher o despachar usinas com menor custo de produção (e que seja possível atender a demanda). Dada a grande presença de usinas hidroelétricas no sistema elétrico brasileiro, o calculo de preços envolve estimar o custo futuro da água. Do manual do programa NEWAVE:

>No Brasil, e em diversos países, a solução do problema é obtida em etapas. Nestas, são utilizados modelos com diferentes graus de detalhamento para a representação do sistema, abrangendo períodos de estudos com horizontes distintos [7], denominados de longo e médio prazos – modelo NEWAVE, curto prazo – modelo DECOMP (Modelo de Planejamento da Operação de Sistemas Hidrotérmicos Interligados de Curto Prazo) e programação da operação diária – modelo DESSEM (Modelo de Despacho Hidrotérmico de Curto Prazo).

O programa NEWAVE usa modelos estocásticos para gerar cenários (tipicamente 2000), com base nos dados históricos de afluencia nos reservatórios das usinas hidroelétricas. Com base nos cenários de afluência, o programa tenta otimizar o processo, tentando minimizar os preços assim como os riscos de desabastecimento e, com isso,  calcula o custo marginal da energia em um horizonte de até cinco anos, além de níveis de reservatórios, transmissão entre subsistemas entre outros.

Como se trata de uma ferramenta de médio-longo prazo, os valores estimados são mensais, sem estimativas diárias ou semanais.

## Objetivos

- Construir um preditor para os preços futuros das maturidades seguindo o modelo no arquivo [next_step_predictor.py](predictor/next_step_predictor.py) usando as séries históricas de maturidade (presentes em data/prices) para o submercado Sudeste.
- Terminar a implementação do objeto para carregar e pré-processar os dados de custos marginais do Newave, presente em [load_newave.py](loaders/newave_loader.py) para o submercado Sudeste.
- Avaliar ganhos modelo proposto.
- Avaliar ganhosdo uso de decks Newave no preditor.

## Referências e links úteis:

- [CCEE](https://www.ccee.org.br/): Câmara de Comercialização de Energia Elétrica, é a entidade responsável pela contabilização mensal e liquidação das diferenças.
- [ONS](https://www.ons.org.br/): Operador Nacional do Sistema Elétrico, é o órgão responsável pela coordenação e controle da operação das instalações de geração e transmissão de energia elétrica no Sistema Interligado Nacional (SIN).
- [Inewave](https://github.com/rjmalves/inewave) : Biblioteca Python para manipulação dos arquivos de entrada e saída do programa NEWAVE.