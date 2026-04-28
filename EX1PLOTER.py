import ROOT
import sys
import os

def ex1ploter(filename):
    if not os.path.isfile(filename):
        print(f"Não existe o ficheiro {filename}.\nÉ melhor criá-lo para não haver problemas.")
        return 1

    colors = [ROOT.kBlue + 2, ROOT.kRed, ROOT.kGreen + 2, ROOT.kMagenta]

    f = ROOT.TFile.Open(filename)

    canvas = ROOT.TCanvas("c1", "Visualizacao", 800, 600)
    canva2 = ROOT.TCanvas("c2", "Visualizacao", 800, 600)
    ROOT.gStyle.SetOptStat(0)

    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)

    hist_names = [key.GetName() for key in f.GetListOfKeys()]

    first = True

    for i, name in enumerate(hist_names):
        h = f.Get(name)

        if i == 0:
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

        h.SetMinimum(10)
        #h.SetMaximum(1e5)

        legend.AddEntry(h, name, "l")

    legend.Draw()

    canvas.SetLogy()
    canvas.Update()
    canva2.Update()
    # canvas.SaveAs("histograma_acumulado.png")

    input("Enter para sair")

    # h.SetLineWidth(2)
    # h.Draw("HIST SAME")
    # canvas.Update()

    # input("Enter para sair")

    return 0

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Nenhum input inserido.")
        exit(1)

    for i in set(sys.argv[1:]):
        if not i.isdigit() or len(i) != 1:
            print(f"Erro: {i} não é um dígito.")
            continue

        ex1ploter(f"ROOTFILES/EX1_HIST_{i}.root")

    exit(0)