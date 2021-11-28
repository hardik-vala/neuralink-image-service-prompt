"""Library of utility functions for NLImage processing."""

from PIL import Image

import image_pb2


def convert_to_nl_image(image):
    pixel_map = image.load()
    width, height = image.size

    image_bytes = bytearray()
    for i in xrange(height):
        for j in xrange(width):
            r, g, b = pixel_map[j, i]
            image_bytes.extend([r, g, b])

    return image_pb2.NLImage(
        color=True,
        data=bytes(image_bytes),
        width=width,
        height=height)


def convert_to_image(nl_image):
    width, height = nl_image.width, nl_image.height
    image = Image.new(mode="RGB", size=(width, height))
    pixel_map = image.load()

    for y in xrange(height):
        for x in xrange(width):
            pixel_map[x, y] = get_pixel_rgb_val(nl_image, x, y)

    return image


def mean_filter(nl_image):
    width, height = nl_image.width, nl_image.height
    
    num_channels = 3 if nl_image.color else 1
    get_pixel_channel_val = get_pixel_rgb_channel_val if nl_image.color else lambda i, x, y, c: get_pixel_grayscale_val(i, x, y)

    out_image_bytes = bytearray()
    
    for y in xrange(height):
        for x in xrange(width):
            out_pixel_vals = []
            for c in xrange(num_channels):
                pixel_and_neighbor_channel_sum = get_pixel_channel_val(nl_image, x, y, c)
                pixel_and_neighbor_vals_cnt = 1
                if x > 0:
                    pixel_and_neighbor_channel_sum += \
                        get_pixel_channel_val(nl_image, x - 1, y, c)
                    pixel_and_neighbor_vals_cnt += 1
                if x > 0 and y > 0:
                    pixel_and_neighbor_channel_sum += \
                        get_pixel_channel_val(nl_image, x - 1, y - 1, c)
                    pixel_and_neighbor_vals_cnt += 1
                if y > 0:
                    pixel_and_neighbor_channel_sum += \
                        get_pixel_channel_val(nl_image, x, y - 1, c)
                    pixel_and_neighbor_vals_cnt += 1
                if x < width - 1 and y > 0:
                    pixel_and_neighbor_channel_sum += \
                        get_pixel_channel_val(nl_image, x + 1, y - 1, c)
                    pixel_and_neighbor_vals_cnt += 1
                if x < width - 1:
                    pixel_and_neighbor_channel_sum += \
                        get_pixel_channel_val(nl_image, x + 1, y, c)
                    pixel_and_neighbor_vals_cnt += 1
                if x < width - 1 and y < height - 1:
                    pixel_and_neighbor_channel_sum += \
                        get_pixel_channel_val(nl_image, x + 1, y + 1, c)
                    pixel_and_neighbor_vals_cnt += 1
                if y < height - 1:
                    pixel_and_neighbor_channel_sum += \
                        get_pixel_channel_val(nl_image, x, y + 1, c)
                    pixel_and_neighbor_vals_cnt += 1
                if x > 0 and y < height - 1:
                    pixel_and_neighbor_channel_sum += \
                        get_pixel_channel_val(nl_image, x - 1, y + 1, c)
                    pixel_and_neighbor_vals_cnt += 1
                out_pixel_channel_val = int(pixel_and_neighbor_channel_sum / float(pixel_and_neighbor_vals_cnt))
                out_pixel_vals.append(out_pixel_channel_val)
            out_image_bytes.extend(out_pixel_vals)

    return image_pb2.NLImage(
        color=nl_image.color,
        data=bytes(out_image_bytes),
        width=width,
        height=height)


def rotate(nl_image, rotation):
    if rotation == image_pb2.NLImageRotateRequest.Rotation.NONE:
        return nl_image

    width, height = nl_image.width, nl_image.height

    out_image_bytes = bytearray()
    if rotation == image_pb2.NLImageRotateRequest.Rotation.NINETY_DEG:
        out_width, out_height = height, width
        coordinates_itr = ((x, y) for x in xrange(width - 1, -1, -1) for y in xrange(height))
    elif rotation == image_pb2.NLImageRotateRequest.Rotation.ONE_EIGHTY_DEG:    
        out_width, out_height = width, height
        coordinates_itr = ((x, y) for y in xrange(height - 1, -1, -1) for x in xrange(width - 1, -1, -1))
    elif rotation == image_pb2.NLImageRotateRequest.Rotation.TWO_SEVENTY_DEG:
        out_width, out_height = height, width
        coordinates_itr = ((x, y) for x in xrange(width) for y in xrange(height -1, -1, -1))

    for x, y in coordinates_itr:
        out_pixel_vals = []
        out_image_bytes.extend(get_pixel_val_list(nl_image, x, y))

    return image_pb2.NLImage(
        color=nl_image.color,
        data=bytes(out_image_bytes),
        width=out_width,
        height=out_height)


def get_pixel_val_list(nl_image, x, y):
    if nl_image.color == True:
    	r = get_pixel_rgb_channel_val(nl_image, x, y, 0)
    	g = get_pixel_rgb_channel_val(nl_image, x, y, 1)
    	b = get_pixel_rgb_channel_val(nl_image, x, y, 2)
    	return [r, g, b]
    else:
        return [get_pixel_grayscale_val(nl_image, x, y)]


def get_pixel_rgb_val(nl_image, x, y):
    r = get_pixel_rgb_channel_val(nl_image, x, y, 0)
    g = get_pixel_rgb_channel_val(nl_image, x, y, 1)
    b = get_pixel_rgb_channel_val(nl_image, x, y, 2)
    return (r, g, b)


def get_pixel_grayscale_val(nl_image, x, y):
    idx = y * nl_image.width + x
    return int(nl_image.data[idx].encode('hex'), 16)


# Expects 0 for r channel, 1 for g channel, and 2 for b channel. 
def get_pixel_rgb_channel_val(nl_image, x, y, channel):
	idx = 3 * y * nl_image.width + 3 * x + channel
	return int(nl_image.data[idx].encode('hex'), 16)
