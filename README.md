## Sigma LS

![Sigma](sigma.jpeg)

A small Language server to assist in writing sigma rules.

Sigma rules are yaml files that contain info to detect malicious behavior when suspecting log files in various SIEMs.

I have been writing a lot of these rules lately and I use neovim (btw), so I wanted to make it easy for myself. It may be useful to y'all.

The LS provides features such a s diagnostics and completion. It also has a little extension for compiling with sigmac and get results from within neovim itself.
No need to leave your beloved editor.

> Note: This code was written when I was a bit ill so expect functional but awful code.


## Installation instructions
To connect to the LSP in Neovim add this to your init.lua file
```lua
vim.api.nvim_create_autocmd('FileType', {
  pattern = 'yaml',
  callback = function (args)
    vim.lsp.start({
      name = 'Sigma_ls',
      cmd = {"/home/m3lk0r/pygls/bin/python3.11", "/home/m3lk0r/Desktop/sigma-ls/main.py"},
    })
  end,
})
```

