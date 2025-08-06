default test_corridor_A08_devil_summoned = False

label test_corridor_A08_sign:
    $ pink.otm.start_continuing_event()
    """This room exists to test sprite collections. In the center of this room should be an interactive pentagram, which
    you can use to summon a devil."""
    $ pink.otm.end_current_event()

label test_corridor_A08_devil:
    $ pink.otm.start_continuing_event()
    "Devil" "Oh hey there, pal! How are you doing?"
    $ pink.otm.end_current_event()

label test_corridor_A08_book:
    $ pink.otm.start_continuing_event()

    if not test_corridor_A08_devil_summoned:
        "An eerie feeling comes forth from the pentagram. A book lies next to it, calling to you."

        menu:
            "Would you like to read the book?"

            "Yes":
                $ test_corridor_A08_devil_circle.stand_animation = "glow"
                """The second your eyes first glimpse the forbidden symbols of the text, the candles surrounding the
                pentagram burst into flame."""

                menu:
                    "Continue Reading?"

                    "Sure, why not?":
                        $ test_corridor_A08_devil_circle.stand_animation = "active"
                        """You are enthralled by the tome, reading its arcane symbols. Its forbidden sigils are like
                        ambrosia to your mind, eagerly consuming each and every unthinkable word."""
                        """At some point, you know not when, you realize that your mouth is now speaking aloud the inhuman
                        phrases before you."""
                        """Even if you wanted to stop, you no longer could. You have become but a vessel for the ritual. The
                        book's pages now turn without your hand, eager to see its purpose completed."""
                        $ test_corridor_A08_devil_summoned = True
                        """And with a sudden clap of thunder, the ritual has passed. You have called forth a demon. Good
                        job."""

                    "No.":
                        $ test_corridor_A08_devil_circle.stand_animation = "off"

            "Hell no":
                    pass
    $ pink.otm.end_current_event()