import sys
import ROOT

def inspecionar_ficheiro_root(caminho_ficheiro):
    try:
        # Abrir ficheiro ROOT
        file = ROOT.TFile.Open(caminho_ficheiro)

        if not file or file.IsZombie():
            print("Erro ao abrir o ficheiro.")
            return 1

        print(f"--- Estrutura do ficheiro: {caminho_ficheiro} ---\n")

        # Iterar sobre os objetos no ficheiro
        for key in file.GetListOfKeys():
            nome = key.GetName()
            obj = key.ReadObj()

            print(f"Objeto: {nome} (Tipo: {obj.ClassName()})")

            # Se for uma TTree
            if obj.InheritsFrom("TTree"):
                print("  Estrutura da TTree:")
                obj.Print()  # equivalente ao show() do uproot

            print("-" * 30)

        file.Close()

        return 0

    except Exception as e:
        print(f"Erro ao ler o ficheiro: {e}")
        return 1


# Exemplo de uso
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Nenhum input inserido.")
        exit(1)

    for file in sys.argv[1:]:
        inspecionar_ficheiro_root(file)
        print("\n")

    exit(0)