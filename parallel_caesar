# Read landmark names from input arg #1 and 
# for each name create a folder that collects
# all point cloud file into it that have been 
# labelled the landmark name. 
# Run a train/eval/test process for each folder

# Usage : "bash train_lnd.sh caesar landmark_names.txt smpl_folder_dir file_locs.pk mapper.py has_lnd.py"
# e.g sh train_lnd.sh caesar "/Users/ahmedbaruwa/Desktop/MSThesis/Talapas/landmark_names.txt" \
#        "/Users/ahmedbaruwa/Desktop/MSThesis/Talapas/caesar_smpl" \
#        "/Users/ahmedbaruwa/Desktop/MSThesis/Talapas/file_locs.pk" \
#        "/Users/ahmedbaruwa/Desktop/MSThesis/Talapas/mapper.py"  \ 
#        "/Users/ahmedbaruwa/Desktop/MSThesis/Talapas/has_lnd.py"
#!/bin/bash
echo "input args - $1 $2 $3 $4 $5 $6"
max_processes=6
chmod +x "$5" 
chmod +x "$6"
# create a new_directory for all caesar landmarks
if [ ! -d "$1" ];
then
    mkdir "$1"
fi
cd "$1"

# check args
echo "checking correctness of args ..." 
if [ ! -e "$2" -o ! -d "$3" -o ! -e "$4" -o ! -e "$5" -o ! -e "$6" ];
then
    echo "check your file paths again, one of them does not exist"
    exit 1
fi

dataset_name=$1
lnd_names_file=$2
smpl_folder=$3
file_locs=$4
mapper_script=$5
has_lnd_script=$6

transform_name(){
    local name="$1"
    local new_name=$(echo "$name" | sed -e 's/[\/\ ]/_/g' -e 's/,//g' | tr A-Z a-z)
    echo "$new_name"
}

NAMES=()
while read name
    do 
        #echo "name - $name"
        # handle punctuations - replace spaces and forward slashes with underscores; commas with spaces
        new_name=$(transform_name "$name")
   
        NAMES+=("$name")
        if [ ! -d $new_name ];
        then 
            echo "creating a new directory ... $new_name"
            mkdir $new_name 
        fi
done < "$2"

collect_files(){
    local lnd_name="$1"
    
    local count=0
    local new_name=$(transform_name "$lnd_name")
    local register="$new_name/register.txt"
    # echo "old name - $lnd_name ; new name - $new_name"
    echo "collecting caesar pc files with $new_name"
    for filename in "$3"/*; # over all smpl numpy files
        do
            echo "$filename"
            local path2file=$(python3 "$mapper_script" "$file_locs" "$lnd_names_file" "$filename")
            
            if [[ ! -f $path2file ]]; 
            then 
                echo "this file - {$path2file} does not exist !"
                exit 1
            fi
            # echo "full path is $path2file"
            local has_lnd=$(python3 $lnd_script "$path2file" "$lnd_name" "$dataset_name")
            echo "output- $path2file $has_lnd"
            if [[ $has_lnd == "True" ]]; then
                #echo "$lnd_name label is on $filename, so copying $filename to $new_name"
                
                # cp $path2file $new_name
                echo "writing file path to register ..."
                echo "$path2file" >> $register
                ((count+=1))
            elif [[ $has_lnd == "False" ]]; then
                echo "$lnd_name not on $filename"
                
            fi
    done
    echo "$count files got copied into $new_name"
}

export -f transform_name collect_files

for lnd_name in "${NAMES[@]}";
do 
     echo "$lnd_name" "$2" "$3" "$4" "$5" "$6" #(collect_files $lnd_name)"

done | xargs -I {} -P $max_processes bash -c 'collect_files "{}"'
