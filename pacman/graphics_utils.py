def add(t1, t2):
	return tuple(map(sum, zip(t1, t2)))


def create_polygon(canvas, coords_list, outline_color, fill_color=None, smoothed=1, width=1):
	c = []
	for coords in coords_list:
		c.append(coords[0])
		c.append(coords[1])
	if fill_color == None: fill_color = outline_color
	return canvas.create_polygon(c, outline=outline_color, fill=fill_color, smooth=smoothed, width=width)


def create_circle(canvas, center_coords, r, outline_color, fill_color=None):
	x, y = center_coords
	x0, x1 = x - r - 1, x + r
	y0, y1 = y - r - 1, y + r
	if fill_color == None: fill_color = outline_color
	return canvas.create_oval(x0, y0, x1, y1, outline=outline_color, fill=fill_color)


def create_arc(canvas, center_coords, r, outline_color, fill_color=None, start=0, extent=359.999):
	x, y = center_coords
	x0, x1 = x - r - 1, x + r
	y0, y1 = y - r - 1, y + r
	if fill_color == None: fill_color = outline_color
	return canvas.create_arc(x0, y0, x1, y1, start=start, extent=extent, outline=outline_color, fill=fill_color)


def create_rectange(canvas, center_coords, width, height, outline_color, fill_color=None):
	if fill_color == None: fill_color = outline_color
	return canvas.create_rectangle(get_coorner_coordinates(center_coords, width, height), outline=outline_color, fill=fill_color)


def get_coorner_coordinates(center_coords, width, height):
	x, y = center_coords
	x0, y0 = x - width / 2, y + height / 2
	x1, y1 = x + width / 2, y - height / 2
	return x0, y0, x1, y1


ghost_shape = [
    (0, 0.5),
    (-0.25, 0.75),
    (-0.5, 0.5),
    (-0.75, 0.75),
    (-0.75, -0.5),
    (-0.5, -0.75),
    (0.5, -0.75),
    (0.75, -0.5),
    (0.75, 0.75),
    (0.5, 0.5),
    (0.25, 0.75)
    ]


def get_ghost_shape(center_coords, dx_canvas, dy_canvas):
	x0, y0 = center_coords
	shape = []
	for x, y in ghost_shape:
		shape.append((x0 + 0.6 * dx_canvas * x, y0 + 0.6 * dy_canvas * y))
	return shape
