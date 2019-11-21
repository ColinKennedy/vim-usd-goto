if get(g:, 'vim_usd_goto_loaded', 0) == 1
    finish
endif

" This command forces the found path from ":norm gf" to be run through USD's ArResolver
set includeexpr=usd#resolve(v:fname)

let g:vim_usd_goto_loaded = 1
