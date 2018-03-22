def quicktree(sentence):
    """Parse a sentence and return a visual representation"""
    from nltk import Tree
    from nltk.draw.util import CanvasFrame
    from nltk.draw import TreeWidget
    from stat_parser import Parser
    from IPython.display import display
    from IPython.display import Image
    parser = Parser()
    parsed = parser.parse(sentence)
    cf = CanvasFrame()
    tc = TreeWidget(cf.canvas(),parsed)
    cf.add_widget(tc,10,10) # (10,10) offsets
    cf.print_to_file('tree.ps')
    cf.destroy()
    # convert tree.ps tree.png
    # rm tree.ps
    return Image(filename='tree.png')
    # rm tree.png
  

quicktree("This is a parse tree.")