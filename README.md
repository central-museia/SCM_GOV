# 🏛️ SCM_GOV

> Plataforma de Inteligência para Monitoramento de Licitações Públicas utilizando a API oficial do Portal Nacional de Contratações Públicas (PNCP).

## 📌 Sobre o projeto

O **SCM_GOV** é uma plataforma desenvolvida para apoiar a **SCM Reformas e Engenharia** na identificação, análise e priorização de oportunidades de licitações públicas.

O sistema consulta automaticamente os dados disponibilizados pelo **PNCP (Portal Nacional de Contratações Públicas)** e transforma grandes volumes de informações em indicadores estratégicos para apoiar a decisão sobre participação em processos licitatórios.

O objetivo é reduzir o tempo gasto com pesquisas manuais e aumentar a assertividade na escolha das licitações mais aderentes à atuação da empresa.

---

# 🎯 Objetivos

- Consultar automaticamente as licitações públicas do PNCP
- Identificar oportunidades compatíveis com a SCM
- Centralizar informações em um único painel
- Classificar oportunidades por relevância
- Acompanhar atas, contratos e contratações
- Gerar indicadores estratégicos
- Apoiar a tomada de decisão

---

# 🚀 Funcionalidades

## Dashboard

- Indicadores gerais
- Licitações abertas
- Atas vigentes
- Contratações
- Valor total das oportunidades
- Atualização automática

---

## Radar de Licitações

Pesquisa inteligente com filtros por:

- Estado
- Município
- Modalidade
- Valor
- Prazo
- Órgão
- Palavra-chave
- Situação

---

## Oportunidades

Classificação automática das licitações conforme critérios da SCM.

Categorias:

- ⭐ Excelente
- ⭐ Muito Boa
- ⭐ Boa
- ⭐ Baixa Prioridade

---

## Detalhes

Visualização completa da contratação.

Incluindo:

- Dados do órgão
- Datas
- Objeto
- Vigência
- Situação
- Histórico
- Compatibilidade com a SCM

---

## Atas de Registro de Preço

Consulta das atas vigentes.

Informações como:

- Vigência
- Possibilidade de adesão
- Cancelamentos
- Órgão responsável

---

## Contratos

Consulta de contratos publicados.

Permite analisar:

- Empresas vencedoras
- Valores contratados
- Órgãos contratantes

---

## Estatísticas

Indicadores gerenciais.

Exemplos:

- Órgãos que mais contratam
- Estados com maior volume
- Valores por período
- Distribuição por modalidade

---

# 🧠 Inteligência SCM

O sistema utilizará uma camada própria de inteligência para classificar automaticamente cada oportunidade.

Critérios previstos:

- Compatibilidade com os CNAEs da SCM
- Tipo de serviço
- Valor estimado
- Localização
- Prazo restante
- Histórico do órgão
- Complexidade

Cada licitação receberá uma pontuação que auxiliará na decisão de participação.

---

# 🗂 Estrutura do Projeto

```
SCM_GOV/

app.py

README.md

requirements.txt

config.py

/pages
    01_🏠_Dashboard.py
    02_🔍_Radar_de_Licitacoes.py
    03_⭐_Oportunidades.py
    04_📑_Detalhes.py
    05_🏛️_Orgaos.py
    06_📅_Atas.py
    07_📋_Contratos.py
    08_📊_Estatisticas.py
    09_⚙️_Configuracoes.py

/api
    pncp.py

/services

/models

/database

/assets
```

---

# 🔌 Fonte de Dados

Portal Nacional de Contratações Públicas (PNCP)

API Oficial

Principais consultas:

- Contratações
- Licitações
- Recebimento de propostas
- Atas de Registro de Preço
- Contratos
- Plano de Contratação Anual (PCA)

---

# 🛠 Tecnologias

- Python
- Streamlit
- Requests
- Pandas
- SQLite
- Plotly
- GitHub

---

# 📈 Roadmap

## Versão 1

- Dashboard
- Radar de Licitações
- Consulta à API PNCP
- Filtros
- Detalhes da contratação

---

## Versão 2

- Sistema de Score
- Favoritos
- Histórico
- Exportação Excel

---

## Versão 3

- Inteligência Artificial
- Leitura automática de editais
- Classificação automática
- Alertas

---

## Versão 4

- Banco histórico
- Indicadores avançados
- Dashboard Executivo
- Análise preditiva

---

# 📊 Público-alvo

O sistema foi desenvolvido para empresas que participam de licitações públicas, especialmente dos segmentos de:

- Engenharia
- Reformas
- Construção Civil
- Manutenção Predial
- Pintura
- Fachadas
- Impermeabilização
- Serviços de Engenharia

---

# 📄 Licença

Projeto desenvolvido para uso interno da **SCM Reformas e Engenharia**.

---

# 👩‍💻 Desenvolvido por

**SCM Reformas e Engenharia**

Projeto SCM_GOV

Plataforma de Inteligência para Licitações Públicas.
