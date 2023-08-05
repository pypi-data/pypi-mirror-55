'''这是“nester.py”模块，提供了名为print_lol()的函数。
   这个函数的作用是打印列表，可以将多层嵌套的列表拆分输出'''
def print_lol(the_list):
    """这个函数取一个位置参数"the_list",这可以是任何Python列表，
    所指定的列表中的每个数据项会递归的输出到屏幕上，各数据项各占一行"""
    for each_item in the_list:
        if isinstance(each_item, list) == True:
            print_lol(each_item)
        else:
            print(each_item)



movies = [
        'The Holy Grail', 1975, 'Terry Jones & Terry Gilliam', 91, 
        ['Graham Chapman',
            ['Michael Palin', 'John Cleese','Terry Gilliam','Eric']]]
print_lol(movies)