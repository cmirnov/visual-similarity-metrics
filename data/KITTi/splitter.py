import sys
import numpy as np


class Center:
    def __init__(self, matrix, idx):
        self.idx = idx
        self.x = matrix[0][3]
        self.y = matrix[1][3]
        self.z = matrix[2][3]
        self.phi = matrix[:, 2] / np.linalg.norm(matrix[:, 2])


class Image:
    def __init__(self, center, flow):
        self.center = center
        self.similar = []
        maxDist = 10.0 # meters
        maxAngle = .5 # radians
        for c in flow:
            [dist, angle] = calc_diff(center, c)
            if dist < (maxDist**2) and abs(angle) < maxAngle and abs(center.idx - c.idx) > 100:
                self.similar.append(c)


def calc_diff(c1, c2):
    dist = (c1.x - c2.x) ** 2 + (c1.y - c2.y) ** 2 + (c1.z - c2.z) ** 2
    angle = np.arccos(np.clip(np.dot(c1.phi, c2.phi), -1.0, 1.0))
    return [dist, angle]

def reader(file_path):
    ans = []
    idx = 0
    with open(file_path) as input_file:
        for line in input_file:
            line = line.strip()
            temp = []
            for number in line.split():
                temp.append(float(number))
            matrix = np.array(temp).reshape((3,4))
            ans.append(Center(matrix, idx))
            idx += 1
    return ans

if __name__ == "__main__":
    file_path = sys.argv[1]
    for file_num in range(10):
        print(file_num)
        temp = reader(file_path + str(file_num) + ".txt")
        neighbors = []
        for c in temp:
            neighbors.append(Image(c, temp))
        f = open("KITTi/dataset/similar/0" + str(file_num) + ".txt", "w+")
        # sys.stdout = f
        for c in neighbors:
            if len(c.similar) > 0:
                f.write(str(c.center.idx))
                for i in range(len(c.similar)):
                    f.write(str(c.similar[i].idx))
                f.write("next")
        f.close()
#    print(neighbors[0].center.idx)
#    print(neighbors[0].similar[1].idx)
