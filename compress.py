import sys


def compress(file: str, out: str):
    from bitstring import ConstBitStream, BitArray, ReadError

    bit_input = ConstBitStream(filename=file)

    # guardando method calls em variáveis torna o código mais rápido
    read = bit_input.read

    dic = {}
    index = dic.get

    bit_str: BitArray = BitArray()
    bit_append = bit_str.append

    bit_output: BitArray = BitArray()
    out_append = bit_output.append

    pos: int = 1
    mode = False

    while 1:
        try:
            bit_append(read(1))
        except ReadError:
            break

        if bit_str.bin not in dic:
            dic[bit_str.bin] = pos
            pos += 1
            if len(bit_str) > 1:
                out_append(
                    '0b' + bin(index(bit_str.bin[:-1]))[2:].zfill((len(dic) - 1).bit_length()) + bit_str.bin[-1:])
            else:
                out_append('0b' + ''.zfill((len(dic) - 1).bit_length()) + bit_str.bin)
            bit_str.clear()

    if len(bit_str.bin) == 1:
        dic[bit_str.bin] = pos
        out_append('0b' + ''.zfill((len(dic) - 1).bit_length()) + bit_str.bin)
    elif len(bit_str.bin) > 1:
        dic[bit_str.bin] = pos
        out_append('0b' + bin(index(bit_str.bin[:-1]))[2:].zfill((len(dic) - 1).bit_length()) + bit_str.bin)
        mode = True

    if len(bit_output) % 8 != 0:
        filler_bits = 8 - (len(bit_output) % 8)
        if mode:
            bit_output.insert('0b' + bin(len(bit_str))[2:].zfill(8), 0)
            bit_output.insert('0b' + '1' + bin(filler_bits)[2:].zfill(7), 0)
        else:
            bit_output.insert('0b' + bin(filler_bits)[2:].zfill(8), 0)

    new_file = open(out, 'wb')
    bit_output.tofile(f=new_file)
    new_file.close()


if __name__ == '__main__':
    in_name = sys.argv[1]
    out_name = sys.argv[2]

    compress(in_name, out_name)
