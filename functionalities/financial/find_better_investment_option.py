def calculate_amount_digital_bank(principal, taxa_juros_mensal, anos):
    n = 12
    montante = principal * (1 + taxa_juros_mensal / 100 / n) ** (n * anos)
    return montante

def calcular_montante_fiis(principal, yields_anuais, anos):
    n = 12
    montante = principal
    for yield_anual in yields_anuais:
        rendimento_mensal = (yield_anual / 100) / n
        for _ in range(int(n * anos)):
            montante *= (1 + rendimento_mensal)
    return montante


principal = 30_000
cdi = 13.04
taxa_juros_mensal = cdi / 12 / 100  # CDI + 100%
anos = 5

# Digital Bank
montante_banco_digital = calculate_amount_digital_bank(principal, taxa_juros_mensal, anos)

yields_anuais = [10.71, 13.02, 10.85]  # Yields dos FIIs GALG11, MXRF11, XPSF11

montante_fiis = calcular_montante_fiis(principal, yields_anuais, anos)

print(f"Montante Fundos Imobiliários Unificados: R$ {montante_fiis:.2f}")
print(f"Banco Digital: R$ {montante_banco_digital:.2f}")









def valor_mensal_rendimento_banco_digital(principal, aporte_mensal, taxa_juros_mensal, anos):
    n = 12  # Composto mensalmente
    montante = principal
    for i in range(int(n * anos)):
        montante += aporte_mensal
        montante *= (1 + taxa_juros_mensal / 100 / n)
    rendimento_mensal = montante / (anos * 12)
    return rendimento_mensal

def valor_mensal_rendimento_fiis(principal, aporte_mensal, yields_anuais, anos):
    n = 12  # Distribuído mensalmente
    montante = principal
    for _ in range(int(n * anos)):
        for yield_anual in yields_anuais:
            montante += aporte_mensal
            rendimento_mensal = (montante / principal) ** (1 / (12 * anos)) - 1
            montante *= (1 + yield_anual / 100 / n)
    rendimento_mensal = montante / (anos * 12)
    return rendimento_mensal

# Exemplo de uso
principal = 30000  # R$ 30.000,00
aporte_mensal = 2500  # R$ 2.500,00
taxa_juros_mensal_banco_digital = 13.04 / 12 / 100  # CDI + 100%
yields_anuais_fiis = [10.71, 13.02, 10.85]  # Yields dos FIIs GALG11, MXRF11, XPSF11
anos = 5

rendimento_mensal_banco = valor_mensal_rendimento_banco_digital(principal, aporte_mensal, taxa_juros_mensal_banco_digital, anos)
rendimento_mensal_fiis = valor_mensal_rendimento_fiis(principal, aporte_mensal, yields_anuais_fiis, anos)

print(f"Rendimento Mensal Banco Digital: R$ {rendimento_mensal_banco:.2f}")
print(f"Rendimento Mensal FIIs: R$ {rendimento_mensal_fiis:.2f}")


# Reajuste de aporte
anos = 2
taxa_inflacao_anual = 0.04
aporte_mensal = 4000
print(aporte_mensal * (1 + taxa_inflacao_anual)**anos)
