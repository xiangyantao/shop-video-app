[app]
title = ShopVideoApp
package.name = shopvideoapp
package.domain = org.example
source.dir = .
source.include_main = True
main.py = main.py
version = 0.1
requirements = python3,kivy==2.2.1,requests==2.31.0,pillow==10.0.1
orientation = portrait
osx.python_version = 3
osx.kivy_version = 2.2.1
android.ndk = 25b
android.sdk = 24
android.api = 33
android.ndk_path = 
android.sdk_path = 
android.add_androidx = True
android.arch = arm64-v8a,armeabi-v7a
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.debug = True
android.enable_androidx = True
android.gradle_dependencies = 
p4a.branch = master
[p4a]
android.ndk = 25b
android.sdk = 24
[buildozer]
log_level = 2
warn_on_root = 1
build_dir = ./buildozer_build
cache_dir = ./buildozer_cache
