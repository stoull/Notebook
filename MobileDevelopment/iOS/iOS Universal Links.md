# iOS Universal Links

[iOS Universal Links](https://support.iterable.com/hc/en-us/articles/360035496511-iOS-Universal-Links-)


[Support Universal Links](https://developer.apple.com/library/archive/documentation/General/Conceptual/AppSearch/UniversalLinks.html#//apple_ref/doc/uid/TP40016308-CH12-SW2)

[Supporting Associated Domains](https://developer.apple.com/documentation/Xcode/supporting-associated-domains)


[How to support Universal Links in iOS App and setup server for it?](https://stackoverflow.com/questions/35609667/how-to-support-universal-links-in-ios-app-and-setup-server-for-it)
The keys are as follows:
apps: Should have an empty array as its value, and it must be present. This is how Apple wants it.
details: Is an array of dictionaries, one for each iOS app supported by the website. Each dictionary contains information about the app, the team and bundle IDs.

There are 3 ways to define paths:
Static: The entire supported path is hardcoded to identify a specific link, e.g. /static/terms
Wildcards: A * can be used to match dynamic paths, e.g. /books/* can matches the path to any author’s page. ? inside specific path components, e.g. books/1? can be used to match any books whose ID starts with 1.
Exclusions: Prepending a path with NOT excludes that path from being matched.

The order in which the paths are mentioned in the array is important. Earlier indices have higher priority. Once a path matches, the evaluation stops, and other paths ignored. Each path is case-sensitive.