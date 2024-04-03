---
sidebar_label: op_uniffi_core
title: onepassword.lib.x86_64.op_uniffi_core
---

## \_UniffiRustBuffer Objects

```python
class _UniffiRustBuffer(ctypes.Structure)
```

#### alloc\_with\_builder

```python
@contextlib.contextmanager
def alloc_with_builder(*args)
```

Context-manger to allocate a buffer using a _UniffiRustBufferBuilder.

The allocated buffer will be automatically freed if an error occurs, ensuring that
we don&#x27;t accidentally leak it.

#### consume\_with\_stream

```python
@contextlib.contextmanager
def consume_with_stream()
```

Context-manager to consume a buffer using a _UniffiRustBufferStream.

The _UniffiRustBuffer will be freed once the context-manager exits, ensuring that we don&#x27;t
leak it even if an error occurs.

#### read\_with\_stream

```python
@contextlib.contextmanager
def read_with_stream()
```

Context-manager to read a buffer using a _UniffiRustBufferStream.

This is like consume_with_stream, but doesn&#x27;t free the buffer afterwards.
It should only be used with borrowed `_UniffiRustBuffer` data.

## \_UniffiPointerManagerCPython Objects

```python
class _UniffiPointerManagerCPython()
```

Manage giving out pointers to Python objects on CPython

This class is used to generate opaque pointers that reference Python objects to pass to Rust.
It assumes a CPython platform.  See _UniffiPointerManagerGeneral for the alternative.

#### new\_pointer

```python
def new_pointer(obj)
```

Get a pointer for an object as a ctypes.c_size_t instance

Each call to new_pointer() must be balanced with exactly one call to release_pointer()

This returns a ctypes.c_size_t.  This is always the same size as a pointer and can be
interchanged with pointers for FFI function arguments and return values.

## Error Objects

```python
class Error(Exception)
```

Error type sent over the FFI by UniFFI.

`uniffi::Error` only supports errors that are enums, so we need to have a single-variant enum here.

## Error Objects

```python
class Error()
```

## Error Objects

```python
class Error(_UniffiTempError)
```

Any error ocurring in the SDK

#### Error

type: ignore

