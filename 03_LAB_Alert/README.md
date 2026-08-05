<img src="https://raw.githubusercontent.com/Databricks-BR/lab_sql/main/images/header_handson_sql.png">

# Hands-On LAB 03 - Criação de um ALERTA

Treinamento Hands-on na plataforma Databricks com foco nas funcionalidades de Analytics (SQL, Query, DataViz, SQL Warehouse).

***Caso os dados ainda não tenham sido carregados, execute antes o Lab 02 - LAB_Notebook.***

## Objetivos do Exercício

O objetivo deste laboratório é explorar a funcionalidade de **Alertas** do Databricks SQL.

Um **Alerta** executa uma consulta SQL periodicamente e, quando o resultado atinge uma
condição que você definiu (por exemplo, um valor acima de um limite), dispara uma
notificação. No dia a dia de uma operadora de saúde, isso é útil para **monitorar**
situações como um gasto elevado de sinistros, um volume atípico de autorizações ou
qualquer indicador que mereça atenção sem depender de alguém olhando o painel o tempo todo.
</br></br>

## Exercício 03.01 - Criando o Alerta

Vamos utilizar a opção do menu **"ALERTS"**.

<img src="https://github.com/Gabriel-Rangel/lab_sql/blob/main/images/v2_lab04_1.png?raw=true" style="height: 200px;">

</br></br>

Clique no botão **CREATE ALERT**.

O SQL Editor agora é integrado ao Alerta. Copie a query abaixo e clique em **RUN**.

A consulta calcula o **total de sinistros dos últimos 30 dias**, que será o valor
monitorado pelo alerta:

``` sql

SELECT SUM(vl_sinistro) AS total_sinistros_30d
FROM dbacademy.<seu_database>.sinistros
WHERE dt_atendimento >= current_date() - INTERVAL 30 DAYS;

```

<img src="https://github.com/Gabriel-Rangel/lab_sql/blob/main/images/v2_lab04_2.png?raw=true">
</br></br>

Com a query rodando com sucesso, a parte de configuração à esquerda será habilitada.
Configure conforme a imagem abaixo:

* Defina a condição de disparo: acione o alerta quando **`total_sinistros_30d`** for
  **maior que** um limite de sua escolha (por exemplo, `100000`). Ajuste o valor conforme
  o resultado que a query retornou para que dê para ver o alerta mudar de estado.

* Não esqueça de nomear seu alerta. Sugestão: **"Alerta_Sinistros_"** + `<SEU_LOGIN>`, e
  clique em **CREATE**.

* No campo **Notify**, coloque o e-mail usado no seu login da Databricks Free Edition.

<img src="https://github.com/Gabriel-Rangel/lab_sql/blob/main/images/v2_lab04_3.png?raw=true" style="height: 700px;">

</br></br>

> ℹ️ **Dica:** o alerta só notifica quando **muda de estado** (por exemplo, de "OK" para
> "acionado"). Para testar, defina um limite abaixo do valor atual da query e observe o
> alerta ser acionado na próxima verificação.
