import pytest


def read_marker(pyfuncitem, marker_name):
    marker = pyfuncitem.get_marker(marker_name)
    return marker.args[0] if marker else None
