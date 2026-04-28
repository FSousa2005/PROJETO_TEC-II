import uproot
import numpy as np
import matplotlib.pyplot as plt
import taichi as ti
import os
import time  # <-- Módulo para medir o tempo

# O GPU DEMORA MAIS PORQUE TEM QUE COPIAR OS DADOS PARA A GRÁFICA, MAS O PROCESSAMENTO É MUITO MAIS RÁPIDO. O CPU É MAIS LENTO NO CÁLCULO, MAS NÃO TEM O OVERHEAD DE TRANSFERÊNCIA. O RESULTADO FINAL DEPENDE DO TAMANHO DOS DADOS E DA POTÊNCIA DA GPU.
#

# Iniciar o cronómetro total
t_total_start = time.perf_counter()

# --- 1. Inicializar Taichi na GPU ---
ti.init(arch=ti.gpu)

# --- 2. Configurações ---
FILE_NAMES = [f'AmberTarget_Run_{i}.root' for i in range(4)]
TREE_NAME = 'tracksData'

NBINS = 200
X_MAX_KEV = 20000

# --- 3. Definir o Kernel do Taichi ---
@ti.kernel
def process_particles(
    pdg: ti.types.ndarray(),
    d0: ti.types.ndarray(),
    d1: ti.types.ndarray(),
    d2: ti.types.ndarray(),
    d3: ti.types.ndarray(),
    out_total_edep: ti.types.ndarray(),
    out_abs_pdg: ti.types.ndarray()
):
    for i in pdg:
        out_total_edep[i] = d0[i] + d1[i] + d2[i] + d3[i]
        out_abs_pdg[i] = ti.abs(pdg[i])

# --- 4. Leitura dos Dados (CPU) ---
print("A ler ficheiros do disco para a RAM...")
t_io_start = time.perf_counter() # Cronómetro de Leitura

pdg_list, d0_list, d1_list, d2_list, d3_list = [], [], [], [], []

for file_name in FILE_NAMES:
    try:
        with uproot.open(file_name) as file:
            tree = file[TREE_NAME]
            arrays = tree.arrays(['particlePDG', 'EdepDet0_keV', 'EdepDet1_keV', 
                                  'EdepDet2_keV', 'EdepDet3_keV'], library='np')
            
            pdg_list.append(arrays['particlePDG'].astype(np.int32))
            d0_list.append(arrays['EdepDet0_keV'].astype(np.float32))
            d1_list.append(arrays['EdepDet1_keV'].astype(np.float32))
            d2_list.append(arrays['EdepDet2_keV'].astype(np.float32))
            d3_list.append(arrays['EdepDet3_keV'].astype(np.float32))
    except Exception as e:
        print(f"Erro ao ler {file_name}: {e}")

arr_pdg = np.concatenate(pdg_list)
arr_d0 = np.concatenate(d0_list)
arr_d1 = np.concatenate(d1_list)
arr_d2 = np.concatenate(d2_list)
arr_d3 = np.concatenate(d3_list)

num_particles = len(arr_pdg)
t_io_end = time.perf_counter()
print(f"Total de partículas extraídas: {num_particles}")

# --- 5. Processamento na GPU com Taichi ---
print("A calcular na GPU...")
t_gpu_start = time.perf_counter() # Cronómetro da GPU

out_edep = np.empty(num_particles, dtype=np.float32)
out_abs_pdg = np.empty(num_particles, dtype=np.int32)

# Chamar a função na GPU
process_particles(arr_pdg, arr_d0, arr_d1, arr_d2, arr_d3, out_edep, out_abs_pdg)

# OBRIGATÓRIO: Sincronizar para medir o tempo exato que a GPU demorou
ti.sync() 
t_gpu_end = time.perf_counter()

# --- 6. Filtragem e Separação (NumPy / CPU) ---
print("A filtrar dados...")
t_filter_start = time.perf_counter() # Cronómetro de Filtragem

mask_positive = out_edep > 0
valid_edep = out_edep[mask_positive]
valid_pdg = out_abs_pdg[mask_positive]

muons = valid_edep[valid_pdg == 13]
pions = valid_edep[valid_pdg == 211]
others = valid_edep[~np.isin(valid_pdg, [13, 211])]

t_filter_end = time.perf_counter()

# --- 7. Visualização ---
print("A desenhar o gráfico...")
t_plot_start = time.perf_counter() # Cronómetro do Gráfico

plt.figure(figsize=(12, 7))

plt.hist(muons, bins=NBINS, range=(0, X_MAX_KEV), histtype='step', linewidth=2, color='blue', label=f'Muões (N={len(muons[muons <= X_MAX_KEV])})') 
plt.hist(pions, bins=NBINS, range=(0, X_MAX_KEV), histtype='step', linewidth=2, color='red', label=f'Piões (N={len(pions[pions <= X_MAX_KEV])})') 
plt.hist(others, bins=NBINS, range=(0, X_MAX_KEV), histtype='step', linewidth=2, color='green', label=f'Outras (N={len(others[others <= X_MAX_KEV])})')

plt.yscale('log')
plt.title(f'Deposição de Energia Total (Taichi GPU - 4 Runs, 0 a {X_MAX_KEV} keV)', fontsize=15, fontweight='bold')
plt.xlabel('Energia Total Depositada [keV]', fontsize=12)
plt.ylabel('Frequência (Entradas)', fontsize=12)
plt.grid(True, which="major", ls="--", alpha=0.5) 
plt.legend(fontsize=11)
plt.xlim(0, X_MAX_KEV) 

os.makedirs('Imagens', exist_ok=True)
output_file = 'Imagens/EX3_Taichi.png' 
plt.savefig(output_file, dpi=150)

t_plot_end = time.perf_counter()
t_total_end = time.perf_counter()

# --- RELATÓRIO DE TEMPO ---
print("\n" + "="*40)
print("⏱️  RELATÓRIO DE DESEMPENHO")
print("="*40)
print(f"Leitura dos ficheiros (I/O) : {t_io_end - t_io_start:.4f} segundos")
print(f"Cálculos Matemáticos (GPU)  : {t_gpu_end - t_gpu_start:.4f} segundos")
print(f"Filtragem Numpy (CPU)       : {t_filter_end - t_filter_start:.4f} segundos")
print(f"Geração do Gráfico          : {t_plot_end - t_plot_start:.4f} segundos")
print("-" * 40)
print(f"TEMPO TOTAL (Script)        : {t_total_end - t_total_start:.4f} segundos")
print("="*40 + "\n")

plt.show()