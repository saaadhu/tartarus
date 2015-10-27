FILE1=$1
FILE2=$2

vimdiff <(python tartarus.py <(avr-objdump -S $FILE1) <(avr-objdump -r $FILE1) <(avr-objdump -t $FILE1)) <(python tartarus.py <(avr-objdump -S $FILE2) <(avr-objdump -r $FILE2) <(avr-objdump -t $FILE2)) 

