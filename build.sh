#!/bin/bash

printf '\e[34mmkdir release\e[m\n';
mkdir release;
printf '\e[34mcp README.md -> release\e[m\n';
cp README.md release;
printf '\e[34mcp LICENSE -> release\e[m\n';
cp LICENSE release;
printf '\e[34mpyinstaller gch\e[m\n';
pyinstaller gch.py --onefile && mv dist/gch release/
printf '\e[34mpyinstaller gdiff\e[m\n';
pyinstaller gdiff.py --onefile && mv dist/gdiff release/
printf '\e[34mtar zcvf\e[m\n';
tar zcvf release.tar.gz release
printf '\e[34mrm -rf build, dist, release\e[m\n';
rm -rf build
rm -rf dist
rm -rf release
printf '\e[34mrm spec filest\e[m\n';
rm *.spec
printf '\e[34mrm rb file\e[m\n';
rm /usr/local/Homebrew/Library/Taps/homebrew/homebrew-core/Formula/gch.rb

