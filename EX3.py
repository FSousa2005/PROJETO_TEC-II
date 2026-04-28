import uproot
import pandas as pd
import matplotlib.pyplot as plt

# --- 1. Configurações e Carregamento ---
FILE_NAME = 'AmberTarget_Run_0.root'
TREE_NAME = 'tracksData'

# --- Configuração do Histograma ---
NBINS = 200
X_MAX_KEV = 20000

print(f"A ler dados de {FILE_NAME}...")

with uproot.open(FILE_NAME) as file:
    tree = file[TREE_NAME]
    df = tree.arrays(['particlePDG', 'EdepDet0_keV', 'EdepDet1_keV', 
                      'EdepDet2_keV', 'EdepDet3_keV'], library='pd')

# --- 2. Processamento dos Dados ---
df['TotalEdep'] = (df['EdepDet0_keV'] + df['EdepDet1_keV'] + 
                   df['EdepDet2_keV'] + df['EdepDet3_keV'])

df_filtered = df[df['TotalEdep'] > 0].copy()
df_filtered['abs_pdg'] = df_filtered['particlePDG'].abs()

muons = df_filtered[df_filtered['abs_pdg'] == 13]['TotalEdep']
pions = df_filtered[df_filtered['abs_pdg'] == 211]['TotalEdep']
others = df_filtered[~df_filtered['abs_pdg'].isin([13, 211])]['TotalEdep']

# --- 3. Visualização ---

plt.figure(figsize=(12, 7))

# --- ALTERAÇÕES APLICADAS AQUI ---
# Para cada histograma, definimos os mesmos `bins` e `range`.

# Histograma dos Muões
plt.hist(muons, 
         bins=NBINS,                      
         range=(0, X_MAX_KEV),            
         histtype='step', linewidth=2, color='blue', 
         label=f'Muões (N={len(muons[muons <= X_MAX_KEV])})') 

# Histograma dos Piões
plt.hist(pions, 
         bins=NBINS,                      
         range=(0, X_MAX_KEV),            
         histtype='step', linewidth=2, color='red', 
         label=f'Piões (N={len(pions[pions <= X_MAX_KEV])})') 

# Histograma das Outras partículas
plt.hist(others, 
         bins=NBINS,                      
         range=(0, X_MAX_KEV),            
         histtype='step', linewidth=2, color='green', 
         label=f'Outras (N={len(others[others <= X_MAX_KEV])})')

# --- FIM DAS ALTERAÇÕES ---

# Estética do Gráfico
plt.yscale('log')
# Título atualizado para refletir o limite
plt.title(f'Deposição de Energia Total (0 a {X_MAX_KEV} keV)', fontsize=15, fontweight='bold')
plt.xlabel('Energia Total Depositada [keV]', fontsize=12)
plt.ylabel('Frequência (Entradas)', fontsize=12)
plt.grid(True, which="both", ls="--", alpha=0.4)
plt.legend(fontsize=11)
plt.xlim(0, X_MAX_KEV) # <-- Boa prática: força o limite visual do eixo

# Guardar e mostrar
output_file = 'Imagens/EX3.png' # <-- Nome do ficheiro alterado
plt.savefig(output_file, dpi=150)
print(f"Sucesso! Foram processadas {len(df_filtered)} partículas com deposição positiva.")
print(f"Gráfico guardado como: {output_file}")
plt.show()