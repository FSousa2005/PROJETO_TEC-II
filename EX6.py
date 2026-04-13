import uproot
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import os

# --- 1. Configurações e Carregamento ---
FILE_NAME = 'AmberTarget_Run_0.root'
TREE_NAME = 'Hits'

# Configuração do Histograma 2D
NBINS = 150
LIMIT_CM = 40  # Janela de -10 a 10 cm

print(f"A gerar mapas 2D de {FILE_NAME}...")

try:
    with uproot.open(FILE_NAME) as file:
        df = file[TREE_NAME].arrays(['detectorID', 'particleCharge', 'hitPosX_cm', 'hitPosY_cm'], library='pd')
except Exception as e:
    print(f"Erro: {e}")
    exit()

# --- 2. Criação da Visualização 2D ---

# Criamos uma grelha: 2 linhas (Carregadas/Neutras) x 4 colunas (Detetores)
fig, axes = plt.subplots(2, 4, figsize=(20, 10))

for det_id in range(4):
    # Filtrar dados do detetor atual
    df_det = df[df['detectorID'] == det_id]
    
    # 1. Partículas CARREGADAS (Linha 0)
    ax_c = axes[0, det_id]
    charged = df_det[df_det['particleCharge'] != 0]
    
    h1 = ax_c.hist2d(charged['hitPosX_cm'], charged['hitPosY_cm'], 
                    bins=NBINS, range=[[-LIMIT_CM, LIMIT_CM], [-LIMIT_CM, LIMIT_CM]],
                    cmap='viridis', norm=colors.LogNorm())
    
    ax_c.set_title(f'Detetor {det_id} [Carregadas]', fontsize=12)
    ax_c.set_aspect('equal') # Garante que o buraco não fique deformado
    fig.colorbar(h1[3], ax=ax_c, fraction=0.046, pad=0.04)

    # 2. Partículas NEUTRAS (Linha 1)
    ax_n = axes[1, det_id]
    neutral = df_det[df_det['particleCharge'] == 0]
    
    h2 = ax_n.hist2d(neutral['hitPosX_cm'], neutral['hitPosY_cm'], 
                    bins=NBINS, range=[[-LIMIT_CM, LIMIT_CM], [-LIMIT_CM, LIMIT_CM]],
                    cmap='magma', norm=colors.LogNorm())
    
    ax_n.set_title(f'Detetor {det_id} [Neutras]', fontsize=12)
    ax_n.set_aspect('equal')
    fig.colorbar(h2[3], ax=ax_n, fraction=0.046, pad=0.04)

# Configurações de labels
for ax in axes.flat:
    ax.set_xlabel('X [cm]')
    ax.set_ylabel('Y [cm]')

plt.suptitle('Distribuição 2D de Hits: Visualização do "Buraco" Central', fontsize=20, y=0.98)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Guardar
if not os.path.exists('Imagens'):
    os.makedirs('Imagens')

output_file = 'Imagens/EX6.png'
plt.savefig(output_file, dpi=150)
print(f"Sucesso! O mapa 2D foi guardado em: {output_file}")
plt.show()