#Aqui vocês irão colocar seu algoritmo de aprendizado

import connection as con
import random as rd

cn = con.connect(2037)

#COMO ESTÁ SENDO SALVO NO ARQUIVO TXT
#linhas n até n + 3 são plataforma n norte, leste, sul e oeste respectivamente 

#Função para recuperar o progresso da q_table
def recover_table(table):
    with open("resultado.txt", "r") as file:
        text = file.readlines()
        
    for n in range(96):
        line = text[n].split(" ")
        for m in range(3):
            table[n][m] = float(line[m])

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
        
#função responsável por atualizar a tabela, sendo x e y as cordenadas na matriz
def q_update(q_table, x, y, reward, alfa, gama, max):
    q_table[x][y] = (1 - alfa) * q_table[x][y] + (alfa * (reward + (gama * max)))

q_table = []
init_table(q_table)        

alfa = 0.25 # Taxa de aprendizagem
gama = 0.50 # Taxa de desconto

act = ['jump','left','right']

recover_table(q_table)
repeat = 0
while repeat < 1000:
    estado, recompensa = con.get_state_reward(cn, rd.choice(act))
    print(f'Estado: {estado} | Recompensa: {recompensa}')

    plataforma, direcao = int(estado[:7],2), int(estado[7:],2)
    print(f'Plataforma: {plataforma} | Direção: {direcao}')
    
    repeat += 1
    
    
#salva os resultados atuais    
with open("resultado.txt", "w") as file:
    text = ""
    
    for n in range(96):
        for m in range(3):
            if m < 2:
                text = f"{text}{q_table[n][m]} "
            else:
                text = f"{text}{q_table[n][m]}\n"
    
    file.write(text)
