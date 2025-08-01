# Dart


## Dart 命令行工具

[Dart - Command-line Tools](https://dart.dev/tools/dart-tool)

```
dart create -t console my_app
cd my_app
dart analyze
dart test
dart run bin/my_app.dart
dart compile exe /bin/cli.dart
```

## Dart 语法

[Introduction to Dart](https://dart.dev/language)


##### Examples

```
import 'package:cli/cli.dart' as cli;
import 'package:cli/dog.dart' as dog_test;

void main(List<String> arguments) {
  print('Hello world: ${cli.calculate()}!');

  var allDogs = dog_test.allDogsInfo();
  print(allDogs);
}
```

```
import 'dart:convert';

String run() {
  return 'A dog is running';
}

List allDogsInfo() {
  var jsonString = '''
  [
    {"name": "Bela", "age": 3},
    {"name": "Max", "age": 5}
  ]
  ''';
  var dogs = jsonDecode(jsonString);
  assert(dogs is List);
  var firstDogInfo = dogs[0];
  assert(firstDogInfo is Map);
  return dogs;
}
```


## Dart 引入


## Dart 包理解

## Dart 包管理工具

