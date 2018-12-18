idx = 0
out = open("CityCentreTextFormat.out", "w+")
with open("CityCentreTextFormat.txt") as f:
	for line in f:
		arr = line.split(",")
		for i in range(len(arr)):
			if abs(idx - i) > 10 and arr[i] == "1":
				out.write(str(i) + "," + str(idx) + "\n")
		idx += 1
