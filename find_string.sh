#Search for “my konfu is the best” in all *.py files, print matched file list
grep -r 'my konfu is the best' * | cut -d':' -f1