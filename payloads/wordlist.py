from typing import Iterator

def load_payloads(filepath: str) -> Iterator[str]:
    with open(filepath, 'r') as f:
        for line in f:
            
            cleaned = line.strip()
            if cleaned and not cleaned.startswith('#'):
                yield cleaned

if __name__ == "__main__":
    for payload in load_payloads('wordlists/password.txt'):
        print(payload)