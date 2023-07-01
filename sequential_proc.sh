#!/bin/bash
# Read landmark names from input arg #1 and 
# for each name create a folder that collects
# all point cloud file into it that have been 
# labelled the landmark name. 
# Run a train/eval/test process for each folder

# Usage : "sh train_lnd.sh caesar landmark_names.txt smpl_folder_dir file_locs.pk mapper.py has_lnd.py"

echo "input args - $1 $2 $3 $4 $5 $6"

# create a new_directory for all caesar landmarks
if [ ! -d "$1" ];
then
    mkdir "$1"
fi
cd "$1"

# check args
echo "checking correctness of args ..." 
if [ ! -e "$2" -o ! -d $3 -o ! -e $4 -o ! -e $5 -o ! -e $6 ];
then
    echo "check your file paths again, one of them does not exist"
    exit 1
fi

function transform_name(){
    local name="$1"
    local new_name=$(echo "$name" | sed -e 's/[\/\ ]/_/g' -e 's/,//g' | tr A-Z a-z)
    echo "$new_name"
}

NAMES=()
while read name
    do 
        #echo "name - $name"
        # handle punctuations - replace spaces and forward slashes with underscores; commas with spaces
        new_name=$(transform_name "$name") #echo "$name" | sed -e 's/[\/\ ]/_/g' -e 's/,//g' | tr A-Z a-z)
        # create a folder titled = "_" separated names in the landmark name e.g 
        # the folder named 10th_rib_midspine represents 10th Rib Midspine 
        NAMES+=("$name")
        if [ ! -d $new_name ];
        then 
            echo "creating a new directory ... $new_name"
            mkdir $new_name 
        fi
done < "$2"

for lnd_name in "${NAMES[@]}";
do 
    echo "collecting caesar pc files with $lnd_name"
    count=0
    new_name=$(transform_name "$lnd_name")
    register="$new_name/register.txt"
    # echo "old name - $lnd_name ; new name - $new_name"
    for filename in $(ls $3); # all smpl numpy files
        do
            path2file=$(python3 "$5" "$4" "$2" "$filename")
            echo "filekey - $filename $path2file"
            if [[ ! -e $path2file ]]; 
            then 
                echo "this file - {$path2file} does not exist !"
                exit 1
            fi
            # echo "full path is $path2file"
            has_lnd=$(python3 "$6" "$path2file" "$lnd_name" "$1")
            echo "output- $path2file $has_lnd"
            if [[ $has_lnd == "True" ]]; then
                echo "writing file path to register ..."
                word1=$path2file
                word2="$3/$filename"
                line="${word1}\t${word2}"
                echo "$line"
                echo "$line" >> $register
                ((count+=1))
            elif [[ $has_lnd == "False" ]]; then
                echo "$lnd_name not on $filename"
                
            fi
    done
    echo "$count files got copied into $new_name"

done
