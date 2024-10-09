import os
import tarfile
import brotli


def setup_chromium():
    # decompress chromium
    with open('/opt/bin/chromium.br', 'rb') as f:
        compressed = f.read()

    decompressed = brotli.decompress(compressed)
    with open('/tmp/chromium', 'wb') as f:
        f.write(decompressed)
    print("Chromium decompressed")
    os.chmod('/tmp/chromium', 0o755)


def setup_fonts():
    # Set up fonts, if not already done
    home_dir = os.environ.get("HOME", "/tmp")
    font_dir = os.path.join(home_dir, ".fonts")
    os.makedirs(font_dir, exist_ok=True)
    os.system(f"cp -r /opt/fonts/* {font_dir}")

    os.environ["FONTCONFIG_PATH"] = os.path.join(home_dir, ".fonts")
    os.environ["FONTCONFIG_FILE"] = os.path.join(home_dir, ".fonts", "fonts.conf")
    print("Fonts copied")


def setup_swiftshader():
    # os.system('cp /opt/swiftshader/* /tmp/')
    # os.environ["SWIFTSHADER_PATH"] = "/tmp"
    # print("Swiftshader copied")

    path = "/opt/swiftshader.tar.br"
    with open(path, 'rb') as f:
        compressed = f.read()
    decompressed = brotli.decompress(compressed)

    with open('/tmp/swiftshader.tar', 'wb') as f:
        f.write(decompressed)

    with tarfile.open('/tmp/swiftshader.tar', 'r') as tar:
        tar.extractall('/tmp/')
    print("Swiftshader extracted")
    os.remove('/tmp/swiftshader.tar')
    os.environ["SWIFTSHADER_PATH"] = "/tmp/"
    print("SWIFTSHADER_PATH:", os.environ["SWIFTSHADER_PATH"])


def setup_libs():
    path = "/opt/lib.tar.br"
    with open(path, 'rb') as f:
        compressed = f.read()

    decompressed = brotli.decompress(compressed)

    with open('/tmp/lib.tar', 'wb') as f:
        f.write(decompressed)

    with tarfile.open('/tmp/lib.tar', 'r') as tar:
        tar.extractall('/tmp/')
    print("Libraries extracted")
    os.remove('/tmp/lib.tar')

    ld_library_path = os.environ.get("LD_LIBRARY_PATH", "")
    os.environ["LD_LIBRARY_PATH"] = "/tmp/lib:" + ld_library_path
    print("LD_LIBRARY_PATH:", os.environ["LD_LIBRARY_PATH"])

