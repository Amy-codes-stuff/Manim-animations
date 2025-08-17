from manim import *
import math
import random
import numpy as np

config.background_color = WHITE

class LogicpediaOutro(Scene):
    def construct(self):
        EPSILON = 1e-9
        try:
            logo = ImageMobject("logicpedia_logo.png")
            logo.scale(1.8).to_edge(UP).shift(DOWN*2)
            self.play(FadeIn(logo, shift=UP, scale=1.1), run_time=0.8)
            
            line1 = Text("For more such videos,", font="Arial", color=BLACK)
            line2 = Text("Like & Subscribe to Logicpedia!", font="Arial Bold", color=BLUE)
            text_group = VGroup(line1, line2).arrange(DOWN, buff=0.3).next_to(logo, DOWN)

            self.play(Write(line1), run_time=0.6)
            self.play(Write(line2), run_time=0.6)
            self.wait(1)
        except:
            # Fallback if the logo file is not found
            outro_text = Text("Thanks for watching!", font_size=48, color=BLACK)
            self.play(Write(outro_text))
        self.wait(2)


