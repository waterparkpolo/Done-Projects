import re
import sys
def main():
    print(parse(input("HTML: ")))

def parse(s):

    if truth:=re.search(r"^.+(https?)(://w?w?w?.?)(youtube.com/embed/)(\w+)\".+$", s):
        fix=truth.group(1)
        if "s" in fix:
            ""
        else:
            fix=fix.replace("http", "https")
        link=fix + truth.group(2) + truth.group(3) + truth.group(4)
        link=link.replace("www.", "").replace("be.com/embed", ".be")
        return link
    else:
        ""
if __name__=="__main__":
    main()
