import ROOT

## PARA MUDAR, AJEITAR UNIDADES

# --- Configuração ---
ROOT_FILE_NAME = "AmberTarget_Run_0.root" 
TREE_NAME = "Hits"

# Definição das categorias e cores
CATEGORIES = ["muon", "pion", "other"]

PARTICLE_LABELS = {
    "muon": "Muões",
    "pion": "Piões",
    "other": "Outras"
}

PARTICLE_COLORS = {
    "muon":  ROOT.kBlue + 1,
    "pion":  ROOT.kRed + 1,
    "other": ROOT.kGray + 1
}

# Parâmetros dos histogramas
N_BINS = 100
X_MIN = 0.0
X_MAX = 5000.0 # 5 MeV
# --------------------

ROOT.gStyle.SetOptStat(0)

print(f"A abrir o ficheiro: {ROOT_FILE_NAME}")
f = ROOT.TFile.Open(ROOT_FILE_NAME)
if not f or f.IsZombie():
    print(f"Erro ao abrir o ficheiro.")
    exit()

tree = f.Get(TREE_NAME)
histograms = {}

# Loop sobre os eventos
n_entries = tree.GetEntries()
print(f"A processar {n_entries} eventos...")

for entry in tree:
    det_id = entry.detectorID
    edep = entry.Edep_keV
    pdg = abs(entry.particlePDG) # Usamos o valor absoluto para simplificar (+/-)
    
    # Lógica de agrupamento
    if pdg == 13:
        p_cat = "muon"
    elif pdg == 211 or pdg == 111:
        p_cat = "pion"
    else:
        p_cat = "other"

    # Inicializar histogramas para o detetor se ainda não existirem
    if det_id not in histograms:
        histograms[det_id] = {}
        for cat in CATEGORIES:
            h_name = f"h_edep_{cat}_det{det_id}"
            h_title = f"Deposição de Energia - Detetor {det_id};Energia (keV);Contagens"
            histograms[det_id][cat] = ROOT.TH1F(h_name, h_title, N_BINS, X_MIN, X_MAX)

    histograms[det_id][p_cat].Fill(edep)

print("A gerar PDF...")

output_pdf_name = "edep_muons_pions_sobrepostos.pdf"
canvases = [] 

if histograms:
    c_open = ROOT.TCanvas("c_open", "open", 1, 1)
    c_open.Print(output_pdf_name + "(", "pdf")

for det_id in sorted(histograms.keys()):
    c = ROOT.TCanvas(f"c_det{det_id}", f"Detetor {det_id}", 900, 700)
    c.SetLogy() # Eixo Y Logarítmico
    canvases.append(c)

    legend = ROOT.TLegend(0.65, 0.7, 0.9, 0.9)
    legend.SetHeader(f"Detetor {det_id}", "C")

    hs = ROOT.THStack(f"hs_det{det_id}", f"Deposição de Energia Sobreposta - Detetor {det_id};Energia (keV);Contagens")
    
    for cat in CATEGORIES:
        h = histograms[det_id][cat]
        if h.GetEntries() > 0:
            color = PARTICLE_COLORS[cat]
            h.SetLineColor(color)
            h.SetLineWidth(2)
            h.SetFillColorAlpha(color, 0.20) # Transparência para ver a sobreposição
            
            hs.Add(h)
            legend.AddEntry(h, f"{PARTICLE_LABELS[cat]} ({int(h.GetEntries())})", "f")

    if hs.GetNhists() > 0:
        hs.SetMinimum(0.5) # Essencial para o LogY
        hs.Draw("HIST NOSTACK") # NOSTACK = Sobrepostos
        legend.Draw()
    
    c.Print(output_pdf_name, "pdf")

if histograms:
    c_close = ROOT.TCanvas("c_close", "close", 1, 1)
    c_close.Print(output_pdf_name + ")", "pdf")

print(f"Concluído! Ficheiro: {output_pdf_name}")
f.Close()