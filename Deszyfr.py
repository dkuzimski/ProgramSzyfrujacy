import ast

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def rebuild_huffman_tree(huffman_codes):        #Odbudowanie drzewa Huffmana na bazie kodów Hufmana
    root = Node(None, 0)
    for char, code in huffman_codes.items():
        current = root
        for bit in code:
            if bit == '0':
                if not current.left:
                    current.left = Node(None, 0)
                current = current.left
            else:
                if not current.right:
                    current.right = Node(None, 0)
                current = current.right
        current.char = char
    return root

def huffman_decode(input_file, output_file):
    with open(input_file, 'rb') as f:
        padding_info = f.readline().decode('utf-8').strip()
        padding = int(padding_info, 2)

        huffman_header = f.readline().decode('utf-8').strip()
        frequencies = ast.literal_eval(huffman_header)  #Rekonstrukcja słownika            

        huffman_codes = {}
        for char, code in frequencies.items():
            huffman_codes[char] = code

        binary_data = f.read()
        encoded_text = ''.join(f"{byte:08b}" for byte in binary_data)

        if padding > 0:
            encoded_text = encoded_text[:-padding]



    root = rebuild_huffman_tree(huffman_codes)

    decoded_text = []       #Dekodowanie kodu
    current = root
    for bit in encoded_text:
        if bit == '0':
            current = current.left
        else:
            current = current.right

        if current.char is not None:  
            decoded_text.append(current.char)
            current = root

    with open(output_file, 'w', encoding='utf-8') as f:     #Zapis wyniku do pliku
        f.write(''.join(decoded_text))

    print("Zapisano odszyfrowany plik:", output_file)

if __name__ == "__main__":
    input_file = 'zaszyfrowanyplik.txt'     #Plik zaszyfrowany
    output_file = 'odszyfrowanyplik.txt'    #Plik odszyfrowany

    huffman_decode(input_file, output_file)
