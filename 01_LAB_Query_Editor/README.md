
<img src="https://raw.githubusercontent.com/Databricks-BR/lab_sql/main/images/header_handson_sql.png">

# Hands-On LAB 01 - Explorando o Editor de Query

Treinamento Hands-on na plataforma Databricks com foco nas funcionalidades de Analytics (SQL, Query, DataViz, Genie).


## Objetivos do Exercício

O objetivo desse laboratório é conhecer as funcionalidades de consulta (_Query_) da plataforma Databricks, utilizando a linguagem SQL (e as interfaces visuais), explorando os potenciais Analíticos. </br>
</br>
Os exercícios deverão ser executados na opção do Menu lateral "**SQL Editor**".

<img src="https://github.com/CaduBettanim/lab_sql/blob/2fcf6023d5922037e7b70bc866419fff55a92f6e/images/v3_lab01_1.png?raw=true">


</br></br></br>
## Sessão 01:  Estrutura TABELAS, DATABASE e CATÁLOGOS

<img src="https://raw.githubusercontent.com/Databricks-BR/lab_sql/main/images/lab01_uc.png">


| Tópico | Comando |
| -- | -- |
| **Catálogo** | CREATE CATALOG <nome_catalogo> |
| **Schema** | CREATE DATABASE IF NOT EXISTS <nome_catalogo>.<nome_database>; |
| **Tabela** | CREATE OR REPLACE TABLE  <nome_catalogo>.<nome_database>.<nome_tabela>; |
| **View** |  CREATE OR REPLACE VIEW  <nome_catalogo>.<nome_database>.<nome_tabela> AS ...; |

#### Referência:
* [Databricks Help - DDL Syntax](https://docs.databricks.com/sql/language-manual/sql-ref-syntax-ddl-create-table.html)

## Exercício 01.01 - Criação do catálago e database

``` sql
--GRANT CREATE CATALOG ON METASTORE TO `account users`;
--CREATE CATALOG IF NOT EXISTS dbacademy;
USE CATALOG dbacademy;

CREATE DATABASE IF NOT EXISTS <seu_usuario>;
USE <seu_usuario>;
```

## Exercício 01.02 - Criação da Tabela
1. Na primeira query do laboratório realizamos a criação de catálago e database e utilizamos a cláusula *USE*, mas ela só é persistida em tempo de execução;
2. Devemos sempre atribuir o nome do catálago e database antes do nome da tabela separado por "." (catalogo.<seu_usuario>.tipo_plano)</br>
ou podemos especificar o catálago e database que queremos usar no próprio editor conforme imagem abaixo:
</br></br>
<img src="https://github.com/CaduBettanim/lab_sql/blob/4af0ea650f77b5feb29dcccca0c0bb5da6850d0a/images/v3_lab01_setcatalago.png?raw=true">
</br></br>

3. Crie a tabela a seguir. Ela é uma tabela auxiliar com a **segmentação assistencial** dos planos de saúde (conforme a ANS):

``` sql
CREATE OR REPLACE TABLE tipo_plano 
  ( id_tipo_plano    INT     COMMENT "codigo do tipo de plano",
    sig_tipo_plano   STRING  COMMENT "sigla do tipo de plano",
    desc_tipo_plano  STRING  COMMENT "descricao da segmentacao assistencial do plano" )
COMMENT "Tabela auxiliar da segmentacao assistencial dos planos de saude (ANS)";
```
</br>

 ## Exercício 01.03 - Inserindo dados na Tabela através de SQL INSERT

 ``` sql
 INSERT INTO tipo_plano VALUES (1, "AMB", "Ambulatorial") ;
 INSERT INTO tipo_plano VALUES (2, "HOSP", "Hospitalar sem obstetricia") ;
 INSERT INTO tipo_plano VALUES (3, "HOSPOBST", "Hospitalar com obstetricia") ;
 INSERT INTO tipo_plano VALUES (4, "REF", "Plano Referencia") ;
 INSERT INTO tipo_plano VALUES (5, "ODONTO", "Odontologico") ;
 INSERT INTO tipo_plano VALUES (6, "COMPLETO", "Ambulatorial + Hospitalar") ;
 INSERT INTO tipo_plano VALUES (7, "NULL", "NULL") ;
```

 ## Exercício 01.04 - Verificando o conteúdo da TABELA

 ``` sql
SELECT * 
FROM tipo_plano 
ORDER BY id_tipo_plano;
```

 ## Exercício 01.05 - Alterando o conteúdo da TABELA

 ``` sql
UPDATE tipo_plano  
SET desc_tipo_plano = "OUTROS" 
WHERE id_tipo_plano = 7;
```

``` sql
SELECT * 
FROM tipo_plano
WHERE id_tipo_plano = 7;
```

``` sql
DELETE 
FROM tipo_plano 
WHERE id_tipo_plano = 7;
```

``` sql
SELECT * FROM tipo_plano;
```

> ℹ️ **Exercícios 01.06 a 01.09 — opcionais / avançados.**
> Os recursos abaixo (Liquid Clustering e Time Travel) são mais avançados e não fazem parte do escopo básico. Sugerimos conduzi-los como **demonstração do instrutor**, deixando o hands-on da turma nos exercícios 01.01–01.05 e 01.10–01.11.

## Exerício 01.06 - Liquid Clustering *(opcional / avançado)*
O Liquid clustering substitui o particionamento de tabelas e o ZORDER para simplificar as decisões de disposição de dados e otimizar o desempenho das consultas. Ele oferece a flexibilidade de redefinir a chave clustering sem reescrever os dados existentes, permitindo que a disposição dos dados evolua junto com as necessidades analíticas ao longo do tempo.

Mas quando aplicar liquid clustering ?
* Tabelas normalmente filtradas por colunas de alta cardinalidade.</br>
* Tabelas com grande distorção na distribuição de dados.</br>
* Tabelas que crescem rapidamente e exigem manutenção e ações de ajuste.</br>
* Tabelas com requisitos de gravação concorrente.</br>
* Tabelas com padrões de acesso que mudam com o tempo.</br>
* Tabelas em que uma chave de partição típica poderia deixar a tabela com muitas ou poucas partições.</br>

A sintaxe para habilitar essa funcionalidade em uma tabela já criada é: </br>
<span style="color:red"> **NÃO EXECUTAR** </span>
```sql
ALTER TABLE <table_name>
CLUSTER BY (<clustering_columns>)
```
Além disso podemos deixar a própria Plataforma de dados inteligente da databricks definir quais são as melhores colunas da nossa tabela para serem definidas como *clustering*.</br>
<span style="color:green"> **VAMOS EXECUTAR ESSE EXEMPLO** </span>
```sql
-- captura informacoes antes de ativar o recurso
DESC EXTENDED tipo_plano;

ALTER TABLE tipo_plano
CLUSTER BY AUTO;

-- captura informacoes depois de ativar o recurso
DESC EXTENDED tipo_plano;
```
#### Referências:
* [Databricks Liquid Clustering](https://docs.databricks.com/aws/pt/delta/clustering)
* [BLOG - Announcing Automatic Liquid Clustering](https://www.databricks.com/blog/announcing-automatic-liquid-clustering)

## Exercício 01.07 - Visualizando o Histórico de Atualizações da tabela *(opcional / avançado)*

 ``` sql
DESCRIBE HISTORY tipo_plano ;
```

## Exercício 01.08 - Visualizando o conteúdo da tabela na versão anterior (TIME TRAVEL) *(opcional / avançado)*

 ``` sql
SELECT * FROM tipo_plano VERSION AS OF 7;
```

## Exercício 01.09 - RESTAURANDO o conteúdo da tabela na versão anterior (TIME TRAVEL) *(opcional / avançado)*

 ``` sql
RESTORE TABLE tipo_plano TO VERSION AS OF 7;
```

## Exercício 01.10 - Visualizando as propriedades da Tabela

 ``` sql
DESCRIBE DETAIL tipo_plano ;
```

## Exercício 01.11 - Visualizando as informações DETALHADAS da Tabela

 ``` sql
DESCRIBE TABLE EXTENDED tipo_plano;
```

</br></br></br>
## Sessão 02: Explorando os dados de saúde carregados (Lab 02)

Agora que você já domina a criação e manipulação de tabelas, vamos consultar as tabelas de **operadora de saúde** carregadas no Lab 02.

## Exercício 01.12 - Consultando os sinistros

``` sql
-- 10 primeiros sinistros
SELECT * FROM sinistros LIMIT 10;
```

``` sql
-- valor total de sinistros por categoria de procedimento
SELECT p.categoria_procedimento,
       count(*)             AS qt_atendimentos,
       round(sum(s.vl_sinistro), 2) AS total_sinistros
FROM sinistros s
JOIN dim_procedimento p ON s.id_procedimento = p.id_procedimento
GROUP BY p.categoria_procedimento
ORDER BY total_sinistros DESC;
```

``` sql
-- top 10 procedimentos mais caros (valor médio por atendimento)
SELECT p.nome_procedimento,
       round(avg(s.vl_sinistro), 2) AS valor_medio
FROM sinistros s
JOIN dim_procedimento p ON s.id_procedimento = p.id_procedimento
GROUP BY p.nome_procedimento
ORDER BY valor_medio DESC
LIMIT 10;
```
