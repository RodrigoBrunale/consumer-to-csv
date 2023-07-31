# 🔥 Firebird Database to CSV

This repository contains scripts to extract data from a Firebird database and format it into a standard CSV format. **These scripts are hardcoded for specific data and may not work as expected with different data. This repository is public for the purpose of demonstrating a specific solution, and the scripts may require modifications to work with other data.**

## 🛠️ Prerequisites

The scripts require Firebird and its associated libraries. You can install them on Fedora with the following command:

```bash
sudo dnf install firebird firebird-devel firebird-doc libicu
```

## 📋 Usage

### Step 1: Restoring the backup

You're ready to restore the backup using the gbak utility:

```bash
gbak -c -v -user SYSDBA -password masterkey /path/to/yourfile.fbconsumer /path/to/yourNewDB.fdb
```
In this command:

- `-c` tells gbak to create a new database.
- `-v` enables verbose output.
- `/path/to/yourfile.fbconsumer` is the path to your backup file.
- `/path/to/yourNewDB.fdb` is the path and filename for the new database you want to create.

### Step 2: Connecting to the database

Connect to the database:

```bash
isql-fb /path/to/yourNewDB.fdb
```

### Step 3: Extracting data

Run the SQL queries to extract data from the `PEDIDOS` and `ITENSPEDIDO` tables:

-- Extract data from the PEDIDOS table
```
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

-- Extract data from the ITENSPEDIDO table
```
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

### Step 4: Formatting the data

Run the `itenspedido.py` and `pedidos.py` scripts to format the data into CSV format.

### Step 5: Uploading to BigQuery

Upload the CSV files to BigQuery or any other data analysis platform.

Please replace `'/path/to/your_db/your_db.fdb'` with the actual path to your Firebird database file. Note that the readme assumes that the user is running a Unix-like operating system and is familiar with basic terminal commands.

## 🚧 Troubleshooting

If you receive an error saying "file is not a valid database", it could be that the file is not a Firebird database or it's a backup that hasn't been restored. Make sure to follow the steps in this guide to restore the backup before trying to connect to the database.

If you encounter problems with ICU library ("Could not find acceptable ICU library"), ensure that the ICU library is installed and properly configured. Try reinstalling it if necessary. If the problem persists, consult the Firebird documentation or seek help from the Firebird community.

## 🎉 Conclusion

This guide showed you how to restore a backup from the Consumer ERP system to a usable Firebird database and how to extract and format data from it. Remember to always keep your systems updated and back up your data regularly to prevent data loss. If you have any questions or issues, feel free to raise an issue in this repository.

Good luck with your data recovery and analysis efforts!
