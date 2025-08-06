default E31_time_of_day = 7
default E_31_morning_light = ('#00ffd3', 0.05)
default E_31_midday_light = ('#e9ff00', 0.03)
default E_31_afternoon_light = ('#ffd600', 0.05)
default E_31_evening_light = ('#24221e', 0.5)
default E_31_night_light = ('#16140f', 0.7)

init python:
    def test_corridor_E31_travel():
        renpy.store.E31_time_of_day += 1
        if renpy.store.E31_time_of_day > 23:
            renpy.store.E31_time_of_day -= 24

    def test_corridor_E31_get_color_alpha_for_time(time):
        if time >= 23:
            color, alpha = E_31_night_light
        elif time >= 20:
            color, alpha = E_31_evening_light
        elif time >= 18:
            color, alpha = E_31_afternoon_light
        elif time >= 12:
            color, alpha = E_31_midday_light
        elif time >= 6:
            color, alpha = E_31_morning_light
        elif time >= 5:
            color, alpha = E_31_evening_light
        else:
            color, alpha = E_31_night_light
        return color, alpha

    def test_corridor_E31_outdoor_room():
        old_color, old_alpha = test_corridor_E31_get_color_alpha_for_time(E31_time_of_day - 1)
        new_color, new_alpha = test_corridor_E31_get_color_alpha_for_time(E31_time_of_day)

        renpy.store.E31_outdoor_overlay = pink_otm_current_map.add_overlay_solid(old_color, 0.0, old_alpha)
        pink_otm_current_map.add_overlay_text("Current time: [E31_time_of_day]:00", 0.0, x=1000, y=10)

        renpy.store.E31_outdoor_overlay.set_color(new_color, 3.0)
        renpy.store.E31_outdoor_overlay.set_alpha(new_alpha, 3.0)