# JavaScript二进制数据操作

#### ArrayBuffer

```
const buffer = new ArrayBuffer(32);
buffer.byteLength; // 32
const v = new Int32Array(buffer);
ArrayBuffer.isView(v) // true
const buffer2 = buffer.slice(0, 1);

```

除了slice方法，ArrayBuffer对象不提供任何直接读写内存的方法，只允许在其上方建立视图，然后通过视图读写。

#### TypedArray

A TypedArray object describes an array-like view of an underlying binary data buffer.

Use `BYTES_PER_ELEMENT` to check the size in bytes, as `Int8Array. BYTES_PER_ELEMENT`

TypedArray objects:

| Type | Value Range | Size in bytes | Web IDL type |
|---|---|---|---|
| Int8Array | -128 to 127 | 1 | byte |
| Uint8Array | 0 to 255 | 1 | octet |
| Uint8ClampedArray | 0 to 255 | 1 | octet |
| Int16Array | -32768 to 32767 | 2 | short |
| Uint16Array | 0 to 65535 | 2 | unsigned short |
| Int32Array | -2147483648 to 2147483647 | 4 | long |
| Uint32Array | 0 to 4294967295 | 4 | unsigned long |
| Float32Array | -3.4e38 to 3.4e38 | 4 | unrestricted float |
| Float64Array | -1.8e308 to 1.8e308 | 8 | unrestricted double |
| BigInt64Array | -263 to 263 - 1 | 8 | bigint |
| BigUint64Array | 0 to 264 - 1 | 8 | bigint |


## TypedArray 与普通Array之间的转换

```
const typedArray = new Uint8Array([1, 2, 3, 4]);
const normalArray = Array.apply([], typedArray);
```

[TypedArray](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray)