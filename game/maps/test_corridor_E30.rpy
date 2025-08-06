default test_corridor_E30_something_visible = False


label test_corridor_E30_sign:
    $ pink.otm.start_continuing_event()
    """Since the Pink Engine does not transition between different scenes during events outside map changes, the default
    ren'py transition effects don't work particularly well for it. As such, the pink engine has its own distinct options
    for screen fades and shakes.

    By standing on the first pink thing in this room, you'll trigger an event that will cause a fade out, change a
    variable so as to make something appear when the screen is wholly black, and then fade back in.

    Standing on it  again will do the fade effect again, except with the something now disappearing.

    The subsequent pink things will give their own descriptions if you stand on them.
    """
    $ pink.otm.end_current_event()

label test_corridor_E30_event_1:
    $ pink.otm.start_continuing_event()

    call pink_otm_fade_in(0.25)
    $ test_corridor_E30_something_visible = not test_corridor_E30_something_visible
    call pink_otm_fade_out(0.25)

    $ pink.otm.end_current_event()


label test_corridor_E30_event_2:
    $ pink.otm.start_continuing_event()

    "With every line of dialogue..."
    $ event_overlay = pink_otm_current_map.add_overlay_solid("#000000", 0.1, 0.25)  # TODO direct
    $ saved_follower_order = [follower_object.sprite_collection_path for follower_object in pink_otm_followers]
    "...this overlay grows darker..."
    $ event_overlay.set_alpha(0.5, 0.25)
    "...and darker..."
    $ event_overlay.set_alpha(0.75, 0.25)
    "...and darker."
    $ event_overlay.set_alpha(0.9, 0.25)
    "...before suddenly..."
    $ event_overlay.set_alpha(0.0, 0.1)
    "...clearing up!"

    $ pink.otm.end_current_event()


label test_corridor_E30_event_3:
    $ pink.otm.start_continuing_event()
    "With every line of dialogue this overlay change color."
    $ event_overlay = pink_otm_current_map.add_overlay_solid("#000000", 0.1, 0.5)  # TODO direct
    $ event_overlay.set_color("#a00000", 0.5)
    "Now it's red!"
    $ event_overlay.set_color("#00a000", 0.5)
    "Now it's green!"
    $ event_overlay.set_color("#0000a0", 0.5)
    "Now it's an unknown mysterious third primary color!"
    $ event_overlay.set_alpha(0.0, 0.1)
    "Aaaaand, it's clear."

    $ pink.otm.end_current_event()


label test_corridor_E30_event_4:
    $ pink.otm.start_continuing_event()
    $ event_overlay = pink_otm_current_map.add_overlay_solid(
        "#000000", 0.1, 0.5,
        x=400, y=200, width=440, height=260)  # TODO direct
    "This overlay does not occupy the entire screen."
    $ event_overlay.set_dimensions(width=260, height=130, move_time=0.5)
    "It can change shape!"
    $ event_overlay.set_dimensions(x=620, y=10, move_time=0.5)
    "It can move around!"
    $ event_overlay.set_dimensions(x=100, y=100, width=300, height=300, move_time=0.5)
    "It can do both at the same time!"
    $ event_overlay.set_dimensions(x=-300, move_time=0.5)
    "It can even move off-screen..."
    $ event_overlay.set_dimensions(x=300, move_time=0.5)
    "And return again later!"
    $ event_overlay.set_alpha(0.0, 0.1)

    $ pink.otm.end_current_event()


label test_corridor_E30_event_5:
    $ pink.otm.start_continuing_event()
    $ event_overlay = pink_otm_current_map.add_overlay_solid(
        "#000000", 0.1, 0.5,
        x=300, y=-100, width=100, height=100)  # TODO direct
    $ event_overlay_2 = pink_otm_current_map.add_overlay_solid(
        "#000000", 0.1, 0.5,
        x=1280, y=-250, width=250, height=250)  # TODO direct
    $ event_overlay_3 = pink_otm_current_map.add_overlay_solid(
        "#000000", 0.1, 0.5,
        x=1280, y=300, width=30, height=300)  # TODO direct
    "You are not limited to having a single overlay at once"

    $ event_overlay.set_dimensions(y=0, move_time=0.5)
    $ event_overlay_2.set_dimensions(x=1030, y=0, move_time=0.5)
    $ event_overlay_3.set_dimensions(x=1250, move_time=0.5)
    "Numerous overlays can be on screen all at once."

    $ event_overlay.set_alpha(0.0, 0.1)
    $ event_overlay_2.set_dimensions(x=340, y=60, width = 600, height=600, move_time=0.5)
    $ event_overlay_3.set_color("#0000a0", 1.0)
    "These can be controlled independently of one another without issue"

    $ event_overlay_2.set_alpha(0.0, 0.1)
    $ event_overlay_3.set_alpha(0.0, 0.1)

    $ pink.otm.end_current_event()


label test_corridor_E30_event_6:
    $ pink.otm.start_continuing_event()
    $ event_overlay = pink_otm_current_map.add_overlay_image(
        "images/overlays/test_overlay.png", 0.25, 0.5)  # TODO direct
    "Overlays are not just limited to solid colors. You can use images as overlays as well."

    $ event_overlay.set_alpha(0.2, 0.25)
    "Like color overlays, image overlays can have their alpha manipulated"

    $ event_overlay.set_dimensions(x=320, y=180, width=640, height=360, move_time=0.5)
    "Or change dimensions"

    $ event_overlay.set_alpha(0.0, 0.1)

    $ pink.otm.end_current_event()

label test_corridor_E30_event_7:
    $ pink.otm.start_continuing_event()
    $ event_overlay = pink_otm_current_map.add_overlay_text(
        "OOOOOOVERLAY", 0.75, 0.5, autosize=False)  # TODO direct
    "There is also an option to use text overlays."

    $ event_overlay.set_alpha(0.25, 0.25)
    "Like other overlays, text overlays can have their alpha manipulated"

    $ event_overlay.set_dimensions(x=320, y=180, width=640, height=360, move_time=0.5)
    "Or change dimensions."
    "Though as you can see, dimensions on overlay text look kinda ugly if you stretch 'em like this."

    $ event_overlay.autosize = True
    """That's why text overlays come with the option to autosize, ensuring that they are the exact size of the
    underlying text object."""

    $ event_overlay.set_text("{b}Bold{/b} {i}Italics{/i} {color=#f00}red{/color} {size=+10}big{/size}")

    "Text overlays use ren'py text objects, so can use all built-in ren'py formatting functions."

    $ event_overlay.set_alpha(0.0, 0.1)

    $ pink.otm.end_current_event()

default test_corridor_E30_event_8_coins = 0
label test_corridor_E30_event_8:
    $ pink.otm.start_continuing_event()
    if not hasattr(renpy.store, 'E30_event_8_overlay'):
        $ E30_event_8_overlay = pink_otm_current_map.add_overlay_text(
            "Coin count: [test_corridor_E30_event_8_coins]", 0.5, 0.75, consistent=True)  # TODO direct
    else:
        $ E30_event_8_overlay.set_alpha(0.75)

    "Text overlays are very useful for UI elements."
    "You can see a coin counter at the top of your screen now"
    "You can interact with the computer to increase the coin count"

    "Note that this overlay is marked as consistent, and will persist even if you leave the room."
    "It's supposed to represent a UI element, after all."

    $ pink.otm.end_current_event()

label test_corridor_E30_computer:
    $ pink.otm.start_continuing_event()

    menu:
        "What would you like to do?"

        "Increase coin count":
            $ pink_otm_current_map.add_overlay_text(
                "{color=#0a0}Coin Count {b} + 1{/b}{/color}", alpha=0.75, fade_time=0.0, y=30,
                target_y=-30, move_time=3.5).set_alpha(0.0, 1.0)
            $ test_corridor_E30_event_8_coins += 1
        "Hide coin counter overlay":
            $ E30_event_8_overlay.set_alpha(0.0, 0.1)


    $ pink.otm.end_current_event()

label test_corridor_E30_event_9:
    $ pink.otm.start_continuing_event()
    $ event_overlay = pink_otm_current_map.add_overlay_solid(
        "#000000", 0.1, 0.5,
        x=400, y=200, width=400, height=400)  # TODO direct
    "Overlays don't have to move in a straight line. They can have an arc set."
    $ event_overlay.set_dimensions(x=620, y=10, x_arc=200, y_arc=100, move_time=0.5)

    "X arc and y arc can be set separately. The previous example included both an x and y arc"

    $ event_overlay.set_dimensions(x=220, y=10, y_arc=-200, move_time=0.5)

    "This version includes only a y arc..."

    $ event_overlay.set_dimensions(x=220, y=310, x_arc=200, move_time=0.5)

    "While this version includes only an x arc"

    $ event_overlay.set_dimensions(x=420, y=310, y_arc=200, move_time=0.5)
    call pink_otm_overlay_movement_wait(event_overlay)
    $ event_overlay.set_dimensions(x=220, y=310, y_arc=-200, move_time=0.5)

    "Movements can be chained together using movement waits, albeit with a one-frame delay between movements."

    $ event_overlay.set_alpha(0.0, 0.1)

    $ pink.otm.end_current_event()

label test_corridor_E30_event_10:
    $ pink.otm.start_continuing_event()
    $ pink_otm_current_map.stop_shaking()
    $ pink_otm_current_map.add_screen_shaker(duration=0.25, frequency=10, x_amp=15)

    "Screen shakers can be used to shake the screen without use of a ren'py transition"

    $ pink_otm_current_map.add_screen_shaker(duration=60, frequency=4, x_amp=20, y_amp=5)
    "They are mostly intended for brief shake effects, but can be made longer."

    $ pink_otm_current_map.stop_shaking()

    "Multiple screen shakers with different frequencies and phases can be combined for a more irregular effect."

    $ pink_otm_current_map.add_screen_shaker(duration=1, frequency=10, x_amp=20)
    $ pink_otm_current_map.add_screen_shaker(duration=1, frequency=8, y_amp=20, phase=0.3)

    "Like so:"

    $ pink_otm_current_map.stop_shaking()

    "Beware of using screen shakers for prolonged periods of time. The effect can be very unpleasant"

    menu:
        "Please show me the unpleasant experience":
            $ pink_otm_current_map.add_screen_shaker(duration=30, frequency=5, x_amp=50)
            $ pink_otm_current_map.add_screen_shaker(duration=30, frequency=1, x_amp=-10, phase=0.1)
            $ pink_otm_current_map.add_screen_shaker(duration=30, frequency=4, y_amp=45, phase=0.5)
            $ pink_otm_current_map.add_screen_shaker(duration=30, frequency=2, y_amp=-14, phase=0.4)

        "Okay":
            pass

    $ pink.otm.end_current_event()
