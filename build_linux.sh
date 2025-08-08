#!/bin/bash
set -e

# Build EasyPixel Toolbox executable for Linux

pyinstaller EasyPixelToolbox.spec --clean --noconfirm

