## Integrate with Neovim
Add the following to your init.lua
```lua
vim.api.nvim_create_autocmd('FileType', {
  pattern = 'yaml',
  callback = function (args)
    vim.lsp.start({
      name = 'Sigma_ls',
      cmd = {"<poetry env info path>/bin/python", "/path/to/repo/main.py"},
    })
  end,
})
```
