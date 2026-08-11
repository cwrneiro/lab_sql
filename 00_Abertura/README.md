# 00 - Abertura e Contextualização

## 1 — Boas-vindas

- **Databricks Day**
- **Treinamento para Curadores de Dados**
- **Unimed Campinas**
- Um dia inteiro, mão na massa (hands-on)

---

## 2 — Objetivos do treinamento + Agenda do dia

**O que você vai aprender hoje:**
- Entender o que é a plataforma Databricks e por que a usamos
- Navegar com autonomia: encontrar catálogos, schemas e tabelas
- Consultar dados com SQL (do básico ao útil no dia a dia)
- Criar visualizações, dashboards e usar IA (Genie) para perguntar em linguagem natural

**Agenda (dia inteiro, hands-on):**
- Abertura e contextualização (agora)
- Tour de navegação da plataforma
- Lab 01 - Query Editor (SQL)
- Lab 02 - Notebook
- Lab 03 - Alertas
- Lab 04 - SQL + Gen AI
- Lab 05 - Dashboards
- Lab 06 - Genie
- Lab 07 - Upload de CSV

---

## 3 — Quem somos / O papel do Curador de Dados

- **Curador de dados** = quem cuida da qualidade, do significado e do bom uso dos dados
- Você é a ponte entre **quem gera o dado** e **quem toma decisão** com ele
- No dia a dia: entender de onde vem o dado, garantir que está correto, organizar e disponibilizar para análise
- Não precisa ser programador: hoje o foco é **SQL e ferramentas visuais**

---

## 4 — Ambiente transacional × Ambiente analítico

**Ambiente transacional** (o sistema do dia a dia)
- Registra as operações **na hora que acontecem**: autorização de guia, cadastro de beneficiário, atendimento
- Feito para **anotar rápido**, um registro de cada vez
- Ex.: sistema de gestão da operadora

**Ambiente analítico** (onde a gente analisa)
- Junta o **histórico** de tudo que aconteceu para **analisar e comparar**
- Feito para **responder perguntas** sobre muitos registros de uma vez
- Ex.: Databricks

**Analogia para quem vem do Excel:**
- Transacional = a **planilha onde você digita** cada lançamento
- Analítico = a **planilha dinâmica / relatório** que resume milhões de lançamentos para você entender o quadro geral

---

## 5 — Como os dados chegam ao Databricks

Fluxo macro (conceitual, sem detalhes técnicos):

1. **Sistemas de origem** — onde o dado nasce (sistema da operadora, planilhas, arquivos, APIs)
2. **Ingestão** — cópias organizadas desses dados são trazidas para a plataforma
3. **Lakehouse + Unity Catalog** — os dados ficam guardados, organizados e **governados** (com controle de acesso) em um só lugar
4. **Consumo** — você usa os dados em **SQL, Dashboards e Genie** para analisar e decidir

`Sistemas de origem → Ingestão → Lakehouse / Unity Catalog → SQL · Dashboards · Genie`

- **Governança**: cada pessoa vê só o que tem permissão para ver
- Você trabalha principalmente na ponta do **consumo**

---

## 6 — Tour da plataforma: Workspace

- **O que é:** o seu "escritório" dentro do Databricks — a área onde você trabalha
- Reúne suas consultas, notebooks, dashboards e pastas
- **Onde fica:** é o próprio site que você acessa ao entrar; o menu lateral esquerdo dá acesso a tudo
- Comparação: como a **janela do seu computador** com todas as ferramentas à mão

---

## 7 — Tour da plataforma: Catálogo (Catalog)

- **O que é:** o nível mais alto de organização dos dados — a "estante" principal
- Agrupa vários schemas relacionados
- **Onde fica:** menu lateral → **Catalog**
- Comparação: como uma **pasta principal** que guarda outras pastas

---

## 8 — Tour da plataforma: Schema (Database)

- **O que é:** uma divisão dentro do catálogo que agrupa tabelas de um mesmo assunto
- Ex.: um schema para "beneficiários", outro para "autorizações"
- **Onde fica:** dentro de um catálogo, no **Catalog Explorer**
- Comparação: uma **subpasta** dentro da estante, ou uma **aba temática** de uma pasta de trabalho

---

## 9 — Tour da plataforma: Tabelas (Tables)

- **O que é:** onde os dados de fato ficam, em **linhas e colunas**
- Muito parecido com uma **planilha do Excel**: cada linha um registro, cada coluna um campo
- Dá para ver a estrutura das colunas (Schema/Sample Data) e uma prévia dos dados
- **Onde fica:** dentro de um schema, no **Catalog Explorer**

---

## 10 — Tour da plataforma: Notebook

- **O que é:** um documento interativo onde você escreve consultas (SQL) e vê os resultados logo abaixo
- Permite misturar **código, texto explicativo e gráficos** no mesmo lugar
- Ótimo para explorar dados passo a passo e documentar o raciocínio
- **Onde fica:** menu lateral → **Workspace / New → Notebook**

---

## 11 — Tour da plataforma: Dashboards (AI/BI)

- **O que é:** painéis visuais com gráficos, números e tabelas para acompanhar indicadores
- Contam a "história dos dados" de forma visual, fáceis de **compartilhar** com a equipe
- Atualizam conforme os dados mudam
- **Onde fica:** menu lateral → **Dashboards**
- Bônus: o **Genie** deixa você **perguntar em linguagem natural** (ex.: "quantas autorizações foram emitidas neste mês?") e recebe a resposta com gráfico

---

## 12 — Casos de sucesso de IA em saúde (ilustrativos)

> **Atenção:** exemplos **ilustrativos e genéricos** do uso de IA/analytics em operadoras e planos de saúde. **Confirmar/atualizar** com casos reais e números antes do evento.

- **Previsão de sinistralidade** — usar o histórico para antecipar custos assistenciais e apoiar o planejamento financeiro
- **Priorização de autorizações** — apoiar a triagem de guias/pedidos, agilizando os casos simples e destacando os que precisam de análise humana
- **Análise da jornada do beneficiário** — entender o caminho do paciente entre atendimentos para melhorar experiência, adesão e prevenção

---

## 13 — Vamos para a prática!

- Agora começa o **hands-on**
- Todos com acesso ao ambiente? Login funcionando?
- Ritmo: acompanhem no seu ritmo, tirem dúvidas a qualquer momento
- **Próximo passo: Lab 01 - Query Editor (SQL)**

