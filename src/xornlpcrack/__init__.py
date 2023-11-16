import string, itertools, time, logging

from nltk.corpus import words
from nltk.tokenize import word_tokenize

logger = logging.getLogger(__name__)

def is_mostly_english(text, threshold: float = 0.5):
    # Tokenize the text into individual words
    words_in_text = word_tokenize(text)

    # Count of English and non-English words
    english_word_count = 0
    total_word_count = 0

    # Set of English words for faster lookup
    english_words = set(words.words())

    # Iterate over each word in the text
    for word in words_in_text:
        # Check if the word is alphanumeric to filter out punctuation and special characters
        if word.isalpha() and word.lower() in english_words:
            english_word_count += 1

    # Calculate the percentage of English words
    if not total_word_count:
        return False
    english_percentage = english_word_count / total_word_count

    # Return True if more than 50% of the words are English, otherwise False
    return english_percentage > threshold

def _ascii_permutations(key_length: int):
    # Generate all possible keys of a given length using printable ASCII characters
    return itertools.product(string.printable, repeat=key_length)

def is_meaningful(text: str) -> bool:
    # Check for excessive non-standard characters
    if not all(char in string.printable for char in text):
        logger.debug(f'not printable {text}')
        return False

    # Check all are alphabetic or all characters are a number, or both
    if text.isalnum():
        logger.debug(f'isalnum {text}')
        return True

    # Optional: Third party NLP tool
    if is_mostly_english(text):
        logger.debug(f'NLP {text}')
        return True

    logger.debug(f'is_meaningful catchall {text}')
    return False

# Python generator to decrypt and derive the original text from the ciphertext
# It includes a step to guess the key length, defaulting to 6
def xor_decrypt_guess_key(ciphertext, key_length_guess=6) -> list(tuple[str, str]):
    # Generate all possible keys of a given length using printable ASCII characters
    possible_keys = _ascii_permutations(key_length_guess)
    start_time = time.time()
    logger.info(f"derived key length in {time.time() - start_time} seconds.")
    for key in possible_keys:
        key_str = ''.join(key)
        decrypted_text = xor(ciphertext, key_str)
        # Heuristic to check if the decrypted text is readable (contains only printable characters)
        logger.debug(f'Heuristic {decrypted_text}')
        if is_meaningful(decrypted_text):
            yield (decrypted_text, key_str)

# MB XOR encoding
def xor(data, key):
    key_length = len(key)
    return ''.join(chr(ord(data[i]) ^ ord(key[i % key_length])) for i in range(len(data)))

def derive_key(ciphertext, with_length: int = None, max_length: int = 6, min_length: int = 1):
    start_time = time.time()
    if with_length:
        logger.info(f"Using length {with_length}")
        for guess, used_key in xor_decrypt_guess_key(ciphertext, with_length):
            logger.info(f"completed in {time.time() - start_time} seconds.")
            if guess:
                print(f"decrypted '{guess} 'with key '{used_key}'")

    else:
        for try_length in range(min_length, max_length+1):
            logger.info(f"Trying length {try_length}")
            for guess, used_key in xor_decrypt_guess_key(ciphertext, try_length):
                logger.info(f"completed in {time.time() - start_time} seconds.")
                if guess:
                    print(f"decrypted '{guess}' with key '{used_key}'")
