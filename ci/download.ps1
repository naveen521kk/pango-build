$COMMIT_RELEASE = $env:COMMIT_RELEASE_CAIRO
$PANGO_VERSION = $env:PANGO_VERSION
$FRIBIDI_VERSION = $env:FRIBIDI_VERSION
$HARFBUZZ_VERSION = $env:HARFBUZZ_VERSION
$GLIB_VERSION = $env:GLIB_VERSION

echo "Getting Cairo"
curl https://gitlab.freedesktop.org/cairo/cairo/-/archive/$($COMMIT_RELEASE)/cairo-$($COMMIT_RELEASE).tar.gz -o cairo.tar.gz
tar -xf cairo.tar.gz
Move-Item -Path cairo-$COMMIT_RELEASE -Destination cairo -Force
      
echo "Getting pkg-config"
curl https://github.com/pkgconf/pkgconf/archive/pkgconf-1.7.0.zip -o pkgconf.zip
7z x pkgconf.zip
Move-Item -Path pkgconf-* -Destination pkgconf -Force

echo "Getting xz Utils"
Invoke-WebRequest https://tukaani.org/xz/xz-5.2.5-windows.zip -OutFile xz.zip
7z x xz.zip -oC:\xzUtil
$env:PATH = "C:\xzUtil\bin_x86-64;$env:PATH"

echo "Getting Pango"
Invoke-WebRequest https://ftp.gnome.org/pub/GNOME/sources/pango/$(("$PANGO_VERSION" -split '\.')[0,1] -join ".")/pango-$($PANGO_VERSION).tar.xz -OutFile pango.tar.xz
xz -d pango.tar.xz
tar -xf pango.tar
Move-Item -Path pango-* -Destination pango -Force

echo "Getting Fribidi"
Invoke-WebRequest https://github.com/fribidi/fribidi/releases/download/v$($FRIBIDI_VERSION)/fribidi-$($FRIBIDI_VERSION).tar.xz -OutFile fribidi.tar.xz
xz -d fribidi.tar.xz
tar -xf fribidi.tar
Move-Item -Path fribidi-* -Destination fribidi -Force

echo "Getting Harfbuzz"
Invoke-WebRequest https://github.com/harfbuzz/harfbuzz/releases/download/$($HARFBUZZ_VERSION)/harfbuzz-$($HARFBUZZ_VERSION).tar.xz -OutFile harfbuzz.tar.xz
xz -d harfbuzz.tar.xz
tar -xf harfbuzz.tar
Move-Item -Path harfbuzz-* -Destination harfbuzz -Force

echo "Getting Glib"
Invoke-WebRequest https://ftp.gnome.org/pub/gnome/sources/glib/$(("$GLIB_VERSION" -split '\.')[0,1] -join ".")/glib-$GLIB_VERSION.tar.xz -OutFile glib.tar.xz
xz -d glib.tar.xz
tar -xf glib.tar
Move-Item -Path glib-* -Destination glib -Force

echo "Setting Up Meson and Ninja"
$env:PATH = "C:\Python38-x64;C:\Python38-x64\Scripts;$env:PATH"
python -m pip install --upgrade pip
pip install --upgrade meson==0.55.3 ninja
      
echo "Copying x86 files"
mkdir x86
cd x86
Copy-Item -Path "$PWD\..\cairo" -Destination "$PWD\cairo" –Recurse
Copy-Item -Path "$PWD\..\pango" -Destination "$PWD\pango" –Recurse
Copy-Item -Path "$PWD\..\fribidi" -Destination "$PWD\fribidi" –Recurse
Copy-Item -Path "$PWD\..\harfbuzz" -Destination "$PWD\harfbuzz" –Recurse
Copy-Item -Path "$PWD\..\pkgconf" -Destination "$PWD\pkgconf" –Recurse
Copy-Item -Path "$PWD\..\glib" -Destination "$PWD\glib" –Recurse
cd ../

echo "Copying x64 files"
mkdir x64
cd x64
Copy-Item -Path "$PWD\..\cairo" -Destination "$PWD\cairo" –Recurse
Copy-Item -Path "$PWD\..\pango" -Destination "$PWD\pango" –Recurse
Copy-Item -Path "$PWD\..\fribidi" -Destination "$PWD\fribidi" –Recurse
Copy-Item -Path "$PWD\..\harfbuzz" -Destination "$PWD\harfbuzz" –Recurse
Copy-Item -Path "$PWD\..\pkgconf" -Destination "$PWD\pkgconf" –Recurse
Copy-Item -Path "$PWD\..\glib" -Destination "$PWD\glib" –Recurse
cd ../