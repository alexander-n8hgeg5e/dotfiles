# dotfiles
This is what you have dreamed of ever since.

        ### Warning ###
        No warranty for anything.
        This manual and the software is probably incomplete and full of bugs additionally contains some crapy stuff.
        If not mentioned or not conflicting with copyrights or rights of others my licence is gpl-v3.

I suggest to install it anyway.

## Description:
My dotfiles are a user interface based on **neovim** , **neovim's terminal emu** ,
**Tmux** and some useful scripts, called shortcuts.
They make use of vims **python interface** to , for instance
load a file to edit into vim.
vim is the main user interface and configured
to switch, resize, open  easily  windows, tabs, terminals.
Tmux is used to run the programs started in vim's terminal.
Tmux is used inside vim and not vim inside tmux.
Because: vim can copy all terminal stuff, scroll the underlying tmux
buffer. vim is better suited to do the window swiching and text copy
and paste stuff.
I can paste text out of vim buffer into the terminal with a vim
shortcut.
This is the full control over your computer.
The keybindings of vim are autogenerated from a vim dictonairy.
They are sorted for the additional modes/states that my vim use.
Terminal , Ex-mode, default.
Insider of each mode exist all usual vim modes.
So it is easy to configure the keybinds.
My vim config makes use of a special highlighting of 
"cursorcolumn" and "cursorline" this highlighing
switches color and indicates the mode.
Only the  active window is with cursorcolumn,line enabled.
This  was not possible without small modification of the vim code.

**Many more features!**


## dependencies:

* My vim config needs neovim version 0.3.1 + my patches onto it

  * patches:  [my-portage-repo](https://github.com/alexander-n8hgeg5e/my-portage-repo/app-editors/neovim/files/)
 
  * build
 
    * either read the ebuild and build like that:

      * see in this file for source url and for what commit to checkout
         [my neovim ebuild](https://github.com/alexander-n8hgeg5e/my-portage-repo/app-editors/neovim/neovim-0.3.1.ebuild)
  
      * configure with python enabled, some other stuff enabled
      
      * don't forget to patch manually
  
    * or:
  
      * make new user with new home dir
  
      * make subdir gentoo inside inside new home dir as the new user
  
      * extract a gentoo stage3 tarball there
  
      * chroot into this dir as described in for example for amd64 architectur:
        [Gentoo Chroot](https://wiki.gentoo.org/wiki/Handbook:AMD64/Installation/Base#Chrooting)
  
      * missing parts of information that i missed here are in the Gentoo Handbook:
        [Gentoo Handbook](https://wiki.gentoo.org/wiki/Handbook:Main_Page)
  
      * I'ts not that hard as it seem in the first place.
        You can get away with tar ball extracting , a bit mounting, then chroot
        and you are nearly ready to compile gentoo stuff.
  
      * clone my repo: [repo](https://github.com/alexander-n8hgeg5e/my-portage-repo)
        to chroots envs: "/usr/local/portage" not "/usr/local/portage/my-portage-repo"
  
      * add it to gentoo:
        maybe it's enough to add these 3 lines to 
        "/etc/portage/repos.conf/localrepo.conf"
        ```
        [my]
        location = /usr/local/portage
        priority = 1000
        ```
  
      * emerge neovim with emerge =app-editors/neovim-0.3.1::my
  
        * patches are auto applied
  
        * portage complains about stuff, fix stuff
  
* shortcuts: [shortcuts](https://github.com/alexander-n8hgeg5e/shortcuts)

      ### Attention
      My shortcuts install many really short commands to the chroot or whereever you install it.
      So be prepared not to hit enter. It could do something.
      The most dangerous commands, i guess, are "sd" shuts down and l locks the screen or "s" suspend.
      So don't be afraid, but no warranty if anything happens you don't want.
      ###

  * emerge shortcuts: "emerge shortcuts"

  * make portage happy emerge missing deps, maybe included in my repo

  * open a file with "e filename"

* Dep best to run this with a special keyboard layout. I use a lets-split keyboard by wootpatoot that i customized for my needs.

  * The layout is similar to the keymap in my nlthr repo and is derived from it.

  * key features of the layout

    * easy to learn
  
    * never need to move your hands while typing.
  
      * maximum movement is a bit rotation, but seldom needed
  
      * usally only finge movement.
  
    * no problems and no deseases from typing to much
  
      * whether you use vim or emacs or 
        useing ctrl-whatever thousand times,
        -> nearly no fatigue of anything
  
  * wait some time , if i have spare time i will load it up to github 
