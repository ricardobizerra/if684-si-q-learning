#Aqui vocês irão colocar seu algoritmo de aprendizado

import connection as con
import random as rd
import numpy as np

cn = con.connect(2037)

#COMO ESTÁ SENDO SALVO NO ARQUIVO TXT
#linhas n até n + 3 são plataforma n norte, leste, sul e oeste respectivamente 

#Função para recuperar o progresso da q_table
def recover_table():
    table = []
    with open("resultado.txt", "r") as file:
        text = file.readlines()
        
    for n in range(96):
        line = text[n].split(" ")
        pos = [float(val) for val in line]
        table.append(pos)
        
    return table

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
def q_update(q_table, x, y, reward, alfa, gama, max):
    if x < len(q_table) and y < len(q_table[x]): q_table[x][y] = (1 - alfa) * q_table[x][y] + (alfa * (reward + (gama * max)))

q_table = recover_table()
#reset_table()

alfa = 0.25 # Taxa de aprendizagem
gama = 0.50 # Taxa de desconto
epsilon = 0.1 # Epsilon value for epsilon-greedy policy

act = ['jump','left','right']

plataforma  = 0

i = 0
while i < 1000:
    print('==============================')
    
    #colocar alfa como o valor padrão e randomizar epsilon nos primeiros testes
    alfa = 0.25
    if i < 50:
        epsilon = rd.random()
    else:
        epsilon = 0.1
    
    # Epsilon-greedy policy
    if rd.random() < epsilon:
        action = rd.choice(act)  # Exploration
    else:
        action = act[np.argmax(q_table[plataforma])]  # Exploitation
    
    estado, recompensa = con.get_state_reward(cn, action)
    print(f'Estado: {estado} | Recompensa: {recompensa}')

    if recompensa < -100:
        alfa = 0.05
        
    plataforma, direcao = int(estado[:7],2), int(estado[7:],2)
    estado = (plataforma * 4) + (direcao % 4)
    
    max_q_value = max(q_table[plataforma])
    q_update(q_table, plataforma, direcao, recompensa, alfa, gama, max_q_value)   
        
    #salva os resultados atuais    
    save_table(q_table)
    
    #aumenta 1 no contador do loop principal
    i += 1
