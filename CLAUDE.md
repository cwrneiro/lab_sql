# CLAUDE.md

Guidance for Claude Code (and humans) working in this repository.

## O que é este repositório

Fork adaptado do workshop **Databricks SQL Labs** (`CaduBettanim/lab_sql`, upstream)
para um **treinamento presencial de nível básico** destinado a **Curadores de Dados
(Data Stewards)**. Todo o conteúdo é em **português do Brasil**.

O trabalho de adaptação vive na branch **`unimed-campinas`** (não na `main`).
Remotes: `origin` = fork pessoal; `upstream` = repo original (para puxar atualizações).

> ⚠️ **Repositório público.** Não coloque neste repo nomes de funcionários do cliente,
> conteúdo de reuniões, estratégia comercial, credenciais, IDs de workspace ou qualquer
> PII. O dataset é 100% **sintético** (ver abaixo). Mantenha assim.

## Objetivo do workshop

Capacitar curadores de dados no **uso básico** do Databricks: navegação na plataforma,
exploração/consulta de dados em SQL, importação de planilha, dashboards e Genie.
Abordagem **prática (hands-on)**, com exemplos no contexto de **operadora de plano de
saúde**. Público heterogêneo (de usuários de Excel a quem já conhece Databricks); assuma
o **menor denominador comum** ao escrever conteúdo — linguagem simples, passo a passo.

Formato-alvo: **dia inteiro, presencial, hands-on guiado**, turma pequena (≤20), com
"floor helpers" circulando. Fio condutor: **um único dataset de saúde o dia inteiro**
(descobre no Catálogo → consulta em SQL/Notebook → importa CSV → visualiza no Dashboard →
pergunta no Genie).

## Restrições de ambiente (importantes)

- Roda na **Databricks Free Edition** (cada participante usa a própria conta gratuita),
  igual à premissa do upstream. Chegou-se a considerar o workspace do cliente, mas a
  criação de recursos (ex.: Genie) é restrita lá — por isso o workshop inteiro roda na
  Free Edition.
- Padrão de nomeação em todos os labs: **`dbacademy.<seu_database>.<tabela>`**
  (`catalog_name = "dbacademy"`, `schema_name` = login/schema do usuário), **como no repo
  original** — cada aluno cria o próprio catálogo/schema no Lab 01. Mantidos como
  placeholder de propósito. Busca global: `dbacademy`, `<seu_database>`, `<seu_usuario>`,
  `schema_name`.
- **Genie é hands-on para todos:** cada participante **cria e configura a própria sala
  Genie** durante o workshop (não há sala pré-configurada). Por isso o `06_LAB_Genie` é
  todo hands-on — sem divisão DEMO/HANDS-ON.

## Estrutura dos módulos (ordem do dia)

| Pasta | Conteúdo | Notas |
|---|---|---|
| `00_Abertura/` | Roteiro de slides: objetivo, transacional × analítico, como os dados chegam, tour da plataforma, casos de IA em saúde | Markdown como slides; casos de IA são ilustrativos, **confirmar antes do evento** |
| `01_LAB_Query_Editor/` | SQL Editor: DDL/DML com `tipo_plano` (segmentação ANS) + consultas às tabelas de saúde | Exs. 01.06–01.09 (Liquid Clustering/Time Travel) marcados **opcionais/demo** |
| `02_LAB_Notebook/` | Notebook Python que **carrega os CSVs** de `dados/` como tabelas Delta | `lab02_01_carga_csv.ipynb` — ver "Dados" abaixo |
| `03_LAB_Alert/` | Alerta do Databricks SQL: monitora o total de `vl_sinistro` dos últimos 30 dias | Adaptado do upstream (era `stock_bigtech`/AAPL) para o contexto de saúde |
| `04_LAB_SQL_Gen_AI/` | AI SQL Functions (`ai_gen`, `ai_analyze_sentiment`, etc.) sobre procedimentos | **Não** é o "Databricks Assistant"; são funções SQL de IA |
| `05_LAB_Dashboard/` | AI/BI Dashboard: série temporal de sinistros + ranking de prestadores (via Genie Code) | Numeração `05.xx` |
| `06_LAB_Genie/` | AI/BI Genie — hands-on: cada participante cria a própria sala | Ver restrição de ambiente acima |
| `07_LAB_Upload_CSV/` | Upload de planilha pela UI → criar tabela → validar | Cliente pediu explicitamente; o aluno cria a tabela `metas_municipio` |

O módulo **Query Profiler** do upstream foi **removido** (avançado, fora do escopo
básico). Não o reintroduza sem motivo. O módulo **Alert** foi **reintroduzido** como
`03_LAB_Alert`, adaptado ao contexto de saúde.

## Dados (`dados/`)

Dataset **sintético** de operadora de saúde, gerado por **`dados/gerar_dados_saude.py`**
(seed fixa; **sem PII** — nomes tipo `BENEFICIARIO 00001`). **Datas em janela rolante:**
`sinistros.dt_atendimento` e `guias.dt_solicitacao` vão de `hoje-365d` até `date.today()`
(e `dt_adesao` é histórica, anterior à janela). Isso mantém o alerta do Lab 03
(`current_date() - INTERVAL 30 DAYS`) sempre com dados recentes. **Consequência:** os
dados **não são mais reprodutíveis entre dias** — regenere e faça `git push` dos CSVs
**pouco antes do evento**. Para
regenerar: `python3 dados/gerar_dados_saude.py`. O notebook do Lab 02 lê os CSVs via URL
raw do GitHub (branch `unimed-campinas`) — **mudanças em `dados/` só chegam ao notebook
após `git push`**.

| Tabela | Linhas | Papel | Chave |
|---|---|---|---|
| `dim_beneficiario` | 2.000 | dimensão | `id_beneficiario` |
| `dim_procedimento` | 400 | dimensão | `id_procedimento` |
| `dim_prestador` | 300 | dimensão | `id_prestador`, **`cod`** |
| `sinistros` | 40.000 | fato | FKs abaixo |
| `guias` | 10.000 | fato (autorizações) | — |

Colunas relevantes: `sinistros(id_sinistro, id_beneficiario, id_prestador,
id_procedimento, dt_atendimento, qt_procedimento, vl_sinistro)`;
`dim_procedimento(..., categoria_procedimento, especialidade, ...)`;
`dim_prestador(id_prestador, cod, rede, xpto, tipo, cep, lat_long)`;
`guias(..., status, qt_solicitada, qt_autorizada)`.

### "Pegadinhas" didáticas — PRESERVE ao mexer nos dados

O upstream embute lições no formato dos dados. A adaptação as manteve no contexto de
saúde — **não "conserte" isso sem querer**:

1. **Join errado vs. certo (Lab 06 – constraints):** `sinistros.id_prestador` casa com
   `dim_prestador.cod` (a chave correta) e **NÃO** com `dim_prestador.id_prestador`.
   O lab ensina a adicionar a constraint correta. Verificado: 100% em `cod`, 0% em `id`.
2. **Coluna mal nomeada (Lab 06):** o nome do prestador está em `dim_prestador.xpto`
   (de propósito); o lab ensina a documentar com `COMMENT`.
3. **Jargão (Lab 06 – instruções):** "alta complexidade" = `categoria_procedimento IN
   ('INTERNACAO','CIRURGIA')` — não existe como valor literal; ensina instruções da Genie.
4. **Taxa/proporção (`guias`):** `qt_autorizada / qt_solicitada` = taxa de autorização.

## Convenções de conteúdo

- Cada lab: header `<img ...>`, título `# Hands-On LAB NN - <título>`, `## Objetivos do
  Exercício`, exercícios numerados `## Exercício NN.xx - ...`, blocos ```sql / ```md.
- Escreva **testando o SQL contra os schemas reais** dos CSVs (nomes de coluna acima).
- Ao adicionar/editar SQL, valide os nomes de tabela/coluna antes de commitar.
- Commits: mensagens em pt-BR descritivas. Trabalhe na branch `unimed-campinas`.

## Pendências (coordenação — fora do código)

- [x] ~~Avisar o autor do repo upstream que houve fork/adaptação.~~ Não é necessário.
- [x] ~~Confirmar com os donos do workspace do cliente se dá para criar Genie agent.~~
      Confirmado que **não dá** — o workshop roda inteiro na **Databricks Free Edition**.
- [x] ~~Definir `catalog_name`/`schema_name` reais e trocar os placeholders.~~ Mantidos
      **como no repo original** (aluno cria o próprio no Lab 01) — sem troca.
- [x] ~~Preparar a sala Genie pré-configurada para o hands-on.~~ Não haverá sala
      pré-configurada — **cada participante cria a própria** durante o workshop (Lab 06).
- [x] ~~Dry run (acessos, upload de CSV, SQL warehouse).~~ Feito em **2026-08-06** na
      Free Edition — **todos os 7 labs rodaram de ponta a ponta**. Correções aplicadas:
      janela rolante de datas (Lab 03), CREATE catálogo/schema ativos (Labs 01/02), URL do
      notebook para o fork (Lab 02), termos de UI atualizados (Alerts/Genie Agents/Add SQL
      dataset/Upload data).
- [ ] Selecionar/confirmar os casos reais de sucesso de IA em saúde para a abertura.
      (Ainda **não confirmados**.)
- [ ] **Regenerar os CSVs e `git push` pouco antes do evento** (datas em janela rolante —
      ver seção "Dados").
- [ ] **Atualizar os screenshots** dos labs para a UI atual (Alert em editor, Genie
      Agents, "Add SQL dataset", "Upload data") — textos já ajustados; prints são o
      próximo passo.
