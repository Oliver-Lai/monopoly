import random as rd
class player:
    def __init__(self,money,name):
        self.__money = money
        self.__state = 0
        self.__prison = 0
        self.__bankrupt = -1
        self.__turn = 0
        self.__name = name

    def check_is_prison(self):
        if(self.get_prison()>0):
            self.__set_prison(self.get_prison()-1)
            return True
        else:
            return False

    def go_to_prison(self,day):
        self.__set_prison(day)

    def roll_dice(self,map_size):
        a = (self.get_state() + rd.randint(1,6))%map_size
        self.__set_state(a)
        return a
    
    def buy(self,cost):
        if(cost<=self.get_money()):
            self.__set_money(self.get_money()-cost)
            return True
        else:
            return False
    
    def pay_bill(self,cost,state):
        if(cost<=self.get_money()):
            self.__set_money(self.get_money()-cost)
            return True
        else:
            self.__set_bankrupt(state)
            return False

    def earn(self,money):
        self.__set_money(self.get_money()+money)

    def turn_up(self):
        self.__turn += 1

    def get_money(self):
        return self.__money

    def get_state(self):
        return self.__state
    
    def get_prison(self):
        return self.__prison

    def get_bankrupt(self):
        return self.__bankrupt    
        
    def get_turn(self):
        return self.__turn

    def get_name(self):
        return self.__name

    def __set_money(self,money):
        self.__money = money
        
    def __set_state(self,state):
        self.__state = state
    
    def __set_prison(self,prison):
            self.__prison = prison
    
    def __set_bankrupt(self,bankrupt):
            self.__bankrupt = bankrupt #若有破產則回傳在哪格破產


# player1 = player(100)
# player1.roll_dice()
# player1.go_to_prison(5)
# while player1.check_is_prison()==True:
#     print("T")
# print("F")
# print(player1.buy(1000))
# print(player1.get_money())
# print(player1.pay_bill(1000))
# print(player1.get_bankrupt())
# print(player1.get_state())


class monopoly():
    def __init__(self,players_money,player_num,map,prison_location,prison_day,run):
        self.__total_players = []
        self.__init_player(players_money,player_num)
        self.__bankrupt_num = 0
        self.__map = map
        self.__map_size = len(map)
        self.__onwer_list = [None]*len(map)
        self.__prison_location = prison_location
        self.__prison_day = prison_day
        self.__trun = 0
        self.__run = run
    
    def play_game(self):
        rd.seed(self.__run)
        while True:
            self.__trun += 1
            for index in range(len(self.__total_players)):
                # 確認當前玩家是否破產
                if(self.__total_players[index].get_bankrupt()!=-1):
                    continue
                else:
                    self.__total_players[index].turn_up()
                # 確認當前玩家是否在監獄中
                if(self.__total_players[index].check_is_prison()==True):
                    continue
                
                # 當前玩家擲骰子
                state = self.__total_players[index].roll_dice(self.__map_size)
                # 若走到監獄則進監獄
                if(state==self.__prison_location):
                    self.__total_players[index].go_to_prison(self.__prison_day)
                    continue
                onwer = self.__onwer_list[state]
                money = self.__map[state]
                # 若走到沒有人的土地則嘗試買入
                if(onwer==None):
                    if(self.__total_players[index].buy(money)==True):
                        self.__onwer_list[state]=index
                # 若走到別人的土地則要付過路費給對方
                elif(onwer!=index):
                    if(self.__total_players[index].pay_bill(money*0.25 ,state) == True):
                        self.__total_players[onwer].earn(money*0.25)
                    else:
                        self.__bankrupt_num += 1
                        for i,j in enumerate(self.__onwer_list):
                            if(j==index): #若玩家破產則土地充公
                                self.__onwer_list[i] = None
                        self.__total_players[onwer].earn(self.__total_players[index].get_money())
                        if(self.__bankrupt_num==len(self.__total_players)-1):
                            return self.__total_players
    
    def __init_player(self,players_money,player_num):
        for i in range(player_num):
            self.__total_players.append(player(players_money,chr(65+i)))
    
    def get_turn(self):
        return self.__trun
    
    def get_win_land(self):
        num = 0
        for i in self.__onwer_list:
            if(i!=None):
                num += 1
        return num
    

class monopoly_no_prison():
    def __init__(self,players_money,player_num,map,run):
        self.__total_players = []
        self.__init_player(players_money,player_num)
        self.__bankrupt_num = 0
        self.__map = map
        self.__map_size = len(map)
        self.__onwer_list = [None]*len(map)
        self.__trun = 0
        self.__run = run
    
    def play_game(self):
        rd.seed(self.__run)
        while True:
            self.__trun += 1
            for index in range(len(self.__total_players)):
                # 確認當前玩家是否破產
                if(self.__total_players[index].get_bankrupt()!=-1):
                    continue
                else:
                    self.__total_players[index].turn_up()
                # 當前玩家擲骰子
                state = self.__total_players[index].roll_dice(self.__map_size)
                onwer = self.__onwer_list[state]
                money = self.__map[state]
                # 若走到沒有人的土地則嘗試買入
                if(onwer==None):
                    if(self.__total_players[index].buy(money)==True):
                        self.__onwer_list[state]=index
                # 若走到別人的土地則要付過路費給對方
                elif(onwer!=index):
                    if(self.__total_players[index].pay_bill(money*0.25 ,state) == True):
                        self.__total_players[onwer].earn(money*0.25)
                    else:
                        self.__bankrupt_num += 1
                        for i,j in enumerate(self.__onwer_list):
                            if(j==index): #若玩家破產則土地充公
                                self.__onwer_list[i] = None
                        self.__total_players[onwer].earn(self.__total_players[index].get_money())
                        if(self.__bankrupt_num==len(self.__total_players)-1):
                            return self.__total_players
    
    def __init_player(self,players_money,player_num):
        for i in range(player_num):
            self.__total_players.append(player(players_money,chr(65+i)))
    
    def get_turn(self):
        return self.__trun
    
    def get_win_land(self):
        num = 0
        for i in self.__onwer_list:
            if(i!=None):
                num += 1
        return num

class monopoly_with_bill():
    def __init__(self,players_money,player_num,map,prison_location,prison_day,run,bill):
        self.__total_players = []
        self.__init_player(players_money,player_num)
        self.__bankrupt_num = 0
        self.__map = map
        self.__map_size = len(map)
        self.__onwer_list = [None]*len(map)
        self.__prison_location = prison_location
        self.__prison_day = prison_day
        self.__trun = 0
        self.__run = run
        self.__bill = bill
    
    def play_game(self):
        rd.seed(self.__run)
        while True:
            self.__trun += 1
            for index in range(len(self.__total_players)):
                # 確認當前玩家是否破產
                if(self.__total_players[index].get_bankrupt()!=-1):
                    continue
                else:
                    self.__total_players[index].turn_up()
                # 確認當前玩家是否在監獄中
                if(self.__total_players[index].check_is_prison()==True):
                    continue
                
                # 當前玩家擲骰子
                state = self.__total_players[index].roll_dice(self.__map_size)
                # 若走到監獄則進監獄並支付罰金
                if(state==self.__prison_location):
                    self.__total_players[index].go_to_prison(self.__prison_day)
                    if(self.__total_players[index].pay_bill(self.__bill,state) == True):
                        continue
                    else:
                        self.__bankrupt_num += 1
                        for i,j in enumerate(self.__onwer_list):
                            if(j==index): #若玩家破產則土地充公
                                self.__onwer_list[i] = None
                        if(self.__bankrupt_num==len(self.__total_players)-1):
                            return self.__total_players
                        continue
                onwer = self.__onwer_list[state]
                money = self.__map[state]
                # 若走到沒有人的土地則嘗試買入
                if(onwer==None):
                    if(self.__total_players[index].buy(money)==True):
                        self.__onwer_list[state]=index
                # 若走到別人的土地則要付過路費給對方
                elif(onwer!=index):
                    if(self.__total_players[index].pay_bill(money*0.25 ,state) == True):
                        self.__total_players[onwer].earn(money*0.25)
                    else:
                        self.__bankrupt_num += 1
                        for i,j in enumerate(self.__onwer_list):
                            if(j==index): #若玩家破產則土地充公
                                self.__onwer_list[i] = None
                        self.__total_players[onwer].earn(self.__total_players[index].get_money())
                        if(self.__bankrupt_num==len(self.__total_players)-1):
                            return self.__total_players
    
    def __init_player(self,players_money,player_num):
        for i in range(player_num):
            self.__total_players.append(player(players_money,chr(65+i)))
    
    def get_turn(self):
        return self.__trun
    
    def get_win_land(self):
        num = 0
        for i in self.__onwer_list:
            if(i!=None):
                num += 1
        return num

class monopoly_with_early_out_prison():
    def __init__(self, players_money, player_num, game_map, prison_location, prison_day, run):
        self.__total_players = []
        self.__init_player(players_money, player_num)
        self.__bankrupt_num = 0
        self.__map = game_map
        self.__map_size = len(game_map)
        self.__owner_list = [None] * len(game_map)
        self.__prison_location = prison_location
        self.__prison_day = prison_day
        self.__turn = 0
        self.__run = run
    
    def play_game(self):
        rd.seed(self.__run)
        while True:
            self.__turn += 1
            for index in range(len(self.__total_players)):
                # 確認當前玩家是否破產
                if self.__total_players[index].get_bankrupt() != -1:
                    continue
                else:
                    self.__total_players[index].turn_up()
                
                
                # 在監獄內擲骰子決定是否提前出獄
                if self.__total_players[index].check_is_prison():
                    dice = rd.randint(1, 6)
                    if dice % 2 == 0:  # 擲出雙數提前離開
                        self.__total_players[index].go_to_prison(0)
                    else:
                        continue
                
                # 擲骰子，若在監獄則保持不動，否則移動
                
                state = self.__total_players[index].roll_dice(self.__map_size)
                
                # 若走到監獄則進監獄
                if state == self.__prison_location:
                    self.__total_players[index].go_to_prison(self.__prison_day)
                    continue
                
                owner = self.__owner_list[state]
                money = self.__map[state]
                
                # 若走到無主土地則嘗試購買
                if owner is None:
                    if self.__total_players[index].buy(money):
                        self.__owner_list[state] = index
                # 若走到別人土地則付過路費，即使在監獄內
                elif owner != index:
                    if self.__total_players[index].pay_bill(money * 0.25, state):
                        self.__total_players[owner].earn(money * 0.25)
                    else:
                        self.__bankrupt_num += 1
                        for i, j in enumerate(self.__owner_list):
                            if j == index:  # 玩家破產則土地充公
                                self.__owner_list[i] = None
                        self.__total_players[owner].earn(self.__total_players[index].get_money())
                        if self.__bankrupt_num == len(self.__total_players) - 1:
                            return self.__total_players
    
    def __init_player(self, players_money, player_num):
        for i in range(player_num):
            self.__total_players.append(player(players_money,chr(65+i)))
    
    def get_turn(self):
        return self.__turn
    
    def get_win_land(self):
        num = 0
        for i in self.__onwer_list:
            if(i!=None):
                num += 1
        return num
    

class monopoly_with_fair_prison():
    def __init__(self, players_money, player_num, game_map, prison_location, prison_day, run, prison_fine):
        self.__total_players = []
        self.__init_player(players_money, player_num)
        self.__bankrupt_num = 0
        self.__map = game_map
        self.__map_size = len(game_map)
        self.__owner_list = [None] * len(game_map)
        self.__prison_location = prison_location
        self.__prison_day = prison_day
        self.__turn = 0
        self.__run = run
        self.__prison_fine = prison_fine
    
    def play_game(self):
        rd.seed(self.__run)
        while True:
            self.__turn += 1
            for index in range(len(self.__total_players)):
                # 確認當前玩家是否破產
                if self.__total_players[index].get_bankrupt() != -1:
                    continue
                else:
                    self.__total_players[index].turn_up()
                
                # 在監獄內擲骰子決定是否提前出獄
                if self.__total_players[index].check_is_prison():
                    dice = rd.randint(1, 6)
                    if dice % 2 == 0:  # 擲出雙數提前離開
                        self.__total_players[index].go_to_prison(0)
                        in_prison = False
                    else:
                        continue
                
                # 擲骰子
                state = self.__total_players[index].roll_dice(self.__map_size)
                
                # 若走到監獄則進監獄，並支付罰金
                if state == self.__prison_location:
                    self.__total_players[index].go_to_prison(self.__prison_day)
                    if(self.__total_players[index].pay_bill(self.__prison_fine,state) == True):
                        continue
                    else:
                        self.__bankrupt_num += 1
                        for i,j in enumerate(self.__owner_list):
                            if(j==index): #若玩家破產則土地充公
                                self.__owner_list[i] = None
                        if(self.__bankrupt_num==len(self.__total_players)-1):
                            return self.__total_players
                        continue
                
                owner = self.__owner_list[state]
                money = self.__map[state]
                
                # 若走到無主土地則嘗試購買
                if owner is None:
                    if self.__total_players[index].buy(money):
                        self.__owner_list[state] = index
                # 若走到別人土地則付過路費
                elif owner != index:
                    if self.__total_players[index].pay_bill(money * 0.25, state):
                        self.__total_players[owner].earn(money * 0.25)
                    else:
                        self.__bankrupt_num += 1
                        for i, j in enumerate(self.__owner_list):
                            if j == index:  # 玩家破產則土地充公
                                self.__owner_list[i] = None
                        self.__total_players[owner].earn(self.__total_players[index].get_money())
                        if self.__bankrupt_num == len(self.__total_players) - 1:
                            return self.__total_players
    
    def __init_player(self, players_money, player_num):
        for i in range(player_num):
            self.__total_players.append(player(players_money,chr(65+i)))
    
    def get_turn(self):
        return self.__turn
    
    def get_win_land(self):
        num = 0
        for i in self.__owner_list:
            if(i!=None):
                num += 1
        return num
