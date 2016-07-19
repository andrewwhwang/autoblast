echo $2 | blastn -task blastn -max_hsps 1 -max_target_seqs 1 -db $1 -outfmt "6 qseqid sgi sstart send slen" -num_threads 8
