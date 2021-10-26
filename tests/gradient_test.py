import unittest

import sys
sys.path.append("/home/pi/leds")

import gradient as gd

class TestGradientInit(unittest.TestCase):

    def test_init(self):
        grad = gd.Gradient()
        self.assertEqual(grad.colors, [(0,0,0), (255, 255, 255)])
        self.assertEqual(grad.func_type, 0)
        self.assertEqual(grad.color_positions, [0, 1])
        self.assertEqual(grad.func_domain, (0, 1))
        self.assertTrue(abs(grad.func_range[0]) < 0.01)
        self.assertTrue(abs(grad.func_range[1] - 1) < 0.01)
    
    def test_init_colors(self):
        grad = gd.Gradient(colors=[(255, 0, 0), (0, 255, 0), (0, 0, 255)], color_positions=[0, 1, 1.5], func_type=1, func_domain=(-1, 2))
        self.assertEqual(grad.colors, [(255, 0, 0), (0, 255, 0), (0, 0, 255)])
        self.assertEqual(grad.func_type, 1)
        self.assertEqual(grad.color_positions, [0, 1, 1.5])
        self.assertEqual(grad.func_domain, (-1, 2))
        self.assertTrue(abs(grad.func_range[0]) < 0.1)
        self.assertTrue(abs(grad.func_range[1] - 4) < 0.1)

        grad2 = gd.Gradient(colors=[(255, 0, 0), (0, 255, 0), (0, 0, 255), (100, 100, 100)])
        self.assertEqual(grad2.color_positions, [0, 0.5, 1, 1.5])

    def test_scaled_line_func(self):
        grad = gd.Gradient(func_type=0, func_domain=(0, 1))
        self.assertTrue(abs(grad.scaled_line_func(0)) < 0.1)
        self.assertTrue(abs(grad.scaled_line_func(1) - 1) < 0.1)
        self.assertTrue(abs(grad.scaled_line_func(0.5) - 0.5) < 0.1)

        grad = gd.Gradient(func_type=1, func_domain=(0, 4))
        self.assertTrue(abs(grad.scaled_line_func(0)) < 0.1)
        self.assertTrue(abs(grad.scaled_line_func(1) - 1) < 0.1)
        self.assertTrue(abs(grad.scaled_line_func(0.5) - 0.25) < 0.1)

    def test_get_color(self):
        grad = gd.Gradient(colors=[(255, 0, 0), (0, 255, 0), (0, 0, 255)])
        
        red = grad.get_color_at(0)
        self.assertTrue(abs(red[0] - 255) < 0.1)
        self.assertTrue(abs(red[1]) < 0.1)
        self.assertTrue(abs(red[2]) < 0.1)

        blue = grad.get_color_at(2/3)
        self.assertTrue(abs(blue[0]) < 5)
        self.assertTrue(abs(blue[1] - 255) < 5)
        self.assertTrue(abs(blue[2]) < 5)

        middle = grad.get_color_at(1/3)
        self.assertTrue(abs(middle[0] - (255/2)) < 5)
        self.assertTrue(abs(middle[1] - (255/2)) < 5)
        self.assertTrue(abs(middle[2]) < 5)

        grad2 = gd.Gradient(colors=[(255, 0, 0), (0, 0, 255)], color_positions=[0.5, 1.5])
        middle2 = grad2.get_color_at(0)
        self.assertTrue(abs(middle2[0] - (255/2)) < 5)
        self.assertTrue(abs(middle2[1]) < 5)
        self.assertTrue(abs(middle2[2] - (255/2)) < 5)


    def test_step(self):
        grad = gd.Gradient(colors=[(255, 0, 0), (0, 255, 0), (0, 0, 255)])
        
        self.assertTrue(abs(grad.color_positions[0] - 0) < 0.1)
        self.assertTrue(abs(grad.color_positions[1] - 2/3) < 0.1)
        self.assertTrue(abs(grad.color_positions[2] - 4/3) < 0.1)

        grad.step(0.3)

        self.assertTrue(abs(grad.color_positions[0] - 0.3) < 0.1)
        self.assertTrue(abs(grad.color_positions[1] - (2/3 + 0.3)) < 0.1)
        self.assertTrue(abs(grad.color_positions[2] - (4/3 + 0.3)) < 0.1)
        self.assertEqual(grad.colors, [(255, 0, 0), (0, 255, 0), (0, 0, 255)])

        grad2 = gd.Gradient(colors=[(255, 0, 0), (0, 255, 0), (0, 0, 255)])
        grad2.step((2/3) + 0.2)
        
        self.assertTrue(abs(grad2.color_positions[0] - 0.2) < 0.1)
        self.assertTrue(abs(grad2.color_positions[1] - (2/3 + 0.2)) < 0.1)
        self.assertTrue(abs(grad2.color_positions[2] - (4/3 + 0.2)) < 0.1)
        self.assertEqual(grad2.colors, [(0, 0, 255), (255, 0, 0), (0, 255, 0)])

        grad3 = gd.Gradient(colors=[(255, 0, 0), (0, 255, 0), (0, 0, 255)])
        grad3.step((4/3) + 0.2)
        
        self.assertTrue(abs(grad3.color_positions[0] - 0.2) < 0.1)
        self.assertTrue(abs(grad3.color_positions[1] - (2/3 + 0.2)) < 0.1)
        self.assertTrue(abs(grad3.color_positions[2] - (4/3 + 0.2)) < 0.1)
        self.assertEqual(grad3.colors, [(0, 255, 0), (0, 0, 255), (255, 0, 0)])

        grad4 = gd.Gradient(colors=[(255, 0, 0), (0, 255, 0), (0, 0, 255)])
        grad4.step(-0.2)

        self.assertTrue(abs(grad4.color_positions[0] - (2/3 - 0.2)) < 0.1)
        self.assertTrue(abs(grad4.color_positions[1] - (4/3 - 0.2)) < 0.1)
        self.assertTrue(abs(grad4.color_positions[2] - 1.8) < 0.1)
        self.assertEqual(grad4.colors, [(0, 255, 0), (0, 0, 255), (255, 0, 0)])



if __name__ == '__main__':
    unittest.main()