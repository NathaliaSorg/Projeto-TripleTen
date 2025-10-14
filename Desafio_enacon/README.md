# Preços no mercado futuro de energia

## 📖 Visão Geral

Este é um preditor de preços no mercado futuro de energia elétrica. Ele utiliza o histórico das diferentes maturidades para prever o preço futuro de cada uma delas.

## 🚀 Execução Rápida

### Pré-requisitos
```bash
# Python 3.8 ou superior
python --version

# Instalar dependências
pip install -r requirements.txt
```

### Executar Simulação
```bash
# Executar simulação básica
python main.py

# Executar testes
python -m pytest tests/

# Executar testes com cobertura
python -m pytest tests/ --cov=.
```

## 🏗️ Estrutura do Sistema

### Componentes Principais

- **`main.py`**: Arquivo principal com exemplo de uso
- **`loaders/`**: Classes de carregamento dos dados (CsvLoader, NewaveLoader)
- **`predictor/`**: Classes de predição (NextStepPredictor)
- **`data/`**: Dados a serem carregados
- **`documentation/`**: Documentos potencialmente relevantes
- **`tests/`**: Testes unitários para validação

### Fluxo

1. **Carregamento dos dados**: Carregamento dos dados usados pelo preditor
2. **Calibração do Preditor**: Ajuste do modelo para os dados
3. **Resultados**: Métricas de performance e estatísticas

## 🔧 Personalização

### Criar novo Preditor

Copie a estrutura do preditor NextStepPredictor e modifique o código para atender às suas necessidades, usando melhor os dados históricos disponíveis.

### Adicionar Dados Newave para melhorar o modelo

Complete a classe NewaveLoader na pasta loaders para carregar os dados do Newave e retornar um DataFrame com os dados.

## 🧪 Testes

### Executar Todos os Testes
```bash
python -m pytest tests/
```

### Teste Específico
```bash
python -m pytest tests/test_policy.py -v
```

### Teste com Cobertura
```bash
python -m pytest tests/ --cov=. --cov-report=html
```

## 📈 Métricas de Performance

O sistema calcula automaticamente:
- MAE: média absoluta do erro
- MSE: média quadrática do erro
- RMSE: raiz quadrada do erro
- MAPE: média absoluta do erro em porcentagem

## 🎯 Próximos Passos

1. **Analise a solução atual** executando `python main.py`
1. **Implemente uma nova abordagem** para melhorar o modelo
1. **Complete a classe para carregar um deck Newave** na pasta loaders
1. **Inclua dados do deck no modelo** para tentar melhorar a perfomance
1. **Documente suas decisões** e resultados

## 📚 Recursos Adicionais

- **`descritivo do desafio.md`**: Documento completo do desafio
- **`pytest.ini`**: Configuração dos testes

## 🤝 Suporte

Para dúvidas sobre o sistema ou implementação, consulte:
- Documentação das classes no código
- Testes unitários como exemplos de uso
- Documento do desafio para contexto completo

---

**Boa sorte** 🚀 