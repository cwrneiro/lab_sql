<img src="https://raw.githubusercontent.com/Databricks-BR/genie_ai_bi/main/images/header_genie.png">

# Hands-On LAB 06 - Criando o Dashboard AI/BI

Treinamento Hands-on na plataforma Databricks com foco nas funcionalidades de Análise Exploratória e Painéis.
</br></br>

## Objetivos do Exercício

O objetivo desse laboratório é montar um Painel, utilizando os dados de ações das Big Tech da NASDAQ.</br> 
***Caso não tenha feito ainda, carregue os dados conforme descrito no Lab 02 - LAB_Notebook.***
</br></br>


## Exercício 06.01 - Criando o Dashboard

No Menu Lateral, escolha a opção DASHBOARDS:

Clique na opção **CREATE DASHBOARD**

Na tela do Dashboard, clique na ABA **"Data"** para adicionar uma fonte de dados:

<img src="https://raw.githubusercontent.com/Databricks-BR/lab_sql/main/images/lab05_ai_01.png" style="height: 300px;"></br>

1 - Escolha a opção *"Create from SQL"*

2 - Copie a consulta abaixo e cole no editor (não se esqueça de incluir seu banco de dados)
``` md
SELECT to_date(`date`, 'MM/dd/yyyy') `nova_data`, * FROM dbacademy.<seu_database>.stock_bigtech
```

3 - Clique em *"Run"*

<img src="https://github.com/CaduBettanim/lab_sql/blob/main/images/v3_lab05_5.png?raw=true" style="height: 300px;">


Vá para a aba de dashboard *"Untitled page"*.  </br>

No canto superior direito, selecione o ícone da Genie Code.

Na caixa de diálogo insira a seguinte informação:
``` md
gráfico de linhas do valor de fechamento por dia e por empresa
```

<img src="https://github.com/CaduBettanim/lab_sql/blob/4a4a65496b601a7a959d55569e8b26e8fa415f01/images/v2_lab05_ai_05.png" style="height: 500px;">

</br></br>
Um gráfico foi gerado como no exemplo abaixo:
<img src="https://github.com/CaduBettanim/lab_sql/blob/main/images/v3_lab05_1.png?raw=true" width="800px">
</br></br></br>

## Exercício 02.03 - Adicionando um FILTRO de página

Clique no menu azul suspenso no ícone de FILTRO.</br>
Escolha o atributo (Field):  "**company**"
</br></br>
<img src="https://raw.githubusercontent.com/Databricks-BR/genie_ai_bi/main/images/lab2_06.png" width="850px">
</br></br></br>


## Exercício 02.04 - Alterando o título do painel por uma imagem

Crie agora um novo objeto do tipo TEXT. No box que foi criado </br>
insira o código (markdown) abaixo: </br>
</br>

``` sql
![image](https://raw.githubusercontent.com/Databricks-BR/genie_ai_bi/main/images/header_painel.png)
```

</br></br>
<img src="https://raw.githubusercontent.com/Databricks-BR/genie_ai_bi/main/images/lab2_07.png" width="700px">
</br></br></br>


Organize o layout do dashboard para que fique com a aparência da imagem abaixo.</br>
Faça o devido alinhamento do gráfico no layout.</br>
Altere o nome do Dashboard na barra superior.</br>
Clique no botão "**Publish**" para publicar o Painel.
</br></br>
<img src="https://raw.githubusercontent.com/Databricks-BR/genie_ai_bi/main/images/lab2_08.png" width="700px">
</br></br></br>


## Exercício 02.05 - Criando um NOVO contexto de dados com Genie Code

Vamos criar agora um novo contexto de dados.</br>
Para isso, selecione novamente o ícone da Genie Code, </br>
No campo de diálogo, copie o texto abaixo (ajuste para o seu banco de dados), cole e execute a instrução</br>
Clique em *"Allow (Permitir)"* caso seja necessário</br>

``` 
Considerando o seguinte database:
dbacademy.<seu_database>.stock_bigtech

Crie um novo dataset:
Selecione o nome da empresa, stock,
mínimo valor de fechamento, máximo valor de fechamento
e percentual de variação entre o mínimo e o máximo valor de fechamento
da tabela dbacademy.<seu_nome>.stock_bigtech
agrupando por empresa e stock.
Use a coluna company para achar o nome da empresa
```
Aguarde a execução terminar 
</br>
</br>
<img src="https://github.com/CaduBettanim/lab_sql/blob/96d89fd92d7e2626f4c364ac0126ef175424b724/images/v2_lab2_09.png" width="700px">
</br></br></br>

Vá até *"Data (Dados)"*
Selecione o novo dataset criado e acrescente ao resultado a linha de concatenação com o nome da ação (STOCK), </br>
com o LINK (URL) de uma imagem. </br>

``` sql

SELECT 
  "https://raw.githubusercontent.com/Databricks-BR/genie_ai_bi/main/images/" || stock || ".png" AS image,
  company,
  stock,
  MIN(close) AS min_close,
  MAX(close) AS max_close,
  ((MAX(close) - MIN(close)) / MIN(close) * 100) AS percentual_variacao
FROM dbacademy.<seu_database>.stock_bigtech
GROUP BY company, stock;

```
</br>
Ao executar a query (botão RUN),</br>
o resultado esperado é o mostrado abaixo:</br>
<img src="https://raw.githubusercontent.com/Databricks-BR/genie_ai_bi/main/images/lab2_10.png" width="700px">
</br></br></br>

## Exercício 02.07 - Adicionando um novo Gráfico com o contexto novo de dados

1. Clique no menu azul suspenso na posição inferior do painel, </br>
no botão com o ícone de gráfico </br>
2. Na barra de configuração (lateral direita do painel),</br>
escolha o nome do nome Dataset (que veio da Query SQL).</br> 
3. Configure o tipo de Visualização para "Tabela"(Table).</br>
4. Marque a opção para incluir TODOS os campos na tabela.
5. Na configuração, clique no campo(coluna) com o nome de "**image**".</br>
</br></br>
<img src="https://github.com/Gabriel-Rangel/lab_sql/blob/main/images/v2_lab05_2.png?raw=true" width="700px">
</br></br></br>

6. Na opção de "Display", configure como "image".
7. Na opção de "SIZE", coloque o valor de "25" no campo "width".
8. Na opção de "Default column width", coloque o valor de "150".
</br></br>
<img src="https://github.com/Gabriel-Rangel/lab_sql/blob/main/images/v2_lab05_3.png?raw=true" width="700px">
</br></br></br>

Como resultado esperado, teremos a figura abaixo.</br>
Salve (Publique) novamente o Painel.
</br></br>
<img src="https://github.com/Gabriel-Rangel/lab_sql/blob/main/images/v2_lab05_4.png?raw=true" width="700px">
</br></br></br>






