# Copyright 2021 Naveen M K

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#note: Should be invoked from root of repo
$versions = Get-Content .\versions.json | ConvertFrom-Json 
$COMMIT_RELEASE = $versions.cairo
$PANGO_VERSION = $versions.pango
$FRIBIDI_VERSION = $versions.fribidi
$HARFBUZZ_VERSION = $versions.harfbuzz
$GLIB_VERSION = $versions.glib
$FONTCONFIG_VERSION = $versions.fontconfig

Write-Output "Getting Cairo"
curl https://gitlab.freedesktop.org/cairo/cairo/-/archive/$($COMMIT_RELEASE)/cairo-$($COMMIT_RELEASE).tar.gz -o cairo.tar.gz
tar -xf cairo.tar.gz
Move-Item -Path cairo-$COMMIT_RELEASE -Destination cairo -Force
      
Write-Output "Getting pkg-config"
curl https://github.com/pkgconf/pkgconf/archive/pkgconf-1.7.0.zip -o pkgconf.zip
7z x pkgconf.zip
Move-Item -Path pkgconf-* -Destination pkgconf -Force

Write-Output "Getting xz Utils"
curl https://tukaani.org/xz/xz-5.2.5-windows.zip -OutFile xz.zip
7z x xz.zip -oC:\xzUtil
$env:PATH = "C:\xzUtil\bin_x86-64;$env:PATH"

Write-Output "Getting Pango"
curl https://ftp.gnome.org/pub/GNOME/sources/pango/$(("$PANGO_VERSION" -split '\.')[0,1] -join ".")/pango-$($PANGO_VERSION).tar.xz -OutFile pango.tar.xz
xz -d pango.tar.xz
tar -xf pango.tar
Move-Item -Path pango-* -Destination pango -Force

Write-Output "Getting Fribidi"
curl https://github.com/fribidi/fribidi/releases/download/v$($FRIBIDI_VERSION)/fribidi-$($FRIBIDI_VERSION).tar.xz -OutFile fribidi.tar.xz
xz -d fribidi.tar.xz
tar -xf fribidi.tar
Move-Item -Path fribidi-* -Destination fribidi -Force

Write-Output "Getting Harfbuzz"
curl https://github.com/harfbuzz/harfbuzz/releases/download/$($HARFBUZZ_VERSION)/harfbuzz-$($HARFBUZZ_VERSION).tar.xz -OutFile harfbuzz.tar.xz
xz -d harfbuzz.tar.xz
tar -xf harfbuzz.tar
Move-Item -Path harfbuzz-* -Destination harfbuzz -Force

Write-Output "Getting Glib"
curl https://ftp.gnome.org/pub/gnome/sources/glib/$(("$GLIB_VERSION" -split '\.')[0,1] -join ".")/glib-$GLIB_VERSION.tar.xz -OutFile glib.tar.xz
xz -d glib.tar.xz
tar -h -xf glib.tar
Move-Item -Path glib-* -Destination glib -Force

Write-Output "Getting FontConfig"
curl https://gitlab.freedesktop.org/fontconfig/fontconfig/-/archive/$($FONTCONFIG_VERSION)/fontconfig-$($FONTCONFIG_VERSION).tar.gz -o fontconfig.tar.gz
tar -xf fontconfig.tar.gz
Move-Item -Path fontconfig-$FONTCONFIG_VERSION -Destination fontconfig -Force

Write-Output "Copying x86 files"
mkdir x86
Set-Location x86
Copy-Item -Path "$PWD\..\cairo" -Destination "$PWD\cairo" -Recurse -Force
Copy-Item -Path "$PWD\..\pango" -Destination "$PWD\pango" -Recurse -Force
Copy-Item -Path "$PWD\..\fribidi" -Destination "$PWD\fribidi" -Recurse -Force
Copy-Item -Path "$PWD\..\harfbuzz" -Destination "$PWD\harfbuzz" -Recurse -Force
Copy-Item -Path "$PWD\..\pkgconf" -Destination "$PWD\pkgconf" -Recurse -Force
Copy-Item -Path "$PWD\..\glib" -Destination "$PWD\glib" -Recurse -Force
Copy-Item -Path "$PWD\..\fontconfig" -Destination "$PWD\fontconfig" -Recurse -Force
Set-Location ../

Write-Output "Copying x64 files"
mkdir x64
Set-Location x64
Copy-Item -Path "$PWD\..\cairo" -Destination "$PWD\cairo" -Recurse -Force
Copy-Item -Path "$PWD\..\pango" -Destination "$PWD\pango" -Recurse -Force
Copy-Item -Path "$PWD\..\fribidi" -Destination "$PWD\fribidi" -Recurse -Force
Copy-Item -Path "$PWD\..\harfbuzz" -Destination "$PWD\harfbuzz" -Recurse -Force
Copy-Item -Path "$PWD\..\pkgconf" -Destination "$PWD\pkgconf" -Recurse -Force
Copy-Item -Path "$PWD\..\glib" -Destination "$PWD\glib" -Recurse -Force
Copy-Item -Path "$PWD\..\fontconfig" -Destination "$PWD\fontconfig" -Recurse -Force
Set-Location ../
