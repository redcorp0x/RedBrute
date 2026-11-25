import config

def read_in_batches():
    if config.stop:
        return None
    try:
        batch = []
        with open(config.wordlist, "r", encoding="latin-1") as wordlist:
            for position,line in enumerate(wordlist):
                item = line.strip()
                if not item:
                    continue
                batch.append((position,item))
                if len(batch) == config.batch:
                    yield batch
                    batch = []
            if batch:
                yield batch
    except KeyboardInterrupt:
        print("\n[WARN] Extraction was interrupted Ctrl-C")
        return