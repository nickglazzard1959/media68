#!/bin/bash
echo "Rebuild book media static website."
echo "Assumes /mnt/booklib is aliased to external-files3."
echo "Index file is bindex.html."
a68g files_to_html.a68 -- -r /mnt/booklib/ -o book_site -p book -v -e '.pdf' --multi -f external-files3 -i bindex.html -t "Book Collection"
