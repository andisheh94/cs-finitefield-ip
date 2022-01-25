for f in $(cat files_to_be_deleted.txt) ; do 
  rm "$f"
done
