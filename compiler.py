class Compiler(object):
    def __init__(self, instructions):
        super().__init__()

        self.instructions = instructions

        for instr in self.instructions:
            if instr.type == 'transition':
                self.start_config = self.generate_drone_takeoff_position(instr.transition)
                break

        if self.start_config is None:
            raise Exception('No transitions found.')

        flying_dirs = self.resolve_instr_table()
        self.udp_commands = self.directions_to_udp(flying_dirs)

    def generate_drone_takeoff_position(self, transition):
        return {drone[0]: [idx + 1, 1] for idx, drone in enumerate(transition)}

    def generate_dictionary(self, transition_list):
        return {drone[0]: list(drone[1:]) for drone in transition_list}

    def resolve_instr_table(self):
        flying_instrcutions = []

        for instr in self.instructions:
            if instr.type == 'takeOff':
                flying_instrcutions.append('takeoff')
            if instr.type == 'land':
                flying_instrcutions.append('land')
            if instr.type == 'wait':
                flying_instrcutions.append('command')
            if instr.type == 'transition':
                transition_dict = self.generate_dictionary(instr.transition)
                self.collision_detection(self.start_config, transition_dict)
                movement_offset = self.calculate_movement_offset(self.start_config, transition_dict)
                movement_queue = self.generate_movement_queue(movement_offset)
                flying_instrcutions.append(movement_queue)
                # self.start_config = transition_dict
        return flying_instrcutions

    def calculate_movement_offset(self, start, finish):
        movement_queue = []
        for drone in start:

            start_pos = start[drone]
            possition = finish[drone]

            move_x = possition[0] - start_pos[0]
            move_y = possition[1] - start_pos[1]
            movement_queue.append([move_x, move_y])

        return movement_queue

    def generate_movement_queue(self, movement_offset):
        individual_movement = []
        for drone in movement_offset:
            x, y = drone

            temp = []
            while x != 0:
                if x > 0:
                    temp.append('right 100')
                    x -= 1
                else:
                    temp.append('left 100')
                    x += 1

            while y != 0:
                if y > 0:
                    temp.append('back 100')
                    y  -= 1
                else:
                    temp.append('forward 100')
                    y += 1
            individual_movement.append(temp)
        return individual_movement

    def directions_to_udp(self, dirs):
        udp_instr  = []

        for idx, drone in enumerate(self.start_config):
            temp = []
            for drone_dir in dirs:
                if isinstance(drone_dir, str):
                    temp.append(self.convert_to_ascii(drone_dir))
                else:
                    for dir in drone_dir[idx]:
                        temp.append(self.convert_to_ascii(dir))
            udp_instr.append(temp)

        return udp_instr

    def convert_to_ascii(self,command):
        return [format(ord(c), 'x') for c in command]

    def collision_detection(self, start, finish):
        for loc in finish:
            if any(sloc == finish[loc] for sloc in list(start.values())):
                raise Exception('Drone collision detected.')