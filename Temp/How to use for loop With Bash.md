# How to use for loop With Bash

[How to read complete line in 'for' loop with spaces](https://askubuntu.com/questions/344407/how-to-read-complete-line-in-for-loop-with-spaces)

### 下面这个如果文件名有空格的话，将会将空格当成分隔符：
`for i $(ls); do echo "$i"; done`


### 如果想将完整的文件名（含空格）输出。需要设置 IFS，详见[IFS (Internal Field Separator)](https://unix.stackexchange.com/questions/16192/what-is-ifs-in-context-of-for-looping)

```
IFS=$'\n'       # make newlines the only separator
for j in $(ls)    
do
    echo "$j"
done
# Note: IFS needs to be reset to default!
```
使用完后设置回去
```
unset IFS
```

## Example
SVN 文件的批量操作：
```
for i in  $(svn st | grep \! | awk -F '^[!][ \t]*?' '{print $2}'); do svn delete $i@; done
```