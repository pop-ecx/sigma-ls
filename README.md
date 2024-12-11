## Sigma LS

![Sigma](sigma.jpeg)

A small Language server to assist in writing sigma rules.

Sigma rules are yaml files that contain info to detect malicious behavior when suspecting log files in various SIEMs.

I have been writing a lot of these rules lately and I use neovim (btw), so I wanted to make it easy for myself. It may be useful to y'all.

The LS provides features such as diagnostics and completion. I've also created a little plugin for compiling with sigmac from within neovim itself.
No need to leave your beloved editor when writing sigma rules. You can get the conversion plugin [here](https://github.com/pop-ecx/sigma_picker.nvim) 


## How it feels
Real time diagnostics is provided as you write your sigma rules
![diagnostics](sigma-ls.png)


## Installation instructions
To connect to the LSP in Neovim add this to your init.lua file
```lua
vim.api.nvim_create_autocmd('FileType', {
  pattern = 'yaml',
  callback = function (args)
    vim.lsp.start({
      name = 'Sigma_ls',
      cmd = {"<poetry env info path>/bin/python", "/home/m3lk0r/Desktop/sigma-ls/main.py"},
    })
  end,
})
```

> :warning: This is still WIP.
