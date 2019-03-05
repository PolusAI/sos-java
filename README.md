# sos-java
## SoS extension for Java. Developed independently from original SoS team. Please refer to [SoS Homepage](http://vatlab.github.io/SoS/) for details.

This language extension to SoS allows to use Java with IJava Jupyter kernel (https://github.com/SpencerPark/IJava) and exchange variables with other languages in Polyglot environment

### Supported variable types for transfer

#### From SoS to Java (`%get` magic):

Scalar (primitive) types

| Source: SoS (Python) type                                                       | Destination: Java primitive type       |
|---------------------------------------------------------------------------------|----------------------------------------|
| `int` `long int` `np.intc` `np.intp` `np.int8` `np.int16` `np.int32` `np.int64` |  `int` `long` (depending on value)     |
| `float` `np.float16` `np.float32` `np.float64`                                  |  `float` `double` (depending on value) |
| `str`                                                                           |  `String`                              |
| `bool`                                                                          |  `boolean`                             |

#### From Java to SoS (`%put` magic):

Scalar types

| Source: Java type                            | Destination: SoS (Python) type |
|----------------------------------------------|--------------------------------|
| `byte` `short` `int` `long`                  | `int`                          |
| `float` `double`                             | `float`                        |
| `char` `String`                              | `str`                          |
| `boolean`                                    | `bool`                         |