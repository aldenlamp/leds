import sys
import math



class Gradient:
    """ Creates a gradients from colors and a function

    The gradient generation can be thought of a as a graph where the x-axis
    goes from 0.0 to 1.0 and the y-axis is the linearly interpolated colors 
    going from 0.0 to 2.0. There is some function on that graph  that maps
    [0.0, 1.0] -> [0.0, 1.0]. When getting a color, the generator goes through
    the function to find the correct color. It also allows a step function to
    rotate the colors along the y axis.

    Attributes:
        func_type: Determines the function to distribute the gradient
        colors: a list of colors for the gradient
        color_positions: the position of the colors on the y-axis
        func_domain: the domain of the function before getting scaled
        func_range: the range of the function beforet getting scaled
        APPROXIMATE_STEP: The step used to find the function_range
    """

    APPROXIMATE_STEP = 0.01

    def __init__(self, colors=None, color_positions=None, 
                 func_domain=(0, 1), func_type=0):
        """Inits the color class

        This will set all the variables in the class along with calculating
         the function_domain

        Args:
            colors: A list of colors to use for the gradient 
              defaults to black and white
            color_positions: A list from 0 to 1 representing the space between
              colors of a gradient. Defaults to equadistant
            func_domain: The domain to use of the given gradient function
            func_type: The function to use for the gradient
        """

        if colors is None:
            colors = [(0, 0, 0,), (255, 255, 255)]
        self.colors = colors
        
        if color_positions is None:  
            self.color_positions = []
            divDist = 2.0 / len(colors)
            for div in range(len(colors)):
                self.color_positions.append(div * divDist)
        else:
            self.color_positions = color_positions
    
        self.func_type = func_type
        self.func_domain = func_domain
        self.func_range = self.approximate_func_range()


    def get_color_at(self, position):
        """Gets the color at the given position

        Given a position, this will do a linear interpolation of the two
        closest colors using the color_positions. It will find the 
        correct color in between those two colors

        Args:
            position: the position of the color from 0 to 1
        
        Returns:
            The color tuple representing that position on the gradient
        """

        if len(self.colors) == 1:
            return self.colors[0]
        
        if position > 1:
            position = 1
        
        if position < 0:
            position = 0
        
        color_pos = self.scaled_line_func(position)

        color_dist = -1.0
        dist_from_left = 0.0

        lower = (0, 0, 0)
        upper = (0, 0, 0)

        if color_pos < self.color_positions[0] or \
           color_pos > self.color_positions[-1]:

            color_dist = 2 - self.color_positions[-1] + self.color_positions[0]
            lower = self.colors[-1]
            upper = self.colors[0]
            
            if color_pos < self.color_positions[0]:
                dist_from_left = 2 - self.color_positions[-1] + color_pos
            else:
                dist_from_left = color_pos - self.color_positions[-1]

        else:
            for i in range(len(self.color_positions) - 1):
                if self.color_positions[i] == color_pos: return self.colors[i]

                if self.color_positions[i] < color_pos and \
                   self.color_positions[i + 1] > color_pos:
                    lower = self.colors[i]
                    upper = self.colors[i + 1]

                    color_dist = self.color_positions[i + 1] - \
                                 self.color_positions[i]
                    dist_from_left = color_pos - self.color_positions[i]
                    break

        if color_dist == -1.0: return
        
        upper_prop = dist_from_left / color_dist
        lower_prop = 1 - upper_prop

        red = lower[0] * lower_prop + upper[0] * upper_prop        
        blue = lower[1] * lower_prop + upper[1] * upper_prop
        green = lower[2] * lower_prop + upper[2] * upper_prop

        return (int(red), int(blue), int(green))

    def step(self, amount): 
        """Rotates the color positions

        All the color positions increase by the given amount. When a color
        goes over 2, it gets moved to the front to make the gradient act as a 
        circle. 

        Args:
            amount: the amount to rotate the gradient positions by
        """

        for i in range(len(self.color_positions)):
            self.color_positions[i] += amount
        
        while self.color_positions[-1] >= 2:
            self.colors.insert(0, self.colors[-1])
            self.colors = self.colors[:-1]
            self.color_positions.insert(0, self.color_positions[-1] - 2)
            self.color_positions = self.color_positions[:-1]

        while self.color_positions[0] < 0:
            self.colors.append(self.colors[0])
            self.colors = self.colors[1:]
            self.color_positions.append(self.color_positions[0] + 2)
            self.color_positions = self.color_positions[1:]
        

    def scaled_line_func(self, x):
        """Gets the scaled function value
        
        This maps the function domain and range to 0 to 1. Given any input 
        within 0 to 1, it will map that to the function domain, call the
        function, then map the output to be between 0 and 1 again

        Args:
            x: a number between 0 to 1 representing the function call
        
        Returns:
            A number between 0 to 1 representing the scaled output of the func
        """ 

        scaled_in = x * (self.func_domain[1] - self.func_domain[0]) + \
                    self.func_domain[0]
        out = self.line_func(scaled_in)
        scaled_out = (out - self.func_range[0]) / \
                     (self.func_range[1] - self.func_range[0])
        return scaled_out

    def line_func(self, x):
        """Calls a mathematical function

        This calls a mathematical function depending on what the value of 
        func_type is. 

        Args:
            x: the mathematical function input

        Returns:
            The output of the mathematical function
        """
        # Line
        if self.func_type == 0:
            return x

        # Square
        if self.func_type == 1:
            return x * x

        # Sine
        if self.func_type == 2:
            return math.sin(x)

        # Cosine
        if self.func_type == 3:
            return math.cos(x)

        # Quad
        if self.func_type == 4:
            return x * x * x * x
        
        # Sqrt
        if self.func_type == 5:
            return x ** 0.5


    def approximate_func_range(self):
        """Approximates the range of the function given the domain

        This steps through func_domain using APPROXIMATE_STEP to fund the max
        and min values of the function.

        Returns:
            A tuple representing the function range on that func_domain 
        """
        max_val = sys.float_info.min
        min_val = sys.float_info.max
        i = float(self.func_domain[0])
        while i < float(self.func_domain[1]):
            val = self.line_func(i)
            if val < min_val:
                min_val = val
            
            if val > max_val:
                max_val = val
            
            i += Gradient.APPROXIMATE_STEP

        return (min_val, max_val)


