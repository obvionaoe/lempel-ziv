import sys


def decompress(file: str, out: str):
    from bitstring import ConstBitStream, BitArray
    from math import ceil, log2

    bit_input = ConstBitStream(filename=file).bin

    flag = bit_input[0]
    filler_size = int(bit_input[1:8], 2)

    if filler_size > 0:
        bit_input = bit_input[8:-filler_size]

    last_seq = ''

    if flag == '1':
        last_seq_size = int(bit_input[:8], 2)
        last_seq = bit_input[-last_seq_size:]
        bit_input = bit_input[8:-last_seq_size]

    bit_input = ConstBitStream(bin=bit_input)

    dic = ['']
    bit_str: str = ''
    bit_output: str = ''

    for bit in bit_input:
        bit_str += str(int(bit))
        if len(bit_str) == ceil(log2(len(dic))) + 1:
            if len(bit_str) > 1:
                reconstructed = dic[int(bit_str[:-1], 2)] + bit_str[-1:]
                dic.append(reconstructed)
                bit_output += reconstructed
            else:
                dic.append(bit_str)
                bit_output += bit_str
            bit_str = ''

    bit_output += last_seq

    new_file = open(out, 'wb')
    BitArray(bin=bit_output).tofile(f=new_file)
    new_file.close()


if __name__ == '__main__':
    in_name = sys.argv[1]
    out_name = sys.argv[2]

    decompress(in_name, out_name)
