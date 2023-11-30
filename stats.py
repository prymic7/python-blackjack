import pygame
from button import Button
import json
import sys
class Stats():
    def __init__(self, app):
        self.app = app
        self.button_font = pygame.font.SysFont("calibri", 23, bold=True)
        self.stats_dict = {}
        self.win_prc = {}
        self.loss_prc = {}
        self.same_prc = {}
        self.bj_prc = {}
        self.wins = 0
        self.losses = 0
        self.draws = 0
        
        
        
        

        

    def draw(self):
        self.bg_orig = pygame.image.load("bg/table.webp")
        self.bg = pygame.transform.scale(self.bg_orig, (800,600))
        self.bg_rect = self.bg.get_rect(topleft=(0,0))
        self.app.screen.blit(self.bg, self.bg_rect)
        self.buttons()
        self.load_stats()
        self.write_text()
        
        


    def load_stats(self):
        try:
            with open("stats.json", "r") as f:
                self.stats_dict = json.load(f)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            self.stats_dict = {"wins": 0, "losses": 0, "draws": 0, "hands_played": 0, "player_bj": 0}
        
        self.math_stats()
        
        
    def write_text(self):
        
        self.ratio_text = self.button_font.render(f"WIN/LOSE/DRAW: {self.win_prc}%/{self.loss_prc}%/{self.same_prc}%", True, "white")
        self.ratio_text_rect = self.ratio_text.get_rect(topleft=(80,160))
        self.app.screen.blit(self.ratio_text, self.ratio_text_rect)
        self.bj_text = self.button_font.render(f"PLAYERS BJ/HAND: {self.bj_prc}%", True, "white")
        self.bj_text_rect = self.bj_text.get_rect(topleft=(80, 130))
        self.app.screen.blit(self.bj_text, self.bj_text_rect)
        self.games_played = self.button_font.render(f"HANDS PLAYED: {self.stats_dict['hands_played']}", True, "white")
        self.games_played_rect = self.games_played.get_rect(topleft=(80, 100))
        self.app.screen.blit(self.games_played, self.games_played_rect)

    def math_stats(self):
        if self.stats_dict["hands_played"] > 0:
            self.win_prc = "{:.1f}".format((self.stats_dict["wins"]/self.stats_dict["hands_played"]) * 100)
            self.loss_prc = "{:.1f}".format((self.stats_dict["losses"]/self.stats_dict["hands_played"]) * 100)
            self.same_prc = "{:.1f}".format(100 - float(self.win_prc) - float(self.loss_prc))
            self.bj_prc = "{:.1f}".format((self.stats_dict["player_bj"]/self.stats_dict["hands_played"]) * 100)


        else:
            self.win_prc = 0
            self.loss_prc = 0
            self.same_prc = 0
            self.bj_prc = 0

    def buttons(self):
        self.btn_image_orig = pygame.image.load("bg/button.png")
        self.shuffle_image = pygame.transform.scale(self.btn_image_orig, (150, 55))
        
        self.back_btn = Button((700,50), self.shuffle_image, "BACK", self.button_font, "white", "red")
        self.back_btn.change_color(self.mouse_pos)
        self.back_btn.update(self.app.screen)

    def update(self):
        self.mouse_pos = pygame.mouse.get_pos()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_btn.check_for_input(self.mouse_pos):
                    self.app.stats_run = False
