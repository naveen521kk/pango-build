import tempfile
from pathlib import Path
import tarfile
import shutil
import os
import subprocess
import sys
import argparse
import requests

#version to build
COMMIT_RELEASE_CAIRO="ed98414686ede45a4f2302b4521dece51acdb785"
PANGO_VERSION="1.47.0"
FRIBIDI_VERSION="1.0.10"
HARFBUZZ_VERSION="2.7.2"
GLIB_VERSION="2.67.0"
PKG_CONFIG_VERSION="1.7.0"

#argparse releated 
parser = argparse.ArgumentParser(description="Build Pango and Cairo")
parser.add_argument(
    "arch", type=str, help="The archistruture to build. On windows, vscode environment should be opened accordingly.",
    choices=["amd64","i686"], default="amd64"
)
args = parser.parse_args()

#download location and other things
final_loaction=Path("dist") / args.arch
build_dir=Path("build") / args.arch

if final_loaction.exists():
  shutil.rmtree(str(final_loaction))
if build_dir.exists():
  shutil.rmtree(str(build_dir))
def call_command(command,pwd=None):
  if pwd:
    a=subprocess.Popen(command.split(),cwd=str(pwd),stderr=subprocess.PIPE,stdout=subprocess.PIPE,env=environment_varibles)
  else:
    a=subprocess.Popen(command.split(),stderr=subprocess.PIPE,stdout=subprocess.PIPE,env=environment_varibles)
  out=a.communicate()
  if out[0].decode()!="":
    print(out[0].decode())
  if out[1].decode()!="":
    print(out[1].decode())
def download(url, target_path):
    """Download url to target_path."""
    print("Downloading {}...".format(url))
    a=requests.get(url)
    with open(target_path,"wb") as f:
      f.write(a.content)

def setup_meson():
  global meson
  print("Setting Up Meson and Ninja")
  call_command(" ".join([sys.executable,"-m","pip","install","--upgrade","pip"]))
  call_command(" ".join([sys.executable,"-m","pip","install","--upgrade","meson==0.55.3","ninja"]))
  #meson = " ".join([sys.executable,"-m","mesonbuild"]) #https://github.com/mesonbuild/meson/issues/7953
  meson = "meson"
def download_cairo():
  print("Getting Cairo...")
  with tempfile.TemporaryDirectory() as tempdir:
    tempdir=Path(tempdir)
    fname=tempdir / "cairo.tar.gz"
    download(f"https://gitlab.freedesktop.org/cairo/cairo/-/archive/{COMMIT_RELEASE_CAIRO}/cairo-{COMMIT_RELEASE_CAIRO}.tar.gz",fname)
    with tarfile.open(fname, "r:gz") as tar:
      tar.extractall(tempdir)
    shutil.move(str(tempdir/f"cairo-{COMMIT_RELEASE_CAIRO}"),str(build_dir/"cairo"))

def download_pango():
  print("Getting Pango...")
  with tempfile.TemporaryDirectory() as tempdir:
    tempdir=Path(tempdir)
    fname=tempdir / "pango.tar.gz"
    download(f"https://ftp.gnome.org/pub/GNOME/sources/pango/{'.'.join(PANGO_VERSION.split('.')[0:2])}/pango-{PANGO_VERSION}.tar.xz",fname)
    with tarfile.open(fname, "r") as tar:
      tar.extractall(tempdir)
    shutil.move(tempdir/f"pango-{PANGO_VERSION}",build_dir/"pango")

def downnload_pkg_config():
  print("Getting pkg_config...")
  with tempfile.TemporaryDirectory() as tempdir:
    tempdir=Path(tempdir)
    fname=tempdir / "pkg-config.tar.gz"
    download(f"https://github.com/pkgconf/pkgconf/archive/pkgconf-{PKG_CONFIG_VERSION}.tar.gz",fname)
    with tarfile.open(fname, "r") as tar:
      tar.extractall(tempdir)
    shutil.move(tempdir/f"pkgconf-pkgconf-{PKG_CONFIG_VERSION}",build_dir/"pkgconf")
def download_fribidi():
  print("Getting fribidi...")
  with tempfile.TemporaryDirectory() as tempdir:
    tempdir=Path(tempdir)
    fname=tempdir / "fribidi.tar.gz"
    download(f"https://github.com/fribidi/fribidi/releases/download/v{FRIBIDI_VERSION}/fribidi-{FRIBIDI_VERSION}.tar.xz",fname)
    with tarfile.open(fname, "r") as tar:
      tar.extractall(tempdir)
    shutil.move(tempdir/f"fribidi-{FRIBIDI_VERSION}",build_dir/"fribidi")
def download_harfbuzz():
  print("Getting Harfbuzz...")
  with tempfile.TemporaryDirectory() as tempdir:
    tempdir=Path(tempdir)
    fname=tempdir / "harfbuzz.tar.gz"
    download(f"https://github.com/harfbuzz/harfbuzz/releases/download/{HARFBUZZ_VERSION}/harfbuzz-{HARFBUZZ_VERSION}.tar.xz",fname)
    with tarfile.open(fname, "r") as tar:
      tar.extractall(tempdir)
    shutil.move(tempdir/f"harfbuzz-{HARFBUZZ_VERSION}",build_dir/"harfbuzz")
def download_glib():
  print("Getting Glib...")
  with tempfile.TemporaryDirectory() as tempdir:
    tempdir=Path(tempdir)
    fname=tempdir / "glib.tar.gz"
    download(f"https://ftp.gnome.org/pub/gnome/sources/glib/{'.'.join(GLIB_VERSION.split('.')[0:2])}/glib-{GLIB_VERSION}.tar.xz",fname)
    with tarfile.open(fname, "r") as tar:
      tar.extractall(tempdir)
    shutil.move(tempdir/f"glib-{GLIB_VERSION}",build_dir/"glib")

download_cairo()
downnload_pkg_config()
download_pango()
download_fribidi()
download_harfbuzz()
download_glib()

environment_varibles=os.environ
environment_varibles["PKG_CONFIG_PATH"]=""
environment_varibles["LD_LIBRARY_PATH"]=""
setup_meson()
print("Building pkg-config")
call_command(command=f"{meson} setup --prefix={(final_loaction/'pkg-config').absolute()} --buildtype=release -Dtests=false pkg_conf_build pkgconf",pwd=build_dir)
call_command(command=f"{meson} compile -C pkg_conf_build",pwd=build_dir)
call_command(command=f"{meson} install --no-rebuild -C pkg_conf_build",pwd=build_dir)
print("Setting UP pkg-config")
__lib_dir=Path(f"{list((final_loaction /'pkg-config'/'lib').iterdir())[0]}").name
print(__lib_dir)
environment_varibles["LD_LIBRARY_PATH"]=f"{(final_loaction /'pkg-config'/'lib'/__lib_dir).absolute()}"
environment_varibles["PATH"]=f"{(final_loaction/'pkg-config'/'bin').absolute()}{os.pathsep}{environment_varibles['PATH']}"
call_command(command=f"ln -sf {(final_loaction/'pkg-config'/'bin'/'pkgconf').absolute()} {(final_loaction/'pkg-config'/'bin'/'pkg-config').absolute()}",pwd=build_dir)

#glib building
print("Building Glib")
call_command(command=f"{meson} setup --default-library=shared --prefix={(final_loaction).absolute()} --buildtype=release glib_builddir glib",pwd=build_dir)
call_command(command=f"{meson} compile -C glib_builddir",pwd=build_dir)
call_command(command=f"{meson} install --no-rebuild -C glib_builddir",pwd=build_dir)

environment_varibles["PATH"]=f"{(final_loaction/'bin').absolute()}{os.pathsep}{environment_varibles['PATH']}"
environment_varibles["PKG_CONFIG_PATH"]=f"{(final_loaction/'lib'/__lib_dir/'pkgconfig').absolute()}{os.pathsep}{environment_varibles['PKG_CONFIG_PATH']}"
environment_varibles["LD_LIBRARY_PATH"]=f"{(final_loaction /'lib'/__lib_dir).absolute()}{os.pathsep}{environment_varibles['LD_LIBRARY_PATH']}"

print("Building Cairo")
#install gperf
#sudo apt-get install gperf
call_command(command=f"{meson} setup --default-library=shared --prefix={(final_loaction).absolute()} --buildtype=release -Dfontconfig=enabled -Dfreetype=enabled -Dglib=enabled -Dzlib=enabled -Dtee=enabled cairo_builddir cairo",pwd=build_dir)
call_command(command=f"{meson} compile -C cairo_builddir",pwd=build_dir)
call_command(command=f"{meson} install --no-rebuild -C cairo_builddir",pwd=build_dir)

print("Building harfbuzz")
call_command(command=f"{meson} setup --default-library=shared --prefix={(final_loaction).absolute()} --buildtype=release -Dfontconfig=enabled -Dfreetype=enabled harfbuzz_builddir harfbuzz",pwd=build_dir)
call_command(command=f"{meson} compile -C harfbuzz_builddir",pwd=build_dir)
call_command(command=f"{meson} install --no-rebuild -C harfbuzz_builddir",pwd=build_dir)

print("Building fribidi")
call_command(command=f"{meson} setup --default-library=shared --prefix={(final_loaction).absolute()} --buildtype=release fribidi_builddir fribidi",pwd=build_dir)
call_command(command=f"{meson} compile -C fribidi_builddir",pwd=build_dir)
call_command(command=f"{meson} install --no-rebuild -C fribidi_builddir",pwd=build_dir)

print("Building pango")
call_command(command=f"{meson} setup --default-library=shared --prefix={(final_loaction).absolute()} --buildtype=release -Dintrospection=false pango_builddir pango",pwd=build_dir)
call_command(command=f"{meson} compile -C pango_builddir",pwd=build_dir)
call_command(command=f"{meson} install --no-rebuild -C pango_builddir",pwd=build_dir)

print("Completed Building")
