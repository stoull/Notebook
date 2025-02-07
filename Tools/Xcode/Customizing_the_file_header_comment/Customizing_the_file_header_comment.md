
# 更改Xcode新建文件时头部的默认注释

### 使用IDETemplateMacros.plist文件
Xcode 在新建一些文件的时候会按模板进行新建，这些模板一般在：`Xcode.app -> Contents -> Developer -> Platforms -> iPhoneOS.platform -> Developer -> Library -> Xcode -> Templates` 目录下。

比如创建NSObject文件的模板在：`/Applications/Xcode.app/Contents/Developer/Platforms/iPhoneOS.platform/Developer/Library/Xcode/Templates/File\ Templates/iOS/Source/Cocoa\ Touch\ Class.xctemplate/NSObjectObjective-C`

根据 ‘Customize text macros’ 的说明，Xcode会在以下目录中第一次找到IDETemplateMacros.plist进行替换，创建文件。

Xcode looks for the value of a text macro in the following locations and uses the first matching macro:

Project user data: <ProjectName>.xcodeproj/xcuserdata/[username].xcuserdatad/IDETemplateMacros.plist.

Project shared data: <ProjectName>.xcodeproj/xcshareddata/IDETemplateMacros.plist

Workspace user data: <WorkspaceName>.xcworkspace/xcuserdata/[username].xcuserdatad/IDETemplateMacros.plist.

Workspace shared data: <WorkspaceName>.xcworkspace/xcshareddata/IDETemplateMacros.plist.

User Xcode data: ~/Library/Developer/Xcode/UserData/IDETemplateMacros.plist.

如果只是想让个人新建的文件使用自定义的文件注释，则只要将文件IDETemplateMacros.plist放到目录： `<ProjectName>.xcodeproj/xcuserdata/[username].xcuserdatad/IDETemplateMacros.plist` 下

### IDETemplateMacros.plist 文件的格式


```
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>FILEHEADER</key>
	<string>
//  ___FILENAME___
//  ___PROJECTNAME___
//
//  Created by ___FULLUSERNAME___ on ___DATE___.
//  Copyright © ___YEAR___ ___ORGANIZATIONNAME___. All rights reserved.
//</string>
</dict>
</plist>
```

ORGANIZATIONNAME：可在Xcode中，点对应的项目，在项目属性(Project Document)中可更改Organization的值


Text macros reference

COPYRIGHT
A copyright string that uses the company name of the team for the project. If there is no company name, the string is blank.

The example shows a copyright string when the company is set to “Apple”.

Copyright © 2018 Apple. All rights reserved.

DATE
The current date.

DEFAULTTOOLCHAINSWIFTVERSION
The version of Swift used for the default toolchain.

FILEBASENAME
The name of the current file without any extension.

FILEBASENAMEASIDENTIFIER
The name of the current file encoded as a C identifier.

FILEHEADER
The text placed at the top of every new text file.

FILENAME
The full name of the current file.

FULLUSERNAME
The full name of the current macOS user.

NSHUMANREADABLECOPYRIGHTPLIST
The entry for the human readable copyright string in the Info.plist file of a macOS app target. The value of the macro must include the XML delimiters for the plist. For example, a valid value is:

<key>NSHumanReadableCopyright</key>

<string>Copyright © 2018 Apple, Inc. All rights reserved.</string>

   

Notice that the value includes a newline.

ORGANIZATIONNAME
The name for your organization that appears in boilerplate text throughout your project folder. The organization name in your project isn’t the same as the organization name that you enter in App Store Connect.

PACKAGENAME
The name of the package built by the current scheme.

PACKAGENAMEASIDENTIFIER
A C-identifier encoded version of the package name built by the current scheme.

PRODUCTNAME
The app name of the product built by the current scheme.

PROJECTNAME
The name of the current project.

RUNNINGMACOSVERSION
The version of macOS that is running Xcode.

TARGETNAME
The name of the current target.

TIME
The current time.

USERNAME
The login name for the current macOS user.

UUID
Returns a unique ID. The first time this macro is used, it generates the ID before returning it. You can use this macro to create multiple unique IDs by using a modifier. Each modifier returns an ID that is unique for that modifier. For example, the first time the UUID:firstPurpose modifier is used, the macro generates and returns a unique ID for that macro and modifier combination. Subsequent uses of the UUID:firstPurpose modifier return the same ID. Adding the UUID:secondPurpose modifier generates and returns a different ID that will be unique to UUID:secondPurpose, and different from the ID for UUID:firstPurpose.

WORKSPACENAME
The name of the current workspace. If there is only one project open, then the name of the current project.

YEAR
The localized year string for the current year.

详见：
[Text macros reference](https://help.apple.com/xcode/mac/current/#/dev7fe737ce0)
[Text macro format](https://help.apple.com/xcode/mac/current/#/devc8a500cb9)

或在Xcode->Help 搜索‘Customize text macros’


