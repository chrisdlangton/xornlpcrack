import src.xornlpcrack as xornlpcrack, time, logging

def test_xor_decrypt():
    # Sample plaintext and keys for testing
    plaintext = "Sample text"
    keys = ["42", "key", "#ctf"]

    for key in keys:
        # Encrypt the plaintext with the given key
        encrypted = xornlpcrack.xor(plaintext, key)
        # Attempt to decrypt using the function
        start_time = time.time()
        for decrypted, used_key in xornlpcrack.xor_decrypt_guess_key(encrypted, len(key)):
            # Check if decryption is successful and matches the original plaintext
            if decrypted == plaintext:
                print(f"key '{used_key}' for '{decrypted}' took {round(time.time() - start_time, 3)} sec")
                break

if __name__ == "__main__":
    logging.basicConfig(format= "%(asctime)s - %(name)s - [%(levelname)s] %(message)s", level=logging.DEBUG)
    test_xor_decrypt()
