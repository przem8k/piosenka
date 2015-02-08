augroup filetypedetect
    au FileType python
        \ setlocal ts=4 sts=4 sw=4 textwidth=80 nocindent
augroup END

let g:syntastic_python_flake8_args='--max-line-length=80'
