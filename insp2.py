import ROOT

def inspecionar_ficheiro_root(caminho_ficheiro):
    try:
        # Abrir ficheiro ROOT
        file = ROOT.TFile.Open(caminho_ficheiro)

        if not file or file.IsZombie():
            print("Erro ao abrir o ficheiro.")
            return

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

    except Exception as e:
        print(f"Erro ao ler o ficheiro: {e}")


# Exemplo de uso
inspecionar_ficheiro_root("ROOTFILES/AmberTarget_Run_0.root")