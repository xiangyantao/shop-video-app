[app]
title = 扫码摄像
package.name = shopvideo
package.domain = org.myapp
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

orientation = portrait
fullscreen = 0

android.api = 33
android.sdk = 24
android.ndk = 25b
android.archs = arm64-v8a armeabi-v7a
android.permissions = CAMERA RECORD_AUDIO READ_EXTERNAL_STORAGE WRITE_EXTERNAL_STORAGE

requirements = python3,kivy,zbar,pyzbar,jnius

[buildozer]
log_level = 2
warn_on_root = 1