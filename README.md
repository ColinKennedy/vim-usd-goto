vim-usd-goto lets you navigate Pixar's USD files with ease, even if
those files aren't written as file paths.

In Vim, the `gf` command lets you open files on-disk if the path is
under your cursor. `gf` doesn't work with most USD Asset paths because
pipelines don't write USD files as "/foo/bar/path.usd". It's usually
some syntax like "my_cool_resolver:?database?asset?v10&extension=usda"
or some other crazy syntax.

Example:

```usda
#usda 1.0
(
    subLayers = [
        @foo:/Some[Tokened]/and/weird/path?extension=.usd,.usdc@
    ]
)
```

This plugin lets you put your cursor in-between the @s and press `gf`.
Vim will navigate to the file on-disk as normal, assuming it actually
exists.


## Installation
Use your favorite plugin manager (examples below).

### 1. Get the plugin
#### vim-plug
```vim
Plug 'ColinKennedy/vim-usd-goto'
```

#### Vundle
```vim
Plugin 'ColinKennedy/vim-usd-goto'
```

### 2. Enable ftplugin support
Also make sure that your ~/.vimrc contains 

```vim
filetype plugin on
```

so that the ftplugin folder is sourced whenever you load usd/usda files.

#### Reference
```
:help ftplugin
https://www.gilesorr.com/blog/vim-ftplugin.html
```


### 3. Define a filetype for USD files
If you haven't done this already, you need to `set filetype` for `*.usd` files
so that the files in the ftplugin folder will be sourced.

Add these lines in your `~/.vimrc`.

```vim
autocmd! BufRead,BufNewFile *.usd set filetype=usd
autocmd! BufRead,BufNewFile *.usda set filetype=usda
```


## Requirements
- Vim 8+ with `+eval` support
- [Pixar's USD](https://github.com/PixarAnimationStudios/USD) must be
compiled and sourced


## How the resolver works
This plugin comes with 2 methods for resolving paths.

### Using Python pxr.Ar
- If Vim actually has Pixar's Python packages sourced, this plugin
attempts to run this code

```python
from pxr import Ar
Ar.GetResolver().Resolve(path)
```

where `path` is whatever is under your cursor when `gf` is pressed.


### Using command-line
- If you don't have USD sourced but the `usdresolve` command-line
executable is found, then it is run and its output will be used instead.


## Help With Non-File-Paths
By default, Vim's `gf` command assumes that the user is trying to select
file paths. In USD, you might have some file resource that has a path
like this:

```usd
@foo:/BAR(BAR)?version=3&something_else=this:.could:be:anything@
```

This plugin can't account for every possible syntax you might need. But
if you wanted to support a path like the one above, you only need to add
this to your `~/.vimrc`:

```vim
set isfname=@,48-57,/,.,-,_,+,,,#,$,%,~,=,:,?,&,(,)
```
(Hint: This is just Vim's default `isfname` + some extra allowed symbols)

So if you're looking to use this plugin to resolve URIs, for example,
your install process may look like this:

```vim
Plug 'ColinKennedy/vim-usd-goto'
set isfname=@,48-57,/,.,-,_,+,,,#,$,%,~,=,:,?,&,(,)
```


## Advanced Setup - Custom resolver function
Most people will be able to resolve USD files using the above 2
methods. But if you don't have Python sourced and you can't rely on the
`usdresolve` command-line function, then the last option is to write
your own resolver function and hook it into this plugin.

- To do that, add a file to Vim's plugin folder.

e.g. `~/.vim/plugin/usd_resolver.vim`

```vim
pythonx << EOF
from vim_usd_goto import usd_path_finder

def resolve(path):
    return "/tmp/default_file.usda"

usd_path_finder.register_resolver(resolver)
EOF
```

- Restart Vim
- The next time you try to open a path with `gf`, if no other resolver
method could be found and "/tmp/default_file.usda" then that file will
be opened in Vim, instead.

Any function can be used for resolution but it must follow these rules:

- Takes on argument (the USD Asset path that will be resolved)
- Returns nothing if no path on-disk could be resolved
- Raises no exceptions

As mentioned before though, most people will never have to use a custom
resolver function. The default resolver functions that this plugin comes
with will work for most people, assuming that their USD environment is
set up correctly.
