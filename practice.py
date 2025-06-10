from manim import *

class ShapeExample(Scene):
    def construct(self):
        circle = Circle().set_color(BLUE)
        square = Square().set_color(RED).shift(RIGHT * 2)

        self.play(Create(circle))
        self.wait(1)
        self.play(Transform(circle, square))
        self.wait(1)
        self.play(FadeOut(circle))
