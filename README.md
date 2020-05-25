<pre>
   ____           _               _
  / __ \         | |             | |
 | |  | |_ __ ___| |__   ___  ___| |_ _ __ ___  _ __   ___
 | |  | | '__/ __| '_ \ / _ \/ __| __| '__/ _ \| '_ \ / _ \
 | |__| | | | (__| | | |  __/\__ \ |_| | | (_) | | | |  __/
  \____/|_|  \___|_| |_|\___||___/\__|_|  \___/|_| |_|\___|
</pre>

# Intro
Orchestrone is a programming language that aids drone orchestration by providing useful data types and abstractions. The ouput of the compiler is a list of UDP commands for each of the instantiated drones.

# Requirements
You need to install the ply library to run this compiler or its tests.
```
pip3 install ply
```

# Compiling a file
Save your Orchestrone code in a file and compile it with:
```
python3 orchestrone.py your_file_name
```
You can also use the provided `example` file to compile an example set of commands.

# Running the test suite
The tests for the compiler and its modules are present in the `tests` folder. The `compiler_test.py` file contains the broadest tests and can be run with the following command:
```
python3 compiler_tests.py
```