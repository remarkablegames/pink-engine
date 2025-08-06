default test_corridor_A25_plant_1 = True
default test_corridor_A25_plant_2 = True
default test_corridor_A25_plant_3 = True
default test_corridor_A25_plant_4 = True
default test_corridor_A25_plant_5 = True
default test_corridor_A25_plant_6 = True

init python:
    def test_corridor_A25_plant_interaction(variable_name, delay):
        setattr(renpy.store, variable_name, False)
        renpy.store.otm_timer.add_timed_code(renpy.store.otm_timer.time + delay, 'renpy.store.' + variable_name + ' = True')

label test_corridor_A25_sign:
    $ pink.otm.start_continuing_event()
    """This room exists to test timed code. Each flower in this room can be interacted with, causing them to vanish.

    They will respawn after a certain number of seconds has passed. The bottom flower will take 1 second, with the
    amount of time doubling for each flower after that.

    The respawn timer will continue even when you leave this map. As long as you are on some kind of OTM map, it will
    keep increasing."""
    $ pink.otm.end_current_event()
