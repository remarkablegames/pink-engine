default pink_otm_E05_time = "morning"
default pink_otm_E05_npc_state = "morning"

init python:
    def pink_otm_E05_time_change():
        if store.pink_otm_E05_time == "morning":
            store.pink_otm_E05_time = "noon"
            if store.pink_otm_E05_npc_state != "morning":
                store.pink_otm_E05_npc_state = "noon"
        elif store.pink_otm_E05_time == "noon":
            store.pink_otm_E05_time = "afternoon"
            if store.pink_otm_E05_npc_state != "noon":
                store.pink_otm_E05_npc_state = "afternoon"
        elif store.pink_otm_E05_time == "afternoon":
            store.pink_otm_E05_time = "evening"
            if store.pink_otm_E05_npc_state != "afternoon":
                store.pink_otm_E05_npc_state = "evening"
        elif store.pink_otm_E05_time == "evening":
            store.pink_otm_E05_time = "night"
            store.pink_otm_E05_npc_state = "night"
        elif store.pink_otm_E05_time == "night":
            store.pink_otm_E05_time = "morning"
            if store.pink_otm_E05_npc_state != "night":
                store.pink_otm_E05_npc_state = "morning"

    def pink_otm_E05_npc_timeset():
        store.pink_otm_E05_npc_state = store.pink_otm_E05_time

    def pink_otm_E05_room_enter():
        store.pink_otm_E05_npc_state = pink_otm_E05_time

    def pink_otm_E05_room_leave():
        store.pink_otm_E05_npc_state = pink_otm_E05_time

label test_corridor_E05_night_pc_removal:
    $ pink.otm.start_dynamic_event()
    "This room is closed during night and the morning. You shall be yeeted out accordingly."
    $ pink.otm.go_to_map(target_map='test_corridor_E05a.json', x_coord=2, y_coord=3, orientation="down")

label test_corridor_E05_closed_door:
    $ pink.otm.start_dynamic_event()
    "The door is closed at morning and during the night."
    $ pink.otm.end_current_event()

label test_corridor_E05_computer:
    $ pink.otm.start_dynamic_event()
    "The current time is: [pink_otm_E05_time]"
    menu:
        "Would you like to advance time?"

        "Yes":
            $ pink_otm_E05_time_change()
        "No":
            pass

    $ pink.otm.end_current_event()