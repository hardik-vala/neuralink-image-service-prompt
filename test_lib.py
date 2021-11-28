import image_pb2
import lib
import unittest
  
class NLImageLibTest(unittest.TestCase):
  
    def test_mean_filter(self):
        width, height = (3, 4)
        pixel_map = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [9, 10, 11],
        ]
        nl_image = _convert_to_nl_image(pixel_map, width, height, is_color=False)

        out_nl_image = lib.mean_filter(nl_image)

        pixel_map_actual = _extract_pixel_map(out_nl_image)
        pixel_map_expected = [
            [2, 2, 3],
            [3, 4, 4],
            [6, 7, 7],
            [8, 8, 9],
        ]
        self.assertEqual(pixel_map_actual, pixel_map_expected)

    def test_mean_filter_color(self):
        width, height = (3, 4)
        pixel_map = [
            [(0, 1, 2), (3, 4, 5), (6, 7, 8)],
            [(9, 10, 11), (12, 13, 14), (15, 16, 17)],
            [(18, 19, 20), (21, 22, 23), (24, 25, 26)],
            [(27, 28, 29), (30, 31, 32), (33, 34, 35)],
        ]
        nl_image = _convert_to_nl_image(pixel_map, width, height, is_color=True)

        out_nl_image = lib.mean_filter(nl_image)

        pixel_map_actual = _extract_pixel_map(out_nl_image)
        pixel_map_expected = [
            [(6, 7, 8), (7, 8, 9), (9, 10, 11)],
            [(10, 11, 12), (12, 13, 14), (13, 14, 15)],
            [(19, 20, 21), (21, 22, 23), (22, 23, 24)],
            [(24, 25, 26), (25, 26, 27), (27, 28, 29)],
        ]
        self.assertEqual(pixel_map_actual, pixel_map_expected)

    def test_rotate_none(self):
        width, height = (3, 4)
        pixel_map = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [9, 10, 11],
        ]
        nl_image = _convert_to_nl_image(pixel_map, width, height, is_color=False)

        out_nl_image = lib.rotate(nl_image,
            image_pb2.NLImageRotateRequest.Rotation.NONE)

        pixel_map_actual = _extract_pixel_map(out_nl_image)
        self.assertEqual(pixel_map_actual, pixel_map)

    def test_rotate_ninety_deg(self):
        width, height = (3, 4)
        pixel_map = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [9, 10, 11],
        ]
        nl_image = _convert_to_nl_image(pixel_map, width, height, is_color=False)

        out_nl_image = lib.rotate(nl_image,
            image_pb2.NLImageRotateRequest.Rotation.NINETY_DEG)

        pixel_map_actual = _extract_pixel_map(out_nl_image)
        pixel_map_expected = [
            [2, 5, 8, 11],
            [1, 4, 7, 10],
            [0, 3, 6, 9],
        ]
        self.assertEqual(pixel_map_actual, pixel_map_expected)

    def test_rotate_one_eighty_deg(self):
        width, height = (3, 4)
        pixel_map = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [9, 10, 11],
        ]
        nl_image = _convert_to_nl_image(pixel_map, width, height, is_color=False)

        out_nl_image = lib.rotate(nl_image,
            image_pb2.NLImageRotateRequest.Rotation.ONE_EIGHTY_DEG)

        pixel_map_actual = _extract_pixel_map(out_nl_image)
        pixel_map_expected = [
            [11, 10, 9],
            [8, 7, 6],
            [5, 4, 3],
            [2, 1, 0],
        ]
        self.assertEqual(pixel_map_actual, pixel_map_expected)

    def test_rotate_two_seventy_deg(self):
        width, height = (3, 4)
        pixel_map = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [9, 10, 11],
        ]
        nl_image = _convert_to_nl_image(pixel_map, width, height, is_color=False)

        out_nl_image = lib.rotate(nl_image,
            image_pb2.NLImageRotateRequest.Rotation.TWO_SEVENTY_DEG)

        pixel_map_actual = _extract_pixel_map(out_nl_image)
        pixel_map_expected = [
            [9, 6, 3, 0],
            [10, 7, 4, 1],
            [11, 8, 5, 2],
        ]
        self.assertEqual(pixel_map_actual, pixel_map_expected)

    def test_rotate_color_none(self):
        width, height = (3, 4)
        pixel_map = [
            [(0, 1, 2), (3, 4, 5), (6, 7, 8)],
            [(9, 10, 11), (12, 13, 14), (15, 16, 17)],
            [(18, 19, 20), (21, 22, 23), (24, 25, 26)],
            [(27, 28, 29), (30, 31, 32), (33, 34, 35)],
        ]
        nl_image = _convert_to_nl_image(pixel_map, width, height, is_color=True)

        out_nl_image = lib.rotate(nl_image,
            image_pb2.NLImageRotateRequest.Rotation.NONE)

        pixel_map_actual = _extract_pixel_map(out_nl_image)
        self.assertEqual(pixel_map_actual, pixel_map)

    def test_rotate_color_ninety_deg(self):
        width, height = (3, 4)
        pixel_map = [
            [(0, 1, 2), (3, 4, 5), (6, 7, 8)],
            [(9, 10, 11), (12, 13, 14), (15, 16, 17)],
            [(18, 19, 20), (21, 22, 23), (24, 25, 26)],
            [(27, 28, 29), (30, 31, 32), (33, 34, 35)],
        ]
        nl_image = _convert_to_nl_image(pixel_map, width, height, is_color=True)

        out_nl_image = lib.rotate(nl_image,
            image_pb2.NLImageRotateRequest.Rotation.NINETY_DEG)

        pixel_map_actual = _extract_pixel_map(out_nl_image)
        pixel_map_expected = [
            [(6, 7, 8), (15, 16, 17), (24, 25, 26), (33, 34, 35)],
            [(3, 4, 5), (12, 13, 14), (21, 22, 23), (30, 31, 32)],
            [(0, 1, 2), (9, 10, 11), (18, 19, 20), (27, 28, 29)],
        ]
        self.assertEqual(pixel_map_actual, pixel_map_expected)

    def test_rotate_color_one_eighty_deg(self):
        width, height = (3, 4)
        pixel_map = [
            [(0, 1, 2), (3, 4, 5), (6, 7, 8)],
            [(9, 10, 11), (12, 13, 14), (15, 16, 17)],
            [(18, 19, 20), (21, 22, 23), (24, 25, 26)],
            [(27, 28, 29), (30, 31, 32), (33, 34, 35)],
        ]
        nl_image = _convert_to_nl_image(pixel_map, width, height, is_color=True)

        out_nl_image = lib.rotate(nl_image,
            image_pb2.NLImageRotateRequest.Rotation.ONE_EIGHTY_DEG)

        pixel_map_actual = _extract_pixel_map(out_nl_image)
        pixel_map_expected = [
            [(33, 34, 35), (30, 31, 32), (27, 28, 29)],
            [(24, 25, 26), (21, 22, 23), (18, 19, 20)],
            [(15, 16, 17), (12, 13, 14), (9, 10, 11)],
            [(6, 7, 8), (3, 4, 5), (0, 1, 2)],
        ]
        self.assertEqual(pixel_map_actual, pixel_map_expected)

    def test_rotate_color_two_seventy_deg(self):
        width, height = (3, 4)
        pixel_map = [
            [(0, 1, 2), (3, 4, 5), (6, 7, 8)],
            [(9, 10, 11), (12, 13, 14), (15, 16, 17)],
            [(18, 19, 20), (21, 22, 23), (24, 25, 26)],
            [(27, 28, 29), (30, 31, 32), (33, 34, 35)],
        ]
        nl_image = _convert_to_nl_image(pixel_map, width, height, is_color=True)

        out_nl_image = lib.rotate(nl_image,
            image_pb2.NLImageRotateRequest.Rotation.TWO_SEVENTY_DEG)

        pixel_map_actual = _extract_pixel_map(out_nl_image)
        pixel_map_expected = [
            [(27, 28, 29), (18, 19, 20), (9, 10, 11), (0, 1, 2)],
            [(30, 31, 32), (21, 22, 23), (12, 13, 14), (3, 4, 5)],
            [(33, 34, 35), (24, 25, 26), (15, 16, 17), (6, 7, 8)],
        ]
        self.assertEqual(pixel_map_actual, pixel_map_expected)


def _convert_to_nl_image(pixel_map, width, height, is_color):
    image_bytes = bytearray()

    if is_color:
        for i in xrange(height):
            for j in xrange(width):
                r, g, b = pixel_map[i][j]
                image_bytes.extend([r, g, b])
    else:
        for i in xrange(height):
            for j in xrange(width):
                image_bytes.extend([pixel_map[i][j]])

    return image_pb2.NLImage(
        color=is_color,
        data=bytes(image_bytes),
        width=width,
        height=height)


def _extract_pixel_map(nl_image):
    width, height = nl_image.width, nl_image.height
    
    out_pixel_map = []
    for y in xrange(height):
        pixel_row = []
        for x in xrange(width):
            if nl_image.color:
                pixel_row.append(lib.get_pixel_rgb_val(nl_image, x, y))
            else:
                pixel_row.append(lib.get_pixel_grayscale_val(nl_image, x, y))
        out_pixel_map.append(pixel_row)

    return out_pixel_map

  
if __name__ == '__main__':
    unittest.main()
