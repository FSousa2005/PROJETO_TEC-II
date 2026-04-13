import sys
import ROOT

# ADICIONAR MAIS TERMOS PARA MANIPULAR MELHOR OS GRÁFICOS (DOMÍNIOS, CORES, DADOS INSERIDOS)
# SUGESTÃO, INSERIR COMO OUTPUT GRÁFICO, E DAR POSSIBILIDADE DE MANIPULAÇÃO EXTERIOR
def rootploter(filename):
    # Abrir ficheiro
    f = ROOT.TFile.Open(filename)

    canvas = ROOT.TCanvas("c", "Auto", 800, 600)
    ROOT.gStyle.SetOptStat(0)

    first = True

    for key in f.GetListOfKeys():
        obj = key.ReadObj()
        
        # Verificar se é histograma
        if obj.InheritsFrom("TH1"):
            obj.SetLineWidth(2)
            
            if first:
                obj.Draw("HIST")
                first = False
            else:
                obj.Draw("HIST SAME")

    canvas.Update()
    input("Enter para sair")



def main(argv):
    rootploter(argv)

    return 0

# script.py arg1 arg2


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(f"Erro: nome de ficheiro nao entregue")
        exit(1)

    rootploter(sys.argv[1])

    # main(sys.argv)
    exit(0)