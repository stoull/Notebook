# Xcode Command line Tools

Command Line Tools Package:
/Library/Developer/CommandLineTools

Xcode自带的命令行工具：/Applications/Xcode.app/Contents/Developer/usr/bin

PackageApplication

## xcode-select

## xcodebuild

## xcrun

Find and execute the named command line tool from the active developer
directory.

`xcrun --help`


用来运行目录`/Applications/Xcode.app/Contents/Developer/usr/bin`中的Xcode工具 如`simctl`, `agvtool`, `altool`, `xctest`, `xcodebuild`
xcrun simctl

#xcrun打包
xcrun -sdk iphoneos PackageApplication -v ./${appdirname}/*.app -o ${build_path}/ipa-build/${ipa_name}.ipa

## xcscontrol

## xctest

[Building from the Command Line with Xcode FAQ](https://developer.apple.com/library/archive/technotes/tn2339/_index.html#//apple_ref/doc/uid/DTS40014588-CH1-WHAT_IS_THE_COMMAND_LINE_TOOLS_PACKAGE_)