import uproot
import pandas as pd
import matplotlib.pyplot as plt
import os

# --- 1. Configurações e Carregamento ---
FILE_NAME = 'AmberTarget_Run_0.root'
TREE_NAME = 'tracksData'

PION_PDG = 211

# --- Configuração do Histograma ---
NBINS = 200
PZ_MIN = -10
PZ_MAX = 220  # Ajustar conforme a energia do feixe

print(f"A analisar piões em {FILE_NAME}...")

try:
    with uproot.open(FILE_NAME) as file:
        tree = file[TREE_NAME]
        # Carregamos pZ, PDG e o marcador de primário
        df = tree.arrays(['particlePDG', 'pZ_GeV', 'IsPrimary'], library='pd')
except Exception as e:
    print(f"Erro: {e}")
    exit()

# --- 2. Processamento ---

# Filtrar apenas por Piões (PDG 211)
df_pions = df[df['particlePDG'].abs() == PION_PDG].copy()

# Separar entre Primários e Secundários
primary_pions = df_pions[df_pions['IsPrimary'] == 1]['pZ_GeV']
secondary_pions = df_pions[df_pions['IsPrimary'] == 0]['pZ_GeV']

# --- 3. Visualização ---

plt.figure(figsize=(12, 7))

# Função para contar dentro do range visual
def count_in(data):
    return len(data[(data >= PZ_MIN) & (data <= PZ_MAX)])

# Plotar Piões Primários
plt.hist(primary_pions, 
         bins=NBINS, 
         range=(PZ_MIN, PZ_MAX), 
         histtype='step', linewidth=2.5, color='red', 
         label=f'Piões Primários (N={count_in(primary_pions)})')

# Plotar Piões Secundários
plt.hist(secondary_pions, 
         bins=NBINS, 
         range=(PZ_MIN, PZ_MAX), 
         histtype='step', linewidth=2, color='orange',
         label=f'Piões Secundários (N={count_in(secondary_pions)})')

# Estética
plt.yscale('log')
plt.title('Distribuição $P_z$: Piões Primários vs Secundários', fontsize=15, fontweight='bold')
plt.xlabel('Momentum $P_z$ [GeV/c]', fontsize=12)
plt.ylabel('Entradas (Log)', fontsize=12)

plt.xlim(PZ_MIN, PZ_MAX)
plt.grid(True, which="both", ls="--", alpha=0.3)
plt.legend(fontsize=11)

# Guardar
if not os.path.exists('Imagens'):
    os.makedirs('Imagens')

output_file = 'Imagens/EX9.png'
plt.savefig(output_file, dpi=150)
print(f"Gráfico guardado: {output_file}")
print(f"Piões processados: {len(df_pions)}")
plt.show()