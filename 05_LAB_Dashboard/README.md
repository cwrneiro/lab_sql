<img src="https://raw.githubusercontent.com/Databricks-BR/genie_ai_bi/main/images/header_genie.png">

# Hands-On LAB 05 - Criando o Dashboard AI/BI

Treinamento Hands-on na plataforma Databricks com foco nas funcionalidades de Análise Exploratória e Painéis.
</br></br>

## Objetivos do Exercício

O objetivo desse laboratório é montar um Painel utilizando os dados de **sinistros da operadora de saúde**.</br> 
***Caso não tenha feito ainda, carregue os dados conforme descrito no Lab 02 - LAB_Notebook.***
</br></br>


## Exercício 05.01 - Criando o Dashboard

No Menu Lateral, escolha a opção **Dashboards** (ou **+ New → Dashboard**).

Na tela do Dashboard, clique na ABA **"Data"** para adicionar uma fonte de dados:

<img src="https://raw.githubusercontent.com/Databricks-BR/lab_sql/main/images/lab05_ai_01.png" style="height: 300px;"></br>

1 - Clique em **"Add SQL dataset"** (na interface atual; em versões anteriores aparecia como *"Create from SQL"*).

2 - Copie a consulta abaixo e cole no editor (não se esqueça de incluir seu banco de dados)
``` md
SELECT s.*,
       to_date(s.dt_atendimento) AS data_atendimento,
       p.categoria_procedimento,
       p.nome_procedimento
FROM dbacademy.<seu_database>.sinistros s
JOIN dbacademy.<seu_database>.dim_procedimento p
  ON s.id_procedimento = p.id_procedimento
```

3 - Clique em *"Run"*

<img src="https://github.com/CaduBettanim/lab_sql/blob/main/images/v3_lab05_5.png?raw=true" style="height: 300px;">


Vá para a aba de dashboard *"Untitled page"*.  </br>

No canto superior direito, selecione o ícone da Genie Code.

Na caixa de diálogo insira a seguinte informação:
``` md
gráfico de linhas do valor total de sinistros por mês e por categoria de procedimento
```

<img src="https://github.com/CaduBettanim/lab_sql/blob/4a4a65496b601a7a959d55569e8b26e8fa415f01/images/v2_lab05_ai_05.png" style="height: 500px;">

</br></br>
Um gráfico foi gerado como no exemplo abaixo:
<img src="https://github.com/CaduBettanim/lab_sql/blob/main/images/v3_lab05_1.png?raw=true" width="800px">
</br></br></br>

## Exercício 05.02 - Adicionando um FILTRO de página

Clique no menu azul suspenso no ícone de FILTRO.</br>
Escolha o atributo (Field):  "**categoria_procedimento**"
</br></br>
<img src="https://raw.githubusercontent.com/Databricks-BR/genie_ai_bi/main/images/lab2_06.png" width="850px">
</br></br></br>


## Exercício 05.03 - Alterando o título do painel por uma imagem

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
Altere o nome do Dashboard na barra superior (ex.: **"Painel de Sinistros"**).</br>
Clique no botão "**Publish**" para publicar o Painel.
</br></br>
<img src="https://raw.githubusercontent.com/Databricks-BR/genie_ai_bi/main/images/lab2_08.png" width="700px">
</br></br></br>


## Exercício 05.04 - Criando um NOVO contexto de dados com Genie Code

Vamos criar agora um novo contexto de dados.</br>
Para isso, selecione novamente o ícone da Genie Code, </br>
No campo de diálogo, copie o texto abaixo, cole (ajuste para o seu banco de dados) e execute a instrução</br>
Clique em *"Allow (Permitir)"* caso seja necessário</br>

``` 
Considerando as seguintes tabelas:
dbacademy.<seu_database>.sinistros
dbacademy.<seu_database>.dim_prestador

Crie um novo dataset:
Selecione o nome do prestador (coluna xpto de dim_prestador), o tipo do prestador,
a quantidade de atendimentos, o valor total de sinistros
e o valor médio por atendimento,
agrupando por prestador e tipo.
Use a coluna cod de dim_prestador para cruzar com id_prestador de sinistros.
```
Aguarde a execução terminar 
</br>
</br>
<img src="https://github.com/CaduBettanim/lab_sql/blob/96d89fd92d7e2626f4c364ac0126ef175424b724/images/v2_lab2_09.png" width="700px">
</br></br></br>

Vá até *"Data (Dados)"*.
Selecione o novo dataset criado e confira/edite a query gerada. Ela deve ser equivalente a: </br>

``` sql
SELECT 
  pr.xpto        AS prestador,
  pr.tipo,
  COUNT(*)                  AS qt_atendimentos,
  SUM(s.vl_sinistro)        AS total_sinistros,
  AVG(s.vl_sinistro)        AS valor_medio_atendimento
FROM dbacademy.<seu_database>.sinistros s
JOIN dbacademy.<seu_database>.dim_prestador pr
  ON s.id_prestador = pr.cod
GROUP BY pr.xpto, pr.tipo
ORDER BY total_sinistros DESC;
```
</br>
Ao executar a query (botão RUN),</br>
o resultado esperado é uma tabela com os prestadores e seus totais de sinistro.</br>
<img src="https://raw.githubusercontent.com/Databricks-BR/genie_ai_bi/main/images/lab2_10.png" width="700px">
</br></br></br>

## Exercício 05.05 - Adicionando um novo Gráfico com o contexto novo de dados

1. Clique no menu azul suspenso na posição inferior do painel, </br>
no botão com o ícone de gráfico </br>
2. Na barra de configuração (lateral direita do painel),</br>
escolha o nome do Dataset (que veio do Genie Code).</br> 
3. Configure o tipo de Visualização para "Table"(Tabela).</br>
4. Na opção Columns (Colunas) clique no sinal "+".
5. Selecione a opção "Add all (Adicionar todos)"

</br></br>
<img src="https://github.com/CaduBettanim/lab_sql/blob/main/images/v4_lab05_2.png?raw=true" width="900px">
</br></br></br>

6. Passe o mouse na coluna **total_sinistros** e selecione a seta para baixo.</br>
7. Clique em "Style (Estilo)".
8. Formate como moeda (R$) e ordene a tabela por essa coluna, de forma decrescente.
</br></br>
<img src="https://github.com/CaduBettanim/lab_sql/blob/main/images/v4_lab05_3.png?raw=true" width="400px">
</br></br></br>

Como resultado esperado, teremos um painel com a evolução dos sinistros por categoria e um ranking de prestadores por valor.</br>
Salve (Publique) novamente o Painel.
</br></br>
<img src="https://github.com/Gabriel-Rangel/lab_sql/blob/main/images/v2_lab05_4.png?raw=true" width="700px">
</br></br></br>
