#!/bin/bash

# faster interactive check
[[ $- == *i* ]]&& export is_interactive=1

is_login(){
    shopt -q login_shell
    return
}

is_interactive(){
    [[ $is_interactive == 1 ]]
}

get_hostname(){
    [[ -v hostnamE ]] && [[ -n $hostnamE ]] || update_hostname
    echo "${hostnamE}"
}
update_hostname(){
    export hostnamE=$(hostname)
}
check_pc(){
    shopt -qs extglob
    true_file_to_check="${HOME}/.is_prefix"
    false_file_to_check="${HOME}/.is_not_prefix"
    [[ -a "${false_file_to_check}" ]] && return 1
    [[ -a "${true_file_to_check}" ]] && return 0
    [[ $( get_hostname ) == @(izbs-tf-*|iamcms-mze-*) ]]
}

setup_display(){
    if [[ -v $DISPLAY ]];then
        setup_x $(get_hostname)
    fi
}


#### case combining functions with stuff in needed all cases combined with "-" ####

setup_login-interactive(){
    #
    echo -n .
    export GIT_PS1_SHOWDIRTYSTATE=1
    export GIT_PS1_SHOWCOLORHINTS=1
    export GIT_PS1_HIDE_IF_PWD_IGNORED=1
    export GIT_PS1_SHOWUNTRACKEDFILES=1
    export GIT_PS1_SHOWUPSTREAM="auto verbose name"
    echo -n .
    export INPUTRC="~/.inputrc"
    echo -n .
    export PROMPT_COMMAND='__git_ps1 "$c_lblue___\u$c_green__@$c_blue___\h:$c_white__\w$c_clear" "$c_lblue___#$c_clear__"'
    echo -n .
}


####   base functions with stuff needed for the case as base ####

setup_base(){
    shopt -qs extglob
    shopt -qs checkwinsize
}


setup_interactive(){
    shopt -s cdspell cmdhist
    source ~/.git-prompt.sh
    setup_display
    [[ -v CLIPBOARD_FILE ]] && [[ -n CLIPBOARD_FILE ]] || export CLIPBOARD_FILE="/tmp/sodufosuuu"
    [[ -v CLIPBOARD_META_FILE ]] && [[ -n CLIPBOARD_META_FILE ]] || export CLIPBOARD_META_FILE="/tmp/sodufosuu"
}


setup_login(){
    
    update_hostname

    export c_red____='\[\e[31m\]'
    export c_green__='\[\e[32m\]'
    export c_yellow_='\[\e[33m\]'
    export c_blue___='\[\e[34m\]'
    export c_magenta='\[\e[35m\]'
    export c_cyan___='\[\e[36m\]'
    export c_white__='\[\e[37m\]'
    export c_clear__='\[\e[0m\]'
    
    export c_lred____='\[\e[1;31m\]'
    export c_lgreen__='\[\e[1;32m\]'
    export c_lyellow_='\[\e[1;33m\]'
    export c_lblue___='\[\e[1;34m\]'
    export c_lmagenta='\[\e[1;35m\]'
    export c_lcyan___='\[\e[1;36m\]'
    export c_lwhite__='\[\e[1;37m\]'
    export c_lclear__='\[\e[0m\]'
}

### functions that contain all stuff needed for the case ###

setup_login_interactive(){
    echo -n .
    setup_base
    echo -n .
    setup_login
    echo -n .
    setup_interactive
    echo -n .
    setup_login-interactive
    echo -n .
}

debug(){
    echo ${FUNCNAME[ 1 ]} >&2
}


setup_fzf(){
    if [[ -f ~/.fzf.bash ]]; then
    
        # Place this into your .bashrc after installing FZF,
        # Then update your .tmux.conf and create key-bindings. Example:
        #
        # unbind s
        # bind   s run "tmux new-window -n 'Switch Session' 'bash -ci tmux_select_session'"
        # unbind K
        # bind   K run "tmux new-window -n 'Kill Session' 'bash -ci tmux_kill_session'"
        # unbind C
        # bind   C run "tmux new-window -n 'Create Session' 'bash -ci tmux_create_session'"
        # unbind C-c
        # bind   C-c run "tmux new-window -n 'Create Session' 'bash -ci PROJECT_PATHS= tmux_create_session'"
    	source ~/.fzf.bash
    
    	_tmux_select_session () (
    		set -eo pipefail
    		local -r prompt=$1
    		local -r fmt='#{session_id}:|#S|(#{session_attached} attached)'
    		{ tmux display-message -p -F "$fmt" && tmux list-sessions -F "$fmt"; } \
    			| awk '!seen[$1]++' \
    			| column -t -s'|' \
    			| fzf -q'$' --reverse --prompt "$prompt> " \
    			| cut -d':' -f1
    	)
    
    	_find_existing_sid () (
    		set -eo pipefail
    		local -r name=$1
    		sid=$(tmux list-sessions -F '#{session_name}:#{session_id}' \
    			| grep "$name" \
    			| head -n 1 \
    			| cut -d ':' -f 2
    		)
    
    		if [ -n "$sid" ]; then
    			echo "$sid"
    			return 0
    		else
    			return 1
    		fi
    	)
    
    	# Select selected tmux session
    	# Note: To be bound to a tmux key in from .tmux.conf
    	# Example: bind-key s run "tmux new-window -n 'Switch Session' 'bash -ci tmux_select_session'"
    	tmux_select_session () (
    		set -eo pipefail
    		_tmux_select_session 'switch session' | xargs tmux switch-client -t
    	)
    
    	# Kill selected tmux session
    	# Note: To be bound to a tmux key in from .tmux.conf
    	# Example: bind-key K run "tmux new-window -n 'Kill Session' 'bash -ci tmux_kill_session'"
    	tmux_kill_session () (
    		set -eo pipefail
    		_tmux_select_session 'kill session' \
    			| {
    				read -r id
    				echo "$id"
    				next=$(tmux list-sessions -F '#{session_id}' | grep -v -F "$id" | head -n1)
    				if [ -n "$next" ]; then
    					tmux switch-client -t "$next"
    				fi && tmux kill-session -t "$id"
    			}
    	)
    
    	tmux_session_name () {
    		sed <<< "$1" 's/[.:]/-/g'
    	}
    
    	# Create a new tmux session
    	# Note: we must spawn the sessions in detached mode and the use
    	# `switch-client` to attach to them. Otherwise we'd get an error saying
    	# that the "terminal is not available"
    	# Note: To be bound to a tmux key in from .tmux.conf
    	# Example: bind-key C run "tmux new-window -n 'Create Session' 'bash -ci tmux_create_session'"
    	tmux_create_session () (
    		unset TMUX
    		set -eo pipefail
    		local new_session_id
    		{
    			new_session_id=$(
    				set -eo pipefail
    				if [ -z "$PROJECT_PATHS" ]; then
    					echo 'Create new session (Ctrl-C to cancel):'
    					echo 'Set $PROJECT_PATHS to streamline this process.'
    					echo
    					read -rep "Set working directory (default: \"$PWD\"):"$'\n> ' dir && \
    					if [ -z "$dir" ]; then dir=$PWD; fi && \
    					echo
    					read -rp "Set name (default \"${dir##*/}\"):"$'\n> ' name && \
    					if [ -z "$name" ]; then name=${dir##*/}; fi
    					tmux new-session -d -c "$dir" -n "$name" -s "$(tmux_session_name "$name")" -P -F "#{session_id}"
    				else
    					local projects=(${PROJECT_PATHS//:/ })
    					for dir in "${projects[@]}"; do
    						if [ -d "$dir" ]; then
    							find "${dir%*/}" -maxdepth 1 -type d | tail -n+2
    						fi
    					done \
    						| awk '!seen[$1]++' \
    						| fzf --reverse --prompt 'Create new session - choose project: ' --expect='~' \
    						| {
    							read -r key;
    							if [[ "$key" == '~' ]]; then
    								tmux new-session -d -c ~ -P -F "#{session_id}"
    							else
    								read -r dir;
    								name=${dir##*/}
    								_find_existing_sid "$name" || {
    									tmux new-session -d -c "$dir" -n "$name" -s "$(tmux_session_name "$name")" -P -F "#{session_id}"
    								}
    							fi
    						}
    				fi
    			) && tmux switch-client -t "$new_session_id"
    		}
    	)
    fi
}

###### main part ######

is_interactive&&echo -n bash init

# login? -> add env vars export
# interactive? -> add interactive stuff
# pc? -> pc add stuff
is_login&&echo -n .l. >&2
is_interactive&&echo -n .i. >&2
check_pc&&echo -n .pc. >&2
if is_login ; then
    if is_interactive ; then
        if check_pc ; then
            source "${HOME}/.bashrc_pc"
            setup_login_interactive_pc
        else
            setup_login_interactive
        fi
    else
        if check_pc ; then
            source "${HOME}/.bashrc_pc"
            setup_login_pc
        else
            setup_login
        fi
    fi
else
    if is_interactive ; then
        if check_pc ; then
            source "${HOME}/.bashrc_pc"
            setup_interactive_pc
        else
            setup_interactive
        fi
    else
        if check_pc ; then
            source "${HOME}/.bashrc_pc"
            setup_pc
        else
            setup_base
        fi
    fi
fi
# finish the line

x(){
    exit
}

is_interactive && echo done
