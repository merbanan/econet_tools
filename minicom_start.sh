FW_SIZE=`ls -la initramfs | awk '{printf "%x\n", $5}'`
export FW_SIZE
minicom -D /dev/ttyUSB0 -S minicomscript.txt -C capturefile.txt

