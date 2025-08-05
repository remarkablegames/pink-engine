<p align="center">
  <img src="https://raw.githubusercontent.com/remarkablegames/pink-engine/master/game/gui/window_icon.png" alt="Pink Engine">
</p>

# Pink Engine

![release](https://img.shields.io/github/v/release/remarkablegames/pink-engine)
[![build](https://github.com/remarkablegames/pink-engine/actions/workflows/build.yml/badge.svg)](https://github.com/remarkablegames/pink-engine/actions/workflows/build.yml)
[![lint](https://github.com/remarkablegames/pink-engine/actions/workflows/lint.yml/badge.svg)](https://github.com/remarkablegames/pink-engine/actions/workflows/lint.yml)

♦️ Create Ren'Py games with [Pink Engine](https://pink-productions.itch.io/pink-engine).

Play the game on:

- [remarkablegames](https://remarkablegames.org/pink-engine)

## Credits

### Art

- [Uncle Mugen](https://lemmasoft.renai.us/forums/viewtopic.php?t=17302)

### Audio

- [Kenney](https://kenney.nl/assets/interface-sounds)

## Prerequisites

Download [Ren'Py SDK](https://www.renpy.org/latest.html):

```sh
git clone https://github.com/remarkablegames/renpy-sdk.git
```

Symlink `renpy`:

```sh
sudo ln -sf "$(realpath renpy-sdk/renpy.sh)" /usr/local/bin/renpy
```

Check the version:

```sh
renpy --version
```

## Install

Clone the repository to the `Projects Directory`:

```sh
git clone https://github.com/remarkablegames/pink-engine.git
cd pink-engine
```

Rename the project:

```sh
git grep -l "Pink Engine" | xargs sed -i '' -e "s/Pink Engine/My Game/g"
```

```sh
git grep -l 'pink-engine' | xargs sed -i '' -e 's/pink-engine/my-game/g'
```

Replace the assets:

- [ ] `web-presplash.jpg`
- [ ] `game/gui/main_menu.png`
- [ ] `game/gui/window_icon.png`

## Run

Launch the project:

```sh
renpy .
```

Or open the `Ren'Py Launcher`:

```sh
renpy
```

Press `Shift`+`R` to reload the game.

Press `Shift`+`D` to open the developer menu.

## Cache

Clear the cache:

```sh
find game -name "*.rpyc" -delete
```

Or open `Ren'Py Launcher` > `Force Recompile`:

```sh
renpy
```

## Lint

Lint the game:

```sh
renpy game lint
```

## License

[MIT](LICENSE)
