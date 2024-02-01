
class Crc32:
    DefaultPolynomial = 0xEDB88320
    DefaultSeed = 0xFFFFFFFF

    def __init__(self, polynomial=DefaultPolynomial, seed=DefaultSeed):
        self.table = self.initialize_table(polynomial)
        self.seed = self.hash_value = seed

    def initialize_table(self, polynomial):
        if polynomial == self.DefaultPolynomial and hasattr(self, '_default_table'):
            return self._default_table

        create_table = [0] * 256
        for i in range(256):
            entry = i
            for j in range(8):
                if entry & 1:
                    entry = (entry >> 1) ^ polynomial
                else:
                    entry = entry >> 1
            create_table[i] = entry

        if polynomial == self.DefaultPolynomial:
            self._default_table = create_table

        return create_table

    def calculate_hash(self, table, seed, buffer, start, size):
        crc = seed
        for i in range(start, size - start):
            crc = (crc >> 8) ^ table[buffer[i] ^ (crc & 0xff)]
        return crc

    # def initialize(self):
    #     self.hash_value = self.seed

    # def hash_core(self, array, start, size):
    #     self.hash_value = self.calculate_hash(self.table, self.hash_value, array, start, size)

    # def hash_final(self):
    #     hash_buffer = self.uint32_to_big_endian_bytes(~self.hash_value)
    #     return hash_buffer

    def calculate(self, buffer):
        return (~self.calculate_hash(self.initialize_table(self.DefaultPolynomial),
                                     self.DefaultSeed,
                                     buffer,
                                     0,
                                     len(buffer))) & 0xFFFFFFFF

    # @staticmethod
    # def uint32_to_big_endian_bytes(uint32):
    #     result = uint32.to_bytes(4, byteorder='big')
    #     return result
