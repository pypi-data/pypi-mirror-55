# prependnewline

This extension is a third party extension for python markdown. This was developed after an experience with python markdown 
where some lists are ignored if an empty line or paragraph isn't inserted before the list.

The extension prepends a new line to a list if marked as a paragraph by the markdown. 

See the python markdown documentation for more information.
Use it in any personal or commercial project you want.

# Current Version: 1.2

# Example Markdown:

```
This is a paragraph
* Run through albums.
```

# Output:
This is a paragraph
* Run through albums.

# Usage / Setup:

`pip install prependnewline`

`md = markdown.Markdown(extensions=['prependnewline']) `

`converted_text = md.convert(text)`