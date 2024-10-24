import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Definir variáveis fuzzy (Entrada e Saída)
qualidade_refeicao = ctrl.Antecedent(np.arange(0, 11, 1), 'qualidade_refeicao')
qualidade_servico = ctrl.Antecedent(np.arange(0, 11, 1), 'qualidade_servico')
tempo_atendimento = ctrl.Antecedent(np.arange(0, 11, 1), 'tempo_atendimento')
gorjeta = ctrl.Consequent(np.arange(0, 26, 1), 'gorjeta')

# Definir funções de pertinência com menos linhas
qualidade_refeicao.automf(3)  # 'poor', 'average', 'good'
qualidade_servico.automf(3)   # 'poor', 'average', 'good'
tempo_atendimento['demorado'] = fuzz.trimf(tempo_atendimento.universe, [0, 0, 5])
tempo_atendimento['mediano'] = fuzz.trimf(tempo_atendimento.universe, [0, 5, 10])
tempo_atendimento['rapido'] = fuzz.trimf(tempo_atendimento.universe, [5, 10, 10])

gorjeta['pouca'] = fuzz.trimf(gorjeta.universe, [0, 0, 10])
gorjeta['media'] = fuzz.trimf(gorjeta.universe, [0, 10, 25])
gorjeta['generosa'] = fuzz.trimf(gorjeta.universe, [10, 25, 25])

# Definir regras fuzzy
rule1 = ctrl.Rule(qualidade_refeicao['poor'] & qualidade_servico['poor'], gorjeta['pouca'])
rule2 = ctrl.Rule(qualidade_refeicao['good'] & qualidade_servico['good'], gorjeta['generosa'])
rule3 = ctrl.Rule(tempo_atendimento['demorado'], gorjeta['pouca'])
rule4 = ctrl.Rule(tempo_atendimento['mediano'] | tempo_atendimento['rapido'], gorjeta['media'])

# Criar o sistema de controle
sistema_controle = ctrl.ControlSystem([rule1, rule2, rule3, rule4])
simulacao = ctrl.ControlSystemSimulation(sistema_controle)

# Inserir valores de entrada (exemplo)
simulacao.input['qualidade_refeicao'] = 7.5
simulacao.input['qualidade_servico'] = 8.0
simulacao.input['tempo_atendimento'] = 6.0

# Executar a simulação
simulacao.compute()

# Mostrar o resultado
print(f"Percentual de gorjeta: {simulacao.output['gorjeta']:.2f}%")
