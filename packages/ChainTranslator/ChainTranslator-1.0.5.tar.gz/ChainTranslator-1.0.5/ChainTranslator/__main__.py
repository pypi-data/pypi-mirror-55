from googletrans import Translator
import argparse

def main():
    parser = argparse.ArgumentParser(description="Mess up some words.", prog="chaintranslator")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-t", help="text to run through the translator", metavar="TEXT", type=str)
    group.add_argument("-f", help="file to open and run through translator", metavar="FILE", type=str)
    parser.add_argument("-p", metavar="CODE", type=str, nargs='+', required=True,
        help="list of languages to translate the text through using iso639-1 codes.\
            Will automatically translate back to original language that it detects.")
    parser.add_argument("-s", help="silent mode", action="store_true", default=False)
    parser.add_argument("-o", help="File to write output to.", metavar="FILE", default=None, type=str)

    args = parser.parse_args()

    toTranslate = ""
    if args.t != None:
        toTranslate = args.t
    else:
        f = open(args.f)
        toTranslate = f.read()

    trans = Translator()

    originLang = trans.detect(toTranslate).lang

    for lang in args.p:
        try:
            toTranslate = trans.translate(toTranslate, dest=lang).text
        except ValueError:
            raise Exception("Invalid destination language: {}".format(lang))
        if not args.s:
            print("{}: {}".format(lang, toTranslate))

    translated = trans.translate(toTranslate, dest=originLang).text

    if not args.s:
        print("\n" + translated)

    if args.o != None:
        with open(args.o, "w+", encoding="utf-8") as f:
            f.write(translated)

if __name__ == "__main__":
    main()