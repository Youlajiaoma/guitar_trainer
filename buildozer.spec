[app]

# (str) Title of your application
title = Guitar Trainer

# (str) Package name
package.name = guitar_trainer

# (str) Package domain (reverse DNS style)
package.domain = org.example

# (str) Source code filename
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# (str) Main application entry point file
entrypoint = main.py

# (str) Supported orientation (one of: portrait, landscape, all)
orientation = portrait

# (str) Application versioning (version name and code)
version = 0.1
version.code = 1

# (list) Application requirements (modules to be installed)
requirements = python3,kivy

# (str) Icon of the app
icon.filename = %(source.dir)s/icon.png

# (str) Supported Android API level
android.api = 33

# (int) Minimum Android API your APK will support
android.minapi = 21

# (int) Android SDK build tools version
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (bool) If True, then the apk will be signed with debug keys.
android.debug = 1

# (list) Permissions
android.permissions = INTERNET

[buildozer]

log_level = 2
warn_on_root = 1
