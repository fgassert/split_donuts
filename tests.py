

from split_donuts import *
from shapely.ops import cascaded_union
from join_donuts import *

def test_split():
    print "Split donut by interior point"
    donut = sg.Point(0, 0).buffer(2.0).difference(sg.Point(0, 0).buffer(1.0))
    center = donut.centroid
    res = split_horiz_by_point(donut, center)
    print "Parts (should be 2): %s" % len(res)
    dif = cascaded_union(res).symmetric_difference(donut).area
    print "Difference: %s" % dif

    print "Split donut by exterior point"
    side = sg.Point(4,4)
    res = split_horiz_by_point(donut, side)
    print "Parts (should be 1): %s" % len(res)
    dif = cascaded_union(res).symmetric_difference(donut).area
    print "Difference: %s" % dif

def test_check_split():
    print "Check if a donut needs to be split"
    donut = sg.Point(0, 0).buffer(2.0).difference(sg.Point(0, 0).buffer(1.0))
    res = check_split_multipoly(donut)
    print "Parts (should be 2): %s" % len(res)
    dif = cascaded_union(res).symmetric_difference(donut).area
    print "Difference: %s" % dif


    print "Check if a multipoly needs to be split"
    multi = sg.MultiPoint([(0, 0),(4, 0)]).buffer(2.0)
    res = check_split_multipoly(multi)
    print "Parts (should be 2): %s" % len(res)
    dif = cascaded_union(res).symmetric_difference(multi).area
    print "Difference: %s" % dif


    print "Check if a complex multipoly needs to be split"
    cx = sg.MultiPoint([(0, 0),(4, 0)]).buffer(2.0).difference(sg.Point(0, 0).buffer(1.0))
    res = check_split_multipoly(cx)
    print "Parts (should be 3): %s" % len(res)
    dif = cascaded_union(res).symmetric_difference(cx).area
    print "Difference: %s" % dif

def test_split_shp():
    print "splitting multip.shp"
    split_donuts("multip.shp","out.shp")
    with fiona.open("out.shp") as source:
        print "Parts (should be 7): %s" % len(source)

def test_closest_pt():
    print "Check closest point in r=3 circle to 1,1"
    donut = sg.Point(0, 0).buffer(3.0)
    exter = np.asarray(donut.exterior)
    res = closest_pt((1,1),exter)
    
    print "Closest point (should be (2.1,2.1)): %s" % exter[res]

def test_join():
    print "Check if a donut needs to be split"
    donut = sg.Point(0, 0).buffer(3.0).difference(sg.Point(0, 1).buffer(1.0))
    res = lazy_short_join_poly(donut)
    print "Interiors (should be 0): %s" % len(res.interiors)
    dif = res.symmetric_difference(donut).area
    print "Difference: %s" % dif
    
def test_split_join():
    print "Check if a complex multipoly needs to be split"
    cx = sg.MultiPoint([(0, 0),(6, 0)]).buffer(2.5).difference(sg.Point(1, 0).buffer(.5))
    res = lazy_short_join_multipoly(cx)
    print "Parts (should be 2): %s" % len(res)
    print "Interiors (should be 0): %s" % sum([len(r.interiors) for r in res])
    dif = cascaded_union(res).symmetric_difference(cx).area
    print "Difference: %s" % dif

def test_join_shp():
    print "splitting multip.shp"
    join_donuts("multip.shp","outjoin.shp")
    with fiona.open("outjoin.shp") as source:
        print "Parts (should be 5): %s" % len(source)    

if __name__ == "__main__":
    test_closest_pt()
    test_join()
    test_split_join()
    test_join_shp()
    test_split()
    test_check_split()
    test_split_shp()
    
