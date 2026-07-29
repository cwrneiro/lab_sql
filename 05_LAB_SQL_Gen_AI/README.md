<img src="https://raw.githubusercontent.com/Databricks-BR/lab_sql/main/images/header_handson_sql.png">

# Hands-On LAB 05 - Funcionalidades de Generative AI no SQL

Treinamento Hands-on na plataforma Databricks com foco nas funcionalidades de Analytics (SQL, Query, Dask, DataViz, SQL end-point).


## Exercício 07.01 - Sobre as Funcionalidades:


Uma forma de aplicar os modelos de IA Generativa é utilizar as Databricks AI SQL Functions.

Estas permitem a utilização de SQL, uma linguagem amplamente utiliza por analistas de dados e de negócio, para executar uma LLM sobre nossos bancos de dados corporativos. Com isso, também podemos criar novas tabelas com as informações extraídas para serem utilizadas em nossas análises mais facilmente.

Existem funções nativas para executar tarefas pré-definidas ou enviar qualquer instrução desejada para ser executada. Seguem as descrições abaixo:



| Gen AI SQL Function | Descrição |
| -- | -- |
| [ai_analyze_sentiment](https://docs.databricks.com/pt/sql/language-manual/functions/ai_analyze_sentiment.html) | Análise de Sentimento |
| [ai_classify](https://docs.databricks.com/pt/sql/language-manual/functions/ai_classify.html) | Classificação de Texto |
| [ai_extract](https://docs.databricks.com/pt/sql/language-manual/functions/ai_extract.html) | Extração de Termos |
| [ai_fix_grammar](https://docs.databricks.com/pt/sql/language-manual/functions/ai_fix_grammar.html) | Correção de Gramática |
| [ai_gen](https://docs.databricks.com/pt/sql/language-manual/functions/ai_gen.html) | Geração de Textos | 
| [ai_mask](https://docs.databricks.com/pt/sql/language-manual/functions/ai_mask.html) | Marcaramento de dados sensíveis |
| [ai_query](https://docs.databricks.com/pt/sql/language-manual/functions/ai_query.html) | Consultas Gen Ai |
| [ai_similarity](https://docs.databricks.com/pt/sql/language-manual/functions/ai_similarity.html) | Análise de Similaridade |
| [ai_summarize](https://docs.databricks.com/pt/sql/language-manual/functions/ai_summarize.html) | Sumarização de Textos |
| [ai_translate](https://docs.databricks.com/pt/sql/language-manual/functions/ai_translate.html) | Tradução de Textos |


</br></br>
Para esse exercício, vamos explorar as funcionalidades citadas,  conforme exemplo abaixo:

**ai_translate**
``` md
SELECT texto as original, 
       ai_translate(texto, 'br') as traducao
  FROM (select 'Hello, how are you?' as texto)
;
```
</br>

**ai_extract**

``` md
SELECT ai_extract(
    'Envie um email para jane.doe@example.com sobre a reunião que marcamos as 10am.',
    array('email', 'time')
  );
```

**ai_mask**.
``` md

SELECT ai_mask(
    'Me chamo Flavio Da Silva. Entre em contato comigo no 555-1234 ou nos visite na Av.Paulista, 1000',
    array('phone', 'address')
);
```

**ai_gen**
``` md
SELECT nome_procedimento
     , ai_gen(concat('explique em linguagem simples, para um beneficiário de plano de saúde, para que serve o procedimento ',nome_procedimento,'. Forneça um texto de até 50 palavras')) 
  FROM dbacademy.<seu_database>.dim_procedimento 
 LIMIT 10
 ;
```

Agora vamos pegar nossa tabela de procedimentos,</br> 
criar uma nova coluna atribuindo comentários (feedback fictício de beneficiários) a cada procedimento de forma aleatória usando a função **ai_gen** </br>
e depois criar uma nova coluna com a análise de sentimento da coluna de comentários usando a função **ai_analyze_sentiment**.

``` md
WITH 
sizing AS (SELECT * FROM dbacademy.<seu_database>.dim_procedimento LIMIT 10),
comentarios AS (
    SELECT
    CASE
            WHEN rand() > 0.5 THEN ai_gen(CONCAT('Escreva em português um comentário positivo de um beneficiário sobre o atendimento do procedimento: ', nome_procedimento))
            ELSE ai_gen(CONCAT('Invente em português um comentário negativo de um beneficiário sobre a demora no procedimento ', nome_procedimento,'. Seja criativo'))
    END AS procedimento_review
    FROM sizing
)
    SELECT
    *,
    ai_analyze_sentiment(procedimento_review) AS sentimento_review
    FROM comentarios;
```


</br></br>
</br></br>


