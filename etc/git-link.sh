
# bash completion for the the git link command
# http://github.com/gvalkov/git-link

_git_flow ()
{
    local cur prev opts

    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    opts="-h --help -v --version -c --clipboard -u --url -b --browser -r --raw"
	# tbd: leverage bash's git comlpetion 
}

# vim: ft=sh:
