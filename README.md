[![Build Status](https://travis-ci.com/LabShare/sos-java.svg?token=y32446ytnVDog9YoNx32&branch=master)](https://travis-ci.com/LabShare/sos-java)
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

Non-scalar types

| Source: SoS (Python) type                             | Destination: Java class                                                                           |
|-------------------------------------------------------|---------------------------------------------------------------------------------------------------|
| `dict` (only homogeneous keys and values)             | [`HashMap<key_type, val_type>`](https://docs.oracle.com/javase/8/docs/api/java/util/HashMap.html) |
| Sequence (`list`, `tuple`; only homogeneous elements) | [`ArrayList`](https://docs.oracle.com/javase/8/docs/api/java/util/ArrayList.html)                 |
| `pandas.DataFrame`                                    | [Tablesaw](https://github.com/jtablesaw/tablesaw)                                                 |

#### From Java to SoS (`%put` magic):

Scalar types

| Source: Java primitive type                  | Destination: SoS (Python) type |
|----------------------------------------------|--------------------------------|
| `byte` `short` `int` `long`                  | `int`                          |
| `float` `double`                             | `float`                        |
| `char` `String`                              | `str`                          |
| `boolean`                                    | `bool`                         |

Non-scalar types

| Source: Java class | Destination: SoS (Python) type |
|--------------------|--------------------------------|
| `HashMap`          | `dict`                         |
| `ArrayList`        | `numpy.ndarray`                |
| Tablesaw           | `pandas.DataFrame`             |
