import os,toml
from jsonvice import __version__

from jsonvice.jsonvice import *


def test_version():
    accepted_version = "1.0.1"  # this is what the release is intended to be.  
                                # every time a new release is made this needs to be updated.

    #now the next too lines make sure that the version string is set in both
    #pyproject.toml and /src/.../__init__.py are the same
    assert __version__ == accepted_version
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    assert toml.load(__location__+"/../pyproject.toml")["tool"]["poetry"]["version"] == accepted_version 

def test_quant():
    # test rounding
    x = quant(5)
    assert str(1.23452) == str(x(1.2345228))
    assert str(1.23457) == str(x(1.2345678))
    x = quant(5, "round")
    assert str(1.23452) == str(x(1.2345228))
    assert str(1.23457) == str(x(1.2345678))

    # test ceil
    x = quant(5, "ceil")

    assert str(1.23453) == str(x(1.2345228))
    assert str(1.23457) == str(x(1.2345678))

    # test ceil
    x = quant(5, "floor")

    assert str(1.23452) == str(x(1.2345228))
    assert str(1.23456) == str(x(1.2345678))


def test_process_data():
    x = '{"a":123.456,\n "1":"this is it "  }'
    r = process_data(x)
    assert '{"a":123.456,"1":"this is it "}' == r

    # test rounding
    x = '{"a":123.456,\n "1":"this is it "  }'
    r = process_data(x, 2)  # uses rounding
    assert '{"a":123.46,"1":"this is it "}' == r

    # test floor
    x = '{"a":123.456,\n "1":"this is it "  }'
    r = process_data(x, 2, "floor")  # uses rounding
    assert '{"a":123.45,"1":"this is it "}' == r

    # test ceil
    x = '{"a":123.456,\n "1":"this is it "  }'
    r = process_data(x, 2, "ceil")  # uses rounding
    assert '{"a":123.46,"1":"this is it "}' == r

    # test beautify
    x = '{"a":123.456,\n "1":"this is it "  }'
    r = process_data(x, 2, "ceil", True)  # uses rounding
    assert '{\n    "1": "this is it ",\n    "a": 123.46\n}\n' == r
