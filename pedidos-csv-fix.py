import pandas as pd

def find_all(string, sub):
    start = 0
    while True:
        start = string.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub)

filename = "/var/home/rodrigo/Documents/EZ/projects/consumer-db/z316-consumer-pedidos.csv"

with open(filename, 'r', encoding='ISO-8859-1') as f:
    lines = f.readlines()

# Get the first "====" line and remove '\n'
separator_line = [line for line in lines if "====" in line][0].replace('\n', '')

# Filter out empty lines, separator lines, and repeated header lines
lines = [line for line in lines if line.strip() != '' and not line.startswith('====')]

# New code: keep the first header and remove subsequent headers
header_line = lines[0]
lines = [line for i, line in enumerate(lines) if i == 0 or line != header_line]

separator_indices = list(find_all(separator_line, ' '))
separator_indices.append(len(separator_line))

start_indices = [0] + [index + 1 for index in separator_indices[:-1]]
end_indices = separator_indices

split_lines = [[line[start:end].strip() for start, end in zip(start_indices, end_indices)] for line in lines[2:]]
df = pd.DataFrame(split_lines)
df[9] = df[9] + df[10]
df = df.drop(10, axis=1)

df.columns = ["timestamp", "DATA_PEDIDO", "ID", "PEDIDO_NUMBER", "ID_VENDEDOR", "NOME_VENDEDOR", "TOTALPRODUTOS", "TOTALVENDA", "DESCONTO", "FORMAPAGAMENTO"]

df = df.iloc[1:]
df["FORMAPAGAMENTO"] = df["FORMAPAGAMENTO"].str.strip()

df.to_csv('/var/home/rodrigo/Documents/EZ/projects/consumer-db/z316-consumer-pedidos_cleaned5.csv', index=False)
