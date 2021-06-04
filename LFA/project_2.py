from automata import Automata


def main():
    try:
        regex = input("\nInput regex expression: ")
        automata = Automata()
        automata.createAutomata(regex)
        automata.print()
        automata.plot()
    except Exception as e:
        print("\n",repr(e),"\n")


if __name__ == '__main__':
    main()
