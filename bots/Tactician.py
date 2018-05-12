class Tactician(object):
    def __init__(self):
        self.notable_enemy_planets = [None, None, None, None, None, None]
        self.notable_neutral_planets = [None, None, None, None, None, None]

    def tact_calculate(self, gameinfo):
        self.notable_enemy_planets = [None, None, None, None, None, None]
        self.notable_neutral_planets = [None, None, None, None, None, None]
        if len(gameinfo.enemy_planets) > 0:
            self.notable_enemy_planets[0] = min(gameinfo.enemy_planets.values(), key = lambda p: p.num_ships)
            self.notable_enemy_planets[1] = max(gameinfo.enemy_planets.values(), key = lambda p: p.num_ships)
            short_dist = 500000
            short_planet = None
            long_dist = 0
            long_planet = None
            for enplanet in gameinfo.enemy_planets.values():
                if enplanet.distance_to(self.biggest_planet) < short_dist:
                    short_dist = enplanet.distance_to(self.biggest_planet)
                    short_planet = enplanet
                if enplanet.distance_to(self.biggest_planet) > long_dist:
                    long_dist = enplanet.distance_to(self.biggest_planet)
                    long_planet = enplanet
            self.notable_enemy_planets[2] = short_planet
            self.notable_enemy_planets[3] = long_planet
            self.notable_enemy_planets[4] = min(gameinfo.enemy_planets.values(), key = lambda p: p.growth_rate)
            self.notable_enemy_planets[5] = max(gameinfo.enemy_planets.values(), key = lambda p: p.growth_rate)
        self.notable_neutral_planets[0] = min(gameinfo.neutral_planets.values(), key = lambda p: p.num_ships)
        self.notable_neutral_planets[1] = max(gameinfo.neutral_planets.values(), key = lambda p: p.num_ships)
        short_dist = 500000
        short_planet = None
        long_dist = 0
        long_planet = None
        for enplanet in gameinfo.neutral_planets.values():
            if enplanet.distance_to(self.biggest_planet) < short_dist:
                short_dist = enplanet.distance_to(self.biggest_planet)
                short_planet = enplanet
            elif enplanet.distance_to(self.biggest_planet) > long_dist:
                long_dist = enplanet.distance_to(self.biggest_planet)
                long_planet = enplanet
        self.notable_neutral_planets[2] = short_planet
        self.notable_neutral_planets[3] = long_planet
        self.notable_neutral_planets[4] = min(gameinfo.neutral_planets.values(), key = lambda p: p.growth_rate)
        self.notable_neutral_planets[5] = max(gameinfo.neutral_planets.values(), key = lambda p: p.growth_rate)

    def fleet_calculate(self, gameinfo, target):
        cur_fleet_size = 0
        planet_mult = 0.5
        planet_num = min(gameinfo.my_planets)
        exclude_strongest_three = True
        attacking_planets = []
        individual_fleets = []
        while cur_fleet_size <= target.num_ships:
            while ((planet_num not in gameinfo.my_planets) and (planet_num < max(gameinfo.my_planets))):
                planet_num += 1
            if planet_num >= max(gameinfo.my_planets):
                cur_fleet_size = 0
                planet_num = min(gameinfo.my_planets)
                attacking_planets = []
                individual_fleets = []
                if ((planet_mult == 0.5) and (exclude_strongest_three)):
                    planet_mult = 0.75
                elif ((planet_mult == 0.75) and (exclude_strongest_three)):
                    planet_mult = 0.9
                elif ((planet_mult == 0.9) and (exclude_strongest_three)):
                    planet_mult = 0.5
                    exclude_strongest_three = False
                elif ((planet_mult == 0.5) and (not exclude_strongest_three)):
                    planet_mult = 0.75
                elif ((planet_mult == 0.75) and (not exclude_strongest_three)):
                    planet_mult = 0.9
                elif ((planet_mult == 0.9) and (not exclude_strongest_three)):
                    planet_mult = 0.99999
                elif planet_mult == 0.99999:
                    planet_mult = 1
                else:
                    for my_planet in gameinfo.my_planets:
                        attacking_planets.append(my_planet)
                        individual_fleets.append(my_planet.num_ships)
                    return attacking_planets, individual_fleets
            if len(gameinfo.my_planets) > 3:
                if exclude_strongest_three:
                    if ((gameinfo.my_planets[planet_num] != self.biggest_planet) and (gameinfo.my_planets[planet_num] != self.second_planet) and (gameinfo.my_planets[planet_num] != self.third_planet)):
                        cur_fleet_size += int(gameinfo.my_planets[planet_num].num_ships * planet_mult)
                        attacking_planets.append(gameinfo.my_planets[planet_num])
                        individual_fleets.append(int(gameinfo.my_planets[planet_num].num_ships * planet_mult))
                else:
                    cur_fleet_size += int(gameinfo.my_planets[planet_num].num_ships * planet_mult)
                    attacking_planets.append(gameinfo.my_planets[planet_num])
                    individual_fleets.append(int(gameinfo.my_planets[planet_num].num_ships * planet_mult))
            else:
                cur_fleet_size += int(gameinfo.my_planets[planet_num].num_ships * planet_mult)
                attacking_planets.append(gameinfo.my_planets[planet_num])
                individual_fleets.append(int(gameinfo.my_planets[planet_num].num_ships * planet_mult))                
            planet_num += 1
        return attacking_planets, individual_fleets
    
    def update(self, gameinfo):
        if gameinfo.my_fleets:
            return
        if gameinfo.my_planets and gameinfo.not_my_planets:
            self.biggest_planet = max(gameinfo.my_planets.values(), key = lambda p: p.num_ships)
            self.second_planet = min(gameinfo.my_planets.values(), key = lambda p: p.num_ships)
            self.third_planet = min(gameinfo.my_planets.values(), key = lambda p: p.num_ships)
            for my_planet in gameinfo.my_planets.values():
                if ((my_planet.num_ships > self.second_planet.num_ships) and (my_planet.num_ships < self.biggest_planet.num_ships)):
                    self.second_planet = my_planet
            for my_planet in gameinfo.my_planets.values():
                if ((my_planet.num_ships > self.third_planet.num_ships) and (my_planet.num_ships < self.second_planet.num_ships)):
                    self.third_planet = my_planet
            self.tact_calculate(gameinfo)
            if gameinfo.enemy_planets:
                if ((self.notable_enemy_planets[1] != None) and (int(self.biggest_planet.num_ships / 2) >= self.notable_enemy_planets[1].num_ships) and (int(self.biggest_planet.growth_rate * 0.5) <= self.notable_enemy_planets[1].growth_rate)):
                    attacking_planets, ships_per_planet = self.fleet_calculate(gameinfo, self.notable_enemy_planets[1])
                    for atk_planum in range(len(attacking_planets)):
                        gameinfo.planet_order(attacking_planets[atk_planum], self.notable_enemy_planets[1], ships_per_planet[atk_planum])
                else:
                    viable_planets = []
                    planet_scores = []
                    for enplanet in gameinfo.enemy_planets.values():
                        for myplanet in gameinfo.my_planets.values():
                            if ((int(enplanet.num_ships * 1.25) <= myplanet.num_ships) and (enplanet not in viable_planets)):
                                viable_planets.append(enplanet)
                                planet_scores.append(0 - (enplanet.num_ships + enplanet.distance_to(self.biggest_planet)) + enplanet.growth_rate)
                    for vplanum in range(len(viable_planets)):
                        if planet_scores[vplanum] == max(planet_scores):
                            attacking_planets, ships_per_planet = self.fleet_calculate(gameinfo, viable_planets[vplanum])
                            for atk_planum in range(len(attacking_planets)):
                                gameinfo.planet_order(attacking_planets[atk_planum], viable_planets[vplanum], ships_per_planet[atk_planum])
            else:
                total_ships = 0
                for my_planet in gameinfo.my_planets.values():
                    total_ships += my_planet.num_ships
                cur_target = min(gameinfo.neutral_planets.values(), key = lambda p: p.growth_rate)
                for nt_planet in gameinfo.neutral_planets.values():
                    if ((nt_planet.num_ships < total_ships) and (nt_planet.growth_rate > cur_target.growth_rate)):
                        cur_target = nt_planet
                attacking_planets, ships_per_planet = self.fleet_calculate(gameinfo, cur_target)
                for atk_planum in range(len(attacking_planets)):
                    gameinfo.planet_order(attacking_planets[atk_planum], cur_target, ships_per_planet[atk_planum])
            pass
