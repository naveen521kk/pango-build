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


param($arch)
Write-Output "Setting enviroment variable using vswhere"
if ($arch -eq 32) {
    Write-Output "Builing 32 bit-binaries"
    $host_arch = "x86"
    $arch = "x86"
}
else {
    Write-Output "Builing 64 bit-binaries"
    $host_arch = "amd64"
    $arch = "amd64"
}
# from https://github.com/microsoft/vswhere/wiki/Start-Developer-Command-Prompt#using-powershell
$installationPath = vswhere.exe -prerelease -latest -property installationPath
if ($installationPath -and (test-path "$installationPath\Common7\Tools\vsdevcmd.bat")) {
    & "${env:COMSPEC}" /s /c "`"$installationPath\Common7\Tools\vsdevcmd.bat`" -no_logo -host_arch=$host_arch -arch=$arch && set" | foreach-object {
        $name, $value = $_ -split '=', 2
        set-content env:\"$name" $value
    }
}

Write-Output "Setting Up Meson and Ninja"
python -m pip install --upgrade pip
pip install --upgrade https://github.com/naveen521kk/meson/archive/patch-2.zip ninja

if ($arch -eq "x86"){
    $env:PKG_CONFIG_PATH=""
    meson setup --prefix=C:\build\pkg-config --buildtype=release -Dtests=false pkg_conf_build pkgconf
    meson compile -C pkg_conf_build
    meson install --no-rebuild -C pkg_conf_build
    ln -sf C:\build\pkg-config\bin\pkgconf.exe C:\build\pkg-config\pkg-config
    Rename-Item C:\build\pkg-config\bin\pkgconf.exe pkg-config.exe -Force
}
$env:PATH="C:\build\pkg-config\bin;$env:PATH"

meson setup --default-library=shared --prefix=C:\build\$arch --buildtype=release glib_builddir glib
meson compile -C glib_builddir
meson install --no-rebuild -C glib_builddir
$env:PATH="C:\build\$arch\bin;$env:PATH"
$env:PKG_CONFIG_PATH="C:\build\$arch\lib\pkgconfig;"

Write-Output "Updating Meson"
pip install -U https://github.com/naveen521kk/meson/archive/0.56.zip

meson setup --default-library=shared --prefix=C:\build\$arch --buildtype=release -Dtests=disabled fontconfig_builddir fontconfig
meson compile -C fontconfig_builddir
meson install --no-rebuild -C fontconfig_builddir

meson setup --default-library=shared --prefix=C:\build\$arch --buildtype=release -Dfontconfig=enabled -Dfreetype=enabled -Dglib=enabled -Dzlib=enabled -Dtee=enabled cairo_builddir cairo
meson compile -C cairo_builddir
meson install --no-rebuild -C cairo_builddir

meson setup --default-library=shared --prefix=C:\build\$arch --buildtype=release -Dfontconfig=enabled -Dfreetype=enabled harfbuzz_builddir harfbuzz
meson compile -C harfbuzz_builddir
meson install --no-rebuild -C harfbuzz_builddir

meson setup --default-library=shared --prefix=C:\build\$arch --buildtype=release fribidi_builddir fribidi
meson compile -C fribidi_builddir
meson install --no-rebuild -C fribidi_builddir

meson setup --default-library=shared --prefix=C:\build\$arch --buildtype=release -Dintrospection=disabled pango_builddir pango
meson compile -C pango_builddir
meson install --no-rebuild -C pango_builddir

$env:PKG_CONFIG_PATH=""
