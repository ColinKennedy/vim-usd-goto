" TODO : Add finish guards
if get(g:, 'vim_usd_goto_loaded', 0) == 1
    finish
endif

xnoremap <silent> <Plug>VimUsdGotoEditFileSelection :call usd#run_command_on_usd_file('edit', 'visual')<CR>
nnoremap <silent> <Plug>VimUsdGotoEditFile :call usd#run_command_on_usd_file('edit', 'normal')<CR>

" This command forces the found path from ":norm gf" to be run through USD's ArResolver
set includeexpr=usd#resolve(v:fname)

" The default expression for finding paths in Vim is too restrictive. We need
" We need to allow more characters or we won't be able to pick up the full path
" e.g. we must add ":", "?", and "&" as valid characters
"
" Reference: `:help isfname`
"
set isfname=@,48-57,/,.,-,_,+,,,#,$,%,~,=,:,?,&

let g:vim_usd_goto_loaded = 1
