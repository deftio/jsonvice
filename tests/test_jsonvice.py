from jsonvice import __version__

from jsonvice.jsonvice import *

def test_version():
    assert __version__ == '0.1.1'

def test_quant():
    #test rounding
    x = quant(5)
    assert str(1.23452) == str(x(1.2345228))
    assert str(1.23457) == str(x(1.2345678))
    x = quant(5, "round")
    assert str(1.23452) == str(x(1.2345228))
    assert str(1.23457) == str(x(1.2345678))

    #test ceil
    x = quant(5, "ceil")

    assert str(1.23453) == str(x(1.2345228))
    assert str(1.23457) == str(x(1.2345678))

    #test ceil
    x = quant(5, "floor")

    assert str(1.23452) == str(x(1.2345228))
    assert str(1.23456) == str(x(1.2345678))    

def test_process_data():
    x = '{"a":123.456,\n "1":"this is it "  }'
    r = process_data(x)
    assert '{"a":123.456,"1":"this is it "}' == r

    x = '{"a":123.456,\n "1":"this is it "  }'
    r = process_data(x,2) # uses rounding
    assert '{"a":123.46,"1":"this is it "}' == r