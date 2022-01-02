import sys
import math
import numpy as np


class Gradient:

    def __init__(self, colors=None, color_positions=None):

        self.colors = colors
        self.color_positions = color_positions

        if self.colors is None:
            self.colors = []
            self.color_positions = []
            
        if self.color_positions is None or len(self.colors) != len(self.color_positions):
            self.color_positions = np.linspace(0, 1, len(self.colors))


        # [[index, (color), position, steps]]
        self.replace_color = []


    def get_insert_index(self, position):
        insert_index = -1

        for i, low, high in enumerate(zip(self.color_positions[:-1], 
                                          self.color_positions[1:])):
            if position > low and position < high:
                insert_index = i
                break

        if not len(self.color_positions):
            insert_index = 0

        if insert_index == -1:
            if position < self.color_positions[0]:
                insert_index = 0
            elif position > self.color_positions[-1]:
                insert_index = len(self.color_positions)
        
        return insert_index


    def insert_color(self, color, position, steps):
        
        new_color = self.get_color_at(position)

        insert_index = self.get_insert_index(position)

        self.colors.insert(insert_index, new_color)
        self.color_positions.insert(insert_index, position)

        for update in self.replace_color:
            if update[0] >= insert_index:
                update[0] += 1

        self.replace_color.append([insert_index, color, position, steps])


    def closest_index(self, position):
        
        smallest_diff = 1
        smallest_index = -1

        for i, pos in enumerate(self.color_positions):
            dist = abs(pos - position)
            if dist < smallest_diff:
                smallest_diff = dist
                smallest_index = i

        return smallest_index


    def replace_color(self, color, position, steps, index=None):

        if index is None:
            index = self.closest_index(position)
        
        if index == -1:
            return

        self.replace_color.append([index, color, position, steps])


    def interpolate(self, a, b, prop):
        return a + ((b - a) * prop)

    def udpate_colors(self):

        self.replace_color = [i for i in self.replace_color if i[3] != 1]
        
        for i, update in enumerate(self.replace_color):

            prop = 1.0 / update[3]

            new_position = interpolate(self.color_positions[update[0]], 
                                       update[2], prop)

            old_color = self.colors[update[0]]

            r = interpolate(update[1][0], old_color[0], prop)
            b = interpolate(update[1][1], old_color[1], prop)
            g = interpolate(update[1][2], old_color[2], prop)

            self.colors[update[0]] = (int(r), int(b), int(g))

            self.color_positions = new_position

            update[3] -= 1


    def get_color_at(self, position, brightness=1):

        if not self.colors:
            return (0, 0, 0)

        if len(self.colors) == 1:
            return self.colors[0]
        
        if position > 1:
            position = 0.99
        
        if position < 0:
            position = 0

        between_index = self.get_insert_index(position)

        lower = self.colors[between_index - 1]
        upper = self.colors[between_index]

        lower_pos = self.color_positions[between_index - 1]
        upper_pos = self.color_positions[between_index if between_index < len(self.color_positions) else 0]

        if between_index == 0:
            lower_pos -= 1

        if between_index == len(self.color_positions):
            lower_pos -= 1
            position -= 1
        
        upper_prop = (position - lower_pos) / (upper_pos - lower_pos)
        lower_prop = 1 - upper_prop

        red = lower[0] * lower_prop + upper[0] * upper_prop        
        blue = lower[1] * lower_prop + upper[1] * upper_prop
        green = lower[2] * lower_prop + upper[2] * upper_prop
        
        red *= brightness
        blue *= brightness
        green *= brightness
        
        if red > 255: red = 255
        if blue > 255: blue = 255
        if green > 255: green = 255

        return (int(red) , int(blue), int(green))
