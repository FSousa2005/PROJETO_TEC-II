import uproot

def inspecionar_ficheiro_root(caminho_ficheiro):
    try:
        # Abrir o ficheiro
        with uproot.open(caminho_ficheiro) as file:
            print(f"--- Estrutura do ficheiro: {caminho_ficheiro} ---\n")
            
            # Listar todas as chaves (objetos) no ficheiro
            for chave in file.keys():
                objeto = file[chave]
                print(f"Objeto: {chave} (Tipo: {type(objeto).__name__})")
                
                # Se for uma TTree, mostrar os ramos e os tipos de dados
                if isinstance(objeto, uproot.TTree):
                    print("  Estrutura da TTree:")
                    # show() imprime os tipos de dados e nomes das colunas
                    objeto.show()
                print("-" * 30)
                
    except Exception as e:
        print(f"Erro ao ler o ficheiro: {e}")

# Exemplo de uso
inspecionar_ficheiro_root("AmberTarget_Run_0.root")