#!/usr/bin/env python3

from argparse import ArgumentParser, RawDescriptionHelpFormatter
from emojipedia import Emojipedia
import secrets
import os.path
import ast

# TODO decorator that takes two messages and prints them before, after with time taken and ram usage!
    
def get_all_emojis() -> set:
    """Uses Emojipedia module to get all existing emojis as a set.
    This takes a while. And uses a lot of memory. Should be rewritten.
    """
    return set([x.character for x in Emojipedia.all() if len(str(x.character)) == 1])


def get_random_emoji_list(emoji_list: set) -> list:
    """Generates and returns a list of random emojis from a list of all available emojis.
    Uses secure random generator https://docs.python.org/3.6/library/secrets.html
    """
    return [emoji_list.pop() for x in range(secrets.randbelow(4) + 3)]


def generate_key(filename):
    """Generates a key in form of a dictionary byte:emoji_list.
    Stores key as key.emojipher. Overwrites existing key if exists!
    
    1. Generate a list of all emojis.
    2. Generate a dictionary of bytes 0 - 256 and their list of emoji.
    3. Store key as key.emojipher.
    """
    
    print("👁👁 Generating key, I am not looking...")
    
    emojis = get_all_emojis()
    
    key = {x : get_random_emoji_list(emojis) for x in range(0, 256)}

    with open(filename + ".emojipher", "w") as f:
        # Write as string, can evaluate string to dict when reading key.
        f.write(str(key))
    
    print("🧑‍💻🤐 Key has been generated! Keep it safe.")
 
    
def encrypt_data(filename: str, key: str):
    """Encrypts given file with given key. If such file exists, it is deleted!
    
    1. Load key.
    2. Iterate file bytes.
    2.1. Convert byte to int and find matching key in dict.
    2.2. Pick one random emoji from according list,
    2.3. Append to file. 
    """
    
    print("🧙🏼🔥 Encrypting your data...")
    
    with open(key, "r") as fr:
        key = ast.literal_eval(fr.read())
        
    output_filename = filename + ".encrypted"
    
    # Remove existing file if needed.
    if os.path.exists(output_filename):
       os.remove(output_filename)
    

    with open(filename, "rb") as fr:
        byte = fr.read(1)
        while byte != b"":
            # Convert byte to int to match in key dictionary.
            b = int.from_bytes(byte, "little")
            byte = fr.read(1)
          
            with open(output_filename, "a") as fw:
                # Find matching random emoji and write to file.
                fw.write(secrets.choice(key[b]))
    
    print("🕵 🕵️‍♂️ Your data has been encrypted and is safe from bioluminescent agents.")
    
    
def decrypt_data(filename: str, key: str):
    """Given a filename and a key, decrypts data into original file."""
    
    print("👀👽 Decrypting data, make sure you are alone!")
    
    with open(key, "r") as fr:
        key = ast.literal_eval(fr.read())
        
    # Invert key, aka make each emoji in list of each key into a new key.
    # So one key with list of 5 emojis becomes 5 keys with same value of byte.
    inverted_key = {}
    for k, v in key.items():
        for e in v:
            inverted_key[e] = k.to_bytes(1, "little")

    output_filename = filename.replace(".emojipher", "")
    
    if os.path.exists(output_filename):
        os.remove(output_filename)

    with open(filename, "r", encoding="utf-8") as fr:
        while True:
            c = fr.read(1)
            if not c:
              break
              
            with open(output_filename, "ab") as fw:
                fw.write(inverted_key[c])
 
    print("👨🏻‍💻🖨 Your data has been decrypted. Have fun!")

 
if __name__ == "__main__":
    description = """
    👽 EMOJIPHER 👽
    
    Your favorite encryption tool!
    
    Are you bored of cryptographically safe means of encryption like AES256?
    You hate asymmetric encryption?
    You are a modern human that loves big hard drives and emojis?
    You want to waste as much bandwith as you can?
    You want to choke NSA and TENCENT servers with emoji?

    If you answered any of those questions with YES, this script is for you.
    
    Encrypt your data by turning each byte of source file into emoji! Yes, thats right.
    Each byte becomes 4 bytes! And you get multiple emoji possibilities per byte!
    Frequency analysis? More like waste of electricity.
    
    Okay, I want this, but how do I start?
    
    1. Generate your personal key by issuing. It will append .emojipher to the end of your given name.
        $ ./emojipher.py -g my_key
        
    2. Encrypt some data!
        $ ./emojipher.py -e my_secrets.txt -k my_key.emojipher
        
    3. ... Do whatever you want, store it, send it, share it 🤡
    
    4. Decrypt your precious data.
        $ ./emojipher.py -d my_secrets.txt.encrypted -k my_key.emojipher
        
    5. Enjoy your decrypted data, but make sure you are alone.
    
    Uses https://github.com/bcongdon/python-emojipedia for emoji generation 😍
    
    Made with 🤡 by the 🤤 in www.exception.lt
    """
    
    parser = ArgumentParser(description=description, formatter_class=RawDescriptionHelpFormatter)
    generate = parser.add_argument_group("key generation")
    generate.add_argument("-g", "--generate", type=str, help="key name")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-e", "--encrypt", type=str, help="file(s) to encrypt")
    group.add_argument("-d", "--decrypt", type=str, help="file(s) to decrypt")
    parser.add_argument("-k", "--key", type=str, help="path to key")
    args = parser.parse_args()
    
    if args.generate:
        generate_key(args.generate)
        
    elif args.encrypt:
        encrypt_data(args.encrypt, args.key)
        
    elif args.decrypt:
        decrypt_data(args.decrypt, args.key)

