class Naive(object):
    def update(self, gameinfo):
        #If there is an active fleet, do not move.
        if gameinfo.my_fleets:
            return
        #If there are planets left both on and off my side...
        if gameinfo.my_planets and gameinfo.not_my_planets:
            #...then choose my planet with the largest fleet as the source.
            big_planet = max(gameinfo.my_planets.values(), key = lambda p: p.num_ships)
            ship_mult = 1
            #Find the enemy planet with the largest fleet that is smaller than my source's fleet.
            destlist = list(gameinfo.not_my_planets.values())
            trunc_destlist = destlist
            remove_these = []
            for enplanet in trunc_destlist:
                if enplanet.num_ships > big_planet.num_ships:
                    remove_these.append(enplanet)
            for remo in remove_these:
                if remo in trunc_destlist:
                    trunc_destlist.remove(remo)
            if len(trunc_destlist) > 0:
                dest = trunc_destlist[0]
                for planet in trunc_destlist:
                    if planet.num_ships > dest.num_ships:
                        dest = planet
            else:
                fleet_size = 0
                for my_planet in gameinfo.my_planets:
                    fleet_size += my_planet.num_ships
                trunc_destlist = destlist
                remove_these = []
                for enplanet in trunc_destlist:
                    if enplanet.num_ships > fleet_size:
                        remove_these.append(enplanet)
                for remo in remove_these:
                    if remo in trunc_destlist:
                        trunc_destlist.remove(remo)
                if len(trunc_destlist) > 0:
                    dest = trunc_destlist[0]
                    for planet in trunc_destlist:
                        if planet.num_ships > dest.num_ships:
                            dest = planet
                else:
                    dest = min(gameinfo.not_my_planets.values(), key = lambda p: p.num_ships)
            sources = []
            src_ships = []
            atk_fleet_size = 0
            for my_planet in gameinfo.my_planets.values():
                if atk_fleet_size < int(1.1 * dest.num_ships):
                    sources.append(my_planet)
                    left_over = my_planet.num_ships
                    planet_fleet = 0
                    while ((atk_fleet_size < int(1.1 * dest.num_ships)) and (left_over > 1)):
                        left_over -= 1
                        planet_fleet += 1
                    src_ships.append(planet_fleet)
            for planet_num in range(len(sources)):
                gameinfo.planet_order(sources[planet_num], dest, src_ships[planet_num])
