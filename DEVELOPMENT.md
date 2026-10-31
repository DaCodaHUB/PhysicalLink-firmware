# Firmware development

This repository is an independent development project for the PhysicalLink library.
`src/`, `library.json`, API.md, LICENSE, and the packaged examples retain the existing
0.9.1 library contents. Root README.md is retained as existing package content;
its 0.9.0/monorepo installation statements are historical. The current manifest is
0.9.1 and the library lives at this repository root. No release is performed by
these local development commands.

## Build and upload

Install PlatformIO Core, CMake, Python 3, and a C++ compiler (Visual Studio 2022 or newer C++
tools on Windows). Run commands from this repository root. The pinned target is
ESP32-WROOM-32, esp32dev, espressif32 7.1.3, Arduino, NimBLE-Arduino 2.5.1.

```sh
pio run -e real-sensors
pio run -e basic
pio run -e stress-test
pio run -e real-sensors -t upload --upload-port COM5
pio device monitor --baud 115200 --port COM5
```

Build environments sequentially. The default is real-sensors; each builds exactly
one sketch and installs this root library through a local symlink dependency.
Replace COM5 with your board's port (`pio device list`). Uploading changes hardware;
no upload is part of validation. See [wiring and acceptance](docs/real-sensor-setup.md).
Windows without pio on PATH can use `& "$env:USERPROFILE/.platformio/penv/Scripts/pio.exe"`
in place of `pio` in PowerShell.

## Native and standalone validation

```sh
cmake -S test/sensor_registry -B .pio/registry-tests
cmake --build .pio/registry-tests --config Release
ctest --test-dir .pio/registry-tests -C Release --output-on-failure
python test/standalone/prepare_consumer.py
pio run -d .pio/standalone-consumer
```

The native suite exercises registration/API, lifecycle, codec, metadata transport,
live sessions, NimBLE binding through a native test port, and checked BME280 access.
It does not establish radio/wiring correctness. Complete the hardware acceptance
steps in the setup guide before claiming hardware validation. No Android checkout
is needed. See [fixture synchronization](test-fixtures/README.md).

## Packaging and releases

```sh
pio pkg pack -o .pio/PhysicalLink-verification.tar.gz
python tools/verify_package.py .pio/PhysicalLink-verification.tar.gz
```

The manifest's explicit export allowlist is authoritative. Development tests,
fixtures, stress-test example, PlatformIO configuration, private history, and caches
must not enter the package. The verifier checks exact membership and byte equality
against current allowlisted files. Do not overwrite existing `releases/` artifacts.
The existing 0.9.1 artifact and manifest version are preserved.

The release workflow runs on approved `v*` tags, requires the tag to match the
manifest, packs the root library, verifies the package, generates SHA256SUMS, and
creates a prerelease. Creating/pushing tags or publishing requires separate owner
approval. For a future release, review version and package documentation together,
run all checks above, review the package and hardware status, and obtain approval
before committing, pushing, tagging, or publishing. Do not retag or replace 0.9.1.

## Layout and historical assets

`test/` and `examples/stress_test/` migrated from Android's firmware/esp32sensors;
CMake and helper paths now target root src and firmware-owned test-fixtures.
`docs/history/` preserves seven previously ignored documents; the original project
guide is archived at docs/legacy-project-guide.md. Existing library and packaged
example files remain unchanged. Generated .pio files and machine-specific editor
settings were not migrated.
