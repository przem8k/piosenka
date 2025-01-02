#!/bin/zsh

# Initialize an associative array to store line counts for each file type
declare -A line_counts
total_lines=0

# Function to process files of a given extension
process_files() {
  local ext="$1"
  local count=$(git ls-files | grep ".$ext$" | grep -v third_party | grep -v migrations | xargs wc -l | tail -n 1 | awk '{print $1}')
  
  # If no files of this type, count will be empty. 
  if [[ -z "$count" ]]; then
    count=0
  fi

  printf "%-5s: %s\n" "$ext" "$count" 
  line_counts[$ext]=$count
  ((total_lines += count))
}

# Process different file types
process_files "py"
process_files "html"
process_files "js"
process_files "css"

# Display the total line count
echo "-----------------------"
echo "total: $total_lines"