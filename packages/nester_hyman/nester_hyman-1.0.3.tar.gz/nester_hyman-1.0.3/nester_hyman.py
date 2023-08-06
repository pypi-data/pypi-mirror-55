"""这是neser.py模块,提供了print_lol函数，循环打印列表及嵌套列表,level为在遇到
嵌套列表时每层缩进显示一个制表,indet 默认关闭缩进，sys.stdout 没有指定文件对象则依然写至屏幕"""
import sys
def print_lol(the_list, indent=False, level=0, fh=sys.stdout):
	for each_item in the_list:
		if isinstance(each_item, list):
			print_lol(each_item, indent, level+1, fh)
		else:
			if indent:
				for tab_stop in range(level):
					print("\t", end='', file=fh)
			print(each_item, file=fh)

			
