" TODO : Add finish guards
if get(g:, 'vim_usd_goto_loaded', 0) == 1
    finish
endif

xnoremap <silent> <Plug>VimUsdGotoEditFileSelection :call usd#run_command_on_usd_file('edit', 'visual')<CR>
nnoremap <silent> <Plug>VimUsdGotoEditFile :call usd#run_command_on_usd_file('edit', 'normal')<CR>

let g:vim_usd_goto_loaded = 1
