#!/usr/bin/python
# -*- coding: utf-8 -*-

import random, sys
import interface

class MkmusBot(interface.Bot):
    """Bot que juega aleatoriamente."""
    NAME = "MkmusBot"

    def play(self, state):
        """Jugar: llamado cada turno.
        Debe devolver una acción (jugada)."""
        cx, cy = state["position"]
        #calcular el cuadrante
        size_y = len(self.map)
        size_x = len(self.map[0])
        cota_x = size_x/2
        cota_y = size_y/2
	faros_por_cuadrante = [0,0,0,0]
	mejor_cuadrante = 0

        #calcular cuadrante con mas faros


        lighthouses = dict((tuple(lh["position"]), lh)
                            for lh in state["lighthouses"])
              
        #for dest in self.lighthouses:
        for dest in state["lighthouses"]:
            (faro_x, faro_y) = dest["position"]
            if ((faro_x<=cota_x) and (faro_y<=cota_y)):
                faros_por_cuadrante+=[1,0,0,0]
            if ((faro_x>cota_x) and (faro_y<=cota_y)):
                faros_por_cuadrante+=[0,1,0,0]
            if ((faro_x<=cota_x) and (faro_y>cota_y)):
                faros_por_cuadrante+=[0,0,1,0]
            if ((faro_x>cota_x) and (faro_y>cota_y)):
                faros_por_cuadrante+=[0,0,0,1]                 
        for indice in [1,2,3]:
             if (faros_por_cuadrante[mejor_cuadrante]<faros_por_cuadrante[indice]): 
                     mejor_cuadrante=indice
        posible_x = 0
	posible_y = 0
	cuadrante_bot = 0
	if ((cx<=cota_x) and (cy<=cota_y)):
		cuadrante_bot = 0
	if ((faro_x>cota_x) and (faro_y<=cota_y)):
		cuadrante_bot = 1
	if ((faro_x<=cota_x) and (faro_y>cota_y)):
		cuadrante_bot = 2
	if ((faro_x>cota_x) and (faro_y>cota_y)):
		cuadrante_bot = 3

	# Si estamos en un faro...
        if (cx, cy) in self.lighthouses:
            # Probabilidad 60%: conectar con faro remoto válido
            if lighthouses[(cx, cy)]["owner"] == self.player_num:
                if random.randrange(100) < 50:
                    possible_connections = []
                    for dest in self.lighthouses:
                        # No conectar con sigo mismo
                        # No conectar si no tenemos la clave
                        # No conectar si ya existe la conexión
                        # No conectar si no controlamos el destino
                        # Nota: no comprobamos si la conexión se cruza.
                        if (dest != (cx, cy) and
                            lighthouses[dest]["have_key"] and
                            [cx, cy] not in lighthouses[dest]["connections"] and
                            lighthouses[dest]["owner"] == self.player_num):
                            possible_connections.append(dest)

                    if possible_connections:
                        return self.connect(random.choice(possible_connections))

            # Probabilidad 60%: recargar el faro
            if random.randrange(100) < 55:
                energy = random.randrange(state["energy"] + 1)
                return self.attack(energy)

        # Mover aleatoriamente
        moves = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))
        # Determinar movimientos válidos
        moves = [(x,y) for x,y in moves if self.map[cy+y][cx+x]]
        move = random.choice(moves)
        return self.move(*move)

if __name__ == "__main__":
    iface = interface.Interface(MkmusBot)
    iface.run()
