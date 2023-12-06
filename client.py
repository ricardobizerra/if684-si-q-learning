#Aqui vocês irão colocar seu algoritmo de aprendizado

import connection as con

cn = con.connect(2037)

act = ['jump','left','right']

while True:
    estado, recompensa = con.get_state_reward(cn,act[0])
    print(f'Estado: {estado} | Recompensa: {recompensa}')

    plataforma, direcao = int(estado[:7],2), int(estado[7:],2)
    print(f'Plataforma: {plataforma} | Direção: {direcao}')