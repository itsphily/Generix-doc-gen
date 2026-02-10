"""Simple script to print a cat in the terminal."""

def print_cat():
    """Prints an ASCII art cat to the console."""
    cat = r"""
    /\_/\
   ( o.o )
    > ^ <
   /|   |\
  (_|   |_)
    """
    print(cat)

def print_anthropic_cat():
    """Prints a cat thinking about Anthropic."""
    print("  What's Claude thinking about?")
    print(r"""
       /\_/\
      ( ^.^ )
       > o <   "I love helping humans!"
      /|   |\
     (_|   |_)
    """)

if __name__ == "__main__":
    print_cat()
    print("\n" + "="*30 + "\n")
    print_anthropic_cat()
