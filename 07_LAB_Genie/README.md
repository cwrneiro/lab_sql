<img src="https://raw.githubusercontent.com/Databricks-BR/genie_ai_bi/main/images/header_genie.png">

# Hands-On LAB 07 - AI/BI Genie

Treinamento Hands-on na plataforma Databricks com foco nas funcionalidades de perguntas e respostas usando linguagem natural.

</br></br>

> ⚠️ **Nota para a turma da Unimed Campinas**
> Neste ambiente os participantes **não têm permissão para criar salas Genie** (`Genie space`). Por isso este laboratório é dividido em dois modos:
> - **[DEMO – instrutor]** — passos de criação/configuração da sala. O instrutor executa e projeta; a turma acompanha.
> - **[HANDS-ON – todos]** — fazer perguntas em uma sala Genie **já criada e compartilhada** pelo instrutor. É aqui que a turma pratica.
>
> **Pré-requisito do instrutor:** criar a Genie Space sobre as tabelas de saúde **antes** do treinamento e compartilhar o link com a turma (permissão *Can run*). Caso a criação de salas também esteja bloqueada para o instrutor no workspace, rode o laboratório inteiro como demonstração a partir de um ambiente próprio (plano B combinado no projeto UCDD).

## Objetivos do Exercício

O objetivo desse laboratório é usar o AI/BI Genie para permitir a análise dos dados da **operadora de saúde** (sinistros, guias, beneficiários) utilizando somente **Português**.</br>
***Caso os dados ainda não tenham sido carregados, execute antes o Lab 02 - LAB_Notebook.***
</br></br>

## Exercício 07.00 - Preparação

1. Em alguns momentos utilizaremos o SQL Editor. Deixe-o preparado em outra janela e selecione seu database.

<img src="https://github.com/Gabriel-Rangel/lab_sql/blob/main/images/v2_genie_1.png?raw=true">

</br></br>

## Exercício 07.01 - Criar a AI/BI Genie **[DEMO – instrutor]**

> A turma **não** executa esta seção — apenas acompanha. Ela mostra *como* uma sala é montada, para que os curadores entendam o que está por trás das respostas.

Vamos criar uma Genie para fazer nossas perguntas. Para isso, seguimos os passos abaixo:

1. No menu principal (à esquerda), clique em `New` > `Genie space`

<img src="https://raw.githubusercontent.com/Databricks-BR/genie_ai_bi/main/images/genie_01.png" width=300><br><br>

2. Configure a Genie
    - Selecione as seguintes tabelas:
        - `sinistros`
        - `guias`
        - `dim_beneficiario`
        - `dim_procedimento`
        - `dim_prestador`
    - Clique em `Create`

3. Altere o nome da Genie Space (ex.: **"Genie — Operadora de Saúde"**).

4. Clique em **Instructions** e atribua a instrução para que as respostas sejam em português:

    ``` %md
    * responda em português (Brasil)
    ```

</br></br>

## Exercício 07.02 - Fazendo perguntas ao AI/BI Genie **[HANDS-ON – todos]**

> Abra o **link da sala Genie compartilhado pelo instrutor** e faça as perguntas abaixo no chat.

- Qual o valor total de sinistros em jun/2025?
- Agora, quebre por categoria de procedimento
- Mantenha somente as 10 categorias com maior valor
- Qual o total de procedimentos realizados de exames?
- Qual o valor total de sinistros de internações?
- Quais os 5 municípios de beneficiários com maior valor de sinistro?
- Qual a taxa de autorização das guias (autorizadas sobre solicitadas) em 2025?

<img src="https://raw.githubusercontent.com/Databricks-BR/genie_ai_bi/main/images/genie_05.png"><br><br>

Notem que, mesmo com muito pouco contexto, a Genie já consegue:
- Inferir quais as tabelas e colunas relevantes para responder as perguntas
- Aplicar filtros e agregações
- Responder perguntas adicionais sobre uma resposta anterior
- Entender jargões
- Combinar diferentes tabelas
- Calcular métricas derivadas

Aproveitem para explorar e fazer perguntas adicionais!

</br>

## Exercício 07.03 - Usando comentários e *constraints* **[DEMO – instrutor]**

> Seção conduzida pelo instrutor. Ilustra por que **documentar tabelas e definir chaves** (trabalho típico do curador de dados!) melhora as respostas da Genie.

Podem ocorrer cenários onde precisamos fornecer contexto adicional à Genie para respostas mais precisas.

A primeira forma é **documentar as tabelas**. Todos os comentários adicionados às tabelas são usados pela Genie para entender melhor o dado. Outra boa prática é adicionar *constraints*, ajudando a Genie a associar corretamente as tabelas.

1. Faça a seguinte pergunta:
   ```%md
    Qual o valor total de sinistros por prestador? Exiba o nome do prestador
    ```

2. OPS! Parece que a Genie não conseguiu realizar a consulta corretamente.

3. A coluna **xpto** da tabela **dim_prestador** é a que contém o nome do prestador — precisamos explicar isso. Além disso, a coluna **id_prestador** de `dim_prestador` **não** é o melhor campo para cruzar com `sinistros`: a chave correta é **cod**! Vamos corrigir rodando no **SQL EDITOR**:

    ``` sql
    ALTER TABLE dim_prestador ALTER COLUMN xpto COMMENT 'Nome do prestador';
    ALTER TABLE dim_prestador ALTER COLUMN cod SET NOT NULL;
    ALTER TABLE dim_prestador ADD CONSTRAINT pk_dim_prestador PRIMARY KEY (cod);
    ALTER TABLE sinistros ADD CONSTRAINT fk_sinistro_dim_prestador FOREIGN KEY (id_prestador) REFERENCES dim_prestador(cod);
    ```
</br>

4. Faça novamente a pergunta anterior.<br><br>

Pronto! Com essas informações a Genie já responde corretamente.

Documentar tabelas com comentários é sempre uma boa prática, assim como atribuir chaves primárias e estrangeiras.</br>
Isso ajuda a compreensão, a descoberta e o reaproveitamento dos dados por outras pessoas — e ainda melhora as respostas da Genie. **Esse é justamente o papel do curador de dados.**
</br></br>

## Exercício 07.04 - Usando instruções **[DEMO – instrutor]**

Como vimos, a Genie usa toda a documentação das tabelas para responder. No entanto, por segurança, ela **não** tem acesso aos dados em si!

Para complementar o conhecimento da Genie, podemos criar **instruções**: sentenças em linguagem natural que explicam abreviações, jargões, formatos e cálculos de métricas.

1. Faça a pergunta:
    ``` %md
    Qual o valor total de sinistros de alta complexidade?
    ```

2. O resultado não parece correto! Na nossa base, o termo "alta complexidade" não aparece. Aqui consideramos alta complexidade os procedimentos de **internação e cirurgia**. Adicione a instrução:
    ``` %md
    * para indicadores de "alta complexidade", filtre categoria_procedimento IN ('INTERNACAO','CIRURGIA')
    ```

3. Faça novamente a pergunta anterior.

Pronto! Agora a Genie já responde perguntas sobre alta complexidade também!

</br></br>

## Exercício 07.05 - Usando funções **[DEMO – instrutor]**

Outro recurso para ajudar a Genie com cálculos complexos são as **funções**: guardam e parametrizam lógicas dentro do catálogo, reutilizáveis por outras pessoas e consultas — inclusive fora da Genie. Funcionam como ferramentas validadas e certificadas que a Genie pode decidir usar.

1. Faça a pergunta:
    ``` %md
    Qual o custo médio por beneficiário do procedimento HEMOGRAMA COMPLETO?
    ```

2. Para padronizar esse cálculo, crie a função abaixo no **SQL EDITOR**:

    ``` sql
    CREATE OR REPLACE FUNCTION custo_medio_procedimento(procedimento STRING)
    RETURNS TABLE(nome_procedimento STRING, custo_medio_beneficiario DOUBLE)
    COMMENT 'Use esta função para calcular o custo médio por beneficiário de um procedimento'
    RETURN
    SELECT
      p.nome_procedimento,
      sum(s.vl_sinistro) / count(DISTINCT s.id_beneficiario) AS custo_medio_beneficiario
    FROM sinistros s
    LEFT JOIN dim_procedimento p
      ON s.id_procedimento = p.id_procedimento
    WHERE p.nome_procedimento = trim(upper(custo_medio_procedimento.procedimento))
    GROUP BY ALL
    ```

3. Adicione a função à Genie: clique na seta para baixo ao lado de `Add` e selecione `SQL function`.

<img src="https://github.com/Gabriel-Rangel/lab_sql/blob/main/images/v2_genie_9.png?raw=true">
</br>

4. Escolha a função criada selecionando o catálogo, schema/database e a função.

<img src="https://github.com/Gabriel-Rangel/lab_sql/blob/main/images/v2_genie_10.png?raw=true">

5. Faça novamente a pergunta anterior.

Pronto! Com isso conseguimos calcular o custo médio do procedimento de forma padronizada!

<br><br>

# Parabéns!

Você concluiu o laboratório do **AI/BI Genie**!

Agora você já sabe como utilizar a Genie para analisar dados usando somente linguagem natural — e entende como a **documentação, as chaves e as instruções** (o trabalho do curador de dados) melhoram diretamente a qualidade das respostas.
