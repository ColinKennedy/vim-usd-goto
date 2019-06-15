function! usd#resolve(path)
pythonx << EOF
import usd_path_finder
import vim

path = usd_path_finder.resolve(vim.eval('a:path'))
vim.command('let l:usd_file_path = "{path}"'.format(path=path))
EOF

    if l:usd_file_path == ''
        echoerr 'No USD file could be found'
        return ''
    endif

    return l:usd_file_path
endfunction
