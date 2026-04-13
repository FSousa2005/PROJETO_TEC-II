import ROOT

# 1. Configurações de sistema e estilo
ROOT.gROOT.SetBatch(False)
ROOT.gStyle.SetOptStat(0)  # Remove a caixa de estatísticas para um look mais limpo

# 2. Abrir o ficheiro e obter a árvore
f = ROOT.TFile.Open("AmberTarget_Run_0.root")
if not f or f.IsZombie():
    print("Erro: Ficheiro não encontrado!")
    exit()

tree = f.Get("hadronicVertex")

# 3. Criar os histogramas (400 bins para boa resolução)
# Usamos (400, 0, 0) para o ROOT tentar calcular os limites automaticamente
h_prim = ROOT.TH1F("h_prim", "Distribuicao de Vertices Hadronicos;Z (cm);Entradas", 400, 0, 0)
h_sec  = ROOT.TH1F("h_sec",  "Distribuicao de Vertices Hadronicos;Z (cm);Entradas", 400, 0, 0)

# 4. Projetar os dados
# O modo "goff" (graphics off) evita que o ROOT tente desenhar janelas intermédias
tree.Draw("vertexPosZ_cm>>h_prim", "IsPrimary == 1", "goff")
tree.Draw("vertexPosZ_cm>>h_sec",  "IsPrimary == 0", "goff")

# 5. Estética do gráfico
h_prim.SetLineColor(ROOT.kBlue)
h_prim.SetLineWidth(2)
# h_prim.SetFillColorAlpha(ROOT.kBlue, 0.3) # Opcional: preenchimento azul claro

h_sec.SetLineColor(ROOT.kRed)
h_sec.SetLineWidth(2)

# 6. Preparar o Canvas
canvas = ROOT.TCanvas("c1", "Vertices Hadronicos", 800, 600)
canvas.SetLogy() # Escala logarítmica é essencial para ver secundários
canvas.SetGrid() # Adiciona uma grelha para facilitar a leitura das coordenadas

# 7. Desenhar e ajustar eixos
# Desenha o que tem mais entradas primeiro para o eixo Y se ajustar
if h_prim.GetMaximum() > h_sec.GetMaximum():
    h_prim.Draw("HIST")
    h_sec.Draw("HIST SAME")
else:
    h_sec.Draw("HIST")
    h_prim.Draw("HIST SAME")

# 8. Legenda dinâmica com contagem de eventos

leg = ROOT.TLegend(0.65, 0.72, 0.88, 0.88) 
leg.AddEntry(h_prim, f"Primarios [{int(h_prim.GetEntries())}]", "l")
leg.AddEntry(h_sec,  f"Secundarios [{int(h_sec.GetEntries())}]", "l")
leg.SetBorderSize(1)
leg.SetFillColor(0) # Fundo branco para não ser transparente sobre as linhas
leg.Draw()

# 9. Finalização
canvas.Update()
canvas.SaveAs("vertices_hadronicos_root.png")

print("Gráfico gerado com sucesso.")
input("Pressione Enter para fechar...")