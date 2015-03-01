# consoleplot.py
#---------------

def plot(x=[], y=[], size_x=100, size_y=20):
    """
    x, y list of values on x- and y-axis.
    plot those values within canvas size.
    """
    # for simplicity, x and y must contain the same number
    # of elements and must be positive.
    if len(x) != len(y) or min(x) < 0 or min(y) < 0:
        print('len(x) != len(y) or some elements are negative')

    # Scale points such that they fit on canvas
    scale_x = float(size_x-1)/max(x) if x and max(x) != 0 else size_x
    scale_y = float(size_y-1)/max(y) if y and max(y) != 0 else size_y
    x_scaled = [int(i * scale_x) for i in x]
    y_scaled = [int(i * scale_y) for i in y]

    # Create empty canvas
    canvas = [[' ' for _ in range(size_x)] for _ in range(size_y)]

    # Add scaled points to canvas
    for ix, iy in zip(x_scaled, y_scaled):
        canvas[size_y-iy+1][ix] = '*'

    # Print rows of canvas
    for row in [''.join(row) for row in canvas]:
        print(row)

    # Print scale
    print(''.join([ 'Max x: ', str(max(x)), ' Max y: ', str(max(y)), '\n' ]))
