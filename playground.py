import random as rd
class player:
    def __init__(self,money):
        self.__money = money
        self.__state = 0
        self.__prison = 0
        self.__bankrupt = -1
        self.__turn = 0

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
            self.__total_players.append(player(players_money))

# play_map = [100,200,300,400,500,600,700]
# a = monopoly(1000,3,play_map,1,3)
# temp,owner = a.play_game()
# for index,i in enumerate(temp):
#     if(i.get_bankrupt()==-1):
#         win = index
#     print(index,' ',i.get_bankrupt(),i.get_turn())
# print(owner)
# print("winner is ",win)