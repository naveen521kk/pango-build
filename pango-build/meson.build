project('pango-build', 'c', 'cpp',
    default_options: [
        'default_library=static',
        'buildtype=release',
        'wrap_mode=nopromote',
        'force_fallback_for=libpng,pixman,zlib,cairo,fontconfig,harfbuzz,glib,freetype,fribidi,libffi,expat,proxy-libintl',
        'cairo:tests=disabled', # We don't need tests
        'cairo:fontconfig=enabled',
        'cairo:freetype=enabled',
        'glib:tests=false',
        'pango:fontconfig=enabled',
        'pango:freetype=enabled',
        'harfbuzz:tests=disabled',
        'glib:sysprof=disabled',
        'pango:build-testsuite=false'
    ],
)

subproject('proxy-libintl')
subproject('pango')
