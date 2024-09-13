# Pango Build

`pango-build` is mainly used for creating wheels for [ManimPango](https://github.com/manimcommunity/manim). It provides a static Windows and macOS build of pango including all its dependencies which ManimPango uses for its binary Windows and macOS wheels.

In addition to pango it also provides a static build of
[pkgconf](https://github.com/pkgconf/pkgconf) which is required by ManimPango
during its wheel build process for locating dependencies.

The build process is based on the [meson](https://mesonbuild.com/) build system
and uses Visual Studio on GitHub Actions to automatically build and publish
everything. See the [workflow file](.github/workflows/main.yml) for details. You
can of course also build everything locally yourself, see the instructions
below.

## Manual build instructions

```bash
# install meson and ninja
pip install -r requirements.txt

# build pango
cd pango-build
meson setup buildDir --prefix=/
meson compile -C buildDir
meson install -C buildDir --destdir ../dist
# see ./dist for the result

# build pkgconf
cd ../pkgconf-build
meson setup buildDir --prefix=/
meson compile -C buildDir
meson install -C buildDir --destdir ../dist
# see ./dist for the result
```

## Updating dependencies

All dependencies and pango itself are included via the [meson wrap
system](https://mesonbuild.com/Wrap-dependency-system-manual.html) and we depend
on the [meson WrapDB](https://github.com/mesonbuild/wrapdb) for updates. The
following is required to pull in new versions from pypi and wrapdb:

```bash
# manually update meson/ninja in requirements.txt
pip install -r requirements.txt
# update wrap files from wrapdb
meson wrap update --sourcedir pango-build
meson wrap update --sourcedir pkgconf-build
```

## Creating a new release

- Create a new release in the GH UI
- GHA will do the rest

## License

All the build script are licensed under Apache License 2.0, and the binaries in release section
is under LGPL same as Pango's license.
