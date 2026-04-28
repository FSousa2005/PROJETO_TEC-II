import uproot
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import os

# --- 1. Configurações e Carregamento ---
FILE_NAME = 'AmberTarget_Run_0.root'
TREE_NAME = 'Hits'

# Configuração do Histograma 2D
NBINS = 150        # Mais bins para melhor definição do buraco
LIMIT_CM = 10      # Janela de -12 a 12 cm para ver as bordas

print(f"A carregar hits de {FILE_NAME} para mapeamento 2D...")

try:
    with uproot.open(FILE_NAME) as file:
        tree = file[TREE_NAME]
        # Carregamos apenas o necessário: ID do detetor e as posições
        df = tree.arrays(['detectorID', 'hitPosX_cm', 'hitPosY_cm'], library='pd')
except Exception as e:
    print(f"Erro ao ler ficheiro: {e}")
    exit()

# --- 2. Criação da Visualização 2D (Grelha 2x2) ---

fig, axes = plt.subplots(2, 2, figsize=(15, 13))
axes = axes.flatten()

for det_id in range(4):
    ax = axes[det_id]
    
    # Filtrar dados do detetor específico
    df_det = df[df['detectorID'] == det_id]
    
    # Criar o histograma 2D
    # range=[[xmin, xmax], [ymin, ymax]]
    h = ax.hist2d(df_det['hitPosX_cm'], df_det['hitPosY_cm'], 
                  bins=NBINS, 
                  range=[[-LIMIT_CM, LIMIT_CM], [-LIMIT_CM, LIMIT_CM]],
                  cmap='viridis', 
                  norm=colors.LogNorm()) # Escala log para realçar detalhes
    
    # Adicionar barra de cores para cada detetor
    fig.colorbar(h[3], ax=ax, label='Número de Hits', fraction=0.046, pad=0.04)
    
    # Configurações estéticas
    ax.set_title(f'Detetor {det_id}', fontsize=15, fontweight='bold')
    ax.set_xlabel('Posição X [cm]', fontsize=10)
    ax.set_ylabel('Posição Y [cm]', fontsize=10)
    
    # FUNDAMENTAL: Manter a proporção 1:1 para o buraco não parecer uma oval
    ax.set_aspect('equal')
    
    # Adicionar grelha subtil
    ax.grid(True, linestyle=':', alpha=0.3, color='white')

# Ajuste final do layout
plt.suptitle('Distribuição Espacial de Hits (Vista Frontal dos Detetores)', fontsize=20, y=0.98)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# --- 3. Guardar o Resultado ---
if not os.path.exists('Imagens'):
    os.makedirs('Imagens')

output_file = 'Imagens/EX5.png'
plt.savefig(output_file, dpi=200) # DPI mais alto para melhor definição
print(f"Sucesso! O mapa 2D foi guardado em: {output_file}")

plt.show()