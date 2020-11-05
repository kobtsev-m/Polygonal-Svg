import os
import json
import math

from .triangulation import get_triangles
from .svg import svg_read

class ParserSvg:

    IN_FILE_PATH = None
    OUT_FILE_SVG_PATH = None
    OUT_FILE_JSON_PATH = None

    SHOW_CIRCUIT = False

    POINTS_APPROXIMATION = 5
    LINES_APPROXIMATION = 5

    POLYGON_DEGENERACY_CHECK = True

    def is_points_near(self, p1, p2):
        return abs(p1[0] - p2[0]) < self.POINTS_APPROXIMATION and \
               abs(p1[1] - p2[1]) < self.POINTS_APPROXIMATION

    @staticmethod
    def get_sides_idx():
        return [[0, 1], [1, 2], [2, 0]]

    @staticmethod
    def is_parallel(line1, line2):
        v1 = (line1[0][0] - line1[1][0], line1[0][1] - line1[1][1])
        v2 = (line2[0][0] - line2[1][0], line2[0][1] - line2[1][1])

        if v2[0] == 0:
            return v1[0] == 0 and v2[0] == 0
        elif v2[1] == 0:
            return v1[1] == 0 and v2[1] == 0
        else:
            return abs(abs(v1[0] / v2[0]) - abs(v1[1] / v2[1])) < 0.05

    def is_lines_near(self, line1, line2):
        p11 = line1[0]
        p12 = line1[1]
        p21 = line2[0]
        p22 = line2[1]

        if abs(p11[0] - p21[0]) < self.LINES_APPROXIMATION and \
           abs(p11[1] - p21[1]) < self.LINES_APPROXIMATION and \
           abs(p12[0] - p22[0]) < self.LINES_APPROXIMATION and \
           abs(p12[1] - p22[1]) < self.LINES_APPROXIMATION:
            return 1

        if abs(p11[0] - p22[0]) < self.LINES_APPROXIMATION and \
           abs(p11[1] - p22[1]) < self.LINES_APPROXIMATION and \
           abs(p12[0] - p21[0]) < self.LINES_APPROXIMATION and \
           abs(p12[1] - p21[1]) < self.LINES_APPROXIMATION:
            return -1

        return 0

    @staticmethod
    def generate_points_string(points):
        return ' '.join(map(lambda point: ' '.join(map(str, point)), points))

    def generate_img(self, tab, in_file=None):

        # Чтение файла
        if not in_file:
            in_file = open(self.IN_FILE_PATH).read()

        # Чтение координат точек из SVG файла и разделение на многоугольники
        view_box, circuit, polygons = svg_read(in_file)

        # Объединение соседних точек в многоугольниках
        if self.POINTS_APPROXIMATION:
            for polygon in polygons:
                polygon_len = len(polygon)
                i = 0
                while i < polygon_len:
                    j = i + 1
                    while j < polygon_len:
                        if self.is_points_near(polygon[i], polygon[j]):
                            polygon.pop(j)
                            polygon_len -= 1
                        else:
                            j += 1
                    i += 1

        # Разбиение многоугольников на треугольники
        triangles = []
        for polygon in polygons:
            polygon_triangles = get_triangles(
                polygon,
                self.POLYGON_DEGENERACY_CHECK
            )
            if polygon_triangles:
                triangles.extend(polygon_triangles)

        # Объединение соседних отрезков
        if self.LINES_APPROXIMATION:
            for i in range(len(triangles)):
                for j in range(i + 1, len(triangles)):
                    for k in self.get_sides_idx():
                        for m in self.get_sides_idx():
                            si = [triangles[i][k[0]], triangles[i][k[1]]]
                            sj = [triangles[j][m[0]], triangles[j][m[1]]]
                            if self.is_parallel(si, sj):
                                is_near = self.is_lines_near(si, sj)
                                if is_near == 1:
                                    triangles[i][k[0]] = triangles[j][m[0]]
                                    triangles[i][k[1]] = triangles[j][m[1]]
                                if is_near == -1:
                                    triangles[i][k[0]] = triangles[j][m[1]]
                                    triangles[i][k[1]] = triangles[j][m[0]]

        # Запись полученного изображения в файл

        svg_basis = '<svg id="{svg_id}" xmlns="http://www.w3.org/2000/svg" ' + \
                    'viewBox="{x1} {y1} {x2} {y2}">\n{content}</svg>'

        path_basis = '\t<polygon id="{polygon_id}" points="{points}">' + \
                     '</polygon>\n'

        content = ''
        cur_id = 0
        data = []

        for triangle in triangles:
            points = self.generate_points_string(triangle)
            content += path_basis.format(
                polygon_id='{}-polygon-{}'.format(tab, cur_id),
                points=points
            )
            data.append({
                'id': '#{}-polygon-{}'.format(tab, cur_id),
                'points': points
            })
            cur_id += 1

        if self.SHOW_CIRCUIT:
            points = self.generate_points_string(circuit)
            content += path_basis.format(
                polygon_id='{}-circuit'.format(tab),
                points=points
            )
            data.append({
                'id': '#{}-circuit'.format(tab),
                'points': points
            })

        if self.OUT_FILE_SVG_PATH:
            with open(self.OUT_FILE_SVG_PATH, 'w') as f:
                f.write(svg_basis.format(
                    svg_id='{}Svg'.format(tab),
                    x1=view_box[0] * 2,
                    y1=view_box[1],
                    x2=view_box[2] * 2,
                    y2=view_box[3],
                    content=content
                ))

        if self.OUT_FILE_JSON_PATH:
            with open(self.OUT_FILE_JSON_PATH, 'w') as f:
                json.dump(data, f, indent=2)

