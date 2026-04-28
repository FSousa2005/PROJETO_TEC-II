import ROOT
import sys

def exercice1(filename, outputname):
    # 1. Abrir o ficheiro
    f = ROOT.TFile.Open(filename)
    edep_Per_Event = f.Get("edep_Per_Event") 

    nbins = 400

    # 1. Definir o mínimo
    # Como no seu Draw você faz o corte "detector > 0", o mínimo faz sentido ser 0.
    xmin = 0.0 

    # 2. Descobrir o máximo global
    # Pedimos ao ROOT o máximo de CADA coluna explicitamente
    max0 = edep_Per_Event.GetMaximum("detector0")
    max1 = edep_Per_Event.GetMaximum("detector1")
    max2 = edep_Per_Event.GetMaximum("detector2")
    max3 = edep_Per_Event.GetMaximum("detector3")

    # O xmax será o maior valor absoluto entre os 4 detetores
    xmax = max(max0, max1, max2, max3) * 1.05

    # 2. Criar o histograma com limites (0, 0)
    # Damos um nome interno "hist"
    histogram = ROOT.TH1F("detetor0", "Energia Total Acumulada;Energia (MeV);Entradas", nbins, xmin, xmax)
    histogram1 = ROOT.TH1F("detetor1", "Energia Total Acumulada;Energia (MeV);Entradas", nbins, xmin, xmax)
    histogram2 = ROOT.TH1F("detetor2", "Energia Total Acumulada;Energia (MeV);Entradas", nbins, xmin, xmax)
    histogram3 = ROOT.TH1F("detetor3", "Energia Total Acumulada;Energia (MeV);Entradas", nbins, xmin, xmax)

    # 3. Projetar os dados
    # O primeiro Draw define os eixos iniciais
    edep_Per_Event.Draw("detector0>>detetor0", "detector0 > 0", "goff")
    edep_Per_Event.Draw("detector1>>detetor1", "detector1 > 0", "goff")
    edep_Per_Event.Draw("detector2>>detetor2", "detector2 > 0", "goff")
    edep_Per_Event.Draw("detector3>>detetor3", "detector3 > 0", "goff")

    ficheiro_saida = ROOT.TFile(outputname, "RECREATE")
    histogram.Write()
    histogram1.Write()
    histogram2.Write()
    histogram3.Write()
    ficheiro_saida.Close()

    print("Histograma gerado com sucesso.")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Nenhum input inserido.")
        exit(1)

    for i in set(sys.argv[1:]):
        if not i.isdigit() or len(i) != 1:
            print(f"Erro: {i} não é um dígito.")
            continue

        exercice1(f"ROOTFILES/AmberTarget_Run_{i}.root", f"ROOTFILES/EX1_HIST_{i}.root")

    exit(0)