import sys
import ROOT


def getHistograms(filename, hist_names=None):
    f = ROOT.TFile.Open(filename)

    if not f or f.IsZombie():
        raise IOError("Erro ao abrir ficheiro ROOT")
    
    if hist_names is None:
        hist_names = [key.GetName() for key in f.GetListOfKeys()]

    histograms = {}

    for name in hist_names:
        h = f.Get(name)

        if h and h.InheritsFrom("TH1"):
            h.SetDirectory(0)
            histograms[name] = h

    f.Close()

    return histograms


def plotTH1(hist,
            lineWidth=None, color=None,
            x_label=None, y_label=None,
            x_min=None, x_max=None, y_min=None, y_max=None,
            drawState="HIST SAME"):
    if not hist or not hist.InheritsFrom("TH1"):
        raise TypeError("hist não é um valor válido")

    if lineWidth is not None:
        hist.SetLineWidth(lineWidth)

    # Cor
    if color is not None:
        hist.SetLineColor(color)

    # Labels
    if x_label:
        hist.GetXaxis().SetTitle(x_label)
    if y_label:
        hist.GetYaxis().SetTitle(y_label)

    # Limites
    if x_min is not None and x_max is not None:
        hist.GetXaxis().SetRangeUser(x_min, x_max)

    if y_min is not None:
        hist.SetMinimum(y_min)

    if y_max is not None:
        hist.SetMaximum(y_max)

    # Draw
    hist.Draw(drawState)


# MELHORAR PARTE DO CONTROLO DO DRAW
# NÃO QUERO O INPUT ENTER DENTRO DA FUNÇÃO
# QUERO CORES DIFERENTES NOS GRÁFICOS
def filePloter(filename, title):
    histograms = getHistograms(filename)

    canvas = ROOT.TCanvas("c", title, 800, 600)
    ROOT.gStyle.SetOptStat(0)

    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)

    first = True

    draw_state = "HIST"

    for hist_name, hist in histograms.items():
        plotTH1(hist, drawState=draw_state)

        if first:
            draw_state = "HIST SAME"
            first = False

        legend.AddEntry(hist, hist_name, "l")

    legend.Draw()

    canvas.SetLogy()
    canvas.Update()

    input("Enter para sair")

    return canvas

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python script.py <ficheiro.root>")
        sys.exit(1)

    filePloter(sys.argv[1], sys.argv[2])
    #input("Enter para sair ")

    exit(0)

    # # Configuração padrão (podes alterar aqui)
    # config = RootPlotAttributes(
    #     hist_names=None,  # ou ["h_primary", "h_secondary"]
    #     colors=[ROOT.kBlue, ROOT.kRed],
    #     title="Distribuição",
    #     x_label="pZ (GeV)",
    #     y_label="Entradas",
    #     logy=True,
    #     xmin=-5,
    #     xmax=210,
    #     ymin=1,
    #     ymax=1e5
    # )

    # rootploter(filename, config)