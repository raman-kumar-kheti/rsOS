#!/bin/bash

# Set your target root directory inside your OS build
TARGET_ROOT="$(realpath ../../config/includes.chroot/usr)"

# Make sure target directories exist
mkdir -p "$TARGET_ROOT/bin" "$TARGET_ROOT/lib"

echo "Building libfm..."
cd ../libfm || exit 1
./configure --prefix="$TARGET_ROOT" || exit 1
make -j$(nproc) || exit 1

echo "Copying libfm output..."
cp libfm/.libs/libfm.so* "$TARGET_ROOT/lib/"

cd ../pcmanfm || exit 1
echo "Building pcmanfm..."
./configure --prefix="$TARGET_ROOT" || exit 1
make -j$(nproc) || exit 1

echo "Copying pcmanfm binary..."
cp src/pcmanfm "$TARGET_ROOT/bin/"

echo "✅ Build complete. Files copied to:"
echo " - Binaries: $TARGET_ROOT/bin"
echo " - Libraries: $TARGET_ROOT/lib"
