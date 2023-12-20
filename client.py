#Aqui vocês irão colocar seu algoritmo de aprendizado

import connection as con
import random as rd
import numpy as np

cn = con.connect(2037)

#COMO ESTÁ SENDO SALVO NO ARQUIVO TXT
#linhas n até n + 3 são plataforma n norte, leste, sul e oeste respectivamente 

#Função para recuperar o progresso da q_table
def recover_table(table):
    #table = []
    with open("resultado.txt", "r") as file:
        text = file.readlines()
        
    for n in range(96):
        line = text[n].split(" ")
        for m in range(3):
            table[n][m] = float(line[m])
        
    #return table

#função para iniciar a q table com 96 espaços para os estados, cada um com 3 comandos possíveis
def init_table(table):
    for n in range(96):
        pos = []
        for m in range(3):
            pos.append(0)
        table.append(pos)
        
#caso necessário uma função para voltarmos ao estado inicial
def reset_table():
    
    with open("resultado.txt", "w") as file:
        text = ""
        for n in range(96):
            text = f"{text}0.000000 0.000000 0.000000\n"
            
        file.write(text)
        
def save_table(table):
    with open("resultado.txt", "w") as file:
        text = ""
        
        for n in range(96):
            for m in range(3):
                if m < 2:
                    text = f"{text}{table[n][m]} "
                else:
                    text = f"{text}{table[n][m]}\n"
        
        file.write(text)
        
#função responsável por atualizar a tabela, sendo x e y as cordenadas na matriz
def q_update(value, alfa, gama, reward, maximum):
    return (1 - alfa) * value + (alfa * (reward + (gama * maximum)))
    

#reset_table()
q_table = []
init_table(q_table)
recover_table(q_table)


alfa = 0.1 # Taxa de aprendizagem
gama = 0.9 # Taxa de desconto
epsilon = 0 # Epsilon value for epsilon-greedy policy

act = ['jump','left','right']

plataforma  = 0
estado_atual = 0

i = 0
while i < 1000:
    print('==============================')
    
    #colocar alfa como o valor padrão e randomizar epsilon nos primeiros testes
    alfa = 0.25
    
    
    # Epsilon-greedy policy
    n_atual = rd.random()
    if n_atual < epsilon:
        action = rd.randint(0, 2)  # Exploration
    else:
        action = 0
        val = 0
        for n in range(3):
            if n == 0:
                val = q_table[estado_atual][n]
            elif q_table[estado_atual][n] > val:
                val = q_table[estado_atual][n]
                action = n
        # Exploitation

    estado, recompensa = con.get_state_reward(cn, act[action])
    print(f'Estado: {estado} | Recompensa: {recompensa}')
    #print(f'criterio:{n_atual} | ação: {action}')
    
    if recompensa < -100:
        alfa = 0.05
    #else:
    #    epsilon *= 0.95
        
    plataforma, direcao = int(estado[2:7],2), int(estado[7:9],2)
    print(f'Plataforma: {plataforma} | direcao: {direcao}')
    estado_int = (plataforma * 4) + (direcao % 4)
    
    max_q_value = max(q_table[estado_int])
    current_q = q_update(q_table[estado_atual][action], alfa, gama, recompensa, max_q_value)   
        
    if (0 <= estado_int <= 300):
        pass
     
    q_table[estado_atual][action] = current_q
    save_table(q_table)
            
    estado_atual = estado_int
    
    #aumenta 1 no contador do loop principal
    i += 1

    
#salva os resultados atuais    
save_table(q_table)
    
