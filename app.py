import streamlit as st
import sqlite3
import hashlib
import random
import os
import html

# ============================================================
# CONFIG
# ============================================================
st.set_page_config(
    page_title="StudyForge | Smart Study Planner",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "study_planner.db")

# ============================================================
# 30-DAY CURRICULUM
# ============================================================
LANGUAGES = {
    "Python": {
        "emoji": "🐍", "color": "#3776AB",
        "topics": [
            "Python Setup & First Program", "Variables & Data Types",
            "Operators & Expressions", "Input, Output & Type Casting",
            "if, elif and else", "for and while Loops",
            "break, continue and pass", "Lists & List Methods",
            "Tuples & Sets", "Dictionaries", "Strings & String Methods",
            "Functions & Arguments", "Lambda Functions", "*args and **kwargs",
            "Recursion", "Modules & Packages", "File Handling",
            "Exception Handling", "Classes & Objects", "Inheritance & Polymorphism",
            "Encapsulation & Abstraction", "Iterators & Generators",
            "Decorators", "Regular Expressions", "JSON",
            "List & Dictionary Comprehensions", "NumPy Basics", "Pandas Basics",
            "Working with APIs", "Mini Project: CLI App",
        ],
    },
    "Java": {
        "emoji": "☕", "color": "#ED8B00",
        "topics": [
            "Java & JDK Setup", "Variables & Data Types", "Operators",
            "if, else and switch", "for, while and do-while",
            "Arrays", "Strings", "Methods", "Method Overloading",
            "Classes & Objects", "Constructors", "Inheritance",
            "Polymorphism", "Abstraction & Interfaces", "Encapsulation",
            "Exception Handling", "ArrayList", "HashMap", "Generics",
            "Multithreading Basics", "File I/O", "static and final",
            "Access Modifiers", "Wrapper Classes", "Enums",
            "Lambda Expressions", "Streams API", "Custom Exceptions",
            "JDBC Basics", "Mini Project: Console App",
        ],
    },
    "C": {
        "emoji": "🔧", "color": "#5C6BC0",
        "topics": [
            "C Setup & First Program", "Variables & Data Types", "Operators",
            "if, else and switch", "Loops", "Arrays", "Strings",
            "Functions", "Pointers Basics", "Pointers & Arrays",
            "Pointers & Functions", "Structures", "Unions",
            "Dynamic Memory Allocation", "File Handling", "Preprocessor",
            "Recursion", "Multi-dimensional Arrays", "Command Line Arguments",
            "Bitwise Operators", "enum", "typedef", "Linked Lists",
            "Stacks using Arrays", "Queues using Arrays", "Sorting Algorithms",
            "Searching Algorithms", "Storage Classes", "Error Handling",
            "Mini Project: Student Management System",
        ],
    },
    "C++": {
        "emoji": "➕", "color": "#004482",
        "topics": [
            "C++ Setup & First Program", "Variables & Data Types",
            "Operators", "if, else and switch", "Loops", "Arrays",
            "Strings", "Functions", "Function Overloading", "Pointers",
            "References", "Dynamic Memory", "Structures",
            "Classes & Objects", "Constructors & Destructors", "Inheritance",
            "Polymorphism", "Operator Overloading", "Virtual Functions",
            "Abstract Classes", "Templates", "STL Vectors", "STL Maps & Sets",
            "Exception Handling", "File Handling", "Namespaces",
            
            "Smart Pointers", "Lambda Expressions", "Multithreading Basics",
            "Mini Project: Console App",
        ],
    },
    "JavaScript": {
        "emoji": "🟨", "color": "#D9A400",
        "topics": [
            "JavaScript Setup & Console", "var, let and const",
            "Data Types & Type Conversion", "Operators",
            "Conditional Statements", "Loops", "Arrays & Array Methods",
            "Objects", "Functions", "Arrow Functions", "Scope & Closures",
            "this Keyword", "Callbacks", "Promises", "async/await",
            "DOM Selection & Manipulation", "Events", "Destructuring",
            "Spread & Rest", "Template Literals", "JSON",
            "try/catch Error Handling", "Classes", "Prototypes & Inheritance",
            "Modules", "Fetch API", "LocalStorage",
            "Higher-Order Functions", "map, filter and reduce",
            "Mini Project: To-Do App",
        ],
    },
    "SQL": {
        "emoji": "🗄️", "color": "#00758F",
        "topics": [
            "Database & SQL Basics", "SELECT", "WHERE & Operators",
            "ORDER BY & LIMIT", "INSERT, UPDATE, DELETE",
            "CREATE & ALTER TABLE", "SQL Data Types", "Constraints",
            "Aggregate Functions", "GROUP BY & HAVING", "INNER JOIN",
            "LEFT JOIN", "SELF & FULL JOIN Concepts", "Subqueries",
            "UNION & INTERSECT", "Views", "Indexes", "Stored Procedures",
            "Triggers", "Transactions & ACID", "Normalization",
            "String Functions", "Date Functions", "Window Functions",
            "CTEs", "CASE Statements", "Database Design",
            "Query Optimization", "Mini Project: Database Schema",
        ],
    },
    "HTML & CSS": {
        "emoji": "🎨", "color": "#E34C26",
        "topics": [
            "HTML Setup", "HTML Document Structure", "Text Formatting",
            "Links & Images", "Lists", "Tables", "Forms & Inputs",
            "Semantic HTML5", "CSS Introduction", "CSS Selectors",
            "Box Model", "Colors & Backgrounds", "Typography",
            "Positioning", "Display", "Flexbox Basics", "Flexbox Advanced",
            "CSS Grid Basics", "CSS Grid Advanced", "Responsive Design",
            "Transitions", "Animations", "CSS Variables",
            "Pseudo-classes & Pseudo-elements", "Bootstrap Overview",
            "Form Styling", "Navigation Bars", "Card Layouts",
            "CSS Best Practices", "Mini Project: Portfolio",
        ],
    },
    "Go": {
        "emoji": "🐹", "color": "#00ADD8",
        "topics": [
            "Go Setup & First Program", "Variables & Data Types",
            "Constants & iota", "Operators", "Conditional Statements",
            "Loops", "Arrays & Slices", "Maps", "Functions",
            "Multiple Return Values", "Variadic Functions", "Structs",
            "Methods", "Interfaces", "Pointers", "Error Handling",
            "Goroutines", "Channels", "select", "WaitGroup & Mutex",
            "defer, panic, recover", "Packages & Modules", "Strings",
            "File Handling", "JSON", "Testing", "Generics",
            "Embedding", "REST API Basics", "Mini Project: CLI Tool",
        ],
    },
    "Ruby": {
        "emoji": "💎", "color": "#CC342D",
        "topics": [
            "Ruby Setup", "Variables & Data Types", "Operators",
            "Conditionals", "Loops", "Arrays", "Hashes",
            "Strings & Symbols", "Methods", "Blocks, Procs & Lambdas",
            "Classes & Objects", "Inheritance", "Modules & Mixins",
            "Exception Handling", "File Handling", "Enumerable",
            "Ranges", "Regular Expressions", "Getters & Setters",
            "Class Variables & Methods", "Duck Typing", "Ruby Gems",
            "JSON", "Struct", "Operator Overloading",
            "Metaprogramming Basics", "RSpec Basics", "Rails Overview",
            "APIs", "Mini Project: Console App",
        ],
    },
    "Kotlin": {
        "emoji": "🅺", "color": "#7F52FF",
        "topics": [
            "Kotlin Setup", "val and var", "Data Types", "Operators",
            "Conditionals", "Loops", "Functions", "Default & Named Arguments",
            "Lambda Expressions", "Null Safety", "Classes & Objects",
            "Constructors", "Inheritance", "Interfaces", "Data Classes",
            "Sealed Classes", "object & Singleton", "Extension Functions",
            "Lists", "Maps & Sets", "Higher-Order Functions",
            "Coroutines", "Exception Handling", "Companion Objects",
            "Enums", "Generics", "Scope Functions", "File Handling",
            "JSON", "Mini Project: Console App",
        ],
    },
}

# ============================================================
# PRACTICAL ASSESSMENTS
# Each question has: question, options, answer, explanation
# Questions are selected by day/topic and shuffled.
# ============================================================
QUESTION_BANK = {
    "Python": [
        {
            "match": ["Variables", "Data Types"],
            "q": "What is printed by this Python code?\n\nx = 10\nx = x + 5\nprint(x)",
            "options": ["10", "15", "105", "Error"],
            "answer": 1,
            "explanation": "x starts at 10 and 5 is added, so the final value is 15.",
        },
        {
            "match": ["Operators"],
            "q": "What is the output of: print(17 // 5)?",
            "options": ["3", "3.4", "2", "4"],
            "answer": 0,
            "explanation": "// performs floor division. 17 divided by 5 gives 3 as the integer floor.",
        },
        {
            "match": ["Input", "Type Casting"],
            "q": "What does int('25') return?",
            "options": ["The string '25'", "The integer 25", "The float 25.0", "An error"],
            "answer": 1,
            "explanation": "int() converts the numeric string '25' into the integer 25.",
        },
        {
            "match": ["if", "elif", "else"],
            "q": "What is printed?\n\nx = 8\nif x > 10:\n    print('A')\nelif x > 5:\n    print('B')\nelse:\n    print('C')",
            "options": ["A", "B", "C", "Nothing"],
            "answer": 1,
            "explanation": "8 is not greater than 10, but it is greater than 5, so the elif branch runs.",
        },
        {
            "match": ["Loops"],
            "q": "How many times does this loop print a number?\n\nfor i in range(3):\n    print(i)",
            "options": ["2", "3", "4", "0"],
            "answer": 1,
            "explanation": "range(3) produces 0, 1 and 2, so the loop runs three times.",
        },
        {
            "match": ["Lists"],
            "q": "What is the value of nums after this code?\n\nnums = [1, 2]\nnums.append(3)",
            "options": ["[1, 2]", "[3, 1, 2]", "[1, 2, 3]", "Error"],
            "answer": 2,
            "explanation": "append() adds one item to the end of a list.",
        },
        {
            "match": ["Dictionaries"],
            "q": "Which expression gets the value 90?\n\nstudent = {'name': 'Ravi', 'marks': 90}",
            "options": ["student[0]", "student['marks']", "student.marks", "student('marks')"],
            "answer": 1,
            "explanation": "Dictionary values are accessed using their keys: student['marks'].",
        },
        {
            "match": ["Functions"],
            "q": "What does a Python function use to send a value back to its caller?",
            "options": ["break", "return", "yield", "continue"],
            "answer": 1,
            "explanation": "return ends the function and sends a value back to the caller.",
        },
        {
            "match": ["Lambda"],
            "q": "What is the result of (lambda x: x * 2)(4)?",
            "options": ["4", "6", "8", "16"],
            "answer": 2,
            "explanation": "The lambda multiplies its input by 2, so 4 * 2 = 8.",
        },
        {
            "match": ["Exception"],
            "q": "Which block is used to handle an exception in Python?",
            "options": ["try/except", "if/error", "catch/error", "handle/exception"],
            "answer": 0,
            "explanation": "Python uses try and except blocks for exception handling.",
        },
        {
            "match": ["Classes", "Objects"],
            "q": "Which keyword creates a class in Python?",
            "options": ["object", "class", "struct", "new"],
            "answer": 1,
            "explanation": "Python class definitions begin with the class keyword.",
        },
        {
            "match": ["Inheritance"],
            "q": "In class Child(Parent):, what is Parent?",
            "options": ["A method", "A child object", "A base/parent class", "A module"],
            "answer": 2,
            "explanation": "Parent is the base class from which Child inherits.",
        },
        {
            "match": ["Comprehensions"],
            "q": "What does [x * 2 for x in [1, 2, 3]] produce?",
            "options": ["[1, 2, 3]", "[2, 4, 6]", "[1, 4, 9]", "6"],
            "answer": 1,
            "explanation": "The comprehension multiplies every list item by 2.",
        },
        {
            "match": ["Generators"],
            "q": "Which keyword produces values one at a time from a generator?",
            "options": ["return", "yield", "generate", "nextonly"],
            "answer": 1,
            "explanation": "yield pauses a generator and provides its next value.",
        },
        {
            "match": ["JSON"],
            "q": "Which Python module is commonly used to work with JSON?",
            "options": ["json", "csvjson", "data", "serialize"],
            "answer": 0,
            "explanation": "Python's standard json module provides JSON encoding and decoding.",
        },
        {
            "match": ["APIs"],
            "q": "Which Python library is commonly used to send HTTP requests?",
            "options": ["requests", "random", "math", "pickle"],
            "answer": 0,
            "explanation": "The requests library is widely used for HTTP requests.",
        },
    ],
    "Java": [
        {
            "match": ["Variables", "Data Types"],
            "q": "What is printed?\n\nint x = 10;\nx = x + 5;\nSystem.out.println(x);",
            "options": ["10", "15", "105", "Compilation error"],
            "answer": 1,
            "explanation": "x becomes 15 after adding 5.",
        },
        {
            "match": ["Operators"],
            "q": "What is the value of 17 / 5 when both operands are int?",
            "options": ["3", "3.4", "2", "4"],
            "answer": 0,
            "explanation": "Integer division discards the fractional part, giving 3.",
        },
        {
            "match": ["Conditionals"],
            "q": "Which keyword handles an additional condition after if?",
            "options": ["elseif", "elif", "else if", "otherwise"],
            "answer": 2,
            "explanation": "Java uses the two-word keyword form else if.",
        },
        {
            "match": ["Loops"],
            "q": "How many times does for(int i=0; i<3; i++) execute its body?",
            "options": ["2", "3", "4", "0"],
            "answer": 1,
            "explanation": "The values are 0, 1 and 2, so the body runs three times.",
        },
        {
            "match": ["Arrays"],
            "q": "What is the first index of a Java array?",
            "options": ["0", "1", "-1", "Depends on the array"],
            "answer": 0,
            "explanation": "Java arrays are zero-indexed.",
        },
        {
            "match": ["Methods", "Overloading"],
            "q": "Method overloading means:",
            "options": ["Same method name with different parameter lists", "Same variable name", "Two classes with same name", "Replacing a constructor"],
            "answer": 0,
            "explanation": "Overloaded methods share a name but have different parameter lists.",
        },
        {
            "match": ["Classes", "Objects"],
            "q": "Which keyword is normally used to create an object in Java?",
            "options": ["class", "new", "object", "create"],
            "answer": 1,
            "explanation": "The new keyword creates an object instance.",
        },
        {
            "match": ["Exception"],
            "q": "Which pair is used to handle exceptions?",
            "options": ["try/catch", "if/error", "handle/except", "test/error"],
            "answer": 0,
            "explanation": "Java uses try and catch blocks to handle exceptions.",
        },
        {
            "match": ["ArrayList"],
            "q": "Which method adds an element to an ArrayList?",
            "options": ["push()", "append()", "add()", "insert()"],
            "answer": 2,
            "explanation": "ArrayList uses add() to append an element.",
        },
        {
            "match": ["HashMap"],
            "q": "A HashMap stores data as:",
            "options": ["Only values", "Key-value pairs", "Only indexes", "Rows and columns"],
            "answer": 1,
            "explanation": "HashMap stores mappings from keys to values.",
        },
        {
            "match": ["Inheritance"],
            "q": "Which keyword is used for class inheritance in Java?",
            "options": ["inherits", "extends", "parent", "base"],
            "answer": 1,
            "explanation": "A class extends another class to inherit from it.",
        },
        {
            "match": ["Interfaces"],
            "q": "A Java class uses which keyword to implement an interface?",
            "options": ["extends", "implements", "interface", "uses"],
            "answer": 1,
            "explanation": "The implements keyword connects a class to an interface.",
        },
        {
            "match": ["Lambda"],
            "q": "Java lambda expressions are mainly used to represent:",
            "options": ["Anonymous function behavior", "A database", "A package", "A class file"],
            "answer": 0,
            "explanation": "Lambdas provide concise function-like behavior, especially with functional interfaces.",
        },
        {
            "match": ["Streams"],
            "q": "Which Stream operation is commonly used to transform elements?",
            "options": ["map()", "change()", "convertAll()", "transformEach()"],
            "answer": 0,
            "explanation": "map() transforms each element into another value.",
        },
    ],
    "C": [
        {
            "match": ["Variables", "Data Types"],
            "q": "Which declaration creates an integer variable named age?",
            "options": ["integer age;", "int age;", "number age;", "age int;"],
            "answer": 1,
            "explanation": "int is the standard C integer type.",
        },
        {
            "match": ["Operators"],
            "q": "What is the result of 17 / 5 when both operands are int?",
            "options": ["3", "3.4", "2", "4"],
            "answer": 0,
            "explanation": "Integer division gives 3.",
        },
        {
            "match": ["Conditionals"],
            "q": "Which keyword tests another condition after if?",
            "options": ["elseif", "elif", "else if", "otherwise"],
            "answer": 2,
            "explanation": "C uses else if.",
        },
        {
            "match": ["Loops"],
            "q": "How many times does for(i=0; i<3; i++) execute?",
            "options": ["2", "3", "4", "0"],
            "answer": 1,
            "explanation": "The loop runs for i = 0, 1 and 2.",
        },
        {
            "match": ["Arrays"],
            "q": "What is the first index of a C array?",
            "options": ["0", "1", "-1", "Depends"],
            "answer": 0,
            "explanation": "C arrays start at index 0.",
        },
        {
            "match": ["Strings"],
            "q": "A C string normally ends with which character?",
            "options": ["\\n", "\\0", "\\t", "EOF"],
            "answer": 1,
            "explanation": "The null character \\0 marks the end of a C string.",
        },
        {
            "match": ["Functions"],
            "q": "Which keyword indicates that a function returns no value?",
            "options": ["null", "empty", "void", "none"],
            "answer": 2,
            "explanation": "void specifies no return value.",
        },
        {
            "match": ["Pointers"],
            "q": "Which operator gets the address of a variable?",
            "options": ["*", "&", "%", "#"],
            "answer": 1,
            "explanation": "The & operator obtains the address of an object.",
        },
        {
            "match": ["Pointers"],
            "q": "Which operator dereferences a pointer?",
            "options": ["&", "*", "->>", "::",],
            "answer": 1,
            "explanation": "The unary * operator accesses the object pointed to.",
        },
        {
            "match": ["Structures"],
            "q": "Which keyword defines a structure in C?",
            "options": ["record", "struct", "class", "object"],
            "answer": 1,
            "explanation": "C uses struct to define structures.",
        },
        {
            "match": ["Dynamic Memory"],
            "q": "Which function dynamically allocates memory in C?",
            "options": ["malloc()", "memory()", "alloc()", "new()"],
            "answer": 0,
            "explanation": "malloc() allocates a requested number of bytes.",
        },
        {
            "match": ["Recursion"],
            "q": "A recursive function must have a condition that eventually:",
            "options": ["Creates another compiler", "Stops recursive calls", "Deletes the program", "Changes the CPU"],
            "answer": 1,
            "explanation": "A base case is needed to stop recursion.",
        },
        {
            "match": ["Bitwise"],
            "q": "Which operator performs bitwise AND in C?",
            "options": ["&&", "&", "and", "|"],
            "answer": 1,
            "explanation": "& performs bitwise AND; && is logical AND.",
        },
    ],
    "C++": [
        {
            "match": ["Variables", "Data Types"],
            "q": "Which declaration creates an integer named count?",
            "options": ["integer count;", "int count;", "number count;", "count int;"],
            "answer": 1,
            "explanation": "int declares an integer.",
        },
        {
            "match": ["Loops"],
            "q": "How many times does for(int i=0;i<3;i++) execute?",
            "options": ["2", "3", "4", "0"],
            "answer": 1,
            "explanation": "The values 0, 1 and 2 make three iterations.",
        },
        {
            "match": ["Functions", "Overloading"],
            "q": "Function overloading allows:",
            "options": ["Same name with different parameter lists", "Same parameter list only", "No return values", "Only global functions"],
            "answer": 0,
            "explanation": "C++ supports multiple functions with the same name and different parameter lists.",
        },
        {
            "match": ["Pointers"],
            "q": "Which operator obtains the address of a variable?",
            "options": ["*", "&", "->", "::"],
            "answer": 1,
            "explanation": "& obtains an object's address.",
        },
        {
            "match": ["References"],
            "q": "Which symbol declares a reference variable?",
            "options": ["*", "&", "%", "#"],
            "answer": 1,
            "explanation": "A reference declaration uses &.",
        },
        {
            "match": ["Classes"],
            "q": "Which keyword defines a class?",
            "options": ["object", "class", "structonly", "type"],
            "answer": 1,
            "explanation": "C++ uses class to define a class type.",
        },
        {
            "match": ["Constructors"],
            "q": "A constructor normally has the same name as the:",
            "options": ["Object", "Class", "File", "Namespace"],
            "answer": 1,
            "explanation": "A constructor has the same name as its class.",
        },
        {
            "match": ["Inheritance"],
            "q": "Which syntax indicates inheritance in a C++ class declaration?",
            "options": ["class B inherits A", "class B : public A", "class B -> A", "class B extends A"],
            "answer": 1,
            "explanation": "C++ uses a colon followed by an access specifier and base class.",
        },
        {
            "match": ["STL", "Vectors"],
            "q": "Which STL container provides a dynamic array?",
            "options": ["vector", "tuple", "stackonly", "pair"],
            "answer": 0,
            "explanation": "std::vector is the standard dynamic-array container.",
        },
        {
            "match": ["Exceptions"],
            "q": "Which block catches an exception in C++?",
            "options": ["except", "catch", "handle", "error"],
            "answer": 1,
            "explanation": "C++ uses try and catch for exceptions.",
        },
        {
            "match": ["Templates"],
            "q": "Templates are mainly used to write:",
            "options": ["Generic code", "Only UI code", "Only file names", "Machine instructions"],
            "answer": 0,
            "explanation": "Templates allow algorithms and classes to work with different types.",
        },
    ],
    "JavaScript": [
        {
            "match": ["var", "let", "const"],
            "q": "Which keyword prevents reassignment of the binding?",
            "options": ["var", "let", "const", "static"],
            "answer": 2,
            "explanation": "A const binding cannot be reassigned.",
        },
        {
            "match": ["Data Types"],
            "q": "What is typeof 10 in JavaScript?",
            "options": ["integer", "number", "int", "numeric"],
            "answer": 1,
            "explanation": "JavaScript uses the number type for ordinary numeric values.",
        },
        {
            "match": ["Arrays"],
            "q": "What does [1,2,3].length return?",
            "options": ["2", "3", "4", "undefined"],
            "answer": 1,
            "explanation": "length gives the number of elements, which is 3.",
        },
        {
            "match": ["Functions", "Arrow"],
            "q": "Which is a valid arrow function?",
            "options": ["function => x", "(x) => x * 2", "arrow(x): x", "=> function(x)"],
            "answer": 1,
            "explanation": "(x) => x * 2 is valid arrow-function syntax.",
        },
        {
            "match": ["Scope"],
            "q": "let and const are primarily:",
            "options": ["Function-scoped only", "Block-scoped", "Global-only", "Class-only"],
            "answer": 1,
            "explanation": "let and const are block-scoped.",
        },
        {
            "match": ["Promises"],
            "q": "Which method handles a fulfilled Promise value?",
            "options": [".then()", ".catchOnly()", ".resolveNow()", ".success()"],
            "answer": 0,
            "explanation": ".then() registers a callback for fulfillment.",
        },
        {
            "match": ["async", "await"],
            "q": "The await keyword is normally used inside a function declared with:",
            "options": ["defer", "async", "promise", "wait"],
            "answer": 1,
            "explanation": "await is normally used inside an async function.",
        },
        {
            "match": ["DOM"],
            "q": "Which method selects the first element matching a CSS selector?",
            "options": ["getFirst()", "querySelector()", "selectOne()", "findCSS()"],
            "answer": 1,
            "explanation": "document.querySelector() returns the first matching element.",
        },
        {
            "match": ["Events"],
            "q": "Which method attaches an event listener?",
            "options": ["listen()", "addEventListener()", "onEvent()", "attach()"],
            "answer": 1,
            "explanation": "addEventListener() registers an event handler.",
        },
        {
            "match": ["JSON"],
            "q": "Which method converts a JavaScript object to a JSON string?",
            "options": ["JSON.parse()", "JSON.stringify()", "JSON.object()", "JSON.encode()"],
            "answer": 1,
            "explanation": "JSON.stringify() serializes a JavaScript value into JSON text.",
        },
        {
            "match": ["map", "filter", "reduce"],
            "q": "Which array method creates a new array by transforming each element?",
            "options": ["filter()", "map()", "reduce()", "find()"],
            "answer": 1,
            "explanation": "map() transforms each element and returns a new array.",
        },
        {
            "match": ["try", "catch"],
            "q": "Which block handles an exception?",
            "options": ["catch", "handle", "except", "error"],
            "answer": 0,
            "explanation": "JavaScript uses try/catch for exception handling.",
        },
    ],
    "SQL": [
        {
            "match": ["SELECT"],
            "q": "Which query returns all columns from students?",
            "options": [
                "GET * FROM students;",
                "SELECT * FROM students;",
                "SHOW ALL students;",
                "READ students;"
            ],
            "answer": 1,
            "explanation": "SELECT * FROM table returns all columns and rows from the table.",
        },
        {
            "match": ["WHERE"],
            "q": "Which query returns students older than 18?",
            "options": [
                "SELECT * FROM students WHERE age > 18;",
                "SELECT * FROM students IF age > 18;",
                "GET students age > 18;",
                "SELECT age > 18 FROM students;"
            ],
            "answer": 0,
            "explanation": "WHERE filters rows based on a condition.",
        },
        {
            "match": ["ORDER BY"],
            "q": "Which clause sorts marks from highest to lowest?",
            "options": ["SORT marks DESC", "ORDER BY marks DESC", "GROUP BY marks DESC", "ORDER marks HIGH"],
            "answer": 1,
            "explanation": "ORDER BY marks DESC sorts marks in descending order.",
        },
        {
            "match": ["INSERT"],
            "q": "Which command adds a new row?",
            "options": ["ADD ROW", "INSERT INTO", "UPDATE ROW", "CREATE ROW"],
            "answer": 1,
            "explanation": "INSERT INTO adds rows to a table.",
        },
        {
            "match": ["UPDATE"],
            "q": "Which command changes existing rows?",
            "options": ["CHANGE", "UPDATE", "ALTER DATA", "MODIFY ROW"],
            "answer": 1,
            "explanation": "UPDATE modifies existing records.",
        },
        {
            "match": ["DELETE"],
            "q": "Which command removes selected rows from a table?",
            "options": ["REMOVE", "DELETE", "DROP ROW", "CLEAR ROW"],
            "answer": 1,
            "explanation": "DELETE removes rows, usually controlled by a WHERE clause.",
        },
        {
            "match": ["Aggregate"],
            "q": "Which function counts rows?",
            "options": ["TOTAL()", "COUNT()", "ROWS()", "NUMBER()"],
            "answer": 1,
            "explanation": "COUNT() returns the number of rows or non-null values depending on its expression.",
        },
        {
            "match": ["GROUP BY"],
            "q": "GROUP BY is mainly used to:",
            "options": ["Group rows for aggregation", "Delete duplicates only", "Create databases", "Rename columns"],
            "answer": 0,
            "explanation": "GROUP BY groups rows so aggregate functions can be applied per group.",
        },
        {
            "match": ["HAVING"],
            "q": "HAVING is commonly used to filter:",
            "options": ["Rows before grouping", "Groups after aggregation", "Tables before creation", "Indexes"],
            "answer": 1,
            "explanation": "HAVING filters grouped/aggregated results.",
        },
        {
            "match": ["INNER JOIN"],
            "q": "An INNER JOIN returns:",
            "options": ["Only matching rows from both tables", "All rows from the left table", "All rows from both tables", "Only unmatched rows"],
            "answer": 0,
            "explanation": "INNER JOIN keeps rows for which the join condition matches in both tables.",
        },
        {
            "match": ["LEFT JOIN"],
            "q": "A LEFT JOIN keeps:",
            "options": ["Only right rows", "All left rows plus matches", "Only matches", "No nulls"],
            "answer": 1,
            "explanation": "A LEFT JOIN preserves every row from the left table.",
        },
        {
            "match": ["Subqueries"],
            "q": "A query nested inside another SQL query is called a:",
            "options": ["subquery", "subtable", "macro", "trigger"],
            "answer": 0,
            "explanation": "A subquery is a query nested inside another query.",
        },
        {
            "match": ["Transactions"],
            "q": "Which command permanently saves a transaction?",
            "options": ["SAVE", "COMMIT", "STORE", "APPLY"],
            "answer": 1,
            "explanation": "COMMIT makes transaction changes permanent.",
        },
        {
            "match": ["CTE"],
            "q": "Which keyword starts a common table expression?",
            "options": ["WITH", "CTE", "TEMP", "COMMON"],
            "answer": 0,
            "explanation": "A CTE is introduced with WITH.",
        },
        {
            "match": ["CASE"],
            "q": "CASE in SQL is commonly used for:",
            "options": ["Conditional expressions", "Creating indexes", "Starting transactions", "Joining databases"],
            "answer": 0,
            "explanation": "CASE provides conditional logic inside SQL expressions.",
        },
    ],
}

# Generic practical banks for the remaining languages.
GENERIC_BANKS = {
    "HTML & CSS": [
        ("Which HTML element is used for the main page heading?", ["<h1>", "<head>", "<title>", "<heading>"], 0,
         "<h1> is the highest-level visible heading."),
        ("Which CSS property changes text color?", ["font-style", "color", "text-color", "foreground"], 1,
         "The color property controls text color."),
        ("Which CSS layout system is designed for one-dimensional layouts?", ["Flexbox", "SQL Grid", "FloatDB", "DOM"], 0,
         "Flexbox is designed for one-dimensional row or column layouts."),
        ("Which CSS property adds space inside an element's border?", ["margin", "padding", "gap-only", "spacing"], 1,
         "Padding is the space between content and the border."),
        ("Which HTML attribute provides alternative text for an image?", ["src", "alt", "href", "text"], 1,
         "alt provides alternative text for an image."),
        ("Which selector targets an element with id='main'?", [".main", "#main", "main#", "*main"], 1,
         "#main selects the element whose id is main."),
        ("Which CSS property controls the space between grid/flex items?", ["gap", "space", "item-gap-only", "between"], 0,
         "gap sets spacing between flex or grid items."),
        ("Which HTML element creates a hyperlink?", ["<link>", "<a>", "<url>", "<href>"], 1,
         "<a> creates a hyperlink."),
        ("Which CSS rule is commonly used to make a page responsive?", ["@media", "@screen", "@responsive", "@device"], 0,
         "@media introduces media queries."),
        ("Which semantic element represents navigation links?", ["<navigate>", "<nav>", "<links>", "<menu-bar>"], 1,
         "<nav> is the semantic navigation element."),
    ],
    "Go": [
        ("Which keyword declares a variable in Go using short declaration syntax?", [":=", "let", "var!", "define"], 0,
         ":= is Go's short variable declaration operator."),
        ("Which Go type stores a sequence of elements of the same type with dynamic size?", ["array", "slice", "tuple", "list"], 1,
         "A slice is a dynamic view over an array."),
        ("Which keyword defines a function?", ["func", "function", "def", "method"], 0,
         "Go uses func to declare functions."),
        ("Which keyword starts a goroutine?", ["go", "async", "thread", "spawn"], 0,
         "The go keyword starts a function call as a goroutine."),
        ("Which keyword handles an error value by returning it from a function?", ["return", "throw", "raise", "except"], 0,
         "Go commonly returns error values explicitly with return."),
        ("Which type is used to define a map?", ["map", "dict", "hash", "object"], 0,
         "Go uses map[K]V syntax for maps."),
        ("Which keyword defines a struct?", ["struct", "record", "class", "object"], 0,
         "Go uses struct to define structured data."),
        ("Which package is commonly used for formatted input/output?", ["fmt", "iofmt", "print", "console"], 0,
         "The fmt package provides formatted I/O functions."),
        ("Which keyword creates a channel?", ["make", "channel", "newchan", "chanmake"], 0,
         "make(chan T) creates a channel."),
        ("Which keyword can recover from a panic?", ["recover", "catch", "handle", "resume"], 0,
         "recover is used inside deferred functions to regain control after panic."),
    ],
    "Ruby": [
        ("Which symbol begins an instance variable in Ruby?", ["@", "$", "#", "&"], 0,
         "Ruby instance variables begin with @."),
        ("Which method adds an item to the end of an Array?", ["append", "push", "add", "insert_end"], 1,
         "Array#push adds an item to the end."),
        ("Which keyword defines a method?", ["def", "function", "method", "func"], 0,
         "Ruby methods are defined with def."),
        ("Which keyword defines a class?", ["class", "type", "object", "struct"], 0,
         "Ruby uses class to define classes."),
        ("Which collection stores key-value pairs?", ["Array", "Hash", "Tuple", "PairList"], 1,
         "Ruby Hash stores key-value mappings."),
        ("Which keyword handles exceptions?", ["rescue", "catch", "except", "handle"], 0,
         "Ruby uses rescue to handle exceptions."),
        ("Which operator checks equality of values?", ["=", "==", "=>", "==="], 1,
         "== compares values for equality."),
        ("Which method is commonly used to iterate over an array?", ["each", "loopEach", "iterate", "forEachOnly"], 0,
         "each is Ruby's common iterator for collections."),
        ("What does nil represent?", ["No value", "Zero only", "False only", "Empty string only"], 0,
         "nil represents the absence of a value."),
        ("Which keyword creates a module?", ["module", "package", "namespace", "mixin"], 0,
         "Ruby uses module to define modules."),
    ],
    "Kotlin": [
        ("Which keyword declares a read-only variable?", ["var", "val", "let", "const"], 1,
         "val declares a read-only reference."),
        ("Which keyword declares a mutable variable?", ["var", "val", "let", "mutable"], 0,
         "var declares a mutable variable."),
        ("Which operator safely accesses a nullable value?", ["?.", "??", "safe.", "!!?"], 0,
         "?. is the safe-call operator."),
        ("Which keyword declares a function?", ["fun", "func", "def", "function"], 0,
         "Kotlin uses fun to declare functions."),
        ("Which keyword creates a data class?", ["data", "record", "model", "dto"], 0,
         "A data class is declared with the data keyword."),
        ("Which collection is commonly immutable by default when created with listOf?", ["List", "MutableList", "ArrayList", "SetOnly"], 0,
         "listOf returns a read-only List interface."),
        ("Which keyword defines a class?", ["class", "type", "objectonly", "struct"], 0,
         "Kotlin uses class."),
        ("Which keyword creates a singleton object declaration?", ["object", "singleton", "one", "static"], 0,
         "object declarations define a singleton."),
        ("Which function transforms every element of a collection?", ["map", "filter", "reduceOnly", "eachOnly"], 0,
         "map returns a collection containing transformed elements."),
        ("Which keyword is used for inheritance from an open class?", ["extends", ":", "inherits", "super"], 1,
         "Kotlin uses a colon before the base type, e.g. class Child : Parent()."),
    ],
}

# ============================================================
# DATABASE
# ============================================================
def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_languages (
            username TEXT,
            language TEXT,
            hours REAL,
            PRIMARY KEY(username, language)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            username TEXT,
            language TEXT,
            day INTEGER,
            completed INTEGER DEFAULT 0,
            score INTEGER DEFAULT 0,
            total INTEGER DEFAULT 10,
            PRIMARY KEY(username, language, day)
        )
    """)
    conn.commit()
    conn.close()


def hash_pw(password):
    return hashlib.sha256(password.encode()).hexdigest()


def create_user(username, email, password):
    username = username.strip()
    email = email.strip()

    if len(username) < 3:
        return False, "Username must contain at least 3 characters."
    if len(password) < 6:
        return False, "Password must contain at least 6 characters."
    if "@" not in email:
        return False, "Please enter a valid email address."

    conn = get_conn()
    try:
        conn.execute(
            "INSERT INTO users VALUES (?, ?, ?)",
            (username, email, hash_pw(password)),
        )
        conn.commit()
        return True, "Account created. You can now log in."
    except sqlite3.IntegrityError:
        return False, "That username is already taken."
    finally:
        conn.close()


def check_login(username, password):
    conn = get_conn()
    row = conn.execute(
        "SELECT password FROM users WHERE username=?",
        (username.strip(),),
    ).fetchone()
    conn.close()
    return row is not None and row[0] == hash_pw(password)


def save_user_language(username, language, hours):
    conn = get_conn()
    conn.execute("""
        INSERT INTO user_languages(username, language, hours)
        VALUES (?, ?, ?)
        ON CONFLICT(username, language)
        DO UPDATE SET hours=excluded.hours
    """, (username, language, hours))
    conn.commit()
    conn.close()


def remove_user_language(username, language):
    conn = get_conn()
    conn.execute(
        "DELETE FROM user_languages WHERE username=? AND language=?",
        (username, language),
    )
    conn.execute(
        "DELETE FROM progress WHERE username=? AND language=?",
        (username, language),
    )
    conn.commit()
    conn.close()


def get_user_languages(username):
    conn = get_conn()
    rows = conn.execute(
        "SELECT language, hours FROM user_languages WHERE username=?",
        (username,),
    ).fetchall()
    conn.close()
    return {r[0]: r[1] for r in rows}


def save_progress(username, language, day, score, total):
    conn = get_conn()
    conn.execute("""
        INSERT INTO progress(username, language, day, completed, score, total)
        VALUES (?, ?, ?, 1, ?, ?)
        ON CONFLICT(username, language, day)
        DO UPDATE SET completed=1, score=excluded.score, total=excluded.total
    """, (username, language, day, score, total))
    conn.commit()
    conn.close()


def get_progress(username, language):
    conn = get_conn()
    rows = conn.execute("""
        SELECT day, completed, score, total
        FROM progress
        WHERE username=? AND language=?
    """, (username, language)).fetchall()
    conn.close()
    return {
        r[0]: {"completed": bool(r[1]), "score": r[2], "total": r[3]}
        for r in rows
    }


init_db()

# ============================================================
# RESOURCE LINKS
# ============================================================
def youtube_url(language, topic):
    query = f"{language} {topic} tutorial".replace(" ", "+")
    return f"https://www.youtube.com/results?search_query={query}"


def practice_url(language, topic):
    query = f"{language} {topic}".replace(" ", "+")
    return f"https://www.google.com/search?q={query}+coding+practice"


def docs_url(language):
    docs = {
        "Python": "https://docs.python.org/3/",
        "Java": "https://docs.oracle.com/en/java/",
        "C": "https://en.cppreference.com/w/c",
        "C++": "https://en.cppreference.com/w/",
        "JavaScript": "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
        "SQL": "https://dev.mysql.com/doc/",
        "HTML & CSS": "https://developer.mozilla.org/en-US/docs/Web",
        "Go": "https://go.dev/doc/",
        "Ruby": "https://www.ruby-lang.org/en/documentation/",
        "Kotlin": "https://kotlinlang.org/docs/home.html",
    }
    return docs.get(language, "https://www.google.com/")


# ============================================================
# ASSESSMENT ENGINE
# ============================================================
def question_matches_topic(question, topic):
    topic_words = set(
        w.lower()
        for w in topic.replace("&", " ").replace("-", " ").split()
        if len(w) > 2
    )
    match_words = set(
        w.lower()
        for item in question.get("match", [])
        for w in item.replace("&", " ").replace("-", " ").split()
        if len(w) > 2
    )
    return bool(topic_words & match_words)


def get_questions(language, day, topic, count=10):
    rng = random.Random(f"{language}|{day}|{topic}")

    specific = QUESTION_BANK.get(language, [])
    matching = [q for q in specific if question_matches_topic(q, topic)]
    others = [q for q in specific if q not in matching]

    pool = matching + others
    rng.shuffle(pool)

    selected = pool[:count]

    if language in GENERIC_BANKS:
        generic = []
        for q, options, answer, explanation in GENERIC_BANKS[language]:
            generic.append({
                "q": q,
                "options": options,
                "answer": answer,
                "explanation": explanation,
            })
        rng.shuffle(generic)
        selected = generic[:count]

    # If there are fewer than 10 practical questions in the bank,
    # reuse questions deterministically so every day has 10 questions.
    if selected:
        while len(selected) < count:
            selected.append(selected[len(selected) % len(selected)])

    # Shuffle options while preserving correct answer.
    result = []
    for item in selected[:count]:
        options = list(item["options"])
        correct_text = options[item["answer"]]
        rng.shuffle(options)
        result.append({
            "question": item["q"],
            "options": options,
            "answer": options.index(correct_text),
            "explanation": item["explanation"],
        })

    return result


# ============================================================
# CSS
# ============================================================
st.markdown("""
<style>
    .block-container {
        max-width: 1400px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    .hero {
        padding: 2rem 2.2rem;
        border-radius: 24px;
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 15px 40px rgba(79,70,229,.20);
    }

    .hero h1 {
        font-size: 2.7rem;
        margin: 0;
        font-weight: 800;
    }

    .hero p {
        margin: .5rem 0 0;
        opacity: .92;
        font-size: 1.05rem;
    }

    .stat {
        padding: 1rem 1.1rem;
        border: 1px solid rgba(128,128,128,.18);
        border-radius: 18px;
        background: rgba(128,128,128,.05);
        min-height: 105px;
    }

    .stat-number {
        font-size: 1.7rem;
        font-weight: 800;
    }

    .stat-label {
        opacity: .72;
        font-size: .85rem;
    }

    .language-card {
        padding: 1.2rem;
        border-radius: 20px;
        color: white;
        min-height: 145px;
        box-shadow: 0 8px 25px rgba(0,0,0,.12);
    }

    .language-card .emoji {
        font-size: 2rem;
    }

    .language-card .title {
        font-size: 1.15rem;
        font-weight: 800;
        margin-top: .35rem;
    }

    .language-card .small {
        opacity: .9;
        font-size: .82rem;
        margin-top: .3rem;
    }

    .day-header {
        padding: 1rem 1.2rem;
        border-radius: 16px;
        border: 1px solid rgba(128,128,128,.18);
        margin-bottom: .7rem;
    }

    .assessment {
        padding: 1.35rem;
        border-radius: 20px;
        border: 1px solid rgba(128,128,128,.20);
        background: rgba(128,128,128,.035);
        margin-top: .8rem;
    }

    .question-label {
        font-weight: 800;
        font-size: 1.03rem;
        margin-bottom: .45rem;
    }

    .code-box {
        background: #111827;
        color: #f9fafb;
        padding: 1rem 1.1rem;
        border-radius: 12px;
        font-family: Consolas, monospace;
        white-space: pre-wrap;
        margin: .7rem 0;
    }

    .result-pass {
        padding: 1.25rem;
        border-radius: 18px;
        border: 1px solid #22c55e;
        background: rgba(34,197,94,.10);
    }

    .result-fail {
        padding: 1.25rem;
        border-radius: 18px;
        border: 1px solid #ef4444;
        background: rgba(239,68,68,.08);
    }

    .badge {
        display: inline-block;
        padding: .28rem .65rem;
        border-radius: 999px;
        font-size: .78rem;
        font-weight: 700;
        background: rgba(79,70,229,.12);
    }

    div[data-testid="stExpander"] {
        border-radius: 18px !important;
    }

    button[kind="primary"] {
        border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================
defaults = {
    "logged_in": False,
    "username": "",
    "open_language": None,
    "assessment_results": {},
    "assessment_answers": {},
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# AUTH
# ============================================================
def auth_page():
    st.markdown("""
    <div class="hero">
        <h1>📚 StudyForge</h1>
        <p>Learn programming with a structured 30-day plan, practical assessments and progress tracking.</p>
    </div>
    """, unsafe_allow_html=True)

    left, center, right = st.columns([1, 1.3, 1])

    with center:
        tab1, tab2 = st.tabs(["🔐 Login", "✨ Create Account"])

        with tab1:
            st.subheader("Welcome back")
            st.caption("Continue your learning journey.")

            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter username")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button(
                    "Login to StudyForge",
                    type="primary",
                    use_container_width=True,
                )

            if submitted:
                if check_login(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username.strip()
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

        with tab2:
            st.subheader("Create your account")
            st.caption("Your study plans and scores will be saved.")

            with st.form("signup_form"):
                username = st.text_input("Choose username")
                email = st.text_input("Email")
                password = st.text_input("Create password", type="password")
                confirm = st.text_input("Confirm password", type="password")
                submitted = st.form_submit_button(
                    "Create Account",
                    type="primary",
                    use_container_width=True,
                )

            if submitted:
                if password != confirm:
                    st.error("Passwords do not match.")
                else:
                    ok, msg = create_user(username, email, password)
                    if ok:
                        st.success(msg)
                    else:
                        st.error(msg)


# ============================================================
# ASSESSMENT UI
# ============================================================
def render_assessment(username, language, day, topic):
    key_base = f"{username}|{language}|{day}"
    questions = get_questions(language, day, topic, 10)

    st.markdown('<div class="assessment">', unsafe_allow_html=True)

    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown("### 🧠 Practical Assessment")
        st.caption(
            "10 questions • Code/output/logic focused • "
            "Minimum 6/10 to mark the day complete"
        )
    with c2:
        st.markdown(
            '<span class="badge">10 MARKS</span>',
            unsafe_allow_html=True,
        )

    answers = {}

    for i, q in enumerate(questions, 1):
        st.markdown(
            f'<div class="question-label">Q{i}. {html.escape(q["question"]).replace(chr(10), "<br>")}</div>',
            unsafe_allow_html=True,
        )

        answers[i - 1] = st.radio(
            "Choose one answer:",
            ["-- Select --"] + q["options"],
            key=f"answer_{key_base}_{i}",
            label_visibility="collapsed",
        )

        if i != len(questions):
            st.markdown("---")

    submit_key = f"submit_assessment_{key_base}"

    if st.button(
        "🎯 Submit Assessment",
        key=submit_key,
        type="primary",
        use_container_width=True,
    ):
        unanswered = [
            i for i, value in answers.items()
            if value == "-- Select --"
        ]

        if unanswered:
            st.warning(
                f"Please answer all 10 questions. "
                f"{len(unanswered)} question(s) are unanswered."
            )
            return

        score = 0
        review = []

        for i, q in enumerate(questions):
            selected = answers[i]
            correct = q["options"][q["answer"]]
            is_correct = selected == correct

            if is_correct:
                score += 1

            review.append({
                "number": i + 1,
                "correct": is_correct,
                "selected": selected,
                "answer": correct,
                "explanation": q["explanation"],
            })

        passed = score >= 6
        save_progress(username, language, day, score, 10)

        st.session_state.assessment_results[key_base] = {
            "score": score,
            "passed": passed,
            "review": review,
        }

        st.rerun()

    result = st.session_state.assessment_results.get(key_base)

    if result:
        score = result["score"]
        passed = result["passed"]

        st.markdown("---")

        if passed:
            st.markdown(
                f"""
                <div class="result-pass">
                    <h3>🎉 Day {day} Completed!</h3>
                    <h2>{score}/10</h2>
                    <p>You passed the assessment. Keep going!</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if score >= 8:
                st.balloons()
        else:
            st.markdown(
                f"""
                <div class="result-fail">
                    <h3>📖 Keep Practicing</h3>
                    <h2>{score}/10</h2>
                    <p>You need 6/10 to pass. Review the explanations below and try again.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("### 🔎 Answer Review")

        for item in result["review"]:
            if item["correct"]:
                st.success(
                    f"Q{item['number']} — Correct\n\n"
                    f"Answer: {item['answer']}\n\n"
                    f"Why: {item['explanation']}"
                )
            else:
                st.error(
                    f"Q{item['number']} — Incorrect\n\n"
                    f"Your answer: {item['selected']}\n\n"
                    f"Correct answer: {item['answer']}\n\n"
                    f"Why: {item['explanation']}"
                )

    st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# LANGUAGE PLAN
# ============================================================
def show_language_plan(username, language, hours):
    info = LANGUAGES[language]
    progress = get_progress(username, language)

    completed = sum(
        1 for item in progress.values()
        if item["completed"]
    )

    avg_score = 0
    scored = [
        item["score"] for item in progress.values()
        if item["completed"]
    ]
    if scored:
        avg_score = sum(scored) / len(scored)

    st.markdown(
        f"""
        <div class="hero">
            <h1>{info['emoji']} {language} — 30 Day Roadmap</h1>
            <p>Learn → Practice → Take the assessment → Track your progress.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    s1, s2, s3, s4 = st.columns(4)

    stats = [
        ("Days Completed", f"{completed}/30"),
        ("Daily Hours", f"{hours:g} hr"),
        ("Average Score", f"{avg_score:.1f}/10"),
        ("Completion", f"{completed / 30 * 100:.0f}%"),
    ]

    for col, (label, value) in zip([s1, s2, s3, s4], stats):
        with col:
            st.markdown(
                f"""
                <div class="stat">
                    <div class="stat-number">{value}</div>
                    <div class="stat-label">{label}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.progress(completed / 30)

    st.markdown("### 🗓️ Your 30-Day Learning Path")

    for day in range(1, 31):
        topic = info["topics"][day - 1]
        item = progress.get(
            day,
            {"completed": False, "score": 0, "total": 10},
        )

        status = "✅ Completed" if item["completed"] else "🔵 Not completed"
        score_text = (
            f" • Score {item['score']}/{item['total']}"
            if item["completed"] else ""
        )

        with st.expander(
            f"{'✅' if item['completed'] else '📅'} "
            f"Day {day}  •  {topic}  •  {status}{score_text}"
        ):
            st.markdown(
                f"""
                <div class="day-header">
                    <strong>Day {day}: {html.escape(topic)}</strong><br>
                    <span style="opacity:.7">
                        Study target: {hours:g} hour(s)
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            b1, b2, b3 = st.columns(3)
            b1.link_button(
                "▶️ Learn on YouTube",
                youtube_url(language, topic),
                use_container_width=True,
            )
            b2.link_button(
                "💻 Find Practice",
                practice_url(language, topic),
                use_container_width=True,
            )
            b3.link_button(
                "📚 Official Docs",
                docs_url(language),
                use_container_width=True,
            )

            st.markdown("---")
            render_assessment(
                username,
                language,
                day,
                topic,
            )


# ============================================================
# MAIN APP
# ============================================================
def main_app():
    username = st.session_state.username
    saved = get_user_languages(username)

    with st.sidebar:
        st.markdown("## 📚 StudyForge")
        st.caption(f"Logged in as **{username}**")
        st.divider()

        st.markdown("### 🎯 Quick Navigation")
        if st.button("🏠 Dashboard", use_container_width=True):
            st.session_state.open_language = None
            st.rerun()

        st.divider()

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.open_language = None
            st.rerun()

    st.markdown(
        """
        <div class="hero">
            <h1>📚 My Study Planner</h1>
            <p>
                Choose what you want to learn, set your daily pace,
                practice every day and prove your skills with practical assessments.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### ⚙️ Build Your Learning Plan")
    st.caption(
        "You can learn multiple languages at the same time. "
        "Each language has its own 30-day roadmap and progress."
    )

    selected = st.multiselect(
        "Choose languages",
        list(LANGUAGES.keys()),
        default=list(saved.keys()),
        format_func=lambda x: f"{LANGUAGES[x]['emoji']} {x}",
    )

    for old_lang in list(saved.keys()):
        if old_lang not in selected:
            remove_user_language(username, old_lang)
            if st.session_state.open_language == old_lang:
                st.session_state.open_language = None

    if selected:
        st.markdown("### ⏱️ Daily Study Time")

        cols = st.columns(min(len(selected), 4))

        for i, language in enumerate(selected):
            with cols[i % len(cols)]:
                current = float(saved.get(language, 1.0))
                hours = st.slider(
                    f"{LANGUAGES[language]['emoji']} {language}",
                    0.5,
                    8.0,
                    current,
                    0.5,
                    key=f"hours_{language}",
                )
                save_user_language(username, language, hours)

    st.divider()

    if not selected:
        st.info(
            "👆 Choose at least one language to create your 30-day study plan."
        )
        return

    # Refresh saved values after sliders.
    saved = get_user_languages(username)

    st.markdown("### 🚀 Your Learning Dashboard")

    cols = st.columns(min(len(selected), 4))

    for i, language in enumerate(selected):
        info = LANGUAGES[language]
        progress = get_progress(username, language)
        done = sum(
            1 for item in progress.values()
            if item["completed"]
        )

        with cols[i % len(cols)]:
            st.markdown(
                f"""
                <div class="language-card"
                     style="background: linear-gradient(135deg,
                     {info['color']}, #111827);">
                    <div class="emoji">{info['emoji']}</div>
                    <div class="title">{language}</div>
                    <div class="small">
                        {done}/30 days complete •
                        {saved.get(language, 1.0):g} hr/day
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                f"Open {language} Roadmap",
                key=f"open_{language}",
                use_container_width=True,
            ):
                st.session_state.open_language = language
                st.rerun()

    if (
        st.session_state.open_language
        and st.session_state.open_language in selected
    ):
        st.divider()
        language = st.session_state.open_language
        show_language_plan(
            username,
            language,
            saved.get(language, 1.0),
        )


# ============================================================
# ENTRY POINT
# ============================================================
if st.session_state.logged_in:
    main_app()
else:
    auth_page()
