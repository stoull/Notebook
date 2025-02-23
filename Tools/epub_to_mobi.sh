

# 注意会将目录下所有的.epub 转成 .mobi格式，并删除.epub 文件
# mac 上先安装 calibre

find . -type f -name '*.epub' -print0 | while IFS= read -r -d '' file; do
    printf '%s\n' "$file"
    printf "${file%.epub}.mobi \n"
    newFile="${file%.epub}.mobi"
    /Applications/calibre.app/Contents/MacOS/ebook-convert "$file" "$newFile" --prefer-author-sort --output-profile=kindle --linearize-tables --smarten-punctuation --enable-
    rm "$file"
done