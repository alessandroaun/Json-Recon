import json

def gerar_tabela_consorcio_com_descontos():
    print("--- Gerador de Tabela de Consórcio ---")
    
    # 1. Solicitação dos Parâmetros
    try:
        # Nova pergunta solicitada
        tipo_plano = input("1. Que tipo de plano? (N, L ou SL): ").upper().strip()
        if tipo_plano not in ['N', 'L', 'SL']:
            print("Erro: Tipo de plano inválido. Use N, L ou SL.")
            return

        id_tabela = input("2. Qual o ID da Tabela? (ex: tabela_natal_imovel2011_201_normal): ")
        
        tx_adm = float(input("3. Informe a Taxa de Administração (ex: 15 para 15%): "))
        fundo_reserva = float(input("4. Informe o Fundo de Reserva (ex: 2 para 2%): "))
        seguro_vida = float(input("5. Informe o Seguro de Vida (ex: 0.05 para 0.05%): "))
        prazo = int(input("6. Informe o Prazo do plano (em meses): "))
        
    except ValueError:
        print("Erro: Por favor, insira números válidos para taxas e prazo.")
        return

    # Definir o fator de redução com base no tipo de plano
    fator_reducao = 1.0 # 100% (Plano Normal)
    if tipo_plano == 'L':
        fator_reducao = 0.75 # Redução de 25%
    elif tipo_plano == 'SL':
        fator_reducao = 0.50 # Redução de 50%

    # --- ALTERAÇÃO AQUI ---
    # Lista de créditos solicitada: 80.000 a 110.000 (passo de 10.000)
    # O range vai até 120000 para incluir o 110000
    lista_valores_credito = range(80000, 120000, 10000) 
    
    # Lista que vai conter todos os objetos de crédito
    lista_dados_calculados = []

    # 2. Processamento dos Cálculos
    for credito in lista_valores_credito:
        
        # --- Cálculo da Parcela Base (Sem Redução de Plano) ---
        
        # 1. Montante total a pagar (Crédito + Taxa Adm + Fundo Reserva)
        total_taxas_percentual = (tx_adm + fundo_reserva) / 100
        montante_total = credito * (1 + total_taxas_percentual)
        
        # 2. Parcela mensal antes da redução do plano (Valor integral)
        parcela_base_integral = montante_total / prazo
        
        # 3. Cálculo do valor do seguro (Fixado sobre o montante total, como solicitado)
        valor_seguro_mensal = montante_total * (seguro_vida / 100)
        
        # --- Aplicação da Lógica do Plano (N, L, SL) ---
        
        # 4. Parcela S/SV: Aplica-se a redução do plano sobre a parcela integral
        # (N=100%, L=75%, SL=50%)
        parcela_ssv = parcela_base_integral * fator_reducao
        
        # 5. Parcela C/SV: Soma a Parcela S/SV (já reduzida, se for L ou SL) com o valor do seguro
        parcela_csv = parcela_ssv + valor_seguro_mensal

        # Estrutura interna do crédito
        item = {
            "credito": credito,
            "prazos": [
                {
                    "prazo": prazo,
                    "parcela_CSV": round(parcela_csv, 2),
                    "parcela_SSV": round(parcela_ssv, 2)
                }
            ]
        }
        
        lista_dados_calculados.append(item)

    # 3. Construção do Objeto JSON Final
    json_final = {
        id_tabela: lista_dados_calculados
    }

    # 4. Geração e Exibição do JSON
    json_output = json.dumps(json_final, indent=4, ensure_ascii=False)
    
    print("\n--- JSON Gerado ---\n")
    print(json_output)
    
    # Salvar em arquivo
    nome_arquivo = f"{id_tabela}_{tipo_plano}.json"
    
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write(json_output)
        print(f"\nArquivo '{nome_arquivo}' salvo com sucesso.")
    except Exception as e:
        print(f"\nErro ao salvar arquivo: {e}")

# Executar a função
if __name__ == "__main__":
    gerar_tabela_consorcio_com_descontos()
