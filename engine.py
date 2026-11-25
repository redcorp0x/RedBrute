import config
import loadBatch
from datetime import datetime
import request
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style

def send_request(word):
    if config.stop:
        return None
    try:
        response = request.dispatch_request(word)
        if response == True:
            return word
    except KeyboardInterrupt:
        print("\n[WARN] Extraction was interrupted Ctrl-C")
        return

def threader():
    try:
        if config.verbose:
            print(f"{Fore.RED}{Style.BRIGHT}RedBrute{Style.RESET_ALL}{Fore.WHITE} is a Python-Based high-performance web brute-forcing tool designed to make large-scale wordlist processing more efficient and resource-conscious. It leverages batch-based wordlists processing to {Fore.CYAN}reduce memory consumption{Fore.WHITE} while utilizing concurrent HTTP request execution to improve scanning and overall performance.{Style.RESET_ALL}\n")
        with ThreadPoolExecutor(max_workers=config.thread) as executor:
            if config.stop:
                executor.shutdown(wait=False, cancel_futures=True)
            start_time = datetime.now()
            for batch_number,batch in enumerate(loadBatch.read_in_batches(), start=1):
                completed = 0
                batch_number = batch_number
                futures = {}
                batch_total = len(batch)                
                for position, word in batch:
                    future = executor.submit(send_request, word=word)
                    futures[future] = (position, word)
                    
                for future in as_completed(futures):
                    position,word = futures[future]
                    position = position
                    word = word
                    result = future.result()
                    completed += 1
                    percentage = (completed/batch_total) * 100
                    status = f"{Fore.GREEN}{Style.BRIGHT}SUCCESSFUL{Style.RESET_ALL}" if result else f"{Fore.YELLOW}{Style.BRIGHT}RUNNING{Style.RESET_ALL}"
                    display_word = word[:15] + "..." if len(word) > 12 else word
                    print(
                        f"\r\033[KProgress: {percentage:.2f}% | Batch Number: {batch_number:<2} | "
                        f"Current: {display_word:<15} | "
                        f"Position: {position:<3} | " 
                        f"Status: {status:<7} ", end="", flush=True
                    )
                    if result:
                        current_word = f"{Fore.GREEN}{Style.BRIGHT}{word}{Style.RESET_ALL}"
                        elapsed = int((datetime.now() - start_time).total_seconds())
                        minutes,seconds = divmod(elapsed, 60)
                        print(
                            f"\r\033[KWord: {current_word:<4} | "
                            f"Position: {position:<3} | " 
                            f"Status: {status:<7} | "
                            f"Elapsed: {minutes:02d}:{seconds:02d} ", end="", flush=True
                        )
                        config.stop = True
                        for pending in futures:
                            if pending != future:
                                pending.cancel()
                        executor.shutdown(wait=False, cancel_futures=True)
                        print("\n\n[!] Program Ended.")
                        return
    except KeyboardInterrupt:
        print("\n[WARN] Extraction was interrupted Ctrl-C")
        return
    