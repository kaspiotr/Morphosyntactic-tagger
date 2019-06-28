import subprocess


def main():
    text = "Wyjątkiem będą maszyny z tymi tłumikami zarejestrowane w Europie do maja 2000 r. Pod naciskiem USA przesunięto o rok termin homologacji i początku zakazu lądowań. Amerykanie oceniają liczbę swoich samolotów objętych nowymi terminami na 1000, UE na 1000-1500. Ministrowie uzgodnili też nowe reguły walki z opóźnieniami w płatnościach handlowych."
    output_xml_file_path = "/home/kaspiotr/Dev/MorphosyntacticTagger/resources/maca_output/out.txt"
    cmd1 = " | maca-analyse -qs morfeusz2-nkjp -o ccl > " + output_xml_file_path
    cmd2 = " | maca-analyse -qs morfeusz2-nkjp -o plain"
    subprocess.call("echo " + text + cmd1, shell=True)
    subprocess.call("echo " + text + cmd2, shell=True)


if __name__ == '__main__':
    main()

