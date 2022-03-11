from time import sleep
registered = False
#init du bestscore
score = 0
while not registered:
    name = input("Entrez votre nom\n")
    if len(name) < 25:
        registered = True
with open("bestScore.txt") as f:
    lines = f.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].split(" ")

players = []
scores = []
for i in lines:
    players.append(i[0]) 
    scores.append(i[1])
    
if name not in players:
    with open('bestScore.txt', 'a') as f:
        f.write(name + " 0")
    players.append(name)
    scores.append(0)
    bestScore = 0
else:
    for i in range(len(players)):
        if players[i] == name:
            bestScore = score[i]
print("\nNow you can play",name,"!") 
print("Your best score is",bestScore,".\n")
print("The game launches ...")
sleep(3)  
 