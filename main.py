
from button import Button
from stats import Stats
import json
import pygame
import random
import sys
W = 800
H = 600



class Game:
    def __init__(self, app):
        self.stats = Stats(self)
        self.app = app
        self.button_font = pygame.font.SysFont("calibri", 23, bold=True)
        self.blackjack_font = pygame.font.SysFont("calibri", 40, bold=True)
        self.both_bj = False
        self.lost = False
        self.win = False
        self.same = False
        self.show_split = False
        self.split = False
        self.hand_finished = False
        self.show_text_bj = False
        self.stats_run = False
        self.start_num = -1
        self.splited_card_count = 0
        self.split_count = 0
        self.active = 0
        self.zup = 0
        self.dat = 0
        self.deck()
        self.lines = {}
        self.players_hand = []
        self.dealers_hand = []
        self.players_value = []
        self.dealers_value = []
        self.starter_deal_cards()
        
        
        

    def draw(self):
        self.bg_orig = pygame.image.load("bg/table.webp")
        self.bg = pygame.transform.scale(self.bg_orig, (800,600))
        self.bg_rect = self.bg.get_rect(topleft=(0,0))
        self.app.screen.blit(self.bg, self.bg_rect)
        
        self.load_images()
        self.buttons()
        
        
    def restart(self):   
        self.players_hand = []
        self.dealers_hand = []
        self.players_value = []
        self.dealers_value = [] 
        self.win = False
        self.lost = False
        self.same = False
        self.hand_finished = False
        self.split = False
        self.show_split = False
        self.active = 0
        self.hand_finished = False
        self.lines.clear()
        self.split_count = 0
        self.dat = 0
        self.start_num = -1
        self.show_text_bj = False
        
    
        
    def load_images(self):
        if self.split == False:
            
            self.text1 = self.blackjack_font.render("YOU WON!", True, "red")
            self.text1_rect = self.text1.get_rect(center=(400,530))

            self.text2 = self.blackjack_font.render("YOU LOST!", True, "red")
            self.text2_rect = self.text2.get_rect(center=(400,530))

            self.text3 = self.blackjack_font.render("DRAW!", True, "red")
            self.text3_rect = self.text3.get_rect(center=(400,530))
            x = 60
            y = 420

            for i in range(0, len(self.players_hand), 2):
                image_origo = pygame.image.load(f"img/{self.players_hand[i]}_of_{self.players_hand[i+1]}.png")
                image = pygame.transform.scale(image_origo,(85,140))
                image_rect = image.get_rect(topleft=(x,y))
                self.app.screen.blit(image, image_rect)
                x += 40
                y -= 40    
            j = 240
            k = 30

            for i in range(0, len(self.dealers_hand), 2):
                image_origo1 = pygame.image.load(f"img/{self.dealers_hand[i]}_of_{self.dealers_hand[i+1]}.png")
                image1 = pygame.transform.scale(image_origo1,(85,140))
                image1_rect = image1.get_rect(topleft=(j,k))
                self.app.screen.blit(image1, image1_rect)
                
                j += 50

            if self.lost:
            
                self.app.screen.blit(self.text2, self.text2_rect)

            if self.win:
            
                self.app.screen.blit(self.text1, self.text1_rect)

            if self.same:
            
                self.app.screen.blit(self.text3, self.text3_rect)   
            
        if self.split:
            every_card_pos = []
            started_cards = []
            started_cards2 = []
            w = 240
            q = 30

            for i in range(0, len(self.dealers_hand), 2):
                image_origo1 = pygame.image.load(f"img/{self.dealers_hand[i]}_of_{self.dealers_hand[i+1]}.png")
                image1 = pygame.transform.scale(image_origo1,(85,140))
                image1_rect = image1.get_rect(topleft=(w,q))
                self.app.screen.blit(image1, image1_rect)
                w += 50
            t = 40
            r = 420
            pos_of_first_cards = []

            for i in range(len(self.players_hand)):
                dat = 40
                
                two_split_images_origo = pygame.image.load(f"img/{self.players_hand[i][0]}_of_{self.players_hand[i][1]}.png")
                two_split_images = pygame.transform.scale(two_split_images_origo, (85, 140))
                two_split_images_rect = two_split_images.get_rect(topleft=(t, r))
                self.app.screen.blit(two_split_images, two_split_images_rect)
                pos_of_first_cards.append([two_split_images_rect.topleft])
                started_cards.append(two_split_images_rect.bottomleft)
                started_cards.append(two_split_images_rect.bottomright)
                started_cards2.append(two_split_images_rect.topleft)
                every_card_pos.append(two_split_images_rect.topleft)
                
                t += 200
                
                for j in range(2, len(self.players_hand[i]), 2):
                 
                    x = pos_of_first_cards[i][0][0] + dat
                    y = r - dat
                    dat += 40                  
                    
                    image_origo2 = pygame.image.load(f"img/{self.players_hand[i][j]}_of_{self.players_hand[i][j + 1]}.png")
                    image2 = pygame.transform.scale(image_origo2, (85, 140))
                    image2_rect = image2.get_rect(topleft=((x), (y)))
                    self.app.screen.blit(image2, image2_rect)
                    every_card_pos.append(image2_rect.topleft)

            
            colors = ["green", "red", "orange"]
            packs = list(self.lines.keys())
            packs.reverse()
            num = len(packs)
            num =- 1
            for key in packs:
                  
                status = self.lines[key]
                color = colors[status]
                pygame.draw.line(self.app.screen, color, (started_cards[num][0], 570), (started_cards[num-1][0], 570), width=4)
                num -= 2
            
            if self.hand_finished == False:
                self.creating_rect(started_cards2, self.dat, self.start_num)
                  
        
    def creating_rect(self, started_cards, dat, start_num):
        rect = pygame.Rect(((started_cards[start_num][0]) + dat), (started_cards[start_num][1] - dat), 85, 140)
        pygame.draw.rect(self.app.screen, "green", rect, 3)
             

    def buttons(self):
        self.btn_image_orig = pygame.image.load("bg/button.png")
        self.shuffle_image = pygame.transform.scale(self.btn_image_orig, (150, 55))
        
        self.stand_btn = Button((700,50), self.shuffle_image, "STAND", self.button_font, "white", "red")
        self.stand_btn.change_color(self.mouse_pos)
        self.stand_btn.update(self.app.screen)
        
        self.hit_btn = Button((700,110), self.shuffle_image, "HIT", self.button_font, "white", "red")
        self.hit_btn.change_color(self.mouse_pos)
        self.hit_btn.update(self.app.screen)
        
        self.shuffle_btn = Button((100, 50), self.shuffle_image, "NEW HAND", self.button_font, "white", "red")
        self.shuffle_btn.change_color(self.mouse_pos)
        # if self.hand_finished:
        self.shuffle_btn.update(self.app.screen)
        
        self.double_btn = Button((100, 110), self.shuffle_image, "DOUBLE", self.button_font, "white", "red")
        self.double_btn.change_color(self.mouse_pos)
        self.double_btn.update(self.app.screen)
        
        self.split_btn = Button((100, 170), self.shuffle_image, "SPLIT", self.button_font, "white", "red")
        self.stats_btn = Button((700,170), self.shuffle_image, "STATS", self.button_font, "white", "red")
        self.stats_btn.change_color(self.mouse_pos)
        self.stats_btn.update(self.app.screen)
        
        if self.show_split == True:
            self.split_btn.change_color(self.mouse_pos)
            self.split_btn.update(self.app.screen)
            

    def update(self):
        self.mouse_pos = pygame.mouse.get_pos()
        
        self.handle_split(self.players_value, self.players_hand)
             
        
    #TYP KARET
    def deck(self):
        self.card_values =  { 
                            'ace': 11,
                            '2': 2,
                            '3': 3,
                            '4': 4,
                            '5': 5,
                            '6': 6,
                            '7': 7,
                            '8': 8,
                            '9': 9,
                            '10': 10,
                            'jack': 10,
                            'queen': 10,
                            'king': 10
                            }
        self.card_type = ["diamonds", "hearts", "spades", "clubs"]

    #ROZDÁNÍ KARET NA ZAČÁTKU
    def starter_deal_cards(self):
             
        self.add_card(self.players_value, self.players_hand)
        self.add_card(self.players_value, self.players_hand)
        self.add_card(self.dealers_value, self.dealers_hand)
        self.handle_players_blackjack()
        
    #ZJISTI JESTLI JE BLACKJACK
    def handle_players_blackjack(self):
        
        if self.split == False:
            self.count_value = 0
            self.count_cards = 0
            self.d_count_value = 0
            self.d_count_cards = 0
            for card in self.players_value:
                self.count_value += card
                self.count_cards += 1
                   
            if self.count_value == 21 and self.count_cards == 2:
                self.open_json()   
                self.finish_dealers_hand(self.dealers_hand, self.dealers_value)
                if self.both_bj == False:
                    self.win = True
                    self.wins += 1
                    self.player_bj += 1
                    self.hands_played += 1
                    self.hand_finished = True
                    self.put_in_json()
                    
                
   
                
    #DOKONČENÍ DEALEROVI HANDY
    def finish_dealers_hand(self, hand, value):
        self.hand_finished = True
        dealer_total = sum(value)
        self.aces = 0
        dealer_total1 = 0
        

        while dealer_total < 17: 
            self.open_json()
            d_count_value = 0
            d_count_cards = 0
            count_cards = 0
            count_value = 0
            
            
            self.add_card(value, hand)
            dealer_total = sum(value)

            if self.split == False:
        
                for card in self.players_value:
                    count_value += card
                    count_cards += 1
                for card in self.dealers_value:
                    d_count_value += card
                    d_count_cards += 1
                
                if d_count_value == 21 and d_count_cards == 2 and count_value == 21 and count_cards == 2:
                    self.same = True
                    self.both_bj = True
                    self.draws += 1
                    self.hands_played += 1
                    self.hand_finished = True
                    self.zup += 1
                    
                    break

                elif d_count_value == 21 and d_count_cards == 2 and count_value == 21 and count_cards != 2:
                    self.lost = True
                    self.losses += 1
                    self.hands_played += 1
                    self.put_in_json()
                    
                    break
                elif d_count_value == 20 and d_count_cards == 2 and count_value == 21 and count_cards == 2:
                   
                    self.both_bj = False
                    
                
        
            for one in value:
                    if one == 11:
                        self.aces += 1

            while dealer_total > 21 and self.aces > 0:
                
                if 11 in value:
                      
                    index_11 = value.index(11)
                    value[index_11] = 1
                    self.aces -= 1
                    dealer_total = sum(value)
                   
                    self.both_bj = False
                else:
                   
                    break
                
                
        
                
                    
                    
        
        self.hand_finished = True 


    #PŘÍDAT KARTU PO ZMAČKNUTÍ "HIT"
    def add_card_to_player(self, hand, value):
        
        self.aces = 0
        self.add_card(value, hand)
        player_total = sum(value)
            
        if player_total > 21 and 11 in value and value:
            value[value.index(11)] = 1
            player_total = sum(value)
        else: pass


        for one in value:
                if one == 11:
                    self.aces += 1


        while player_total > 21 and self.aces > 0:
            try:  
                index_11 = value.index(11)
                value[index_11] = 1
                self.aces -= 1
                player_total = sum(value)
            except:
                player_total = sum(value)
                
                break

            
                    
    #MŮŽEM SPLITNOUT?
    def handle_split(self, value, hand):
        if self.split == True and self.split_count < 3:
            for x in value:
                if len(x) == 2 and x[0] == x[1]:
                    self.show_split = True
            for y in hand:
                if len(y) == 4 and y.count("ace") == 2:
                    self.show_split = True
        if self.split == False:
            if len(value) == 2 and value[0] == value[1]:
                self.show_split = True
       
    #ZMÁČKNUTÍ TLAČÍTKA SPLIT   
    def split_two_cards(self):
        self.split_count += 1
        
        self.dat = 0
        self.show_split = False
        new_value = []
        new_hand = []
        #SPLIT PO PRVÉ
        if self.split == False:
            
            for x in self.players_value:
                new_value.append([x])

            for i in range(0, len(self.players_hand), 2):
                new_hand.append([self.players_hand[i], self.players_hand[i + 1]])
            self.players_hand = new_hand
            self.players_value = new_value
            self.active = len(self.players_value) 
            
        
        #SPLIT VÍCEKRÁT
        if self.split == True:
            
        
            for inner_list in self.players_hand:
                if len(inner_list) > 2 and inner_list == self.players_hand[self.active-1]:
                    for i in range(0, len(inner_list), 2):
                        new_hand.append([inner_list[i], inner_list[i+1]])
                else:
                    new_hand.append(inner_list)

            for sub_list in self.players_value:
                if len(sub_list) > 1 and sub_list == self.players_value[self.active - 1]:
                    for element in sub_list:
                        new_value.append([element])
                else:
                    new_value.append(sub_list)

            self.players_hand = new_hand
            self.players_value = new_value
            
            self.active += 1
        self.split = True
            
        
    #PŘIDÁNÍ KARTY
    def add_card(self, value, hand):
        if self.split == False:
            choose_card = random.choice(list(self.card_values.keys()))
            choose_type = random.choice(self.card_type)
            value.append(self.card_values[choose_card])
            hand.append(choose_card)
            hand.append(choose_type)
            

        if self.split == True:
            
            choose_card = random.choice(list(self.card_values.keys()))
            choose_type = random.choice(self.card_type)
            value.append(self.card_values[choose_card])
            hand.append(choose_card)
            hand.append(choose_type)

    def move_cards(self):
        
        if self.split == True and self.active != 1:
            if sum(self.players_value[self.active - 1]) > 21:
                self.active -= 1
                self.dat = 0
                self.start_num -= 1
        if self.split == True and sum(self.players_value[0]) > 21:
            self.finish_dealers_hand(self.dealers_hand, self.dealers_value)
            self.check_winner()

    
    def open_json(self):
        try:
            with open("stats.json", "r") as f:
                self.stats_dict = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.stats_dict = {"wins": 0, "losses": 0, "draws": 0, "hands_played": 0, "player_bj": 0}

        self.losses = self.stats_dict.get("losses", 0)
        self.wins = self.stats_dict.get("wins", 0)
        self.draws = self.stats_dict.get("draws", 0)
        self.hands_played = self.stats_dict.get("hands_played", 0)
        self.player_bj = self.stats_dict.get("player_bj", 0)
        

        
    #ZKONTROLUJ VÍTĚZE
    def check_winner(self):
        self.open_json()

        if self.split == False:
            if sum(self.players_value) > 21:  
                self.lost = True
                self.losses += 1
                self.hands_played += 1
                self.hand_finished = True
                self.put_in_json()
                
            elif sum(self.dealers_value) > 21:
                self.win = True
                self.wins += 1
                self.hands_played += 1
                self.hand_finished = True
                self.put_in_json()
               

            elif sum(self.players_value) <= 21 and sum(self.dealers_value) <= 21:
                if self.hand_finished:
                    if sum(self.players_value) > sum(self.dealers_value):   
                        self.win = True
                        self.wins += 1
                        self.hands_played += 1
                        self.put_in_json()
                       
                    elif sum(self.players_value) < sum(self.dealers_value):
                        self.lost = True
                        self.losses += 1
                        self.hands_played += 1
                        self.put_in_json()
                       
                    elif sum(self.players_value) == 21 and sum(self.dealers_value) == 21 and len(self.players_value) > 2 and len(self.dealers_value) == 2:
                        self.lost = True
                        self.losses += 1
                        self.hands_played += 1
                        self.put_in_json()
                        
                    else:
                        self.same = True
                        self.draws += 1
                        self.hands_played += 1
                        self.put_in_json()
                        
        

        else:
            for i in range(len(self.players_value)):
                if sum(self.players_value[i]) > 21:
                    
                    self.lost = True
                    self.losses += 1
                    self.hands_played += 1
                    self.lines[i] = 1
                    self.put_in_json()
                    self.hand_finished = True
                elif sum(self.dealers_value) > 21:
                   
                    self.win = True
                    self.wins += 1
                    self.hands_played += 1
                    self.lines[i] = 0
                    self.put_in_json()


                elif sum(self.players_value[i]) <= 21 and sum(self.dealers_value) <= 21:
                    if self.hand_finished:
                        if sum(self.players_value[i]) > sum(self.dealers_value):   
                            self.win = True
                            self.wins += 1
                            self.hands_played += 1
                            self.lines[i] = 0
                            self.put_in_json()
                            
                        
                        elif sum(self.players_value[i]) < sum(self.dealers_value):
                            
                            self.lost = True
                            self.losses += 1
                            self.hands_played += 1
                            self.lines[i] = 1
                            self.put_in_json()
                        
                        elif sum(self.players_value[i]) == 21 and sum(self.dealers_value) == 21 and len(self.players_value[i]) == 2 and len(self.dealers_value) == 2:
                            self.lost = True
                            self.losses += 1
                            self.hands_played += 1
                            self.lines[i] = 1
                            self.put_in_json()
                            
                        else:
                            self.same = True
                            self.draws += 1
                            self.hands_played += 1
                            self.lines[i] = 2
                            self.put_in_json()
                            
        
        
        
    def put_in_json(self):
        self.stats_dict = {"wins": self.wins, "losses": self.losses, "draws": self.draws, "hands_played": self.hands_played, "player_bj": self.player_bj}
        
        with open("stats.json", "w") as f:
            json.dump(self.stats_dict, f)


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.hand_finished == False:
                    if self.hit_btn.check_for_input(self.mouse_pos):

                        if self.split == False:
                            self.add_card_to_player(self.players_hand, self.players_value)
                            self.check_winner()

                        if self.split == True:
                            self.dat += 40
                            self.add_card_to_player(self.players_hand[self.active - 1], self.players_value[self.active - 1])
                            self.move_cards()
                    if self.stand_btn.check_for_input(self.mouse_pos):
                        if self.split == False:
                            self.finish_dealers_hand(self.dealers_hand, self.dealers_value)
                            self.check_winner()

                        if self.split == True:
                            self.active -= 1
                        
                            if self.active == 0:
                                self.finish_dealers_hand(self.dealers_hand, self.dealers_value)
                                self.check_winner()

                            else:
                                self.start_num -= 1
                                self.dat = 0
                                self.move_cards()

                    if self.split_btn.check_for_input(self.mouse_pos):
                        self.split_two_cards()

                if self.shuffle_btn.check_for_input(self.mouse_pos):
                
                    self.restart()
                    self.starter_deal_cards()
                    
                
                if self.stats_btn.check_for_input(self.mouse_pos):
                    self.app.stats_run = True
                    self.stats.load_stats()
                    
                    

class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Blackjack")
        self.screen = pygame.display.set_mode((W, H))
        self.game = Game(self)
        self.stats = Stats(self)  
        self.stats_run = False      


    def update(self):
        if self.stats_run == False:
            self.game.update()
        if self.stats_run == True:
            self.stats.update()

    
    def draw(self):
        self.screen.fill((0,0,0))
        if self.stats_run == False:
            self.game.draw()
        if self.stats_run == True:
            self.stats.draw()
        
        pygame.display.update()


    def check_events(self):
        if self.stats_run == False:
            self.game.check_events()
        if self.stats_run == True:
            self.stats.check_events()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()



    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
            

            

app = App()
app.run()




    


    
        

