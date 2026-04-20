import ROOT

# 1. Abrir o ficheiro
f = ROOT.TFile.Open("ROOTFILES/AmberTarget_Run_0.root")
edep_Per_Event = f.Get("edep_Per_Event") 

nbins = 400

# 1. Definir o mínimo
# Como no seu Draw você faz o corte "detector > 0", o mínimo faz sentido ser 0.
xmin = 0.0 

# 2. Descobrir o máximo global
# Pedimos ao ROOT o máximo de CADA coluna explicitamente
max0 = edep_Per_Event.GetMaximum("detector0")
max1 = edep_Per_Event.GetMaximum("detector1")
max2 = edep_Per_Event.GetMaximum("detector2")
max3 = edep_Per_Event.GetMaximum("detector3")

# O xmax será o maior valor absoluto entre os 4 detetores
xmax = max(max0, max1, max2, max3) * 1.05

# 2. Criar o histograma com limites (0, 0)
# Damos um nome interno "hist"
histogram = ROOT.TH1F("hist", "Energia Total Acumulada;Energia (MeV);Entradas", nbins, xmin, xmax)
histogram1 = ROOT.TH1F("hist1", "Energia Total Acumulada;Energia (MeV);Entradas", nbins, xmin, xmax)
histogram2 = ROOT.TH1F("hist2", "Energia Total Acumulada;Energia (MeV);Entradas", nbins, xmin, xmax)
histogram3 = ROOT.TH1F("hist3", "Energia Total Acumulada;Energia (MeV);Entradas", nbins, xmin, xmax)

# 3. Projetar os dados
# O primeiro Draw define os eixos iniciais
edep_Per_Event.Draw("detector0>>hist", "detector0 > 0", "goff")
edep_Per_Event.Draw("detector1>>hist1", "detector1 > 0", "goff")
edep_Per_Event.Draw("detector2>>hist2", "detector2 > 0", "goff")
edep_Per_Event.Draw("detector3>>hist3", "detector3 > 0", "goff")

# 4. Visualização
canvas = ROOT.TCanvas("c1", "Visualizacao", 800, 600)
ROOT.gStyle.SetOptStat(0) 
histogram.SetLineColor(ROOT.kBlue)      # Azul
histogram1.SetLineColor(ROOT.kRed)       # Vermelho
histogram2.SetLineColor(ROOT.kGreen + 2) # Verde escuro
histogram3.SetLineColor(ROOT.kMagenta)   # Rosa/Roxo

histogram.SetLineColor(ROOT.kBlue + 2)
histogram.SetLineWidth(2)
histogram.Draw("HIST") 
histogram1.Draw("same") 
histogram2.Draw("same") 
histogram3.Draw("same") 

canvas.SetLogy()
canvas.Update()
# canvas.SaveAs("histograma_acumulado.png")

ficheiro_saida = ROOT.TFile("Meus_Histogramas_Energia.root", "RECREATE")
histogram.Write()
histogram1.Write()
histogram2.Write()
histogram3.Write()
ficheiro_saida.Close()

print("Histograma gerado com sucesso.")
input("Pressione Enter para fechar...")