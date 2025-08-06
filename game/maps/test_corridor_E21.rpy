label test_corridor_E21_follower:
    $ pink.otm.start_continuing_event()
    "Blob" "When I'm your follower, you can interact with me and get an event."
    $ pink.otm.add_player_follower("pink_engine/sprite_collections/sevarihk pink blob.json")
    $ follower_blob = pink.otm.get_follower("pink_engine/sprite_collections/sevarihk pink blob.json")
    $ follower_blob.event_on_activate = "test_corridor_E21_follower_event"
    $ pink.otm.end_current_event()

label test_corridor_E21_follower_event:
    $ pink.otm.start_continuing_event()
    "Blob" "I am Blob. Lord of Blobs. The only Blob follower with an event!"
    $ pink.otm.end_current_event()
