## Sigma LS

![Sigma](sigma.jpeg)

This is not based on the popular sigma memes you see around. It is instead intended as a language server for sigma rules.

Sigma rules are yaml files that contain info to detect malicious behavior when suspecting log files in various SIEMs.

I have been writing a lot of these rules lately and I use neovim (btw), so I wanted to make it easy for myself. It may be useful to you or not.

> Note: This code was written when I was a bit ill so expect functional but awful code.

## To do 
- Supposed to allow for code completion
- Supposed to allow for snippets too
- Since I'm doing this for Neovim, I won't write a client, I'll just connect to it using lua.
- Extend telescope to show backend conversion to various backends like elasticsearch

Let's do this
