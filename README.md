# README: Optimizations and Syntax Extensions for Python++ Compiler

Python++ is an extended Python compiler supporting powerful optimizations and new syntax features that enable writing high-performance and safe code.

---

## Main Features and Optimizations

### 1. inline — Function and Method Inlining

- Marking a function/method as inline signals the compiler to substitute the function body directly at the call site.
- Reduces overhead of function calls.
- Ideal for short and frequently called methods (e.g., getters, operators).

### 2. const qualifier

- Marks a variable or method as constant.
- A const variable is an immutable reference or value (enabling storage optimizations).
- A const method guarantees no modification of object state.
- Allows the compiler to optimize code and reduce runtime checks.

### 3. comp_cast{T1, T2}(expr) — Compile-time Cast and Type Checking

- Checks if an operation or method call with types T1 and T2 is valid for expression expr.
- Removes runtime checks by ensuring safety at compile-time.
- For example, it can verify correctness of calling __add__ or other dunder methods.

### 4. bool_cast{T}(expr) — Boolean Context Checking

- Checks if an object of type T can be converted to bool (via __bool__ or __len__).
- Optimizes branching and conditionals by eliminating runtime errors.

### 5. noexcept — Exception Handling Optimization

- Marks functions that do not throw exceptions.
- Compiler can remove try-catch wrappers and speed up calls.
- If calls inside are not noexcept, inlining with exception handling is performed.

### 6. nodict qualifier for classes

- Disables creation of __dict__ attribute for class instances.
- Saves memory and speeds up attribute access by using fixed fields (__slots__-like optimization).
- Useful for large projects with many similar objects.

### 7. nocopy blocks

- Allows declaring code blocks where object copying is forbidden.
- Minimizes overhead of creating temporary objects.
- Used in performance-critical sections.

### 8. Preprocessor Directives

- Introduces directives prefixed with @ to control compilation:
  - Conditional compilation (@if, @else, @endif).
  - Loops and repeats (@repeat).
  - Logging and debugging (@debug, @info, @warning, @error).
  - Code transformations (@mirror, @invisible, etc.).
  - Support for custom plugins and extensions.

### 9. Compile-time Variables and Environment

- Predefined variables (__FILE__, __DATE__, __VERSION__, __COUNTER__, etc.).
- User-defined compile-time variables with arithmetic and condition support.
- Build environment control for conditional code generation and optimizations.

### 10. Preprocessor Plugins

- The compiler supports an extensible plugin system for the preprocessor.
- Plugins are directive handlers registered dynamically.
- Each plugin is a function receiving a list of source lines and current line index.
- Plugins can modify source code, insert, remove, or transform lines.
- Enables creating custom directives, complex macros, and syntax extensions without modifying the compiler core.
- Supports registration and deregistration of handlers during compilation via API.
- Allows implementing any user-defined preprocessing logic including conditionals, loops, logging, and more.

---

## Usage Examples

nodict class Vector:
    x: float
    y: float
    z: float

    inline const def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    inline def __add__(self, other):
        comp_cast{Vector, Vector}(self + other)
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    inline def __bool__(self):
        return bool_cast{Vector}(self.x != 0 or self.y != 0 or self.z != 0)

@noexcept
def safe_divide(a, b):
    if b == 0:
        return 0
    return a / b

@if BUILD_MODE == "debug"
    @debug "Debug mode is ON"
@endif

---

## Performance Benefits

- Reduced function call overhead via inlining.
- Eliminated runtime checks via comp_cast and bool_cast.
- Optimized exception handling with noexcept.
- Memory and access speed improvements with nodict.
- Reduced copying overhead with nocopy.
- Code and build control via preprocessor.
- Compile-time analysis and optimization possibilities.

---

## Future Plans

- Extending qualifiers set (mutable, volatile, etc.).
- Integration with performance analyzers.
- Support for additional architectures and platforms.
- Advanced DSL for macros and plugins.

---

Need help with setup or examples?  
This compiler is designed to give you freedom to write fast, clean Python code with low-level optimizations.

---

Example of registering a preprocessor plugin:

def my_custom_directive(lines: List[str], line_index: int) -> int:
    # code processing...
    return new_line_index

register_handler("@mydirective", my_custom_directive)

This approach makes the preprocessor system flexible and extensible, allowing users to tailor compilation to their needs.
