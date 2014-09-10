"""
Tests specific to the collections module.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import six

from nose.tools import assert_equal
import numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal

import matplotlib.pyplot as plt
import matplotlib.collections as mcollections
import matplotlib.transforms as mtransforms
from matplotlib.collections import EventCollection
from matplotlib.testing.decorators import cleanup, image_comparison


def generate_EventCollection_plot():
    '''
    generate the initial collection and plot it
    '''
    positions = np.array([0., 1., 2., 3., 5., 8., 13., 21.])
    extra_positions = np.array([34., 55., 89.])
    orientation = 'horizontal'
    lineoffset = 1
    linelength = .5
    linewidth = 2
    color = [1, 0, 0, 1]
    linestyle = 'solid'
    antialiased = True

    coll = EventCollection(positions,
                           orientation=orientation,
                           lineoffset=lineoffset,
                           linelength=linelength,
                           linewidth=linewidth,
                           color=color,
                           linestyle=linestyle,
                           antialiased=antialiased
                           )

    fig = plt.figure()
    splt = fig.add_subplot(1, 1, 1)
    splt.add_collection(coll)
    splt.set_title('EventCollection: default')
    props = {'positions': positions,
             'extra_positions': extra_positions,
             'orientation': orientation,
             'lineoffset': lineoffset,
             'linelength': linelength,
             'linewidth': linewidth,
             'color': color,
             'linestyle': linestyle,
             'antialiased': antialiased
             }
    splt.set_xlim(-1, 22)
    splt.set_ylim(0, 2)
    return splt, coll, props


@image_comparison(baseline_images=['EventCollection_plot__default'])
def test__EventCollection__get_segments():
    '''
    check to make sure the default segments have the correct coordinates
    '''
    _, coll, props = generate_EventCollection_plot()
    check_segments(coll,
                   props['positions'],
                   props['linelength'],
                   props['lineoffset'],
                   props['orientation'])


@cleanup
def test__EventCollection__get_positions():
    '''
    check to make sure the default positions match the input positions
    '''
    _, coll, props = generate_EventCollection_plot()
    np.testing.assert_array_equal(props['positions'], coll.get_positions())


@cleanup
def test__EventCollection__get_orientation():
    '''
    check to make sure the default orientation matches the input
    orientation
    '''
    _, coll, props = generate_EventCollection_plot()
    assert_equal(props['orientation'], coll.get_orientation())


@cleanup
def test__EventCollection__is_horizontal():
    '''
    check to make sure the default orientation matches the input
    orientation
    '''
    _, coll, _ = generate_EventCollection_plot()
    assert_equal(True, coll.is_horizontal())


@cleanup
def test__EventCollection__get_linelength():
    '''
    check to make sure the default linelength matches the input linelength
    '''
    _, coll, props = generate_EventCollection_plot()
    assert_equal(props['linelength'], coll.get_linelength())


@cleanup
def test__EventCollection__get_lineoffset():
    '''
    check to make sure the default lineoffset matches the input lineoffset
    '''
    _, coll, props = generate_EventCollection_plot()
    assert_equal(props['lineoffset'], coll.get_lineoffset())


@cleanup
def test__EventCollection__get_linestyle():
    '''
    check to make sure the default linestyle matches the input linestyle
    '''
    _, coll, _ = generate_EventCollection_plot()
    assert_equal(coll.get_linestyle(), [(None, None)])


@cleanup
def test__EventCollection__get_color():
    '''
    check to make sure the default color matches the input color
    '''
    _, coll, props = generate_EventCollection_plot()
    np.testing.assert_array_equal(props['color'], coll.get_color())
    check_allprop_array(coll.get_colors(), props['color'])


@image_comparison(baseline_images=['EventCollection_plot__set_positions'])
def test__EventCollection__set_positions():
    '''
    check to make sure set_positions works properly
    '''
    splt, coll, props = generate_EventCollection_plot()
    new_positions = np.hstack([props['positions'], props['extra_positions']])
    coll.set_positions(new_positions)
    np.testing.assert_array_equal(new_positions, coll.get_positions())
    check_segments(coll, new_positions,
                   props['linelength'],
                   props['lineoffset'],
                   props['orientation'])
    splt.set_title('EventCollection: set_positions')
    splt.set_xlim(-1, 90)


@image_comparison(baseline_images=['EventCollection_plot__add_positions'])
def test__EventCollection__add_positions():
    '''
    check to make sure add_positions works properly
    '''
    splt, coll, props = generate_EventCollection_plot()
    new_positions = np.hstack([props['positions'],
                               props['extra_positions'][0]])
    coll.add_positions(props['extra_positions'][0])
    np.testing.assert_array_equal(new_positions, coll.get_positions())
    check_segments(coll,
                   new_positions,
                   props['linelength'],
                   props['lineoffset'],
                   props['orientation'])
    splt.set_title('EventCollection: add_positions')
    splt.set_xlim(-1, 35)


@image_comparison(baseline_images=['EventCollection_plot__append_positions'])
def test__EventCollection__append_positions():
    '''
    check to make sure append_positions works properly
    '''
    splt, coll, props = generate_EventCollection_plot()
    new_positions = np.hstack([props['positions'],
                               props['extra_positions'][2]])
    coll.append_positions(props['extra_positions'][2])
    np.testing.assert_array_equal(new_positions, coll.get_positions())
    check_segments(coll,
                   new_positions,
                   props['linelength'],
                   props['lineoffset'],
                   props['orientation'])
    splt.set_title('EventCollection: append_positions')
    splt.set_xlim(-1, 90)


@image_comparison(baseline_images=['EventCollection_plot__extend_positions'])
def test__EventCollection__extend_positions():
    '''
    check to make sure extend_positions works properly
    '''
    splt, coll, props = generate_EventCollection_plot()
    new_positions = np.hstack([props['positions'],
                               props['extra_positions'][1:]])
    coll.extend_positions(props['extra_positions'][1:])
    np.testing.assert_array_equal(new_positions, coll.get_positions())
    check_segments(coll,
                   new_positions,
                   props['linelength'],
                   props['lineoffset'],
                   props['orientation'])
    splt.set_title('EventCollection: extend_positions')
    splt.set_xlim(-1, 90)


@image_comparison(baseline_images=['EventCollection_plot__switch_orientation'])
def test__EventCollection__switch_orientation():
    '''
    check to make sure switch_orientation works properly
    '''
    splt, coll, props = generate_EventCollection_plot()
    new_orientation = 'vertical'
    coll.switch_orientation()
    assert_equal(new_orientation, coll.get_orientation())
    assert_equal(False, coll.is_horizontal())
    new_positions = coll.get_positions()
    check_segments(coll,
                   new_positions,
                   props['linelength'],
                   props['lineoffset'], new_orientation)
    splt.set_title('EventCollection: switch_orientation')
    splt.set_ylim(-1, 22)
    splt.set_xlim(0, 2)


@image_comparison(
    baseline_images=['EventCollection_plot__switch_orientation__2x'])
def test__EventCollection__switch_orientation_2x():
    '''
    check to make sure calling switch_orientation twice sets the
    orientation back to the default
    '''
    splt, coll, props = generate_EventCollection_plot()
    coll.switch_orientation()
    coll.switch_orientation()
    new_positions = coll.get_positions()
    assert_equal(props['orientation'], coll.get_orientation())
    assert_equal(True, coll.is_horizontal())
    np.testing.assert_array_equal(props['positions'], new_positions)
    check_segments(coll,
                   new_positions,
                   props['linelength'],
                   props['lineoffset'],
                   props['orientation'])
    splt.set_title('EventCollection: switch_orientation 2x')


@image_comparison(baseline_images=['EventCollection_plot__set_orientation'])
def test__EventCollection__set_orientation():
    '''
    check to make sure set_orientation works properly
    '''
    splt, coll, props = generate_EventCollection_plot()
    new_orientation = 'vertical'
    coll.set_orientation(new_orientation)
    assert_equal(new_orientation, coll.get_orientation())
    assert_equal(False, coll.is_horizontal())
    check_segments(coll,
                   props['positions'],
                   props['linelength'],
                   props['lineoffset'],
                   new_orientation)
    splt.set_title('EventCollection: set_orientation')
    splt.set_ylim(-1, 22)
    splt.set_xlim(0, 2)


@image_comparison(baseline_images=['EventCollection_plot__set_linelength'])
def test__EventCollection__set_linelength():
    '''
    check to make sure set_linelength works properly
    '''
    splt, coll, props = generate_EventCollection_plot()
    new_linelength = 15
    coll.set_linelength(new_linelength)
    assert_equal(new_linelength, coll.get_linelength())
    check_segments(coll,
                   props['positions'],
                   new_linelength,
                   props['lineoffset'],
                   props['orientation'])
    splt.set_title('EventCollection: set_linelength')
    splt.set_ylim(-20, 20)


@image_comparison(baseline_images=['EventCollection_plot__set_lineoffset'])
def test__EventCollection__set_lineoffset():
    '''
    check to make sure set_lineoffset works properly
    '''
    splt, coll, props = generate_EventCollection_plot()
    new_lineoffset = -5.
    coll.set_lineoffset(new_lineoffset)
    assert_equal(new_lineoffset, coll.get_lineoffset())
    check_segments(coll,
                   props['positions'],
                   props['linelength'],
                   new_lineoffset,
                   props['orientation'])
    splt.set_title('EventCollection: set_lineoffset')
    splt.set_ylim(-6, -4)


@image_comparison(baseline_images=['EventCollection_plot__set_linestyle'])
def test__EventCollection__set_linestyle():
    '''
    check to make sure set_linestyle works properly
    '''
    splt, coll, _ = generate_EventCollection_plot()
    new_linestyle = 'dashed'
    coll.set_linestyle(new_linestyle)
    assert_equal(coll.get_linestyle(), [(0, (6.0, 6.0))])
    splt.set_title('EventCollection: set_linestyle')


@image_comparison(baseline_images=['EventCollection_plot__set_linewidth'])
def test__EventCollection__set_linewidth():
    '''
    check to make sure set_linestyle works properly
    '''
    splt, coll, _ = generate_EventCollection_plot()
    new_linewidth = 5
    coll.set_linewidth(new_linewidth)
    assert_equal(coll.get_linewidth(), new_linewidth)
    splt.set_title('EventCollection: set_linewidth')


@image_comparison(baseline_images=['EventCollection_plot__set_color'])
def test__EventCollection__set_color():
    '''
    check to make sure set_color works properly
    '''
    splt, coll, _ = generate_EventCollection_plot()
    new_color = np.array([0, 1, 1, 1])
    coll.set_color(new_color)
    np.testing.assert_array_equal(new_color, coll.get_color())
    check_allprop_array(coll.get_colors(), new_color)
    splt.set_title('EventCollection: set_color')


def check_segments(coll, positions, linelength, lineoffset, orientation):
    '''
    check to make sure all values in the segment are correct, given a
    particular set of inputs

    note: this is not a test, it is used by tests
    '''
    segments = coll.get_segments()
    if (orientation.lower() == 'horizontal'
            or orientation.lower() == 'none' or orientation is None):
        # if horizontal, the position in is in the y-axis
        pos1 = 1
        pos2 = 0
    elif orientation.lower() == 'vertical':
        # if vertical, the position in is in the x-axis
        pos1 = 0
        pos2 = 1
    else:
        raise ValueError("orientation must be 'horizontal' or 'vertical'")

    # test to make sure each segment is correct
    for i, segment in enumerate(segments):
        assert_equal(segment[0, pos1], lineoffset + linelength / 2.)
        assert_equal(segment[1, pos1], lineoffset - linelength / 2.)
        assert_equal(segment[0, pos2], positions[i])
        assert_equal(segment[1, pos2], positions[i])


def check_allprop(values, target):
    '''
    check to make sure all values match the given target

    note: this is not a test, it is used by tests
    '''
    for value in values:
        assert_equal(value, target)


def check_allprop_array(values, target):
    '''
    check to make sure all values match the given target if arrays

    note: this is not a test, it is used by tests
    '''
    for value in values:
        np.testing.assert_array_equal(value, target)


def test_null_collection_datalim():
    col = mcollections.PathCollection([])
    col_data_lim = col.get_datalim(mtransforms.IdentityTransform())
    assert_array_equal(col_data_lim.get_points(),
                       mtransforms.Bbox.null().get_points())


@cleanup
def test_add_collection():
    # Test if data limits are unchanged by adding an empty collection.
    # Github issue #1490, pull #1497.
    ax = plt.axes()
    plt.figure()
    ax2 = plt.axes()
    coll = ax2.scatter([0, 1], [0, 1])
    ax.add_collection(coll)
    bounds = ax.dataLim.bounds
    coll = ax2.scatter([], [])
    ax.add_collection(coll)
    assert_equal(ax.dataLim.bounds, bounds)


@cleanup
def test_quiver_limits():
    ax = plt.axes()
    x, y = np.arange(8), np.arange(10)
    data = u = v = np.linspace(0, 10, 80).reshape(10, 8)
    q = plt.quiver(x, y, u, v)
    assert_equal(q.get_datalim(ax.transData).bounds, (0., 0., 7., 9.))

    plt.figure()
    ax = plt.axes()
    x = np.linspace(-5, 10, 20)
    y = np.linspace(-2, 4, 10)
    y, x = np.meshgrid(y, x)
    trans = mtransforms.Affine2D().translate(25, 32) + ax.transData
    plt.quiver(x, y, np.sin(x), np.cos(y), transform=trans)
    assert_equal(ax.dataLim.bounds, (20.0, 30.0, 15.0, 6.0))


@cleanup
def test_barb_limits():
    ax = plt.axes()
    x = np.linspace(-5, 10, 20)
    y = np.linspace(-2, 4, 10)
    y, x = np.meshgrid(y, x)
    trans = mtransforms.Affine2D().translate(25, 32) + ax.transData
    plt.barbs(x, y, np.sin(x), np.cos(y), transform=trans)
    # The calculated bounds are approximately the bounds of the original data,
    # this is because the entire path is taken into account when updating the
    # datalim.
    assert_array_almost_equal(ax.dataLim.bounds, (20, 30, 15, 6),
                              decimal=1)


@image_comparison(baseline_images=['EllipseCollection_test_image'],
                  extensions=['png'],
                  remove_text=True)
def test_EllipseCollection():
    # Test basic functionality
    fig, ax = plt.subplots()
    x = np.arange(4)
    y = np.arange(3)
    X, Y = np.meshgrid(x, y)
    XY = np.vstack((X.ravel(), Y.ravel())).T

    ww = X/float(x[-1])
    hh = Y/float(y[-1])
    aa = np.ones_like(ww) * 20  # first axis is 20 degrees CCW from x axis

    ec = mcollections.EllipseCollection(ww, hh, aa,
                                        units='x',
                                        offsets=XY,
                                        transOffset=ax.transData,
                                        facecolors='none')
    ax.add_collection(ec)
    ax.autoscale_view()


@image_comparison(baseline_images=['polycollection_close'],
                  extensions=['png'], remove_text=True)
def test_polycollection_close():
    from mpl_toolkits.mplot3d import Axes3D

    vertsQuad = [
        [[0., 0.], [0., 1.], [1., 1.], [1., 0.]],
        [[0., 1.], [2., 3.], [2., 2.], [1., 1.]],
        [[2., 2.], [2., 3.], [4., 1.], [3., 1.]],
        [[3., 0.], [3., 1.], [4., 1.], [4., 0.]]]

    fig = plt.figure()
    ax = Axes3D(fig)

    colors = ['r', 'g', 'b', 'y', 'k']
    zpos = list(range(5))

    poly = mcollections.PolyCollection(
        vertsQuad * len(zpos), linewidth=0.25)
    poly.set_alpha(0.7)

    ## need to have a z-value for *each* polygon = element!
    zs = []
    cs = []
    for z, c in zip(zpos, colors):
        zs.extend([z] * len(vertsQuad))
        cs.extend([c] * len(vertsQuad))

    poly.set_color(cs)

    ax.add_collection3d(poly, zs=zs, zdir='y')

    ## axis limit settings:
    ax.set_xlim3d(0, 4)
    ax.set_zlim3d(0, 3)
    ax.set_ylim3d(0, 4)


if __name__ == '__main__':
    import nose
    nose.runmodule(argv=['-s', '--with-doctest'], exit=False)
