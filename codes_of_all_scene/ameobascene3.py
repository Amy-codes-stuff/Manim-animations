from manim import *
import math
import random
import numpy as np

class AmeobaScene(Scene):
    EPSILON = 1e-9
    def construct(self):
        self.camera.background_color = WHITE
        
        # --- Start Scene 4: MonteCarloAmoeba ---
        outer_side_amoeba = 4
        total_points_amoeba = 1000
        radius_amoeba = 1.0
        batch_size_amoeba = 5
        dot_inner_radius = 0.07
        dot_border_offset = 0.01

        outer_square_amoeba = Square(side_length=outer_side_amoeba, color=BLACK)
        self.play(Create(outer_square_amoeba)); self.wait(0.5)

        def generate_amoeba_points(radius=1.0, n_points=300):
            thetas = np.linspace(0, 2 * math.pi, n_points)
            r_values = radius * (1 + 0.3 * np.sin(5 * thetas))
            x_coords, y_coords = r_values * np.cos(thetas), r_values * np.sin(thetas)
            return [np.array([x, y, 0]) for x, y in zip(x_coords, y_coords)]
        def is_inside_amoeba(point, radius=1.0):
            x, y = point[0], point[1]
            r_point = np.sqrt(x**2 + y**2)  # ✅ FIXED
            theta = np.arctan2(y, x)
            if theta < 0:
                theta += 2 * math.pi
            return r_point < radius * (1 + 0.3 * np.sin(5 * theta))

        amoeba_points = generate_amoeba_points(radius_amoeba)
        amoeba = VMobject().set_points_as_corners([*amoeba_points, amoeba_points[0]]).set_fill(BLUE, opacity=0.3).set_stroke(BLUE, width=2)
        self.play(Create(amoeba)); self.wait(0.5)

        outer_label_amoeba = MathTex(f"{outer_side_amoeba}", color=BLACK, font_size=28).next_to(outer_square_amoeba, RIGHT)
        inner_label_amoeba = MathTex(r"\text{Amoeba}", font_size=28).next_to(amoeba, LEFT, buff=1.0)
        self.play(Write(outer_label_amoeba), Write(inner_label_amoeba)); self.wait(0.5)

        inside_count_amoeba = 0
        frac_counter_amoeba = MathTex(r"\frac{0}{0}", font_size=36, color=GREEN).next_to(outer_square_amoeba.get_corner(UL),(LEFT+UP), buff = 1)
        prob_value_amoeba = DecimalNumber(0, num_decimal_places=4, color=RED, font_size=36).next_to(outer_square_amoeba.get_corner(DR),(RIGHT + DOWN), buff = 1)
        prob_label_amoeba = Text("Area \u2248 ", font_size=36, color=RED).next_to(prob_value_amoeba, LEFT, buff=0.2)
        prob_group_amoeba = VGroup(prob_label_amoeba, prob_value_amoeba)
        self.add(frac_counter_amoeba, prob_group_amoeba); self.wait(0.5)

        half_outer_amoeba = outer_side_amoeba / 2
        points_group_amoeba = VGroup()

        for i in range(0, total_points_amoeba, batch_size_amoeba):
            current_batch_count_amoeba = min(batch_size_amoeba, total_points_amoeba - i)
            batch_points_amoeba = VGroup()

            for j in range(current_batch_count_amoeba):
                point_coords_amoeba = np.array([random.uniform(-half_outer_amoeba, half_outer_amoeba), random.uniform(-half_outer_amoeba, half_outer_amoeba), 0])
                if is_inside_amoeba(point_coords_amoeba, radius_amoeba):
                    inner_color = GREEN; inside_count_amoeba += 1
                else: inner_color = RED
                # ✅ CHANGED
                outer_dot = Dot(point=point_coords_amoeba, radius=dot_inner_radius + dot_border_offset, color=BLACK)
                inner_dot = Dot(point=point_coords_amoeba, radius=dot_inner_radius, color=inner_color)
                dot_amoeba = VGroup(outer_dot, inner_dot)
                batch_points_amoeba.add(dot_amoeba)
            
            self.add(batch_points_amoeba)
            points_group_amoeba.add(batch_points_amoeba)
            total_so_far_amoeba = i + current_batch_count_amoeba
            
            new_frac_tex_amoeba = MathTex(rf"\frac{{{inside_count_amoeba}}}{{{total_so_far_amoeba}}}", font_size=36, color=GREEN).move_to(frac_counter_amoeba.get_center())
            self.play(Transform(frac_counter_amoeba, new_frac_tex_amoeba), run_time=0.1)
            prob_value_amoeba.set_value(inside_count_amoeba / total_so_far_amoeba)
            self.wait(0.1)

        self.wait(1)
        # ... (Final animation sequence remains the same)
        figure_group_amoeba = VGroup(outer_square_amoeba, amoeba, outer_label_amoeba, inner_label_amoeba, points_group_amoeba)
        self.play(figure_group_amoeba.animate.move_to(UP *1.75), FadeOut(frac_counter_amoeba), FadeOut(prob_group_amoeba))
        self.wait(0.25)
        estimated_formula_amoeba = MathTex(rf"\text{{Estimated Area}} \approx \frac{{{inside_count_amoeba}}}{{{total_points_amoeba}}} = {inside_count_amoeba / total_points_amoeba:.4f}", color=BLACK).scale_to_fit_width(7).next_to(figure_group_amoeba, DOWN, buff=1.2)
        self.play(Write(estimated_formula_amoeba)); self.wait(0.5)
        self.play(FadeOut(figure_group_amoeba, estimated_formula_amoeba)); self.wait(1)
