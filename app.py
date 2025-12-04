import pikepdf
import sys
import time
from datetime import datetime

def print_banner():
    print("\033[1;32m" + "="*60)
    print("        SAFE PDF PASSWORD CRACKER")
    print("="*60 + "\033[0m")
    print("Author: Your Name")
    print("Version: 2.1")
    print("Purpose: For educational use only")
    print("\033[93m" + "⚠️  Legal Use Only: For your own files only" + "\033[0m")

def crack_pdf_password(pdf_file, wordlist_file, max_attempts=10000):
    """
    PDF password crack karne ka secure function - FIXED VERSION for pikepdf v8+
    """
    try:
        print(f"\n\033[96m[*] Target PDF: {pdf_file}")
        print(f"[*] Wordlist: {wordlist_file}")
        print(f"[*] Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"[*] Using pikepdf version: {pikepdf.__version__}\033[0m")
        
        # Wordlist read karna
        try:
            with open(wordlist_file, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()]
        except UnicodeDecodeError:
            # Agar UTF-8 nahi chal raha to binary mode mein try karo
            with open(wordlist_file, 'rb') as f:
                passwords = [line.decode('utf-8', errors='ignore').strip() for line in f if line.strip()]
        
        total = len(passwords)
        if total == 0:
            print("\033[91m[!] Wordlist is empty or couldn't be read!\033[0m")
            return None
        
        print(f"\033[92m[+] Total passwords to try: {total}")
        print(f"[+] Max attempts: {max_attempts}\033[0m")
        
        attempts = 0
        start_time = time.time()
        last_progress_time = start_time
        
        # Brute force attack
        for idx, password in enumerate(passwords):
            if attempts >= max_attempts:
                print(f"\033[93m[!] Max attempts ({max_attempts}) reached\033[0m")
                break
            
            attempts += 1
            
            # Progress display every 100 attempts or 5 seconds
            current_time = time.time()
            if attempts % 100 == 0 or (current_time - last_progress_time) > 5:
                elapsed = current_time - start_time
                rate = attempts / elapsed if elapsed > 0 else 0
                remaining = total - idx
                eta = remaining / rate if rate > 0 else 0
                print(f"\033[94m[*] Progress: {idx}/{total} ({idx/total*100:.1f}%) | Rate: {rate:.1f}/sec | ETA: {eta:.1f} sec\033[0m")
                last_progress_time = current_time
            
            try:
                # PDF open karne ki koshish - FIXED for pikepdf v8+
                with pikepdf.open(pdf_file, password=password) as pdf:
                    end_time = time.time()
                    elapsed = end_time - start_time
                    
                    print("\n" + "\033[1;42m" + "="*60 + "\033[0m")
                    print("\033[1;32m" + "✅ PASSWORD FOUND!" + "\033[0m")
                    print("\033[1;42m" + "="*60 + "\033[0m")
                    print(f"\033[1;32mPassword: \033[1;37m{password}\033[0m")
                    print(f"\033[93mAttempts: {attempts}")
                    print(f"Time: {elapsed:.2f} seconds")
                    print(f"Speed: {rate:.1f} passwords/sec\033[0m")
                    
                    # PDF info show karein
                    print(f"\033[96m[*] PDF Info:")
                    print(f"   Pages: {len(pdf.pages)}")
                    print(f"   Encrypted: {pdf.is_encrypted}")
                    if pdf.docinfo:
                        print(f"   Title: {pdf.docinfo.get('/Title', 'N/A')}")
                        print(f"   Author: {pdf.docinfo.get('/Author', 'N/A')}\033[0m")
                    
                    return password
                    
            except pikepdf.PasswordError:
                # Wrong password, continue - SIMPLIFIED for v8+
                pass
                
            except Exception as e:
                # Agar koi aur error ho to dikhayein
                error_str = str(e).lower()
                if "password" in error_str or "incorrect password" in error_str or "invalid password" in error_str:
                    # Password error hai, continue karo
                    pass
                else:
                    # Unexpected error - show only once every 1000 attempts
                    if attempts % 1000 == 0:
                        print(f"\033[91m[!] Error at attempt {attempts}: {str(e)[:100]}\033[0m")
        
        # Agar password nahi mila
        print("\n" + "\033[1;41m" + "="*60 + "\033[0m")
        print("\033[1;31m" + "❌ PASSWORD NOT FOUND" + "\033[0m")
        print("\033[1;41m" + "="*60 + "\033[0m")
        print(f"\033[93m[*] Final Statistics:")
        print(f"   Total attempts: {attempts}")
        print(f"   Total time: {time.time() - start_time:.2f} seconds")
        print(f"   Average speed: {attempts/(time.time()-start_time):.1f} passwords/sec\033[0m")
        return None
        
    except FileNotFoundError as e:
        print(f"\033[91m[!] File not found: {e}\033[0m")
        return None
    except Exception as e:
        print(f"\033[91m[!] Unexpected error: {e}\033[0m")
        import traceback
        traceback.print_exc()
        return None

def create_sample_wordlist():
    """Sample wordlist banaye"""
    common_passwords = [
        "password", "123456", "12345678", "1234", "qwerty",
        "12345", "dragon", "baseball", "football", "letmein",
        "monkey", "abc123", "111111", "mustang", "access",
        "shadow", "master", "michael", "superman", "696969",
        "123123", "admin", "welcome", "password123", "123456789",
        "sunshine", "iloveyou", "trustno1", "admin123", "letmein123",
        "1234567890", "password1", "qwerty123", "1q2w3e4r", "test123"
    ]
    
    # Digital date patterns
    for year in range(2000, 2026):
        common_passwords.append(str(year))
        common_passwords.append(f"pass{year}")
        common_passwords.append(f"admin{year}")
    
    # Simple numeric patterns (0000-9999)
    for i in range(10000):
        common_passwords.append(str(i))
    
    with open("sample_wordlist.txt", "w") as f:
        for pw in common_passwords:
            f.write(f"{pw}\n")
            # Simple variations
            f.write(f"{pw}!\n")
            f.write(f"{pw}@\n")
            f.write(f"{pw}#\n")
            f.write(f"{pw}$\n")
            f.write(f"{pw}123\n")
    
    print(f"\033[92m[+] Sample wordlist created: sample_wordlist.txt with {len(common_passwords)*6} passwords\033[0m")
    return "sample_wordlist.txt"

def check_pikepdf_version():
    """Check pikepdf version aur compatibility"""
    try:
        import pikepdf
        version = pikepdf.__version__
        print(f"\033[96m[*] pikepdf version: {version}")
        
        # Version check
        major_version = int(version.split('.')[0])
        if major_version >= 8:
            print("[*] Using new pikepdf API (v8+) - Compatible")
        else:
            print("[*] Using old pikepdf API (v7 or earlier)")
            
        return True
    except ImportError:
        print("\033[91m[!] pikepdf library not installed!")
        print("[*] Install with: pip install pikepdf")
        print("[*] Or: pip install 'pikepdf<8' for older API\033[0m")
        return False

def main():
    print_banner()
    
    # Check library version
    if not check_pikepdf_version():
        return
    
    print("\n\033[96m" + "1. Crack PDF password")
    print("2. Create sample wordlist")
    print("3. Test PDF opening (with known password)")
    print("4. Exit" + "\033[0m")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == "1":
        pdf_file = input("PDF file path: ").strip()
        if not pdf_file:
            print("\033[91m[!] Please provide a PDF file path\033[0m")
            return
            
        wordlist = input("Wordlist path (or Enter for sample): ").strip()
        if not wordlist:
            wordlist = create_sample_wordlist()
        
        max_attempts = input("Max attempts (default 10000, 0 for unlimited): ").strip()
        try:
            max_attempts = int(max_attempts) if max_attempts else 10000
            if max_attempts == 0:
                max_attempts = 10**9  # Practically unlimited
        except ValueError:
            max_attempts = 10000
        
        result = crack_pdf_password(pdf_file, wordlist, max_attempts)
        
        if result:
            print("\n\033[1;32m[+] Success! Use this password to open your PDF.\033[0m")
            # Save password to file
            with open("found_password.txt", "w") as f:
                f.write(f"PDF: {pdf_file}\nPassword: {result}\n")
            print(f"\033[92m[+] Password saved to: found_password.txt\033[0m")
        else:
            print("\n\033[93m[!] Password not found in wordlist")
            print("[*] Suggestions:")
            print("   - Use a larger wordlist (like rockyou.txt)")
            print("   - Try different password patterns")
            print("   - Check if PDF uses owner password instead of user password")
            print("   - Some PDFs use strong encryption that can't be brute-forced\033[0m")
    
    elif choice == "2":
        create_sample_wordlist()
    
    elif choice == "3":
        pdf_file = input("PDF file path: ").strip()
        password = input("Password (for testing): ").strip()
        try:
            with pikepdf.open(pdf_file, password=password) as pdf:
                print(f"\033[92m[+] Success! PDF opened with {len(pdf.pages)} pages\033[0m")
        except Exception as e:
            print(f"\033[91m[!] Failed to open: {e}\033[0m")
    
    elif choice == "4":
        print("\033[92m[+] Goodbye!\033[0m")
        sys.exit(0)
    
    else:
        print("\033[91m[!] Invalid choice\033[0m")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\033[93m[!] Process interrupted by user\033[0m")
    except Exception as e:
        print(f"\033[91m[!] Unexpected error: {e}\033[0m")
        import traceback
        traceback.print_exc()