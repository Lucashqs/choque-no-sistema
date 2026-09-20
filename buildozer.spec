[app]

title = Choque no Sistema
package.name = choquenosistema
package.domain = com.choquenosistema
version = 0.1

source.dir = .
source.include_exts = py,png,jpg,mp3,wav,ttf

requirements = python3,pygame

orientation = portrait
fullscreen = 1

android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_licenses = True

# Definição apenas da arquitetura moderna de 64 bits (evita erros no SDL2_mixer)
android.archs = arm64-v8a

[buildozer]
log_level = 2
