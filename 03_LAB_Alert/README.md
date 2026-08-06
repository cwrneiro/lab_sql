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

No menu lateral, clique em **"Alerts"**.

> ℹ️ **Interface atual:** a tela de Alertas tem duas abas — **"Alerts"** (a experiência
> nova, que usaremos) e **"Legacy alerts"** (a antiga). Fique na aba **"Alerts"** e clique
> em **"Create alert"**. Você cai em um editor com três passos: **1) escrever e rodar a
> query → 2) configurar a condição → 3) agendar o alerta**.

</br></br>

**1) Escreva e rode a query.** Copie a consulta abaixo no editor e clique em **Run all**.
Ela calcula o **total de sinistros dos últimos 30 dias**, que será o valor monitorado:

``` sql
SELECT SUM(vl_sinistro) AS total_sinistros_30d
FROM dbacademy.<seu_database>.sinistros
WHERE dt_atendimento >= current_date() - INTERVAL 30 DAYS;
```

> Se aparecer um aviso para iniciar o compute, confirme **"Start, attach and run"** — o
> **Serverless Starter Warehouse** liga sozinho (pode levar alguns segundos no primeiro uso).

</br></br>

**2) Configure a condição** (painel **Condition**, à direita):

* Em **Trigger alert when**, escolha **First row** / coluna **`total_sinistros_30d`**.
* Escolha o operador **`>`** (maior que) e, em **Static Value**, informe um limite de sua
  escolha (por exemplo, `50000000`). Ajuste o valor conforme o resultado que a query
  retornou, para conseguir ver o alerta mudar de estado.
* (Opcional) Em **Notifications → Notify**, adicione o e-mail usado no seu login da
  Databricks Free Edition.

**3) (Opcional) Agende o alerta** para que ele seja avaliado periodicamente, e dê um nome
ao alerta (sugestão: **"Alerta_Sinistros_"** + `<SEU_LOGIN>`). Clique em **Create** / salve.

</br></br>

> ℹ️ **Dica:** o alerta só notifica quando **muda de estado** (por exemplo, de "OK" para
> "acionado"). Para testar, defina um limite abaixo do valor atual da query e observe o
> alerta ser acionado.
