from tanks import TankController, MOVE_FORWARD, MOVE_BACKWARD, TURN_LEFT, TURN_RIGHT, SHOOT, TANK_SIZE, GameState, Tank, normalize_angle, INITIAL_TANK_HEALTH, TREE_RADIUS
from math import degrees, atan2, sqrt
import random


class CPUTankController(TankController):
    def __init__(self, tank_id: str):
        self.tank_id = tank_id

    @property
    def id(self) -> str:
        return "Sinai-D"

    def find_closest_enemy_tank(self, gameState: GameState) -> Tank:
        my_tank = next(tank for tank in gameState.tanks if tank.id == self.id)
        alive_enemy_tanks = [
            tank for tank in gameState.tanks if tank.id != self.id and tank.health > 0]

        min_distance = float('inf')
        closest_enemy = None
        for enemy_tank in alive_enemy_tanks:
            dx = enemy_tank.position[0] - my_tank.position[0]
            dy = enemy_tank.position[1] - my_tank.position[1]
            distance = sqrt(dx * dx + dy * dy)
            if distance < min_distance:
                min_distance = distance
                closest_enemy = enemy_tank

        return closest_enemy

    def find_weakest_enemy_tank(self, gameState: GameState) -> Tank:
        my_tank = next(tank for tank in gameState.tanks if tank.id == self.id)
        alive_enemy_tanks = [
            tank for tank in gameState.tanks if tank.id != self.id and tank.health > 0]

        # Find the tank with the lowest health
        lowest_health_enemy_tank = min(
            alive_enemy_tanks, key=lambda tank: tank.health)

        return lowest_health_enemy_tank

    def find_strongest_enemy_tank(self, gameState: GameState) -> Tank:
        my_tank = next(tank for tank in gameState.tanks if tank.id == self.id)
        alive_enemy_tanks = [
            tank for tank in gameState.tanks if tank.id != self.id and tank.health > 0]

        highest_health_enemy_tank = max(
            alive_enemy_tanks, key=lambda tank: tank.health)
        return highest_health_enemy_tank

    def is_tree_in_path(self, p1, p2, trees):
        # Loop over all trees
        for tree in trees:
            # Calculate the coefficients for the line equation ax + by = c
            # This line passes through points p1 and p2
            a = p2[1] - p1[1]
            b = p1[0] - p2[0]
            c = a*p1[0] + b*p1[1]

            # Calculate the distance from the center of the tree to the line
            tree_center_to_line_distance = abs(
                a*tree.position[0] + b*tree.position[1] - c) / sqrt(a*a + b*b)

            # If the distance is less than the tree's size (radius), then the line intersects the tree
            if tree_center_to_line_distance < TREE_RADIUS:
                return True
        # If no tree was found to intersect the path, return False
        return False

    def decide_what_to_do_next(self, gameState: GameState) -> str:
        my_tank = next(tank for tank in gameState.tanks if tank.id == self.id)
        enemy_tank = self.find_strongest_enemy_tank(gameState)

        dx = enemy_tank.position[0] - my_tank.position[0]
        dy = enemy_tank.position[1] - my_tank.position[1]

        distance = sqrt(dx * dx + dy * dy)
        desired_angle = normalize_angle(degrees(atan2(-dy, dx)))
        angle_diff = my_tank.angle - desired_angle

        if (my_tank.health < INITIAL_TANK_HEALTH/2):
            if random.random() < 0.7:
                return MOVE_BACKWARD
            if random.random() < 0.2:
                return TURN_RIGHT

        if (random.random() < 0.2):
            return SHOOT

        if abs(angle_diff) > 3:
            return TURN_LEFT if angle_diff < 0 else TURN_RIGHT
        elif distance < max(TANK_SIZE) * 5:
            if not self.is_tree_in_path(my_tank.position, enemy_tank.position, gameState.trees):
                return SHOOT
            else:
                # Decide what to do if there's a tree in the way
                return TURN_RIGHT
        else:
            return MOVE_FORWARD
