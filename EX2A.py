import uproot
import pandas as pd
import matplotlib.pyplot as plt

# --- Configuração ---
FILE_NAME = 'AmberTarget_Run_0.root'
TREE_NAME = 'tracksData'

# IDs das partículas
MUON_PDG = 13
PION_PDG = 211

# --- Configuração do Histograma ---  # <-- NOVO
NBINS = 200
X_MAX_KEV = 10000

# --- 1. Carregar os Dados ---
print(f"A processar o ficheiro {FILE_NAME}...")

try:
    with uproot.open(FILE_NAME) as file:
        tree = file[TREE_NAME]
        df = tree.arrays(['particlePDG', 'EdepDet0_keV', 'EdepDet1_keV', 
                         'EdepDet2_keV', 'EdepDet3_keV'], library='pd')
except Exception as e:
    print(f"Erro ao ler o ficheiro: {e}")
    exit()

df['abs_pdg'] = df['particlePDG'].abs()

# --- 2. Definição dos Grupos de Partículas ---
groups = [
    {'label': 'Muões', 'mask': (df['abs_pdg'] == MUON_PDG), 'color': 'blue'},
    {'label': 'Piões', 'mask': (df['abs_pdg'] == PION_PDG), 'color': 'red'},
    {'label': 'Outras', 'mask': ~(df['abs_pdg'] == MUON_PDG) & ~(df['abs_pdg'] == PION_PDG), 'color': 'green'}
]

# --- 3. Criação dos Histogramas Sobrepostos ---
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
axes = axes.flatten()

for i in range(4):
    ax = axes[i]
    col_name = f'EdepDet{i}_keV'
    
    has_data = False
    
    for group in groups:
        data_particle = df[group['mask']]
        clean_energy = data_particle[col_name][data_particle[col_name] > 0]
        
        if not clean_energy.empty:
            has_data = True
            # AQUI ESTÁ A MUDANÇA PRINCIPAL
            ax.hist(clean_energy, 
                    bins=NBINS,                  # <-- ALTERADO para usar a constante
                    range=(0, X_MAX_KEV),        # <-- A LINHA CHAVE!
                    histtype='step', 
                    linewidth=2, 
                    label=f"{group['label']} (N={len(clean_energy[clean_energy <= X_MAX_KEV])})", # Conta apenas eventos no range
                    color=group['color'],
                    alpha=0.9)

    # Configuração estética do subplot
    ax.set_title(f'Detetor {i}', fontsize=15, fontweight='bold')
    ax.set_xlabel('Deposição de Energia (keV)', fontsize=12)
    ax.set_ylabel('Frequência (Log)', fontsize=12)
    ax.set_yscale('log')
    ax.grid(True, which="both", ls="-", alpha=0.2)
    
    # Opcional, mas garante que o limite visual é exatamente o que definimos
    ax.set_xlim(0, X_MAX_KEV) # <-- BOA PRÁTICA

    if has_data:
        ax.legend(loc='upper right', frameon=True)
    else:
        ax.text(0.5, 0.5, 'Sem depósitos registrados (>0)', 
                ha='center', va='center', transform=ax.transAxes)

# Ajustes finais
plt.suptitle(f'Deposição de Energia por Detetor (0 a {X_MAX_KEV} keV, Apenas Valores > 0)', fontsize=20, y=0.98) # Título atualizado
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Guardar o resultado
output_file = 'Imagens/EX2A.png' # <-- Nome do ficheiro alterado
plt.savefig(output_file, dpi=150)
print(f"Sucesso! O gráfico foi guardado como '{output_file}'.")
plt.show()