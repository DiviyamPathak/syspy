# Auction Platform

## Compiling Python project

This project has been heavily optimized and modified to be fully compatible with the **Codon** compiler. Codon is a high-performance Python compiler that translates Python code directly to native machine code using LLVM. 

While Codon supports a large subset of Python's syntax, it enforces strict static typing and does not support some highly dynamic Python features. Below is a summary of the changes made to the standard Python code and the reasons behind them:

### 1. Class-Level Field Declarations
* **Standard Python:** Instance variables are typically declared dynamically inside the `__init__` method (e.g., `self.name = name`).
* **Codon:** Requires all class fields to be statically typed and declared directly in the class body before `__init__`.
* **Reason:** Codon needs to calculate the exact memory layout of object instances at compile-time. Without explicit declarations, Codon attempts generic inference, which can fail (e.g., throwing a `cannot realize...` error).

### 2. Strict Type Annotations
* **Standard Python:** Employs dynamic "duck typing" where variables can hold any type, and collections like lists can mix types.
* **Codon:** Requires strict static type hints (e.g., `name: str`, `amount: float`). Generic collections must also declare their internal types explicitly (e.g., `List[User]`, `Optional[Bid]`).
* **Reason:** The compiler relies entirely on these hints to generate specific, heavily optimized machine code for each variable instead of using generic Python object wrappers.

### 3. Replacing Complex Standard Libraries (`datetime`)
* **Standard Python:** Utilizes dynamic standard modules like `datetime` for calculating end times (`datetime.timedelta`).
* **Codon:** Heavy, heavily-dynamic standard libraries are sometimes unsupported or only partially implemented.
* **Reason:** We replaced the `datetime` module with the built-in `time` module. Using standard integer UNIX epoch timestamps (e.g., `int(time.time()) + 86400`) translates flawlessly to native C-like primitives, avoiding unsupported complex library dependencies.

### 4. Avoiding Lambdas in Higher-Order Functions
* **Standard Python:** Easily resolves `max(bids, key=lambda b: b.amount)` or `sorted(bids, ...)`.
* **Codon:** Type inference can occasionally fail or act unpredictably when passing generic lambda closures to built-in sequence functions.
* **Reason:** We replaced higher-order functions and lambdas with explicit `for` loops. While slightly more verbose, these compile deterministically and are aggressively optimized by Codon into hyper-fast native loops.

### 5. Explicit Subclass Constructors (`__init__`)
* **Standard Python:** Subclasses automatically inherit their parent's `__init__` method if not explicitly overridden.
* **Codon:** Omitting `__init__` in a subclass prompts Codon to auto-generate a constructor expecting *all* class fields as positional arguments, breaking instantiation calls.
* **Reason:** We explicitly defined `__init__` methods in inherited classes (`EnglishAuction`, `FirstPriceSealedBidAuction`, etc.) and manually invoked `super().__init__(...)` to ensure the correct constructor constraints were locked in during compilation.

### 6. Explicit String Conversions
* **Standard Python:** `print("Error:", e)` automatically interpolates the exception.
* **Codon:** Requires manual string casting in certain contexts.
* **Reason:** Replaced with `print("Error: " + str(e))` to ensure the compiler knows how to safely build the string out of the exception struct.

---

### Benchmark & Performance
By adhering to these rules, the codebase can be compiled with:
```bash
codon build -release -exe main.py
```

Comparing the CPython interpretation of the code against the compiled executable revealed roughly a **~7x real-world speedup**. 

This massive improvement is due to skipping bytecode interpretation, removing dynamic type-checking overhead, running calculations directly on the CPU, and utilizing Codon's underlying Boehm Garbage Collector (which leverages idle CPU cores to perform cleanup concurrently instead of blocking the main thread).