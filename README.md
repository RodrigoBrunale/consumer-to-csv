
# 🔥 Firebird Database to CSV

This repository contains scripts to extract data from a Firebird database and format it into a standard CSV format. **These scripts are hardcoded for specific data and may not work as expected with different data. This repository is public for the purpose of demonstrating a specific solution, and the scripts may require modifications to work with other data.**

## 🛠️ Prerequisites

The scripts require Firebird and its associated libraries. You can install them on Fedora with the following command:

```bash
sudo dnf install firebird firebird-devel firebird-doc libicu
```

## 📋 Usage

1. Start the Firebird SQL environment with the following command:

```bash
isql-fb -user sysdba -password masterkey
```

2. Connect to the database:

```bash
CONNECT '/path_to_your_db/your_db.fdb';
```

3. Run the SQL queries to extract data from the `PEDIDOS` and `ITENSPEDIDO` tables:

```sql
-- Extract data from the PEDIDOS table
SELECT
    P.DATAABERTURA as "timestamp",
    CAST(P.DATAABERTURA AS DATE) as data_pedido,
    COALESCE(P.CODIGO, 0) as id,
    COALESCE(P.CODIGO, 0) as pedido_number,
    COALESCE(P.CODIGOCOLABORADOR, 0) as id_vendedor,
    COALESCE(U.LOGIN, 'Unknown') as nome_vendedor,
    COALESCE(P.VALORTOTALITENS, 0) as totalProdutos,
    (COALESCE(P.VALORTOTALITENS, 0) - COALESCE(P.TOTALDESCONTO, 0)) as totalVenda,
    COALESCE(P.TOTALDESCONTO, 0) as desconto,
    COALESCE(F.DESCRICAO, 'Unknown') as formaPagamento
FROM
    PEDIDOS P
LEFT JOIN
    USUARIOS U ON P.CODIGOCOLABORADOR = U.CODIGOCONTATO
LEFT JOIN
    (
        SELECT PG.CODIGOPEDIDO, MIN(PG.CODIGOFORMAPAGAMENTO) as CODIGOFORMAPAGAMENTO
        FROM PAGAMENTOS PG
        GROUP BY PG.CODIGOPEDIDO
    ) PGmin ON P.CODIGO = PGmin.CODIGOPEDIDO
LEFT JOIN
    FORMASPAGAMENTO F ON PGmin.CODIGOFORMAPAGAMENTO = F.CODIGO;
```

```sql
-- Extract data from the ITENSPEDIDO table
SELECT
    P.DATAABERTURA as "timestamp",
    CAST(P.DATAABERTURA AS DATE) as data_pedido,
    COALESCE(P.CODIGO, 0) as id,
    COALESCE(P.CODIGO, 0) as pedido_number,
    COALESCE(P.CODIGOCOLABORADOR, 0) as id_vendedor,
    COALESCE(U.LOGIN, 'Unknown') as nome_vendedor,
    COALESCE(I.CODIGOPRODUTO, 0) as idProduto,
    COALESCE(I.NOMEPRODUTO, 'Unknown') as descricao,
    COALESCE(I.QUANTIDADE, 0) as quantidade,
    COALESCE(I.VALORUNITARIO, 0) as valor,
    COALESCE(I.PRECOCUSTO, 0) as preco_custo
FROM
    PEDIDOS P
LEFT JOIN
    USUARIOS U ON P.CODIGOCOLABORADOR = U.CODIGOCONTATO
LEFT JOIN
    ITENSPEDIDO I ON P.CODIGO = I.CODIGOPEDIDO;
```

4. Run the `itenspedido.py` and `pedidos.py` scripts to format the data into CSV format.

5. Upload the CSV files to BigQuery or any other data analysis platform.

Please replace `'/path_to_your_db/your_db.fdb'` with the actual path to your Firebird database file. Note that the readme assumes that the user is running a Unix-like operating system and is familiar with basic terminal commands.
