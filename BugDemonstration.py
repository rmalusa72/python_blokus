from MCTSPlayers import *


p = monteCarloPlayer(1)
p.root = MCNode(Gamestate())
p.current = p.root

p.mcIteration()

print("P's wins:")
print(p.root.wins)

print("P's playouts:")
print(p.root.playouts)

print("P's children:")
for move, child in p.root.children.items():
    print("Child:")
    print(move)
    print(child)
    print("Wins:")
    print(child.wins)
    print("Playouts:")
    print(child.playouts)
