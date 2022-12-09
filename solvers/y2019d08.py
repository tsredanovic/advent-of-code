
from advent_of_code.basesolver import BaseSolver


class Pixel:
    def __init__(self, v):
        self.v = v

    def __str__(self):
        return str(self.v)

    def __repr__(self):
        return str(self)


class Layer:
    def __init__(self):
        self.rows = []

    def __str__(self):
        return str(self.rows)

    def __repr__(self):
        return str(self)

    def num_of(self, digit):
        num_of_digit = 0
        for row in self.rows:
            for pixel in row:
                if digit == pixel.v:
                    num_of_digit += 1
        return num_of_digit


class Image:
    def __init__(self, w, h):
        self.layers = []

    def __str__(self):
        return str(self.layers)

    def __repr__(self):
        return str(self)


def load_input(data):
    return data.strip()


def create_image(w, h, content):
    pixels_per_layer = w*h
    layers_per_image = len(content) / pixels_per_layer
    if int(layers_per_image) != layers_per_image:
        print('Something goofed! Layers per image should be int.')
    layers_per_image = int(layers_per_image)
    rows_per_layer = h

    # Create empty image
    image = Image(w, h)
    for i in range(layers_per_image):
        layer = Layer()
        for j in range(rows_per_layer):
            layer.rows.append([])
        image.layers.append(layer)

    # Fill empty image with pixels
    for pixel_i in range(len(content)):
        pixel = Pixel(int(content[pixel_i]))

        layer_i = int(pixel_i / pixels_per_layer)
        layer = image.layers[layer_i]
        for row_i, row in enumerate(layer.rows):
            if len(row) < w:
                break

        layer.rows[row_i].append(pixel)

    return image

def print_layer(layer):
    result = ''
    for row in layer.rows:
        row_result = ''
        for pixel_v in row:
            if pixel_v == 1:
                row_result += '#'
            elif pixel_v == 0:
                row_result += '.'
        result += row_result + '\n'
    return '\n{}'.format(result.strip())


class Y2019D08Solver(BaseSolver):
    def solve_part_a(self):
        content = load_input(self.data)

        image = create_image(25, 6, content)

        min_0_layer = image.layers[0]
        for i, layer in enumerate(image.layers):
            if layer.num_of(0) < min_0_layer.num_of(0):
                min_0_layer = layer

        return min_0_layer.num_of(1) * min_0_layer.num_of(2)
    

    def solve_part_b(self):
        content = load_input(self.data)

        w = 25
        h = 6

        image = create_image(w, h, content)

        # WAY 1
        decoded_layer = Layer()
        for i in range(h):
            row = [-1] * w
            decoded_layer.rows.append(row)

        for image_layer in image.layers:
            for row_i, image_layer_row in enumerate(image_layer.rows):
                for pixel_i, image_pixel in enumerate(image_layer_row):
                    image_pixel_v = image_pixel.v
                    decoded_layer_pixel_v = decoded_layer.rows[row_i][pixel_i]

                    if decoded_layer_pixel_v == -1 and image_pixel_v != 2:
                        decoded_layer.rows[row_i][pixel_i] = image_pixel_v

        # WAY 2
        d_l_2 = Layer()
        for i in range(h):
            row = [-1] * w
            d_l_2.rows.append(row)

        for i in range(h):
            for j in range(w):
                for layer in image.layers:
                    l_v = layer.rows[i][j].v
                    if l_v != 2:
                        break
                d_l_2.rows[i][j] = l_v

        return print_layer(d_l_2)
