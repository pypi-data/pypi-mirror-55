def start():
    print("import successful")

def run():

	import jieba

	txt = open("D:/demo/input.txt", "r").read()
	res = open("D:/demo/output.txt", "w")
	words = jieba.cut(txt)
	size = 4
	# print("size: ", size)
	i = 0
	for word in words:
		if i == size:
			res.write('\n')
			i = 0
		else:
			res.write(word)
			i += 1

	# txt.close()
	res.close()