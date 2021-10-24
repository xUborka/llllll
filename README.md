https://citrimoldin.de/ - 18 - 0
https://www.fils-fine-arts.de/ - 4914 - 0
https://rittercollection.ch/ - 23 - 0
https://sitrag-blachen.ch/ - 1188 - 0
https://wfw.ch/ - 618 - 0
https://www.ivr-ias.ch/ - 73 - 0
https://www.alpenhain.de/ - 803 - 0


pool = Pool(processes=8)
for _ in tqdm.tqdm(pool.imap_unordered(do_work, tasks), total=len(tasks)):
    pass