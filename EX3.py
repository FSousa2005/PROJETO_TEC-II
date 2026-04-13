import ROOT

# Garante que a interface gráfica abre
ROOT.gROOT.SetBatch(False)

# 1. Abrir o ficheiro e buscar a árvore 'Hits' (e não a edep_Per_Event)
f = ROOT.TFile.Open("AmberTarget_Run_0.root")
if not f or f.IsZombie():
    print("Erro ao abrir o ficheiro!")
    exit()

tree_hits = f.Get("tracksData") 

# 2. Criar os histogramas para cada tipo de partícula
# A variável na árvore está em keV (Edep_keV)
h_muoes = ROOT.TH1F("h_muoes", "Energia Depositada por Particula;Energia (keV);Entradas", 200, 0, 20000)
h_pioes = ROOT.TH1F("h_pioes", "Energia Depositada por Particula;Energia (keV);Entradas", 200, 0, 20000)
h_outras = ROOT.TH1F("h_outras", "Energia Depositada por Particula;Energia (keV);Entradas", 200, 0, 20000)

# 3. Definir os "Cuts" (Filtros) com base no código PDG
# Usamos abs() para apanhar tanto a partícula como a antipartícula (+ e -)
cut_muoes = "abs(particlePDG) == 13"
cut_pioes = "abs(particlePDG) == 211 || particlePDG == 111"
cut_outras = "abs(particlePDG) != 13 && abs(particlePDG) != 211 && particlePDG != 111"

# 4. Projetar os dados (Edep_keV) da árvore para os histogramas aplicando os filtros
tree_hits.Draw("EdepDet0_keV+EdepDet1_keV+EdepDet2_keV+EdepDet3_keV>>h_muoes", cut_muoes, "goff")
tree_hits.Draw("EdepDet0_keV+EdepDet1_keV+EdepDet2_keV+EdepDet3_keV>>h_pioes", cut_pioes, "goff")
tree_hits.Draw("EdepDet0_keV+EdepDet1_keV+EdepDet2_keV+EdepDet3_keV>>h_outras", cut_outras, "goff")

# 5. Estilização
h_muoes.SetLineColor(ROOT.kBlue)
h_muoes.SetLineWidth(2)

h_pioes.SetLineColor(ROOT.kRed)
h_pioes.SetLineWidth(2)

h_outras.SetLineColor(ROOT.kGreen + 2)
h_outras.SetLineWidth(2)

# 6. Visualização
canvas = ROOT.TCanvas("c1", "Energia por Particula", 800, 600)
ROOT.gStyle.SetOptStat(0) # Esconde a caixa de estatísticas
canvas.SetLogy() # Escala logarítmica no eixo Y é recomendada para comparar contagens baixas e altas

# Desenhar (h_outras desenhado primeiro porque costuma ter mais contagens, definindo melhor o eixo Y)
h_outras.Draw("HIST")
h_pioes.Draw("HIST SAME")
h_muoes.Draw("HIST SAME")

# Adicionar uma Legenda para sabermos qual é qual
legenda = ROOT.TLegend(0.65, 0.7, 0.85, 0.85) # Coordenadas X1, Y1, X2, Y2 (em percentagem do ecrã)
legenda.AddEntry(h_muoes, "Muoes", "l")
legenda.AddEntry(h_pioes, "Pioes", "l")
legenda.AddEntry(h_outras, "Outras", "l")
legenda.SetBorderSize(0)
legenda.Draw()

# Atualizar e manter aberto
canvas.Update()
canvas.Draw()
canvas.SaveAs("energia_por_particula.png")

print("Gráfico gerado! Verifica o ficheiro 'energia_por_particula.png'.")
input("Pressione Enter para fechar...")