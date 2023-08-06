import os
import numpy as np


def test_compilation():
    """
    Compile models and make sure they exist afterwards
    :return:
    """
    import os
    from compile import compile_xmile
    src = "./test_models/test_trend.stmx"
    dest = "./test_models/test_trend.py"
    target = "py"

    compile_xmile(src, dest, target)
    assert os.path.isfile(dest)

    import os
    from compile import compile_xmile
    src = "./test_models/test_if.stmx"
    dest = "./test_models/test_if.py"
    target = "py"



    compile_xmile(src, dest, target)
    assert os.path.isfile(dest)

    import os
    from compile import compile_xmile
    src = "./test_models/test_step.stmx"
    dest = "./test_models/test_step.py"
    target = "py"

    compile_xmile(src, dest, target)
    assert os.path.isfile(dest)

    from compile import compile_xmile
    src = "./test_models/test_dt_fraction.stmx"
    dest = "./test_models/test_dt_fraction.py"
    target = "py"

    compile_xmile(src, dest, target)
    assert os.path.isfile(dest)

    from compile import compile_xmile
    src = "./test_models/test_dt_rational.stmx"
    dest = "./test_models/test_dt_rational.py"
    target = "py"

    compile_xmile(src, dest, target)
    assert os.path.isfile(dest)

    from compile import compile_xmile
    src = "./test_models/test_no_dimensions.stmx"
    dest = "./test_models/test_no_dimensions.py"
    target = "py"

    compile_xmile(src, dest, target)
    assert os.path.isfile(dest)

    from compile import compile_xmile
    src = "./test_models/test_time.stmx"
    dest = "./test_models/test_time.py"
    target = "py"

    compile_xmile(src, dest, target)
    assert os.path.isfile(dest)

    from compile import compile_xmile
    src = "./test_models/test_smooth.stmx"
    dest = "./test_models/test_smooth.py"
    target = "py"

    compile_xmile(src, dest, target)
    assert os.path.isfile(dest)

    from compile import compile_xmile
    src = "./test_models/test_abs.stmx"
    dest = "./test_models/test_abs.py"
    target = "py"

    compile_xmile(src, dest, target)
    assert os.path.isfile(dest)

    from compile import compile_xmile
    src = "./test_models/test_cos.stmx"
    dest = "./test_models/test_cos.py"
    target = "py"

    compile_xmile(src, dest, target)
    assert os.path.isfile(dest)

    import os
    from compile import compile_xmile
    src = "./test_models/test_tan.stmx"
    dest = "./test_models/test_tan.py"
    target = "py"

    compile_xmile(src, dest, target)
    assert os.path.isfile(dest)

    import os
    from compile import compile_xmile
    src = "./test_models/test_sim_builtins.stmx"
    dest = "./test_models/test_sim_builtins.py"
    target = "py"

    compile_xmile(src, dest, target)
    assert os.path.isfile(dest)

    src = "./test_models/test_random.stmx"
    dest = "./test_models/test_random.py"
    target = "py"

    compile_xmile(src, dest, target)
    assert os.path.isfile(dest)

    import os
    from compile import compile_xmile
    src = "./test_models/test_array.stmx"
    dest = "./test_models/test_array.py"
    target = "py"

    compile_xmile(src, dest, target)
    assert os.path.isfile(dest)

    import os
    from compile import compile_xmile
    src = "./test_models/test_delay.stmx"
    dest = "./test_models/test_delay.py"
    target = "py"

    compile_xmile(src, dest, target)
    assert os.path.isfile(dest)

def test_trend_model():
    """
    TREND
    :return:
    """
    test_data = {1.0: 0.693147, 1.1: 0.697040160401, 1.2: 0.700323219004, 1.3: 0.703089928837, 1.4: 0.705420181666,
                 1.5: 0.707381895491,
                 1.6: 0.709032694287,
                 1.7: 0.710421386843,
                 1.8: 0.711589257659,
                 1.9: 0.712571186098,
                 2.0: 0.713396611268,
                 2.1: 0.714090360164,
                 2.2: 0.71467335582,
                 2.3: 0.71516322101,
                 2.4: 0.715574791619,
                 2.5: 0.71592055229,
                 2.6: 0.716211005471,
                 2.7: 0.716454983599,
                 2.8: 0.716659912871,
                 2.9: 0.71683203587,
                 3.0: 0.71697659933,
                 3.1: 0.717098012368,
                 3.2: 0.717199979768,
                 3.3: 0.717285614178,
                 3.4: 0.717357530533,
                 3.5: 0.717417925486,
                 3.6: 0.717468644203,
                 3.7: 0.717511236531,
                 3.8: 0.717547004206,
                 3.9: 0.717577040536,
                 4.0: 0.717602263746,
                 4.1: 0.717623444997,
                 4.2: 0.717641231926,
                 4.3: 0.717656168424,
                 4.4: 0.717668711245,
                 4.5: 0.717679243966,
                 4.6: 0.717688088705,
                 4.7: 0.717695515965,
                 4.8: 0.717701752905,
                 4.9: 0.717706990285,
                 5.0: 0.717711388292,
                 5.1: 0.717715081448,
                 5.2: 0.717718182712,
                 5.3: 0.717720786944,
                 5.4: 0.717722973802,
                 5.5: 0.717724810175,
                 5.6: 0.717726352235,
                 5.7: 0.717727647151,
                 5.8: 0.717728734532,
                 5.9: 0.71772964764,
                 6.0: 0.717730414404,
                 6.1: 0.717731058279,
                 6.2: 0.71773159896,
                 6.3: 0.717732052986,
                 6.4: 0.717732434246,
                 6.5: 0.717732754401,
                 6.6: 0.717733023245,
                 6.7: 0.717733249002,
                 6.8: 0.717733438576,
                 6.9: 0.717733597767,
                 7.0: 0.717733731445,
                 7.1: 0.717733843698,
                 7.2: 0.71773393796,
                 7.3: 0.717734017115,
                 7.4: 0.717734083584,
                 7.5: 0.717734139399,
                 7.6: 0.717734186269,
                 7.7: 0.717734225628,
                 7.8: 0.717734258678,
                 7.9: 0.717734286431,
                 8.0: 0.717734309737,
                 8.1: 0.717734329307,
                 8.2: 0.71773434574,
                 8.3: 0.71773435954,
                 8.4: 0.717734371128,
                 8.5: 0.717734380859,
                 8.6: 0.71773438903,
                 8.7: 0.717734395892,
                 8.8: 0.717734401654,
                 8.9: 0.717734406492,
                 9.0: 0.717734410556,
                 9.1: 0.717734413967,
                 9.2: 0.717734416832,
                 9.3: 0.717734419238,
                 9.4: 0.717734421258,
                 9.5: 0.717734422955,
                 9.6: 0.71773442438,
                 9.7: 0.717734425576,
                 9.8: 0.71773442658,
                 9.9: 0.717734427424,
                 10: 0.717734428132}
    from test_models.test_trend import simulation_model
    sim = simulation_model()

    assert sim.dt == 0.1
    assert sim.starttime == 1
    assert sim.stoptime == 10


    for i in np.arange(sim.starttime, sim.stoptime, sim.dt):
        i = round(i, 1)
        assert round(sim.equations['trendOfInputFunction'](i), 3) == round(test_data[i], 3)

    os.remove("test_models/test_trend.py")

def test_smooth():
    """
    SMTH1
    :return:
    """
    from test_models.test_smooth import simulation_model
    sim = simulation_model()
    assert sim.dt == 0.1
    assert sim.starttime == 1
    assert sim.stoptime == 10

    for i in np.arange(sim.starttime, sim.stoptime, sim.dt):
        assert sim.equations['exponentialAverage'](i)==sim.equations['smooth'](i)

    os.remove("test_models/test_smooth.py")


def test_abs():
    """
    ABS(x)
    :return:
    """
    import numpy as np
    import os
    from test_models.test_abs import simulation_model
    sim = simulation_model()
    assert sim.dt == 0.25
    assert sim.starttime == 1
    assert sim.stoptime == 61

    assert sum([sim.equations["stock1"](x) for x in np.arange(sim.starttime, sim.stoptime, sim.dt)]) == (
                sim.stoptime - 1) * (1 / sim.dt) * 100

    os.remove("test_models/test_abs.py")

def test_dt_fraction():
    """
    DT as fraction (1/4)
    :return:
    """
    from test_models.test_dt_fraction import simulation_model
    sim = simulation_model()
    assert sim.dt == 0.25
    assert sim.starttime == 1
    assert sim.stoptime == 61
    os.remove("test_models/test_dt_fraction.py")


def test_dt_rational():
    """
    DT rational
    :return:
    """
    from test_models.test_dt_rational import simulation_model
    sim = simulation_model()
    assert sim.dt == 0.25
    assert sim.starttime == 1
    assert sim.stoptime == 61
    os.remove("test_models/test_dt_rational.py")

def test_no_dimensions():
    """
    Simple model without dimensions.
    :return:
    """
    from test_models.test_no_dimensions import simulation_model
    sim = simulation_model()
    assert sim.dt == 0.25
    assert sim.starttime == 1
    assert sim.stoptime == 61
    os.remove("test_models/test_no_dimensions.py")

def test_time():
    """
    TIME
    :return:
    """
    from test_models.test_time import simulation_model
    sim = simulation_model()
    assert sim.dt == 0.25
    assert sim.starttime == 1
    assert sim.stoptime == 61
    os.remove("test_models/test_time.py")


def test_cos():
    """
    COS(X)
    :return:
    """
    import numpy as np
    import os
    from test_models.test_cos import simulation_model
    sim = simulation_model()
    assert sim.dt == 0.25
    assert sim.starttime == 1
    assert sim.stoptime == 61

    for i in np.arange(sim.starttime,sim.stoptime,sim.dt):
        assert sim.equations["stock1"](i) == np.cos(1.0)
    os.remove("test_models/test_cos.py")

def test_tan():
    """
    TAN(x)
    :return:
    """
    import numpy as np
    import os
    from test_models.test_tan import simulation_model
    sim = simulation_model()
    assert sim.dt == 0.25
    assert sim.starttime == 1
    assert sim.stoptime == 61

    for i in np.arange(sim.starttime,sim.stoptime,sim.dt):
        assert sim.equations["stock1"](i) == np.tan(1.0)
    os.remove("test_models/test_tan.py")

def test_sim_builtins():
    """
    DT, starttime, stoptime
    :return:
    """
    import numpy as np
    import os
    from test_models.test_sim_builtins import simulation_model
    sim = simulation_model()
    assert sim.dt == 0.25
    assert sim.starttime == 1
    assert sim.stoptime == 61

    for i in np.arange(sim.starttime,sim.stoptime,sim.dt):
        assert sim.equations["p"](i) == np.pi
        assert sim.equations["start"](i) == sim.starttime
        assert sim.equations["stop"](i) == sim.stoptime
    os.remove("test_models/test_sim_builtins.py")

def test_random():
    '''
    Random and Random with seed
    :return:
    '''
    import numpy as np
    import os
    from test_models.test_random import simulation_model
    sim = simulation_model()
    assert sim.dt == 0.25
    assert sim.starttime == 1
    assert sim.stoptime == 61

    for i in np.arange(sim.starttime,sim.stoptime,sim.dt):
        val_btw_0_10 = sim.equations['rndBetween0And10'](i)
        assert val_btw_0_10 < 10 and val_btw_0_10 > 0
        assert sim.equations["rnd"](i) == 1
        assert sim.equations["rndSeed"](i) == 1
    os.remove("test_models/test_random.py")


def test_step():
    import numpy as np
    import os
    from test_models.test_step import simulation_model
    sim = simulation_model()
    assert sim.dt == 0.25
    assert sim.starttime == 1
    assert sim.stoptime == 13

    for i in np.arange(sim.starttime, sim.stoptime, sim.dt):
        assert sim.equations["function"](i) == 100.0 if i < 4.0 else sim.equations["function"](i) == 150

    os.remove("test_models/test_step.py")



def test_delay():
    import numpy as np
    import os
    from test_models.test_delay import simulation_model
    sim = simulation_model()
    assert sim.dt == 0.25
    assert sim.starttime == 1
    assert sim.stoptime == 13

    for i in np.arange(sim.starttime, sim.stoptime, sim.dt):
        assert sim.equations["function"](i) == 100.0 if i < 5.0 else sim.equations["function"](i) == 150

    os.remove("test_models/test_delay.py")

def test_if():
    import numpy as np
    import os
    from test_models.test_if import simulation_model
    sim = simulation_model()
    assert sim.dt == 0.25
    assert sim.starttime == 1
    assert sim.stoptime == 13

    for i in np.arange(sim.starttime, sim.stoptime, sim.dt):
        print(str(i) + "\t\t" + str(sim.equations["function"](i)))
        assert sim.equations["function"](i) == 100.0 if i < 4.0 else sim.equations["function"](i) == 150

    os.remove("test_models/test_if.py")