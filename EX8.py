import uproot
import pandas as pd
import matplotlib.pyplot as plt
import os

# --- 1. Configurações e Carregamento ---
FILE_NAME = 'AmberTarget_Run_0.root'
TREE_NAME = 'tracksData'

# IDs das partículas
MUON_PDG = 13
PION_PDG = 211

# --- Configuração do Histograma ---
NBINS = 200
PZ_MIN = 0    # GeV/c
PZ_MAX = 210  # GeV/c (Ajusta conforme a energia do teu feixe)

print(f"A processar {FILE_NAME} (Tree: {TREE_NAME})...")

try:
    with uproot.open(FILE_NAME) as file:
        tree = file[TREE_NAME]
        # Carregamos PDG e o momentum Z (exatamente como no teu dump)
        df = tree.arrays(['particlePDG', 'pZ_GeV'], library='pd')
except Exception as e:
    print(f"Erro ao ler os dados: {e}")
    exit()

# --- 2. Processamento ---

# Valor absoluto do PDG para incluir anti-partículas
df['abs_pdg'] = df['particlePDG'].abs()

# Filtrar grupos
# Criamos máscaras para selecionar apenas os dados dentro do range para a legenda
muons_pz = df[df['abs_pdg'] == MUON_PDG]['pZ_GeV']
pions_pz = df[df['abs_pdg'] == PION_PDG]['pZ_GeV']

# --- 3. Visualização ---

plt.figure(figsize=(12, 7))

# Função para contar quantos eventos estão de facto no gráfico
def count_in(data):
    return len(data[(data >= PZ_MIN) & (data <= PZ_MAX)])

# Plotar Muões
plt.hist(muons_pz, 
         bins=NBINS, 
         range=(PZ_MIN, PZ_MAX), 
         histtype='step', linewidth=2, color='blue', 
         label=f'Muões (N={count_in(muons_pz)})')

# Plotar Piões
plt.hist(pions_pz, 
         bins=NBINS, 
         range=(PZ_MIN, PZ_MAX), 
         histtype='step', linewidth=2, color='red', 
         label=f'Piões (N={count_in(pions_pz)})')

# Estética do Gráfico
plt.yscale('log') # Logarítmico é essencial para ver os piões se o feixe for de muões
plt.title('Distribuição do Momento Longitudinal ($P_z$)', fontsize=15, fontweight='bold')
plt.xlabel('Momentum $P_z$ [GeV/c]', fontsize=12)
plt.ylabel('Frequência (Entradas)', fontsize=12)

plt.xlim(PZ_MIN, PZ_MAX)
plt.grid(True, which="both", ls="--", alpha=0.3)
plt.legend(fontsize=11)

# Guardar o ficheiro
if not os.path.exists('Imagens'):
    os.makedirs('Imagens')

output_file = 'Imagens/EX8.png'
plt.savefig(output_file, dpi=150)
print(f"Sucesso! Gráfico guardado como: {output_file}")
plt.show()