import uproot
import pandas as pd
import matplotlib.pyplot as plt
import os

# --- 1. Configurações e Carregamento ---
FILE_NAME = 'AmberTarget_Run_0.root'
TREE_NAME = 'Hits'

# Configuração do Histograma
NBINS = 200
T_MIN = 0    # ns
T_MAX = 50   # ns

print(f"A processar dados temporais de {FILE_NAME}...")

try:
    with uproot.open(FILE_NAME) as file:
        df = file[TREE_NAME].arrays(['detectorID', 'particleHitTime_ns'], library='pd')
except Exception as e:
    print(f"Erro: {e}")
    exit()

# --- 2. Visualização Sobreposta ---

plt.figure(figsize=(12, 7))

# Cores para distinguir os detetores
colors = ['blue', 'red', 'green', 'orange']

for det_id in range(4):
    # Filtrar dados por detetor
    time_data = df[df['detectorID'] == det_id]['particleHitTime_ns']
    
    # Contagem para a legenda (apenas os que estão no range)
    n_in_range = len(time_data[(time_data >= T_MIN) & (time_data <= T_MAX)])
    
    # Plotar histograma sobreposto (usando histtype='step' para melhor visibilidade)
    plt.hist(time_data, 
            bins=NBINS, 
            range=(T_MIN, T_MAX), 
            histtype='step', 
            linewidth=2, 
            color=colors[det_id], 
            label=f'Detetor {det_id} (N={n_in_range})')

# Estética do Gráfico
plt.yscale('log')
plt.title('Distribuição Temporal de Hits: Comparação entre Detetores', fontsize=15, fontweight='bold')
plt.xlabel('Tempo do Hit [ns]', fontsize=12)
plt.ylabel('Frequência (Entradas)', fontsize=12)

plt.xlim(T_MIN, T_MAX)
plt.grid(True, which="both", ls="--", alpha=0.3)
plt.legend(fontsize=11, loc='upper right')

# Guardar o resultado
if not os.path.exists('Imagens'):
    os.makedirs('Imagens')

output_file = 'Imagens/distribuicao_temporal_sobreposta.png'
plt.savefig(output_file, dpi=150)
print(f"Gráfico sobreposto guardado em: {output_file}")
plt.show()