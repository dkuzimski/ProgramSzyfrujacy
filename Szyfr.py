import heapq
import os

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(frequencies):
    heap = [Node(char, freq) for char, freq in frequencies.items()]        #Kolejka priorytetowa
    heapq.heapify(heap)
    
    while len(heap) > 1:
        left = heapq.heappop(heap) 
        right = heapq.heappop(heap)  
        merged = Node(None, left.freq + right.freq) 
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
    return heap[0]

def build_huffman_codes(root):
    huffman_codes = {}

    def generate_codes(node, current_code):
        if not node:
            return
        if node.char is not None:  
            huffman_codes[node.char] = current_code
            return
        generate_codes(node.left, current_code + "0")
        generate_codes(node.right, current_code + "1")

    generate_codes(root, "")
    return huffman_codes

def huffman_encode(input_file, output_file, freq_output_file):
    
    with open(input_file, 'r', encoding='utf-8') as f:   #Wczytywanie pliku
        text = f.read()

    frequencies = {}        #Zliczanie znaków
    for char in text:
        frequencies[char] = frequencies.get(char, 0) + 1

    with open(freq_output_file, 'w', encoding='utf-8') as f:        #Zapis znaków do plików
        for char, freq in frequencies.items():
            f.write(f"{repr(char)}: {freq}\n")

    root = build_huffman_tree(frequencies)      #Tworzenie drzewa
    huffman_codes = build_huffman_codes(root)

    encoded_text = ''.join(huffman_codes[char] for char in text)

    padding = 8 - len(encoded_text) % 8
    encoded_text += '0' * padding       #Dopełnienia do zakodowanego tekstu Huffmana
    padding_info = f"{padding:08b}"

    with open(output_file, 'wb') as f:
        f.write(padding_info.encode('utf-8')) 
        f.write(b'\n')
        f.write(str(huffman_codes).encode('utf-8'))
        f.write(b'\n')
        binary_data = bytearray()
        for i in range(0, len(encoded_text), 8):
            byte = encoded_text[i:i+8]
            binary_data.append(int(byte, 2))
        f.write(binary_data)

    print("Zapisano zakodowany plik:", output_file)
    print("Zapisano częstotliwości występowania znaków w pliku:", freq_output_file)

if __name__ == "__main__":  #Operacje na plikach
    input_file = 'plik.txt'
    output_file = 'zaszyfrowanyplik.txt'
    freq_output_file = 'zliczone.txt'  

    if not os.path.exists(input_file):
        print(f"Plik '{input_file}' nie istnieje. Upewnij się, że jest w tym samym katalogu co skrypt.")
    else:
        huffman_encode(input_file, output_file, freq_output_file)
