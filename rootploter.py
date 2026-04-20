import sys
import ROOT

class RootPlotAttributes:
    def __init__(
        self,
        hist_names=None,
        colors=None,
        title="Plot",
        x_label="",
        y_label="",
        logy=False,
        xmin=None,
        xmax=None,
        ymin=None,
        ymax=None
    ):
        # Tipos obrigatórios / validações

        if hist_names is not None and not isinstance(hist_names, list):
            raise TypeError("hist_names deve ser uma lista de strings ou None")

        if colors is not None:
            if not isinstance(colors, list):
                raise TypeError("colors deve ser uma lista")
            for c in colors:
                if not isinstance(c, int):
                    raise TypeError("Cada cor deve ser um inteiro (ex: ROOT.kRed)")

        if not isinstance(title, str):
            raise TypeError("title deve ser string")

        if not isinstance(x_label, str):
            raise TypeError("x_label deve ser string")

        if not isinstance(y_label, str):
            raise TypeError("y_label deve ser string")

        if not isinstance(logy, bool):
            raise TypeError("logy deve ser boolean")

        for val, name in [(xmin,"xmin"), (xmax,"xmax"), (ymin,"ymin"), (ymax,"ymax")]:
            if val is not None and not isinstance(val, (int, float)):
                raise TypeError(f"{name} deve ser número ou None")

        if xmin is not None and xmax is not None and xmin >= xmax:
            raise ValueError("xmin deve ser menor que xmax")

        if ymin is not None and ymax is not None and ymin >= ymax:
            raise ValueError("ymin deve ser menor que ymax")

        # Atribuição
        self.hist_names = hist_names
        self.colors = colors
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.logy = logy
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

# ADICIONAR MAIS TERMOS PARA MANIPULAR MELHOR OS GRÁFICOS (DOMÍNIOS, CORES, DADOS INSERIDOS)
# SUGESTÃO, INSERIR COMO OUTPUT GRÁFICO, E DAR POSSIBILIDADE DE MANIPULAÇÃO EXTERIOR
def rootploter(filename, config: RootPlotAttributes):
    f = ROOT.TFile.Open(filename)

    if not f or f.IsZombie():
        raise IOError("Erro ao abrir ficheiro ROOT")

    canvas = ROOT.TCanvas("c", config.title, 800, 600)
    ROOT.gStyle.SetOptStat(0)

    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)

    # Histogramas
    if config.hist_names is None:
        hist_names = [key.GetName() for key in f.GetListOfKeys()]
    else:
        hist_names = config.hist_names

    first = True

    for i, name in enumerate(hist_names):
        h = f.Get(name)

        if not h or not h.InheritsFrom("TH1"):
            continue

        h.SetLineWidth(2)

        # Cor
        if config.colors and i < len(config.colors):
            h.SetLineColor(config.colors[i])

        # Labels
        if config.x_label:
            h.GetXaxis().SetTitle(config.x_label)
        if config.y_label:
            h.GetYaxis().SetTitle(config.y_label)

        # Limites
        if config.xmin is not None and config.xmax is not None:
            h.GetXaxis().SetRangeUser(config.xmin, config.xmax)

        if config.ymin is not None:
            h.SetMinimum(config.ymin)

        if config.ymax is not None:
            h.SetMaximum(config.ymax)

        # Draw
        if first:
            h.Draw("HIST")
            first = False
        else:
            h.Draw("HIST SAME")

        legend.AddEntry(h, name, "l")

    legend.Draw()

    if config.logy:
        canvas.SetLogy()

    canvas.Update()
    input("Enter para sair")

# script.py arg1 arg2

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python script.py <ficheiro.root>")
        sys.exit(1)

    filename = sys.argv[1]

    # Configuração padrão (podes alterar aqui)
    config = RootPlotAttributes(
        hist_names=None,  # ou ["h_primary", "h_secondary"]
        colors=[ROOT.kBlue, ROOT.kRed],
        title="Distribuição",
        x_label="pZ (GeV)",
        y_label="Entradas",
        logy=True,
        xmin=-5,
        xmax=210,
        ymin=1,
        ymax=1e5
    )

    rootploter(filename, config)