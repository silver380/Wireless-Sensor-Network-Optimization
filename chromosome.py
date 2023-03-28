import random

class Chromosome:
    def __init_(self, map_size, mut_prob, recomb_prob, max_BW):
        # List of sensors: [x, y, BW]
        self.sensors = []
        # Indicates each neighborhood is connected to which sensor
        self.adj_id = [[-1] for i in range(map_size) for j in range(map_size)]
        self.mut_prob = mut_prob
        self.recomb_prob = recomb_prob
        self.max_BW = max_BW
        self.map_size = map_size
    
    def mut_append(self):
        append_prob = random.uniform(0,1)
        if append_prob <= self.mut_prob:
            x = min(random.ranint(0,19) + random.random(),19)
            y = min(random.randint(0,19) + random.random(),19)
            bw = random.randint(0,self.max_BW) + random.random()
            self.sensors.append([x,y,bw])
            
    def mut_relocation(self):
        for i in range(self.map_size):
            for j in range(self.map_size):
                reloaction_prob = random.uniform(0,1)
                if reloaction_prob <= self.mut_prob:
                    self.adj_id[i][j] = random.randint(0,len(self.sensors)-1)


    def mut_power(self):
        for sensor_id in range(len(self.sensors)):
            add_power_prob = random.uniform(0,1)
            if add_power_prob <= self.mut_prob:
                # TODO: test gussian, ...
                new_power = random.randint(0, self.max_BW) + random.random()
                self.sensors[sensor_id][2] = new_power


    def mut_pop(self):
        pop_prob = random.uniform(0,1)
        if pop_prob <= self.mut_append and len(self.sensors) > 0:
            self.sensors.pop()

    def mutation(self):
        self.mut_append()
        self.mut_relocation()
        self.mut_power()
        self.mut_pop()
