# Rank	Steps Gained with Win	Steps Lost with Loss	Steps needed to Advance a Tier
# Bronze	2	0	4
# Silver	2	1	5
# Gold	    1	1	6
# Platinum	1	1	7
# Diamond	1	1	7

# never get pushed to a lower rank

WINRATE_INCREMENT = 0.01
MAX_GAMES = 10000
import random

ranks = [
    {"title": "Bronze", "PerWin": 2, "PerLoss": 0, "PerTier": 4},
    {"title": "Silver", "PerWin": 2, "PerLoss": 1, "PerTier": 5},
    {"title": "Gold", "PerWin": 1, "PerLoss": 1, "PerTier": 6},
    {"title": "Platinum", "PerWin": 1, "PerLoss": 1, "PerTier": 7},
    {"title": "Diamond", "PerWin": 1, "PerLoss": 1, "PerTier": 7},
    {"title": "Mythic", "PerWin": 1, "PerLoss": 1, "PerTier": 99999999999999999999999}
]



class Player:
    def __init__(self, winrate):
        self.winrate = winrate
        self.rank = 0
        self.tier = 4
        self.steps = 0
    def getRank(self):
        return ranks[self.rank]
    def simGame(self):
        # Returns true for win false for loss
        return random.random() <= self.winrate
    def simRanked(self):
        rank = self.getRank()
        win = self.simGame()
        if win:
            self.steps += rank["PerWin"]
        else:
            self.steps -= rank["PerLoss"]

        self.steps = max(0, self.steps) 
        if self.steps < 0:
            self.downgradeTier()
        if self.steps >= rank["PerTier"]:
            self.upgradeTier()
    def upgradeTier(self):
        self.tier -= 1
        if self.tier <= 0:
            self.upgradeRank()
        self.steps = 0
    def downgradeTier(self):
        self.tier = min(4, self.tier)
        self.steps = 0
    def upgradeRank(self):
        self.rank += 1
        self.steps = 0
        self.tier = 4
    def getFormattedRank(self):
        r = "{} {}.{}".format(self.getRank()["title"],self.tier,self.steps)
        while len(r) < 12:
            r += ' '
        return r

padding = ''.join([' ' for _ in range(12)])

print("WINRATE  50{0}100{0}500{0}1000{0}{1}".format(padding,MAX_GAMES))

for w in range(0,100, int(WINRATE_INCREMENT*100)):
    winrate = w/100.
    player = Player(winrate)
    s = '{}     '.format(winrate if len(str(winrate)) == 4 else "{} ".format(winrate))
    for i in range(1,MAX_GAMES):
        player.simRanked()
        if i / 50 == 1.0 or i / 100 == 1.0 or i / 500 == 1.0 or i / 1000 == 1.0 or i / MAX_GAMES == 1.0:
            s += '{}   '.format(player.getFormattedRank())
    s += '{}   '.format(player.getFormattedRank())
    print(s)
