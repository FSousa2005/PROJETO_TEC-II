import ROOT

# 1. Configurações e ficheiro
ROOT.gROOT.SetBatch(False)
f = ROOT.TFile.Open("AmberTarget_Run_0.root")
tree_hits = f.Get("Hits")

# 2. Criar o Canvas dividido em 2x2
canvas = ROOT.TCanvas("c_hits", "Distribuicao Espacial Hits", 1200, 1000)
canvas.Divide(2, 2)

# Lista para guardar os histogramas (para o Python não os apagar da memória)
hists = []

# 3. Loop pelos 4 detetores
for i in range(4):
    canvas.cd(i + 1) # Mudar para o quadrante correspondente
    
    # Criar TH2F: nome, título, nBinsX, minX, maxX, nBinsY, minY, maxY
    h_name = f"h_det{i}"
    h_title = f"Detetor {i}: Posicao dos Hits;X (cm);Y (cm)"
    # Ajustei os limites para -10 a 10 cm, mas podes usar (100,0,0, 100,0,0) para auto
    h2 = ROOT.TH2F(h_name, h_title, 150, -40, 40, 150, -40, 40)
    
    # Projetar X e Y filtrando pelo detectorID
    # O formato para 2D no Draw é "Y:X"
    draw_cmd = f"hitPosY_cm:hitPosX_cm>>{h_name}"
    cut_cmd = f"detectorID == {i}"
    
    tree_hits.Draw(draw_cmd, cut_cmd, "colz") # "colz" adiciona a paleta de cores lateral
    
    hists.append(h2)

# 4. Finalização
canvas.Update()
canvas.SaveAs("hits_XY_detetores.png")

print("Mapas de calor (XY) gerados para os 4 detetores.")
input("Pressione Enter para fechar...")