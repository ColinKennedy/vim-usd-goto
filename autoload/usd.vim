" This function had to be moved to autoload to avoid this issue with Vim commands
" Reference: https://stackoverflow.com/a/22633702/3626104
"
function! usd#run_command_on_usd_file(command, mode)
pythonx << EOF
import usd_path_finder
import vim

path = usd_path_finder.get_selected_path(vim.eval('a:mode'))
vim.command('let l:usd_file_path = "{path}"'.format(path=path))
EOF

    execute ':' . a:command . ' ' . l:usd_file_path
endfunction
