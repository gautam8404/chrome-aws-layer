# Chrome AWS Layer 
Layer to run Chrome in AWS Lambda.

## How to use?
Upload the layer to your AWS account and add it to your lambda function.
After adding check for functions in setup.py to setup chromium and libs on runtime

## Its not working anymore, how to fix it?
Go through pain and these steps:

#### Download chromium headless binary, you can do that using npx
```bash 
 npx @puppeteer/browsers install chrome-headless-shell@stable    
```

It'll be downloaded in path that looks like this
`/home/$USER/chrome-headless-shell/linux-129.0.6668.89/chrome-headless-shell-linux64`

#### Compress chromium binary using brotli
```bash
    brotli chrome-headless-shell -o chromium.br
```

#### Make a folder name `bin` in the root of the layer and put the compressed file in it.
Copy everything else in `chrome-headless-shell-linux64` folder except licenses `hyphen-data` and `locales` to `swiftshader` folder in root of layer.
Make a tar archive of swiftshader folder and compress it using brotli
This folder contents will be extracted to `/tmp` on runtime. Note only contents of swiftshader folder not the folder itself.

Copy fonts as it is from this repo (i copied from `chrome-aws-lambda` repo) to `fonts` folder in root of layer

#### Libs
you need to find all libs that chromium uses and put them in `libs` folder in root of layer. You can find them by running `ldd` on chromium binary
```bash
   ldd chrome-headless-shell 
```

You will need to copy all libs from a amazon linux docker image to preven GLIBC errors. 

```bash
    docker run -it amazonlinux:latest 
```

After getting into container install these dependencies using `yum`

```bash
alsa-lib.x86_64
atk.x86_64
cups-libs.x86_64
gtk3.x86_64
ipa-gothic-fonts
libXcomposite.x86_64
libXcursor.x86_64
libXdamage.x86_64
libXext.x86_64
libXi.x86_64
libXrandr.x86_64
libXScrnSaver.x86_64
libXtst.x86_64
pango.x86_64
xorg-x11-fonts-100dpi
xorg-x11-fonts-75dpi
xorg-x11-fonts-cyrillic
xorg-x11-fonts-misc
xorg-x11-fonts-Type1
xorg-x11-utils
```

After installing these dependencies, copy all the required libs from `/lib64` folder to `libs` folder in root of layer.
```bash
    docker cp <container_id>:/lib64/lib-name /path/to/libs
```

Same as swiftshader, make a tar archive of `libs` folder and compress it using brotli
Extract this folder to `/tmp/lib` on runtime and update `LD_LIBRARY_PATH` to include this folder.

These are all libs chromium uses at the time of writing this.

```bash
libasound.so
libasound.so.2
libasound.so.2.0.0
libatk-1.0.so
libatk-1.0.so.0
libatk-1.0.so.0.23609.1
libatk-bridge-2.0.so.0
libatk-bridge-2.0.so.0.0.0
libatspi.so.0
libatspi.so.0.0.1
libdbus-1.so.3
libdbus-1.so.3.19.17
libdbus-1.so.3.32.4
libdrm.so.2
libdrm.so.2.4.0
libEGL.so
libexpat.so.1
libexpat.so.1.8.10
libfreebl3.so
libfreeblpriv3.so
libgbm.so.1
libgbm.so.1.0.0
libGLESv2.so
libnspr4.so
libnss3.so
libnssutil3.so
libplc4.so
libplds4.so
libsoftokn3.so
libsqlite3.so.0
libsystemd.so.0
libsystemd.so.0.35.0
libudev.so.1
libudev.so.1.7.5
libuuid.so.1
libvk_swiftshader.so
libvulkan.so.1
libwayland-server.so.0
libwayland-server.so.0.22.0
libX11-xcb.so.1
libX11-xcb.so.1.0.0
libX11.so.6
libX11.so.6.4.0
libXau.so.6
libXau.so.6.0.0
libxcb.so.1
libxcb.so.1.1.0
libXcomposite.so.1
libXcomposite.so.1.0.0
libXcursor.so.1
libXcursor.so.1.0.2
libXdamage.so.1
libXdamage.so.1.1.0
libXext.so.6
libXext.so.6.4.0
libXfixes.so.3
libXfixes.so.3.1.0
libXi.so.6
libXi.so.6.1.0
libxkbcommon.so.0
libxkbcommon.so.0.0.0
libXrandr.so.2
libXrandr.so.2.2.0
libXrender.so.1
libXrender.so.1.3.0
```

#### Common issues

- `libGL error: No matching fbConfigs or visuals found` - This is because of missing `libGL` lib you can find `libGLESv2.so ` etc in `chrome-headless-shell-linux64` when you download chromium binary place them in `lib` folder in root of layer.
- `Invalid file descriptor to ICU data received` - This is because of missing `icudtl.dat` file, you can find it in `chrome-headless-shell-linux64`, place it along with chromium binary in `/tmp` on runtime.
- `libXYZ.so: cannot open shared object file: No such file or directory` - Missing lib download required packages and copy libs

- still getting missing lib errors but on lambda runtime? - Use ldd in runtime to find missing libs