import pickle
import sys
import pprint

robots = int(sys.argv[1])
merged = {}
for i in range(1, robots+1):
    try:
        with open(f"/home/adhi/catkin_ws/src/multiple_turtlebot3/robot{i}", "rb") as f:
            database = pickle.load(f)
            for j in database:
                if j not in merged:
                    merged[j] = database[j]
                else:
                    merged[j].extend(database[j])
                merged[j].sort()
    except: pass

def dist(a, b):
    return ((a[0]-b[0])**2) + ((a[1]-b[1])**2)

new_merged = {}
#pprint.pp(merged)
for label in merged:
    #print(label, merged[label])
    i = 0
    while i < len(merged[label])-1:
        coords = merged[label]
        j = 1
        while i+j < len(merged[label]) and dist(coords[i], coords[i+j]) <= 16:
            if label not in new_merged:
                new_merged[label] = []
            #new_merged[label].append([(coords[i][0] + coords[i+1][0]) / 2, (coords[i][1] + coords[i+1][1]) / 2])
            j += 1
        #print(coords)
        #print(i,j)
        new_merged[label].append([sum(coords[i:i+j][0])/j, sum(coords[i:i+j][1])/j])
      ##  else:
       #     if label not in new_merged:
       #         new_merged[label] = []
       #     new_merged[label].append([coords[i][0], coords[i][1]])
        i += j

pprint.pp(new_merged)
with open("/home/adhi/catkin_ws/src/items.txt", "w") as f:
    item_num = 1
    for label in new_merged:
        for coord in new_merged[label]:
            f.write(f"{label} {item_num}\n({coord[0]},{coord[1]})\n")
            item_num += 1
