import sys
import ROOT

def exercice9(filename, outputname):
    # Abrir ficheiro
    f = ROOT.TFile.Open(filename)
    tree = f.Get("tracksData")

    nbins = 200
    xmin = -5
    xmax = 210

    # Criar histogramas
    h_primary = ROOT.TH1F("h_primary", "pZ - Pioes Primarios", nbins, xmin, xmax)
    h_secondary = ROOT.TH1F("h_secondary", "pZ - Pioes Secundarios", nbins, xmin, xmax)

    # Cortes
    cut_pions = "(particlePDG == 211 || particlePDG == -211)"
    cut_primary = "IsPrimary == 1"
    cut_secondary = "IsPrimary == 0"

    # Preencher histogramas SEM desenhar
    tree.Draw("pZ_GeV >> h_primary", f"{cut_pions} && {cut_primary}", "goff")
    tree.Draw("pZ_GeV >> h_secondary", f"{cut_pions} && {cut_secondary}", "goff")

    # Criar ficheiro de saída
    ficheiro_saida = ROOT.TFile(outputname, "RECREATE")

    # Guardar histogramas
    h_primary.Write()
    h_secondary.Write()

    ficheiro_saida.Close()
    f.Close()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Nenhum input inserido.")
        exit(1)

    for i in set(sys.argv[1:]):
        if not i.isdigit() or len(i) != 1:
            print(f"Erro: {i} não é um dígito.")
            continue

        exercice9(f"ROOTFILES/AmberTarget_Run_{i}.root", f"ROOTFILES/EX9_HIST_{i}.root")

    exit(0)