" TODO : Add finish guards
if get(g:, 'vim_usd_goto_loaded', 0) == 1
    finish
endif

xnoremap <silent> <Plug>VimUsdGotoEditFileSelection :call usd#run_command_on_usd_file('edit', 'visual')<CR>
nnoremap <silent> <Plug>VimUsdGotoEditFile :call usd#run_command_on_usd_file('edit', 'normal')<CR>

" This command forces the found path from ":norm gf" to be run through USD's ArResolver
set includeexpr=usd#resolve(v:fname)

" The default expression for finding paths in Vim is too strict. It only
" searches for paths like "/foo.py". We need Vim to allow URI-friendly
" characters like ":", "?", and "&". Otherwise, an incomplete path will
" be passed to ArResolver and `usd#resolve` will fail.
"
" Reference: `:help isfname`
"
set isfname=@,48-57,/,.,-,_,+,,,#,$,%,~,=,:,?,&

let g:vim_usd_goto_loaded = 1
