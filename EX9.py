import sys
import ROOT

def exercice9(filename):
    # Abrir ficheiro
    f = ROOT.TFile.Open(filename)

    # Escolher a TTree correta (recomendo tracksData)
    tree = f.Get("tracksData")

    nbins = 200
    xmin = -5
    xmax = 210

    # Criar histogramas
    h_primary = ROOT.TH1F("h_primary", "pZ - Pioes Primarios; pZ (GeV); Entradas", nbins, xmin, xmax)
    h_secondary = ROOT.TH1F("h_secondary", "pZ - Pioes Secundarios; pZ (GeV); Entradas", nbins, xmin, xmax)

    # Cortes (cuts)
    cut_pions = "(particlePDG == 211 || particlePDG == -211)"
    cut_primary = "IsPrimary == 1"
    cut_secondary = "IsPrimary == 0"

    # Projetar dados
    tree.Draw("pZ_GeV >> h_primary", f"{cut_pions} && {cut_primary}", "goff")
    tree.Draw("pZ_GeV >> h_secondary", f"{cut_pions} && {cut_secondary}", "goff")
    ROOT.gStyle.SetOptStat(0)

    # Visualização
    canvas = ROOT.TCanvas("c1", "Distribuicao pZ", 800, 600)

    h_primary.SetLineColor(ROOT.kBlue)
    h_secondary.SetLineColor(ROOT.kRed)

    h_primary.SetLineWidth(2)
    h_secondary.SetLineWidth(2)

    h_primary.SetMinimum(1)     # valor mínimo no eixo Y
    h_primary.SetMaximum(1e5)   # valor máximo no eixo Y

    h_primary.Draw("HIST")
    h_secondary.Draw("HIST SAME")

    # Legenda
    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
    legend.AddEntry(h_primary, "Primarios", "l")
    legend.AddEntry(h_secondary, "Secundarios", "l")
    legend.Draw()

    canvas.SetLogy()
    canvas.Update()

    ficheiro_saida = ROOT.TFile("Meus_Histogramas_Energia.root", "RECREATE")
    histogram.Write()
    histogram1.Write()
    histogram2.Write()
    histogram3.Write()
    ficheiro_saida.Close()

    input("Pressione Enter para fechar...")

# Exemplo de uso
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Nenhum input inserido.")
        exit(1)

    for i in set(sys.argv[1:]):
        if not i.isdigit() or len(i)!=1:
            print(f"Erro: {i} não é um dígito.")
            continue

        exercice9(f"ROOTFILES/AmberTarget_Run_{i}.root")

    exit(0)