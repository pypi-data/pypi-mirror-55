from itertools import combinations
import logging
import networkx as nx
from networkx.exception import NetworkXNoPath
import numpy as np
from scipy.spatial import Voronoi
from scipy.ndimage import filters
from shapely.geometry import LineString, Point
from shapely.geometry import shape
#import gdal
from osgeo import gdal
import sys
import time
from glacier_length.exceptions import LengthError


logger = logging.getLogger(__name__)


def get_all_length(
        src,
        filename0,
        error_filename,
        dem
):
    """
    冰川长度终结者
    :param src: 冰川边界面图层，的.geojson格式。

    :return: allcenterlines,即 .geojson 中所有所有的所有冰川的长度。
    """

    top_head0 = '{"type":"FeatureCollection", "features":['
    top = top_head0.replace("'", " ")
    # print(top)
    with open(filename0, 'a') as f:
        f.write(top)


    allcenterlines = []
    n0 = 0
    for i in src:
        sum0 = len(src)
        name1 = i["properties"]["NEW_ID"]  #冰川名称字段
        print(name1)
        a = shape(i["geometry"])
        b = a.geom_type
        logger.debug("geometry type %s", a.geom_type)
        if b == "MultiPolygon":

            with open(error_filename, 'a') as f:
                f.write('\r\n')
                f.write(str(name1))
            n0 += 1
        else:
            all_outline_points, outline_pointss, all_area = _get_all_outline_points(a)
            #print(all_outline_points)
            #print("看一下all_outline_points是什么类型。。。。。。。。。。。。。。。。。。。。。。。。。。。。。。")
            #print(outline_pointss)
            #print("看一下outline_pointss和all_outline_points是不是一个类型。。。。。。。。。。。。。。。。。。。。。")

            vor = Voronoi(all_outline_points)
            #print(vor)
            #fig = voronoi_plot_2d(vor, point_size=10, line_alpha=1)
            #plt.show()
            print("生成了voronoi===================================================")
            graph = _graph_from_voronoi(vor, a)  # 这一步真的挺慢的
            #nx.draw(graph, point_size=2)
            #plt.show()
            print("生成了graph==================================================")

            start_end_nodes0 = _get_end_nodes(graph)
            print(start_end_nodes0)
            print("这是start_end_nodes0。。。。。。。。。。。。。。。。。。。。")
            print(len(start_end_nodes0))
            print("这是start_end_nodes0的个数。。。。。。。。。。。。。。。。。。。。。")
            # 匹配point.geojson==============================================
            #points_geo = []
            #for points_g in points_geo0:
                #name2 = points_g["properties"]["OBJECTID"]  #冰川名称字段
                #print(name2)
                #if name2 == name1:
                    #points_geo.append(points_g)
            #print("匹配了point.geojson=============================================")
            # =============================================================
            #points_geo1, highest_value, lowest_value = bubble_sort(points_geo)
            if all_area > 2510000:
                all_contours, hiers, lo, hi, all_contours_sort = _get_high_border_contour(outline_pointss, dem)
                end_high_nodes = _get_high_nodes(start_end_nodes0, vor, hiers, graph)

            else:
                all_contours, lo, hi, all_contours_sort = _get_high_border_contour2(outline_pointss, dem)
                end_high_nodes = _get_high_nodes2(start_end_nodes0,vor,hi,all_contours_sort,graph)

            #all_contours = get_high_border_contour(outline_pointss)
            print(all_contours)
            print("这是冰川 外边界点（有高程的）。。。。。。。")
            #print(hiers)
            #print("test......................................")
            end_low_nodes = _get_low_nodes(start_end_nodes0, vor,lo,all_contours_sort,graph)
            #end_high_nodes = get_high_nodes(start_end_nodes0, vor, hiers, graph)
            print(end_low_nodes)
            print(end_high_nodes)
            print("====test end_low_nodes 和 end_high_nodes========================================")


            longest_path, high_xy, low_xy = _get_longest_path(end_low_nodes, end_high_nodes, vor, graph,name1)
            #print(longest_path)
            if len(longest_path):
                centerlin = _get_single_centerline(longest_path, vor, i, low_xy,high_xy)
                print(centerlin)
                #allcenterlines.append(centerlin)
                #print(allcenterlines)
                db = '{0},'.format(centerlin)
                db1 = db.replace("'", " ")
                with open(filename0, 'a') as f:
                    f.write(db1)
                print("一个又一个=======================================================")
                n0 += 1
            else:
                with open(error_filename, 'a') as f:
                    f.write('\r\n')
                    f.write(str(name1))
                n0 += 1
        print(n0, sum0)

    top_head2 = ']}'
    with open(filename0, 'a') as f:
        f.write(top_head2)




#######################


def _get_high_threshold(all_contours):
    """
    :param all_contours:是冰川外边界的点（包含了高程）
    :return: threshold 是一个冰川的最高海拔和最低海拔的四分之三， 阈值 。
    """

    #我排序只是为了找到最低点和最高点的高程值。
    all_contours2 = all_contours
    for i in range(len(all_contours2) - 1):
        for j in range(len(all_contours2) - 1 - i):
            if all_contours2[j]["value"] > all_contours2[j + 1]["value"]:
                all_contours2[j], all_contours2[j + 1] = all_contours2[j + 1], all_contours2[j]
    #print(all_contours2)
    lo = all_contours2[0]["value"]
    hi = all_contours2[-1]["value"]
    threshold = int(((hi-lo) * 4) / 5 + lo)
    #print(hi)
    #print(lo)
    #print(threshold)
    #print("all_contours2....................................................")
    return threshold,lo,hi

def _get_contour_value(dem, x, y):
    """
    如果提取高程出错，那一定是因为dem的坐标和冰川边界的坐标不一致。
    :param dem: 区域范围内的dem。
    :param x: x坐标
    :param y: y坐标
    :return: 我 希望 返回的 data 是一个数值，一个坐标一个值。
    """
    gdal.AllRegister()
    dataset = gdal.Open(dem, gdal.GA_ReadOnly)
    if dataset is None:
        #print('Could not open image')
        sys.exit(1)

    # rows = dataset.RasterYSize
    # cols = dataset.RasterXSize
    # n_band = dataset.RasterCount
    # print("rows,cols,bands:", rows, cols, n_band)

    transform = dataset.GetGeoTransform()
    x_origin = transform[0]
    y_origin = transform[3]
    #print("x origin, y origin: " + str(x_origin) + " " + str(y_origin))
    pixelWidth = transform[1]
    pixelHeight = transform[5]
    #print("pixel width, pixel height:" + str(pixelWidth) + " " + str(pixelHeight))

    #x_offset_list = []
    #y_offset_list = []
    # xy = (-2739471.4233753365, 4689468.996877703)

    xOffset = int((x - x_origin) / pixelWidth)
    yOffset = int((y - y_origin) / pixelHeight)
    #print("xoffset, yoffset: ", xOffset, yOffset)

    band = dataset.GetRasterBand(1)
    data = band.ReadAsArray(xOffset, yOffset, 1, 1)
    return data[0][0]

def _get_high_border_contour(outline_pointss,dem):
    """
    :param outline_pointss: 是 get_all_outline_points(a)中得到的，冰川外边界的点。形式是[( , ),( , ),( , )...]
    :return: all_contours [{( ，):值},{( , ):值}..] 是所有外边界点(包含了高程)；
             hiers [] 是30个点内最高的点；
             lo 冰川边界的最低海拔值。
             hi 冰川边界的最高海拔值。
             all_contours_sort 是排序好的 all_contours。
    """
    all_contours = []
    for lis in outline_pointss:
        coo_contours = {}
        vv = _get_contour_value(dem,lis[0],lis[1]) #vv是高程值
        #print(vv)
        coo_contours['type'] = Point
        coo_contours['coordinates'] = lis
        coo_contours['value'] = vv
        all_contours.append(coo_contours) #生成了我想要的[{():55},{():88}..]   {元组：值}
    all_contours_sort = sorted(all_contours, key=lambda x: x["value"], reverse=False)
    #print(all_contours)
    #print(len(all_contours))

    hiers = []
    nn = [nn for nn in range(0,len(all_contours), 40)]
    if len(all_contours)/40 == 0:
        print(nn)
    else:
        nn.append(len(all_contours))
    #print(nn)
    #print(len(nn))
    for i in range(len(nn)):
        if i < len(nn)-1:
            #print(i)
            hii = []
            for j in all_contours[nn[i]:nn[i+1]]:
                hii.append(j)
            hier = sorted(hii,key=lambda x:x["value"],reverse=False)[-1] #列表嵌套字典的排序
            # print("paixule............................")
            threshold,lo,hi = _get_high_threshold(all_contours)
            if hier["value"] > threshold:
                hiers.append(hier)

    return all_contours, hiers, lo,hi, all_contours_sort

def _get_high_border_contour2(outline_pointss,dem):
    """
    和get_high_border_contour 的区别是 这个函数是提供给面积小的冰川。只找一个最高点而不是一个列表的最高点。
    :param outline_pointss: 是get_all_outline_points(a)中得到的，冰川外边界的点。形式是[( , ),( , ),( , )...]
    :return: all_contours [{( ，):值},{( , ):值}..]是所有外边界点(包含了高程)；
             hiers [] ；
             lo 冰川边界的最低海拔值。
             hi 冰川边界的最高海拔值。
             all_contours_sort 是排序好的 all_contours。
    """
    all_contours = []
    for lis in outline_pointss:
        coo_contours = {}
        vv = _get_contour_value(dem,lis[0],lis[1]) #vv是高程值
        #print(vv)
        coo_contours['type'] = Point
        coo_contours['coordinates'] = lis
        coo_contours['value'] = vv
        all_contours.append(coo_contours) #生成了我想要的[{():55},{():88}..]   {元组：值}
    all_contours_sort = sorted(all_contours, key=lambda x: x["value"], reverse=False)
    #print(all_contours)
    #print(len(all_contours))
    threshold, lo, hi = _get_high_threshold(all_contours)
    return all_contours, lo,hi, all_contours_sort

def _get_all_outline_points(a):
    """
    :param a:    a = shape(i["geometry"]), //for i in src: //src = fiona.open(url + "json_818_2.geojson", "r")
    :return: all_outline_points 内外边界所有的点。
             outline_pointss 是外边界的所有的点。
             all_area 冰川的面积， 用来做判断用的。
    """
    all_outline_points = []
    outline_pointss = []
    all_area = a.area
    print(all_area)

    for subai in a.interiors:
        points = []
        max_len = 0.5
        for previous, current in zip(subai.coords, subai.coords[1:]):  # zip()函数"成语接龙"
            line_segment = LineString([previous, current])
            # add points on line segment if necessary  extend() 函数用于在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）
            points.extend([
                line_segment.interpolate(max_len * i).coords[0]
                for i in range(int(line_segment.length / max_len))
            ])  # int()取整。
            # finally, add end point
            points.append(current)  # 我懂了，这个函数，就是边界的点与点之间的距离如果过远，就疯狂打断点生成无数个点在points里。最后points列表里就有无数个边界点了。
        outline = LineString(points)
        outline_points = outline.coords

        simplification = 0.05
        max_points = 5000
        simplification_updated = simplification
        while len(outline_points) > max_points:
            # if geometry is too large, apply simplification until geometry
            # is simplified enough (indicated by the "max_points" value)
            simplification_updated += simplification
            outline_points = outline.simplify(simplification_updated).coords  # object.simplify()返回几何对象的简化表示形式。
        print("a.interiors finished==================================================")
        all_outline_points.extend(outline_points)

    # # # # # # ====exterior==== # # # # # #
    points0 = []
    max_len = 0.5
    for previous, current in zip(a.exterior.coords, a.exterior.coords[1:]):  # zip()函数"成语接龙"
        line_segment0 = LineString([previous, current])
        # add points on line segment if necessary  extend() 函数用于在列表末尾一次性追加另一个序列中的多个值（用新列表扩展原来的列表）
        points0.extend([
            line_segment0.interpolate(max_len * i).coords[0]
            for i in range(int(line_segment0.length / max_len))
        ])  # int()取整。
        # finally, add end point
        points0.append(current)  # 我懂了，这个函数，就是边界的点与点之间的距离如果过远，就疯狂打断点生成无数个点在points里。最后points列表里就有无数个边界点了。
    outline0 = LineString(points0)
    outline_points0 = outline0.coords

    simplification = 0.05
    max_points = 5000
    simplification_updated0 = simplification
    while len(outline_points0) > max_points:
        # if geometry is too large, apply simplification until geometry
        # is simplified enough (indicated by the "max_points" value)
        simplification_updated0 += simplification
        outline_points0 = outline0.simplify(simplification_updated0).coords  # object.simplify()返回几何对象的简化表示形式。
    print("a.exterior finished==================================================")
    all_outline_points.extend(outline_points0)
    outline_pointss.extend(outline_points0)
    return all_outline_points, outline_pointss,all_area

def _yield_ridge_vertices(vor, geometry, dist=False):
    """Yield Voronoi ridge vertices within geometry."""
    for x, y in vor.ridge_vertices: #面上的顶点序号？ https://wenku.baidu.com/view/ca446817c381e53a580216fc700abb68a982ad71.html
        if x < 0 or y < 0: #为啥？
            continue
        point1 = Point(vor.vertices[[x, y]][0])
        point2 = Point(vor.vertices[[x, y]][1])
        #print((vor.vertices[[x,y]]))###这个我必须留下，这个出来的list是没有裁剪过得泰森多边形。###
        #print(vor.vertices[[x]])
        #print(x)
        #print(y)
        #print("我要看看x 和y 是什么。。。。。。。。。。。。。。。。。。")
        #print("00000000000000000000000000000000000000000000000000")
        #print(vor.vertices[[x,y]][1])
        #print("111111111111111111111111111111111111111111111111111111")
        #print(vor.ridge_vertices[0])

        # Eliminate all points outside our geometry.
        if point1.within(geometry) and point2.within(geometry):
            #print((vor.vertices[[x, y]]))# 这个必须留下，这个出来的list是裁剪过的泰森多边形
            #print("ssssssssssssssssssssssssssssss")
            if dist:
                yield x, y, point1.distance(point2)

            else:
                yield x, y

def _graph_from_voronoi(vor, geometry):
    """Return networkx.Graph from Voronoi diagram within geometry."""
    graph = nx.Graph()
    for x, y, dist in _yield_ridge_vertices(vor, geometry, dist=True):
        graph.add_nodes_from([x, y])

        graph.add_edge(x, y, weight=dist)

    return graph

def _get_end_nodes(graph):
    """
    :param graph:graph = nx.Graph()
    :return: 返回graph中只有一个邻居节点的节点列表（为后面找到和最高点最低点相近的节点做铺垫）。
    """
    return [i for i in graph.nodes() if len(list(graph.neighbors(i))) == 1]

def _bubble_sort(points_geo):
    """
    ：使用了bubble_sort算法进行排序。
    :param points_geo: 是从arcgis中获取的最高点最低点的 POINT 的geojson文件。
    :return: 返回的是排序好的最高点最低点。points_geo1[0]就是最低点。
    """

    points_geo1 = []
    for x in points_geo:
        points_geo1.append(x)
    for i in range(len(points_geo1)-1):
        for j in range(len(points_geo1)-1-i):
            if points_geo1[j]["properties"]["RASTERVALU"] > points_geo1[j+1]["properties"]["RASTERVALU"]:
                points_geo1[j], points_geo1[j+1] = points_geo1[j+1], points_geo1[j]
    highest_value = points_geo1[-1]["properties"]["RASTERVALU"]
    lowest_value = points_geo1[0]["properties"]["RASTERVALU"]
    #print(points_geo1)
    #print("points_geo1....................................................")
    return points_geo1, highest_value, lowest_value

def _get_low_nodes(start_end_nodes,vor,lo,all_contours_sort,graph):
    """
    :param start_end_nodes: graph中只有一个邻居节点的节点列表。
    :param vor:是之前生成的vor。
    :param lo: 冰川最低海拔， 是一个数值。
    :param all_contours_sort:排序好的 冰川外边界 所有点（包含了高程）。
    :param graph:
    :return: 返回最低点附近的节点列表的第一个，因为我只希望最低点有且只有一个。
             向graph中添加了一个（最低点）节点，和（最低点和接近它的一个node）边，和距离。
    """
    end_low_nodes = []
    low_nodes = {}
    #po = shape(points_geo1[0]["geometry"])
    #low_xy = '[{0} {1}]'.format(points_geo1[0]["geometry"]["coordinates"][0],points_geo1[0]["geometry"]["coordinates"][1]) #这是个[x y]
    #low_xy = points_geo1[0]["geometry"]["coordinates"] #这是个元组
    #print(low_xy)
    n = 0
    for v in all_contours_sort[0:]:
        if v["value"] == lo:
            n = n + 1
    #print(n)
    #print("这是边界点中， 等于最低点的点的个数。。。。。。。。。。。。")
    look = []

    for q in all_contours_sort[0:n]:
        po = Point(q["coordinates"])
        zz = {}
        for j in start_end_nodes:
            jj = Point(vor.vertices[j])
            dio = jj.distance(po)
            low_nodes[j] = dio
        aa = sorted(low_nodes.items(),key=lambda  x:x[1],reverse=False)
        zz["coordinates"] = q["coordinates"]
        zz["dis"] = aa[0]
        look.append(zz)
        low_nodes.clear()
    look_gd = sorted(look,key=lambda x:x["dis"],reverse=False)[0]
    #print(look_gd)
    #print("看一下有没有和边界最低点连的node.............................")
    graph.add_node(look_gd["coordinates"])
    graph.add_edge(look_gd["coordinates"],look_gd["dis"][0],weight=look_gd["dis"][1])
    end_low_nodes.append(look_gd["coordinates"])
        #end_low_nodes.append(aa[0][0])
        #graph.add_node(q["coordinates"])
        #graph.add_edge(q["coordinates"],aa[0][0],weight=po.distance(Point(vor.vertices[aa[0][0]])))
        #end_low_nodes.append(q["coordinates"])
        #low_nodes.clear()
    return end_low_nodes

def _get_high_nodes2(start_end_nodes,vor,hi,all_contours_sort,graph):
    """
    原理同get_low_nodes函数。
    和get_high_nodes2的区别是 这是为小冰川准备的， 只想要一个最高点。
    :param start_end_nodes:
    :param vor:
    :param hi:
    :param all_contours_sort:
    :param graph:
    :return:
    """
    end_high_nodes = []
    high_nodes = {}
    #po = shape(points_geo1[0]["geometry"])
    #low_xy = '[{0} {1}]'.format(points_geo1[0]["geometry"]["coordinates"][0],points_geo1[0]["geometry"]["coordinates"][1]) #这是个[x y]
    #low_xy = points_geo1[0]["geometry"]["coordinates"] #这是个元组
    #print(low_xy)
    n = 0
    for v in all_contours_sort:
        if v["value"] == hi:
            n = n + 1
    #print(n)
    #print("这是边界点中， 等于最高点的点的个数。。。。。。。。。。。。")
    look = []

    for q in all_contours_sort[-n:]:
        po = Point(q["coordinates"])
        zz = {}
        for j in start_end_nodes:
            jj = Point(vor.vertices[j])
            dio = jj.distance(po)
            high_nodes[j] = dio
        aa = sorted(high_nodes.items(),key=lambda  x:x[1],reverse=False)
        zz["coordinates"] = q["coordinates"]
        zz["dis"] = aa[0]
        look.append(zz)
        high_nodes.clear()
    look_gd = sorted(look,key=lambda x:x["dis"],reverse=False)[0]
    graph.add_node(look_gd["coordinates"])
    graph.add_edge(look_gd["coordinates"],look_gd["dis"][0],weight=look_gd["dis"][1])
    end_high_nodes.append(look_gd["coordinates"])
        #end_low_nodes.append(aa[0][0])
        #graph.add_node(q["coordinates"])
        #graph.add_edge(q["coordinates"],aa[0][0],weight=po.distance(Point(vor.vertices[aa[0][0]])))
        #end_low_nodes.append(q["coordinates"])
        #low_nodes.clear()
    return end_high_nodes

def _get_high_nodes(start_end_nodes,vor,hiers,graph):
    """
    :param start_end_nodes: graph中只有一个邻居节点的节点列表。
    :param vor: 是之前生成的vor.
    :param hiers: 是大冰川特有的，对大冰川最高点的选取是一个列表，多个值。
    :param graph:
    :return: 返回每个最高点附近的最近的一个节点，最后生成总的列表。
             且向graph中添加了。
    """
    end_high_nodes = []
    high_nodes = {}
    #highest_value1 = highest_value - 200
    #n = 0
    #for v in points_geo1[1:]:
        #if v["properties"]["RASTERVALU"] < highest_value1:
            #n = n + 1
    #print(n)
    #for q in points_geo1[n:]:
    for q in hiers:
        #po = shape(q["geometry"])
        #print(q["geometry"])
        #print("我要看一看q[geometry] 到底是个啥。。。。。。。。。")
        po = Point(q["coordinates"])
        for j in start_end_nodes:
            jj = Point(vor.vertices[j])
            dio = po.distance(jj)
            high_nodes[j] = dio
        aa = sorted(high_nodes.items(),key=lambda x:x[1],reverse=False)
        #print(aa)
        #end_high_nodes.append(aa[0][0])
        #把最高点添加到graph中
        #print(aa[0][0])
        #print(po)
        #print("ceshi po aa[0][0]0000000000000000000000000000000000000000000000000")
        graph.add_node(q["coordinates"])

        graph.add_edge(q["coordinates"], aa[0][0], weight=po.distance(Point(vor.vertices[aa[0][0]])))
        end_high_nodes.append(q["coordinates"])
        high_nodes.clear()
    return end_high_nodes

def _get_longest_paths(end_low_nodes,end_high_nodes,graph):
    """
    :param end_low_nodes: source节点。
    :param end_high_nodes: target节点。
    :param graph: graph = nx.Graph（）。
    :param maxnum: 这里的maxnum参数我需要最后修改。
    :return: 返回每个最高点附近的最近的一个节点，最后生成总的列表。
    """
    def get_paths_distances():
        for node1 in end_low_nodes:
            for node2 in end_high_nodes:
                try:
                    yield nx.single_source_dijkstra(G=graph, source=node1, target=node2,weight="weight")
                except NetworkXNoPath:
                    continue
    return [x for (y,x) in sorted(get_paths_distances(),reverse=True)][:len(end_high_nodes)]

def _get_longest_path(end_low_nodes,end_high_nodes,vor,graph,name1):
    """
    在这个函数里，我做了一个判断，如果最后得到的最长路径列表是空，就跳过，记录在txt中。
    :param end_low_nodes: source节点。
    :param end_high_nodes: target节点。
    :param graph: graph = nx.Graph（）。
    :param name1: 冰川的名称。
    :param maxnum: 这里的maxnum参数我需要最后修改。
    :return: 只返回最长的那条线 or 空列表。
    """
    def get_paths_distances():
        for node1 in end_low_nodes:
            for node2 in end_high_nodes:
                try:
                    yield nx.single_source_dijkstra(G=graph, source=node1, target=node2,weight="weight")
                except NetworkXNoPath:
                    continue
    aha = [x for (y, x) in sorted(get_paths_distances(), reverse=True)]
    #print([x for (y, x) in sorted(get_paths_distances(), reverse=True)])
    #print(aha)
    #print("我看一下这个列表里有什么。。。。。。。。。。。。。。。。")
    if len(aha):
        high_xy = [x for (y, x) in sorted(get_paths_distances(), reverse=True)][0][-1]
        #high_xy = tuple(vor.vertices[high]) #这是个元组

        low_xy = [x for (y, x) in sorted(get_paths_distances(), reverse=True)][0][0]
        #low_xy = tuple(vor.vertices[low])
        #return [x for (y,x) in sorted(get_paths_distances(),reverse=True)][0], high_xy, low_xy
        return [x for (y, x) in sorted(get_paths_distances(), reverse=True)][0], high_xy, low_xy
    else:
        #print(name1)
        high_xy = 0
        low_xy = 0
        lis5 = []
        return lis5, high_xy, low_xy
    #return [x for (y,x) in sorted(get_paths_distances(),reverse=True)][0],high_xy,low_xy

def _get_single_centerline(longest_path,vor,one,low_xy,high_xy):
    """
    [
        {"type":"Feature","geometry":{"type":"LineString","coordinates":[[],[],[],[]]},"properties":{"OBJECTID":7139}}
    ]
    :param longest_path:是get_longest_path()函数的产物。
    :param vor:
    :param one:是.geojson文件里的每一条信息。
    :param low_xy:是一条冰川中的最低点的点位置坐标，它是个tuple形式。
    :return:
    """

    lis1 = list(low_xy) #元组到列表
    liss = [] #创建一个列表添加进去low_value和vor.vertices[longest_path]
    liss.append(lis1)
    aa = vor.vertices[longest_path[1:-1]].tolist() #ndarray 转list
    liss.extend(aa)
    lis2 = list(high_xy)
    liss.append(lis2)
    centerline0 = LineString(liss)
    #print(centerline0)#这个也留下，这个是没有平滑过得冰川长度线
    centerlin_sm = _smooth_linestring(centerline0, low_xy, high_xy, smooth_sigma=2)
    #centerlin_sm = centerline0
    centerline1 = []
    for i in centerlin_sm.coords:
        ll = list(i)
        centerline1.append(ll)
    name = one["properties"]["NEW_ID"]    #冰川冰川字段
    form1 = '{"type":"Feature","geometry":{"type":"LineString",'
    form2 = '"coordinates":{0}'.format(centerline1)
    form3 = '},"properties":{'
    form4 ='"NEW_ID":"{0}"'.format(name)   #冰川名称字段
    form5 = '}}'
    form = form1+form2+form3+form4+form5
    return form

def _smooth_linestring(linestring,low_xy,high_xy, smooth_sigma=2):
    """Use a gauss filter to smooth out the LineString coordinates."""
    lis1 = list(zip(np.array(filters.gaussian_filter1d(linestring.xy[0], smooth_sigma, mode='nearest', truncate=3)),np.array(filters.gaussian_filter1d(linestring.xy[1], smooth_sigma, mode='nearest', truncate=3))))
    lis2 = list(low_xy)
    lis22 = list(high_xy)
    lis3 = []
    lis3.append(lis2)
    lis3.extend(lis1)
    lis3.append(lis22)
    tuple1 =tuple(lis3)
    #tuple1 = tuple(lis1)
    return LineString(tuple1)

def _get_all_data(filename, allcenterlines):

    top_head0 = '{"type":"FeatureCollection", "features":'
    top_head1 = '{0}'.format(allcenterlines)
    top_head2 = '}'
    top_head = top_head0 + top_head1 + top_head2
    top = top_head.replace("'", " ")
    #print(top)
    with open(filename, 'w') as f:
        f.write(top)
    return

def _get_all_data1(filename, centerline):


    top_head1 = '{0}'.format(centerline)
    top_head2 = '}'
    top_head = top_head1 + top_head2
    top = top_head.replace("'", " ")
    #print(top)
    with open(filename, 'w') as f:
        f.write(top)
    return
