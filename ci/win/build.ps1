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
if ($arch -eq "x86"){
    $env:PKG_CONFIG_PATH=""
    meson setup --prefix=C:\build\pkg-config --buildtype=release -Dtests=false pkg_conf_build pkgconf
    meson compile -C pkg_conf_build
    meson install --no-rebuild -C pkg_conf_build
    ln -sf C:\build\pkg-config\bin\pkgconf.exe C:\build\pkg-config\pkg-config
    Rename-Item C:\build\pkg-config\bin\pkgconf.exe pkg-config.exe -Force
}
$env:PATH="C:\build\pkg-config\bin;$env:PATH"
# Apply Patch to cairo meson.build
#& "C:\Program Files\Git\bin\bash" -lc "patch -u cairo/meson.build ../patches/cairo.meson.build.patch"

meson setup --default-library=shared --prefix=C:\build\$arch --buildtype=release glib_builddir glib
meson compile -C glib_builddir
meson install --no-rebuild -C glib_builddir
$env:PATH="C:\build\$arch\bin;$env:PATH"
$env:PKG_CONFIG_PATH="C:\build\$arch\lib\pkgconfig;"

meson setup --default-library=shared --prefix=C:\build\$arch --buildtype=release -Dfontconfig=enabled -Dfreetype=enabled -Dglib=enabled -Dzlib=enabled -Dtee=enabled cairo_builddir cairo
cd cairo_builddir
(Get-Content build.ninja) -replace '"/MD"','"/MT"' | Out-File build.ninja.patch
Move-Item build.ninja.patch build.ninja -Force
cd ../
meson compile -C cairo_builddir
meson install --no-rebuild -C cairo_builddir

meson setup --default-library=shared --prefix=C:\build\$arch --buildtype=release -Dfontconfig=enabled -Dfreetype=enabled harfbuzz_builddir harfbuzz
meson compile -C harfbuzz_builddir
meson install --no-rebuild -C harfbuzz_builddir

meson setup --default-library=shared --prefix=C:\build\$arch --buildtype=release fribidi_builddir fribidi
meson compile -C fribidi_builddir
meson install --no-rebuild -C fribidi_builddir

meson setup --default-library=shared --prefix=C:\build\$arch --buildtype=release -Dintrospection=disabled pango_builddir pango
cd pango_builddir
(Get-Content build.ninja) -replace '"/MD"','"/MT"' | Out-File build.ninja.patch
Move-Item build.ninja.patch build.ninja -Force
cd ../
meson compile -C pango_builddir
meson install --no-rebuild -C pango_builddir

$env:PKG_CONFIG_PATH=""
