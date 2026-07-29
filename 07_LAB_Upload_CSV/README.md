<img src="https://raw.githubusercontent.com/Databricks-BR/lab_sql/main/images/header_handson_sql.png">

# Hands-On LAB 07 - Importando uma Planilha (CSV) pela Interface

Treinamento Hands-on na plataforma Databricks com foco nas funcionalidades de Analytics (SQL, Query, DataViz, Genie).


## Objetivos do Exercício

O objetivo desse laboratório é aprender a **subir uma planilha própria (arquivo CSV) para o Databricks usando apenas a interface (UI), sem precisar escrever código de ingestão**. Ao final, você terá transformado uma planilha do seu dia a dia em uma **tabela governada no Unity Catalog**, pronta para ser consultada em SQL, usada em Dashboards ou explorada no Genie.</br>
</br>
Esse é um cenário muito comum para o **Curador de Dados**: muitas vezes você tem uma lista mantida em Excel/planilha (uma tabela de referência, um cadastro auxiliar, uma lista de metas) e precisa disponibilizá-la para análise. Aqui você fará isso de ponta a ponta, seguindo o padrão de nomeação `dbacademy.<seu_database>.<tabela>` usado nos demais labs.
</br></br>
Vamos usar como exemplo uma **tabela de metas de atendimento por município** — algo típico do contexto de uma operadora de saúde.
</br></br>


## Exercício 07.01 - Preparando o arquivo CSV de exemplo

Antes de subir qualquer dado, você precisa de um arquivo `.csv` no seu computador. Um arquivo CSV é simplesmente uma planilha salva como **texto separado por vírgulas** — a primeira linha são os nomes das colunas (o cabeçalho) e cada linha seguinte é um registro.

1. Abra um editor de texto simples (Bloco de Notas / TextEdit) **ou** o Excel / Google Sheets.
2. Copie o conteúdo abaixo:

``` md
municipio,meta_atendimentos,ano
Campinas,12000,2026
Valinhos,3500,2026
Vinhedo,2100,2026
Sumaré,4800,2026
Hortolândia,4200,2026
Paulínia,2600,2026
Indaiatuba,5300,2026
```

3. Salve o arquivo com o nome **`metas_municipio.csv`**.
   - No Bloco de Notas / TextEdit: cole o texto e salve com a extensão `.csv` (em "Salvar como", escolha *Todos os arquivos* e digite o nome com `.csv`).
   - No Excel / Google Sheets: cole os dados em células (ou digite), depois use *Arquivo > Salvar como / Baixar* e escolha o formato **CSV (separado por vírgulas)**.

> **Dica:** Na prática, essa planilha pode ser qualquer base própria sua — uma lista de CIDs, um cadastro de prestadores, uma tabela de metas. O importante é que a **primeira linha contenha os nomes das colunas**.


## Exercício 07.02 - Fazendo o upload pela interface do Databricks

Agora vamos subir o arquivo `metas_municipio.csv` usando a UI do Databricks. Nenhum código é necessário nesta etapa.

1. No topo do menu lateral, clique no botão **"+ New"** (Novo).
2. Escolha a opção **"Add or upload data"** (Adicionar ou carregar dados).
3. Na tela que abrir, selecione **"Create or modify table"** (Criar ou modificar tabela) — essa é a opção para subir um arquivo e virar tabela.
4. **Selecione o arquivo**: arraste o `metas_municipio.csv` para a área indicada **ou** clique para procurá-lo no seu computador.
5. Aguarde o upload. O Databricks vai ler o arquivo e mostrar uma **prévia dos dados** já organizados em colunas.


## Exercício 07.03 - Escolhendo o destino e revisando as colunas

Ainda na mesma tela de upload, você define **onde** a tabela será criada e confirma como os dados foram interpretados.

1. No topo da prévia, escolha o **catálogo**: selecione **`dbacademy`**.
2. Escolha o **schema (database)**: selecione o **`<seu_database>`** (o mesmo que você vem usando nos outros labs, normalmente o seu login).
3. Confira a caixa **"First row contains the header"** (A primeira linha contém o cabeçalho) — ela deve estar **marcada**, para que `municipio`, `meta_atendimentos` e `ano` virem nomes de coluna (e não uma linha de dados).
4. **Revise os tipos de coluna inferidos** pelo Databricks:
   - `municipio` → `STRING` (texto)
   - `meta_atendimentos` → `INT` ou `BIGINT` (número inteiro)
   - `ano` → `INT`
   - Se algum tipo não fizer sentido, clique sobre o nome do tipo e ajuste. Para dados de referência, deixar como `STRING` quando houver dúvida é seguro.
5. No campo **"Table name"** (Nome da tabela), digite: **`metas_municipio`**.
6. Clique em **"Create table"** (Criar tabela).

Pronto! Sua planilha agora é a tabela `dbacademy.<seu_database>.metas_municipio`, governada pelo Unity Catalog.


## Exercício 07.04 - Consultando a tabela recém-criada

Vamos confirmar que os dados chegaram corretamente. Abra o **"SQL Editor"** no menu lateral e execute:

``` sql
SELECT *
FROM dbacademy.<seu_database>.metas_municipio;
```

Você deve ver as mesmas 7 linhas que estavam na sua planilha, agora consultáveis em SQL.


## Exercício 07.05 - Validando os dados

Um bom curador sempre valida a base depois de subir. Vamos fazer algumas checagens simples.

1. **Contar quantas linhas foram carregadas** (esperamos 7):

``` sql
SELECT count(*) AS total_linhas
FROM dbacademy.<seu_database>.metas_municipio;
```

2. **Conferir os valores distintos de uma coluna** (quais municípios entraram):

``` sql
SELECT DISTINCT municipio
FROM dbacademy.<seu_database>.metas_municipio
ORDER BY municipio;
```

3. **Verificar se algum campo essencial veio vazio** (nulo) — útil para achar problemas na planilha original:

``` sql
SELECT count(*) AS linhas_sem_meta
FROM dbacademy.<seu_database>.metas_municipio
WHERE meta_atendimentos IS NULL;
```

4. **Uma pequena análise** — soma das metas por ano:

``` sql
SELECT ano,
       count(*)               AS qtd_municipios,
       sum(meta_atendimentos) AS meta_total
FROM dbacademy.<seu_database>.metas_municipio
GROUP BY ano
ORDER BY ano;
```


## Conclusão

Você acabou de disponibilizar uma **base própria** no Databricks sem depender do time de engenharia de dados: bastou subir a planilha pela interface. A partir de agora, essa tabela pode ser cruzada com outras bases em SQL, virar um gráfico no **Dashboard** (Lab 05) ou ser explorada em linguagem natural pelo **Genie** (Lab 06).

> **No dia a dia do Curador de Dados:** sempre que você tiver uma lista de referência mantida em Excel (metas, cadastros, listas de CIDs, tabelas de-para), esse fluxo permite publicá-la rapidamente para análise — mantendo tudo governado no Unity Catalog e disponível para o restante da equipe.

#### Referência:
* [Databricks Help - Create or modify a table using file upload](https://docs.databricks.com/ingestion/add-data/upload-data.html)
