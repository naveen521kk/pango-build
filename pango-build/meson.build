project('pango-build', 'c', 'cpp',
    default_options: [
        'default_library=static',
        'buildtype=release',
        'wrap_mode=nopromote',
        'force_fallback_for=libpng,pixman,zlib,cairo,fontconfig,harfbuzz,glib,freetype2,fribidi,libffi,expat,proxy-libintl,libffi',
        'cairo:tests=disabled', # We don't need tests
        'cairo:fontconfig=enabled',
        'cairo:freetype=enabled',
        'glib:tests=false',
        'pango:fontconfig=enabled',
        'pango:freetype=enabled',
        'harfbuzz:tests=disabled',
        'glib:sysprof=disabled',
        'pango:build-testsuite=false',
        'harfbuzz:cairo=disabled', # not strictly needed and allows a recursive dependency
        'harfbuzz:freetype=disabled' # this backend not required
    ],
)

subproject('proxy-libintl')
subproject('pango')
