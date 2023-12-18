#Mac上遇到的问题

Mac上遇到的，不了解的问题记录

### pod install 报错

进入文件夹也报错：

```
% cd /to/a/path         
RVM used your Gemfile for selecting Ruby, it is all fine - Heroku does that too,
you can ignore these warnings with 'rvm rvmrc warning ignore /Users/hut/Documents/mygro/Gemfile'.
To ignore the warning for all files run 'rvm rvmrc warning ignore allGemfiles'.

Unknown ruby interpreter version (do not know how to handle): >=2.6.10.
```

pod insatll 报错

```
error /System/Library/Frameworks/Ruby.framework/Versions/2.6/usr/lib/ruby/2.6.0/rubygems.rb:283:in `find_spec_for_exe': can't find gem bundler (>= 0.a) with executable bundle (Gem::GemNotFoundException)
	from /System/Library/Frameworks/Ruby.framework/Versions/2.6/usr/lib/ruby/2.6.0/rubygems.rb:302:in `activate_bin_path'
	from /usr/bin/bundle:23:in `<main>'
✖ Installing Ruby Gems
error Looks like your iOS environment is not properly set. Please go to https://reactnative.dev/docs/environment-setup?os=macos&platform=android and follow the React Native CLI QuickStart guide for macOS and iOS.
```

This error is saying (in a very particular way) that RubyGems was unable to find the exact version of Bundler that is in your `Gemfile.lock`.

Install the exact Bundler
`$ gem install bundler -v "$(grep -A 1 "BUNDLED WITH" Gemfile.lock | tail -n 1)"`

[Solutions for 'Cant find gem bundler (>= 0.a) with executable bundle'](https://bundler.io/blog/2019/05/14/solutions-for-cant-find-gem-bundler-with-executable-bundle.html)

[React Native — ‘Installing Cocoapods dependencies Error: Looks like your iOS enviornment is not properly set…’ ](https://medium.com/@rubybellekim/react-native-installing-cocoapods-dependencies-error-looks-like-your-ios-enviornment-is-not-b371e69fa696)