# consoleplot.py
#---------------
from math import floor

def plot(x=[], y=[]):
    """
    x, y list of values on x- and y-axis.
    plot those values within canvas size.
    """
    # for simplicity, x and y must contain the same number
    # of elements and must be positive.
    if len(x) != len(y) or min(x) < 0 or min(y) < 0:
        print('len(x) != len(y) or some elements are negative')
        return

    # Get Terminal size
    [size_x, size_y] = getTerminalSize()
    # offset for caption
    size_y -= 5

    # Scale points such that they fit on canvas
    scale_x = float(size_x-1)/(max(x)-min(x)) if x and max(x)-min(x) != 0 else size_x
    scale_y = float(size_y-1)/(max(y)-min(y)) if y and max(y)-min(y) != 0 else size_y
    x_scaled = [floor((i-min(x)) * scale_x) for i in x]
    y_scaled = [floor((i-min(y)) * scale_y) for i in y]

    # Create empty canvas
    canvas = [[' ' for _ in range(size_x)] for _ in range(size_y)]

    # Add scaled points to canvas
    for ix, iy in zip(x_scaled, y_scaled):
        canvas[size_y-iy-1][ix] = '*'

    # Print rows of canvas
    for row in [''.join(row) for row in canvas]:
        print(row)

    # Print scale
    print('\n', ''.join([
        'Min x: ',  str(min(x)),
        ' Max x: ', str(max(x)),
        ' Min y: ', str(min(y)),
        ' Max y: ', str(max(y)),
        '\n'
    ]))


def getTerminalSize():
    """ Source: http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
    """
    import os
    env = os.environ
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
        except:
            return
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        cr = (env.get('LINES', 25), env.get('COLUMNS', 80))

        ### Use get(key[, default]) instead of a try/catch
        #try:
        #    cr = (env['LINES'], env['COLUMNS'])
        #except:
        #    cr = (25, 80)
    return int(cr[1]), int(cr[0])