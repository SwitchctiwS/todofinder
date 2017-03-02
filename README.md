#todofinder
Recurses in folder and finds all the different todo's in a file and outputs every todo to stdout. If there is a file named 'TODO.txt' or 'todo.txt' as the input, then it will output that file's contents. 

##Operation
Put HTML-like todo flags around code, bullet points, etc.

```
<TODO>
[...]
</TODO>
```
or
```
<TODO>[...]</TODO>
```

##Input
Program takes in a list of files/folders with arguments. Help argument is `-h` or `--help`.

```
todofinder.py [option(s)] file(s)/folder(s)
```

##Output
All text between the todo flags will be output to stdout with line numbers.

###Example
```
filename: file.txt
23 <TODO>Todo Text</TODO>
```
At stdout:
```
file.txt
	TODO1
	  23 Todo Text
	END1
```

##Todo
(heh)
<ul>
<li>Find TODO.txt/todo.txt and output all text</li>
<li>Add exceptions</li>
</ul>
