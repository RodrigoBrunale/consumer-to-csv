import pandas as pd

def find_all(string, sub):
    start = 0
    while True:
        start = string.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)

filename = "/var/home/rodrigo/Documents/EZ/projects/consumer-to-bigquery/z316-consumer-itenspedido.csv"

with open(filename, 'r', encoding='ISO-8859-1') as f:
    lines = f.readlines()

# Get the first "====" line and remove '\n'
separator_line = [line for line in lines if "====" in line][0].replace('\n', '')

# Filter out empty lines and separator lines
lines = [line for line in lines if line.strip() != '' and not line.startswith('====')]

separator_indices = list(find_all(separator_line, ' '))
separator_indices.append(len(separator_line))

start_indices = [0] + [index + 1 for index in separator_indices[:-1]]
end_indices = separator_indices

split_lines = [[line[start:end].strip() for start, end in zip(start_indices, end_indices)] for line in lines[2:]]
df = pd.DataFrame(split_lines)
df[10] = df[10] + df[11]
df = df.drop(11, axis=1)

df.columns = ["timestamp", "DATA_PEDIDO", "ID", "PEDIDO_NUMBER", "ID_VENDEDOR", "NOME_VENDEDOR", "IDPRODUTO", "DESCRICAO", "QUANTIDADE", "VALOR", "PRECO_CUSTO"]

df = df.iloc[1:]

# Remove any rows that match the header row
df = df[~(df == df.columns.tolist()).all(axis=1)]

df.to_csv('/var/home/rodrigo/Documents/EZ/projects/consumer-to-bigquery/z316-consumer-itenspedido_cleaned2.csv', index=False)
