import re

def get_current_point(coords_string, prev_point=None):

    if ',' in coords_string:
        x, y = map(float, coords_string.split(','))
    elif coords_string.count('-') == 1:
        coords = coords_string.split('-')
        x = float(coords[0])
        y = float('-' + coords[1])
    else:
        coords = coords_string.split('-')
        x = float('-' + coords[1])
        y = float('-' + coords[2])

    if prev_point:
        x, y = prev_point[0] + x, prev_point[1] + y

    return round(x, 2), round(y, 2)


def svg_read(svg):

    view_box_string = ''
    for symb in svg[svg.find('viewBox')+9:]:
        if symb == '"':
            break
        view_box_string += symb

    view_box = list(map(int, view_box_string.split()))

    circuit = []
    polygons = []
    cur_polygon = []
    cur_flag = 'M'
    r = ''

    for symb in svg[svg.find('path')+9: svg.find('"/>')]:
        
        if symb.lower() in ['m', 'l', 'h', 'v', 'z']:

            point = None

            if cur_flag in ['M', 'L']:
                point = get_current_point(r)
            elif cur_flag == 'H':
                point = (float(r), cur_polygon[-1][1])
            elif cur_flag == 'V':
                point = (cur_polygon[-1][0], float(r))
            elif cur_flag == 'm':
                point = get_current_point(r, polygons[-1][-1])
            elif cur_flag == 'l':
                point = get_current_point(r, cur_polygon[-1])
            elif cur_flag == 'h':
                point = (cur_polygon[-1][0] + float(r), cur_polygon[-1][1])
            elif cur_flag == 'v':
                point = (cur_polygon[-1][0], cur_polygon[-1][1] + float(r))
            else:
                if not circuit:
                    circuit = cur_polygon[:-2]
                else:
                    polygons.append(cur_polygon[:-2])
                cur_polygon = []

            r = ''
            cur_flag = symb

            if point:
                cur_polygon.append(point)
                
        else:
            r += symb

    return view_box, circuit, polygons
