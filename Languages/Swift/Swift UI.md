# Swift UI

### `@State`



`@State`

`@ViewBuilder`

### `@ Binding`


@FocusedBinding

toggle()


### `@EnvironmentObject`

### `@Published`

[A Complete Guide to Binding in SwiftUI](https://www.waldo.com/blog/complete-guide-to-swiftui-binding)

Three steps about the Data for a new view:

What data does this view need to do its job?
How will the view manipulate the data?
Where will the data come from?


#### Binding
* SwiftUI components accept `Binding`
* `Binding` can be derived from `State` and `ObservableObject`
* Derive a binding by using $ prefix

#### `ObservableObject`


Using `ObservableObject` as the data dependency surface:
	
	* Manage life cycle of your data
	* Handle side-effects
	* Integrate with existing components
	
Variables with `@Published` in `ObservableObject`:
	
	* Automatically works with ObservableObject
	* Publishes everytime the value changes in willSet

How to create an ObservableObject dependency:

* `@ObservableObject`
	- Tracks the ObservableObject as a dependency
	- Doesn't own the instance
* `@StateObject`
	- SwiftUI owns the ObservableObject
	- Creation and destruction is tied to the view's life cycle
	- Instantiaed just before body
* `@EnvironmentObject`
	- Adds Ergonomics to access `@ObservableObject`
	
	 SwiftUI will keep the object alive for the whole life cycle of the view.


### Data life time

Who owns the data?

	- Lift Data to common ancestor
	- Leverage @StateObject
	- Consider placing global data in app

SceneStorage: Scene-scoped, SwiftUI managed, View-only
AppStorage: App-scoped, User defaults, Usabel anywhere

`@SceneStorage` 和 `@AppStorage`

[Data Essentials in SwiftUI](https://developer.apple.com/videos/play/wwdc2020/10040/)

[App essentials in SwiftUI](https://developer.apple.com/videos/play/wwdc2020/10037)






## SwiftUI lifecycle









