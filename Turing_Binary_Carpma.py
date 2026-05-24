class TuringMachine:
    def __init__(self, tape):
        self.tape = list(tape) + ['_'] * 100
        self.head = 0
        self.state = "q_start"
        self.step_count = 0

    def display_tape(self):
        tape_str = ''.join(self.tape).rstrip('_')

        head_indicator = ' ' * self.head + '^'

        print(f"Bant : {tape_str}")
        print(f"        {head_indicator}")

    def move_right(self):
        self.head += 1

    def move_left(self):
        if self.head > 0:
            self.head -= 1

    def read(self):
        return self.tape[self.head]

    def write(self, symbol):
        self.tape[self.head] = symbol

    def log_step(self, read_symbol, write_symbol, move):
        print("\n--------------------------------")
        print(f"Adım: {self.step_count}")
        print(f"Durum: {self.state}")
        print(f"Okunan Sembol: {read_symbol}")
        print(f"Yazılan Sembol: {write_symbol}")
        print(f"Kafa Hareketi: {move}")
        self.display_tape()

    def run(self):
        print("\n===== TURING MAKINESI BASLADI =====\n")

        # 1. '*' karakterini bul
        self.state = "q_find_delimiter"

        while self.read() != '*':
            read_symbol = self.read()
            self.log_step(read_symbol, read_symbol, "R")
            self.move_right()
            self.step_count += 1

        # '*' bulundu
        self.log_step('*', '*', "R")
        delimiter_index = self.head

        # 2. Operandları ayır
        multiplicand = ''.join(self.tape[:delimiter_index])

        self.move_right()

        multiplier_start = self.head

        while self.read() != '=':
            self.move_right()

        multiplier_end = self.head

        multiplier = ''.join(
            self.tape[multiplier_start:multiplier_end]
        )

        self.state = "q_operands_parsed"

        print("\n===== OPERANDLAR AYRISTIRILDI =====")
        print(f"Birinci Sayi (Multiplicand): {multiplicand}")
        print(f"Ikinci Sayi (Multiplier): {multiplier}")

        # 3. Shift & Add işlemi
        self.state = "q_multiply"

        result = 0

        reversed_multiplier = multiplier[::-1]

        for shift, bit in enumerate(reversed_multiplier):

            print("\n================================")
            print(f"Multiplier biti inceleniyor: {bit}")
            print(f"Kaydirma miktari: {shift}")

            if bit == '1':
                shifted_value = int(multiplicand, 2) << shift

                print(f"{multiplicand} sola kaydirildi -> "
                      f"{bin(shifted_value)[2:]}")

                result += shifted_value

                print(f"Guncel sonuc -> {bin(result)[2:]}")
            else:
                print("Bit 0 oldugu icin toplama yapilmadi.")

        # 4. Sonucu banda yaz
        result_binary = bin(result)[2:]

        self.state = "q_write_result"

        equal_index = self.tape.index('=')

        self.head = equal_index + 1

        for bit in result_binary:
            read_symbol = self.read()

            self.write(bit)

            self.log_step(read_symbol, bit, "R")

            self.move_right()

            self.step_count += 1

        self.state = "q_accept"

        print("\n===== MAKINE DURDU =====")
        print("Durum: KABUL")

        final_tape = ''.join(self.tape).rstrip('_')

        print("\nFinal Bant:")
        print(final_tape)

        print("\n===== SONUC =====")
        print(f"Binary Sonuc : {result_binary}")
        print(f"Decimal Sonuc: {result}")


def validate_binary(value):
    return all(ch in ['0', '1'] for ch in value)


def main():

    print("===== BINARY CARPMA TURING MAKINESI =====\n")

    num1 = input("Birinci binary sayiyi girin: ")
    num2 = input("Ikinci binary sayiyi girin : ")

    # Binary doğrulama
    if not validate_binary(num1):
        print("HATA: Birinci sayi binary degil!")
        return

    if not validate_binary(num2):
        print("HATA: Ikinci sayi binary degil!")
        return

    # Bant oluştur
    tape = f"{num1}*{num2}="

    print("\nOlusturulan Bant:")
    print(tape)

    # Turing makinesi çalıştır
    tm = TuringMachine(tape)

    tm.run()


if __name__ == "__main__":
    main()