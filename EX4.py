import uproot
import pandas as pd
import matplotlib.pyplot as plt
import os

# --- 1. Configurações e Carregamento ---
FILE_NAME = 'AmberTarget_Run_0.root'
TREE_NAME = 'hadronicVertex'

# --- Configuração do Histograma (Ajusta aqui os limites do teu alvo) ---
NBINS = 200
Z_MIN = -510  # cm
Z_MAX = 510  # cm

print(f"A ler vértices de {FILE_NAME}...")

try:
    with uproot.open(FILE_NAME) as file:
        tree = file[TREE_NAME]
        df = tree.arrays(['vertexPosZ_cm', 'IsPrimary'], library='pd')
except Exception as e:
    print(f"Erro ao abrir a TTree {TREE_NAME}: {e}")
    exit()

# --- 2. Separação entre Primários e Secundários ---
primary_z = df[df['IsPrimary'] == 1]['vertexPosZ_cm']
secondary_z = df[df['IsPrimary'] == 0]['vertexPosZ_cm']

# --- 3. Visualização ---

plt.figure(figsize=(12, 7))

# Função auxiliar para contar eventos no range (para a legenda)
def count_in_range(data, zmin, zmax):
    return len(data[(data >= zmin) & (data <= zmax)])

# --- Plotar Primários ---
plt.hist(primary_z, 
         bins=NBINS, 
         range=(Z_MIN, Z_MAX), 
         histtype='stepfilled', color='blue', alpha=0.4, 
         label=f'Primários (N={count_in_range(primary_z, Z_MIN, Z_MAX)})')

plt.hist(primary_z, 
         bins=NBINS, 
         range=(Z_MIN, Z_MAX), 
         histtype='step', color='blue', linewidth=1.5)

# --- Plotar Secundários ---
plt.hist(secondary_z, 
         bins=NBINS, 
         range=(Z_MIN, Z_MAX), 
         histtype='stepfilled', color='orange', alpha=0.3, 
         label=f'Secundários (N={count_in_range(secondary_z, Z_MIN, Z_MAX)})')

plt.hist(secondary_z, 
         bins=NBINS, 
         range=(Z_MIN, Z_MAX), 
         histtype='step', color='darkorange', linewidth=1.5)

# Configurações do Gráfico
plt.title(f'Distribuição Z dos Vértices ({Z_MIN} a {Z_MAX} cm)', fontsize=15, fontweight='bold')
plt.xlabel('Posição Z [cm]', fontsize=12)
plt.ylabel('Número de Vértices', fontsize=12)
plt.yscale('log') 

plt.grid(True, which="both", ls="--", alpha=0.3)
plt.legend(fontsize=11, loc='upper right')

# Forçar o limite visual do eixo X
plt.xlim(Z_MIN, Z_MAX)

# Adicionar uma linha vertical em Z=0 (referência comum)
plt.axvline(0, color='black', linestyle=':', alpha=0.5, label='Z=0')

# Criar pasta se não existir e guardar
if not os.path.exists('Imagens'):
    os.makedirs('Imagens')

output_file = 'Imagens/EX4_limitado.png'
plt.savefig(output_file, dpi=150)
print(f"Gráfico guardado como: {output_file}")
print(f"Total no range: {count_in_range(df['vertexPosZ_cm'], Z_MIN, Z_MAX)} vértices.")
plt.show()