import ROOT
import sys
import os

def ex9ploter(filename):
    if not os.path.isfile(filename):
        print(f"Não existe o ficheiro {filename}.\nÉ melhor criá-lo para não haver problemas.")
        return 1

    colors = [ROOT.kBlue, ROOT.kRed]

    f = ROOT.TFile.Open(filename)

    canvas = ROOT.TCanvas("c", "Distribuição", 800, 600)
    ROOT.gStyle.SetOptStat(0)

    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)

    hist_names = [key.GetName() for key in f.GetListOfKeys()]

    first = True

    for i, name in enumerate(hist_names):
        h = f.Get(name)

        h.SetLineWidth(2)
        h.SetLineColor(colors[i])

        h.GetXaxis().SetTitle("pZ (GeV)")
        h.GetYaxis().SetTitle("Entradas")
        #h.GetXaxis().SetRangeUser(config.xmin, config.xmax)

        if first:
            h.Draw("HIST")
            first = False
        else:
            h.Draw("HIST SAME")

        h.SetMinimum(1)
        h.SetMaximum(1e5)

        legend.AddEntry(h, name, "l")

    legend.Draw()

    canvas.SetLogy()

    canvas.Update()
    input("Enter para sair")

    return 0

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Nenhum input inserido.")
        exit(1)

    for i in set(sys.argv[1:]):
        if not i.isdigit() or len(i) != 1:
            print(f"Erro: {i} não é um dígito.")
            continue

        ex9ploter(f"ROOTFILES/EX9_HIST_{i}.root")

    exit(0)