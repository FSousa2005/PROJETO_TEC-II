import ROOT

myFile = ROOT.TFile("ROOTFILES/AmberTarget_Run_3.root", "READ")

tree = myFile.Get("tracksData")

if not tree:
    print("Erro: TTree não encontrada!")
    exit()

# Criar histograma
hist = ROOT.TH1D("h_pz", "Momento Z dos piões; p_{z} [GeV]; Eventos", 200, -10, 10)

# Corte para piões (carregados e neutros)
cut_pioes = "abs(particlePDG)==211 || abs(particlePDG)==111"

# (opcional) primários vs secundários
# Ajusta isto conforme os branches disponíveis!
cut_primarios   = "parentID==0"
cut_secundarios = "parentID!=0"

# Combinar cortes (exemplo: todos os piões)
cut_total = f"({cut_pioes})"

# Se quiseres separar:
# cut_total = f"({cut_pioes}) && ({cut_primarios})"

# Desenhar diretamente
tree.Draw("pz >> h_pz", cut_total)

# Mostrar
c = ROOT.TCanvas()
hist.Draw()
c.Update()

# import ROOT

# # Distribuição do momento na componente Z para piões primários e secundários.

# myFile=ROOT.TFile("ROOTFILES/AmberTarget_Run_0.root","READ")
# browser=ROOT.TBrowser()

# # PGD code

# # hits = myFile.Get("Hits")

# cut_pioes = "abs(particlePDG) == 211 || abs(particlePDG) == 111"

# vertexTree=myFile.Get("Hits; 1")
# # vertexTree.Print()
# vertexTree.Draw("momentumPioes")
# histogram=ROOT.TH1D("momentum_GeV","momentum_GeV",400,-400.,0.)
# vertexTree.Draw("momentumPioes>>momentum_GeV", "", "")

# # INSERIR EIXOS E LEGENDA DOS GRÁFICOS



# # h = ROOT.TH1F("myHist", "myTitle", 64, -4, 4)
# # h.FillRandom("gaus")
# # h.Draw()

# # Guardar histograma e distribuição

