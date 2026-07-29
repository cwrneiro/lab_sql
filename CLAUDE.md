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

- Roda no **workspace do cliente**, **não** na Databricks Free Edition (o upstream assume
  Free Edition — ao trazer mudanças do upstream, reverifique isso).
- Padrão de nomeação em todos os labs: **`dbacademy.<seu_database>.<tabela>`**
  (`catalog_name = "dbacademy"`, `schema_name` = login/schema do usuário). Estão como
  **placeholder** — trocar pelos valores reais quando o catálogo/schema de treino for
  definido. Busca global: `dbacademy`, `<seu_database>`, `<seu_usuario>`, `schema_name`.
- **Criação de salas Genie pode ser restrita** para os participantes. Por isso o
  `07_LAB_Genie` é dividido em **[DEMO – instrutor]** (criar/configurar a sala) e
  **[HANDS-ON – todos]** (só consumir uma sala pré-criada). Plano B: se nem o instrutor
  puder criar no workspace do cliente, rodar o lab inteiro como demo em ambiente próprio.

## Estrutura dos módulos (ordem do dia)

| Pasta | Conteúdo | Notas |
|---|---|---|
| `00_Abertura/` | Roteiro de slides: objetivo, transacional × analítico, como os dados chegam, tour da plataforma, casos de IA em saúde | Markdown como slides; casos de IA são ilustrativos, **confirmar antes do evento** |
| `01_LAB_Query_Editor/` | SQL Editor: DDL/DML com `tipo_plano` (segmentação ANS) + consultas às tabelas de saúde | Exs. 01.06–01.09 (Liquid Clustering/Time Travel) marcados **opcionais/demo** |
| `02_LAB_Notebook/` | Notebook Python que **carrega os CSVs** de `dados/` como tabelas Delta | `lab02_01_carga_csv.ipynb` — ver "Dados" abaixo |
| `05_LAB_SQL_Gen_AI/` | AI SQL Functions (`ai_gen`, `ai_analyze_sentiment`, etc.) sobre procedimentos | **Não** é o "Databricks Assistant"; são funções SQL de IA |
| `06_LAB_Dashboard/` | AI/BI Dashboard: série temporal de sinistros + ranking de prestadores (via Genie Code) | Numeração `06.xx` |
| `07_LAB_Genie/` | AI/BI Genie em modo DEMO + HANDS-ON | Ver restrição de ambiente acima |
| `08_LAB_Upload_CSV/` | Upload de planilha pela UI → criar tabela → validar | Cliente pediu explicitamente; o aluno cria a tabela `metas_municipio` |

Os módulos **03 (Query Profiler)** e **04 (Alert)** do upstream foram **removidos**
(avançados, fora do escopo básico). Não os reintroduza sem motivo.

## Dados (`dados/`)

Dataset **sintético** de operadora de saúde, gerado por **`dados/gerar_dados_saude.py`**
(seed fixa = reprodutível; **sem PII** — nomes tipo `BENEFICIARIO 00001`). Para
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

1. **Join errado vs. certo (Lab 07 – constraints):** `sinistros.id_prestador` casa com
   `dim_prestador.cod` (a chave correta) e **NÃO** com `dim_prestador.id_prestador`.
   O lab ensina a adicionar a constraint correta. Verificado: 100% em `cod`, 0% em `id`.
2. **Coluna mal nomeada (Lab 07):** o nome do prestador está em `dim_prestador.xpto`
   (de propósito); o lab ensina a documentar com `COMMENT`.
3. **Jargão (Lab 07 – instruções):** "alta complexidade" = `categoria_procedimento IN
   ('INTERNACAO','CIRURGIA')` — não existe como valor literal; ensina instruções da Genie.
4. **Taxa/proporção (`guias`):** `qt_autorizada / qt_solicitada` = taxa de autorização.

## Convenções de conteúdo

- Cada lab: header `<img ...>`, título `# Hands-On LAB NN - <título>`, `## Objetivos do
  Exercício`, exercícios numerados `## Exercício NN.xx - ...`, blocos ```sql / ```md.
- Escreva **testando o SQL contra os schemas reais** dos CSVs (nomes de coluna acima).
- Ao adicionar/editar SQL, valide os nomes de tabela/coluna antes de commitar.
- Commits: mensagens em pt-BR descritivas. Trabalhe na branch `unimed-campinas`.

## Pendências (coordenação — fora do código)

- [ ] Avisar o autor do repo upstream que houve fork/adaptação.
- [ ] Confirmar com os donos do workspace do cliente se dá para criar Genie agent
      (senão, preparar demo em ambiente próprio).
- [ ] Definir `catalog_name`/`schema_name` reais e trocar os placeholders.
- [ ] Selecionar/confirmar os casos reais de sucesso de IA em saúde para a abertura.
- [ ] Dry run (acessos, upload de CSV, SQL warehouse) antes do evento.
- [ ] Preparar a sala Genie pré-configurada (tabelas + instruções) para o hands-on.
