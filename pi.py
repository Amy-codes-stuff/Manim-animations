from manim import *
import random
import math # Import math for math.sqrt and math.pi

# Define custom colors for consistent use
GREEN_SCREEN = ManimColor("#00FF00")
ORANGE_COLOR = ManimColor("#FFA500") # Custom orange for true Pi
config.background_color = WHITE

# --- Scene 1: Introduction to Pi and the Problem ---
class IntroductionScene(Scene):
    def construct(self):
        title = Text("Estimating Pi (π)", font_size=50, color = BLACK).to_edge(UP)
        self.play(Write(title), run_time = 0.5)
        self.wait(0.5)

        circle = Circle(radius=2, color=BLUE)
        diameter_line = Line(circle.get_left(), circle.get_right(), color=RED)
        diameter_label = Tex("Diameter (d)", font_size=30, ).next_to(diameter_line, DOWN)

        self.play(Create(circle))
        self.play(Create(diameter_line), Write(diameter_label))
        self.wait(2)

        circumference_label = Tex("Circumference (C)", font_size=30).next_to(circle, RIGHT, buff=0.5)
        self.play(Write(circumference_label))

        # Simulate unwrapping the circumference
        unwrapped_circumference = Line(ORIGIN, RIGHT * 2 * math.pi, color=GREEN, stroke_width=7).align_to(diameter_line, LEFT)
        unwrapped_circumference.shift(DOWN * 1.5)
        unwrapped_circumference_label = Tex("$C = \\pi d$", font_size=40).next_to(unwrapped_circumference, UP)

        self.play(
            FadeOut(circle, diameter_line, diameter_label, circumference_label),
            ReplacementTransform(circle.copy().set_opacity(0), unwrapped_circumference), # Placeholder transform
            Write(unwrapped_circumference_label)
        )
        self.wait(1)

        pi_approx = Text(f"{math.pi:.8f}", font_size=40, color=YELLOW).next_to(unwrapped_circumference_label, DOWN, buff=0.5)
        self.play(Write(pi_approx))
        self.wait(1.5)

        question = Text("How can we estimate this infinite value?", font_size=35).next_to(pi_approx, DOWN, buff=1)
        self.play(Write(question))
        self.wait(1.5)
        self.play(FadeOut(question))

        monte_carlo_intro = Text("Introducing the Monte Carlo Method!", font_size=45, color=GREEN_SCREEN).to_edge(DOWN)
        self.play(Write(monte_carlo_intro))
        self.wait(2)

        self.play(FadeOut(*self.mobjects))

# --- Scene 2: Setting the Stage - The Square and the Circle ---
class SetupScene(Scene):
    def construct(self):
        square_side = 4
        circle_radius = square_side / 2

        square = Square(side_length=square_side, color=DARK_BLUE, stroke_width=3)
        square_label = Tex("Square", font_size=35,color=BLACK).next_to(square, UP)


        circle = Circle(radius=circle_radius, color=RED, stroke_width=3)
        circle_label = Tex("Inscribed Circle", font_size=35,color = BLACK).next_to(circle, DOWN)
        self.play(Create(circle), Write(circle_label),Create(square), Write(square_label))

        radius_line = Line(circle.get_center(), circle.get_right(), color=RED, stroke_width=2)
        radius_label = MathTex("r", font_size=35, color  = BLACK).next_to(radius_line, UP)

        side_line_left = Line(square.get_corner(UL), square.get_corner(DL), color=GREEN, stroke_width=2)
        side_label_left = MathTex("2r", font_size=35, color = BLACK).next_to(side_line_left, LEFT)
        self.play(Create(radius_line), Write(radius_label),Create(side_line_left), Write(side_label_left))

        group_objects = VGroup(square, circle, radius_line, radius_label, side_line_left, side_label_left, square_label, circle_label)
        self.play(group_objects.animate.shift(LEFT * 3))
        self.wait(0.3)

        text_area_intro = Text("Let's look at their areas...", font_size=40, color = BLACK).next_to(group_objects, RIGHT, buff=1)
        self.play(Write(text_area_intro), run_time = 0.5)
        self.play(FadeOut(text_area_intro))

        area_circle_formula = MathTex(
            "A_{\\text{circle}} = \\pi r^2",
            font_size=45, color = BLACK
        ).next_to(group_objects, RIGHT, buff=1, aligned_edge=UP)

        area_square_formula = MathTex(
            "A_{\\text{square}} = (2r)^2 = 4r^2",
            font_size=45, color = BLACK
        ).next_to(area_circle_formula, DOWN, aligned_edge=LEFT)
        self.play(Write(area_circle_formula),Write(area_square_formula))
        self.wait(0.3)

        ratio_formula = MathTex(
            "\\frac{A_{\\text{circle}}}{A_{\\text{square}}} = \\frac{\\pi r^2}{4r^2}",
            font_size=45, color = BLACK
        ).next_to(area_square_formula, DOWN, aligned_edge=LEFT, buff=0.7)
        self.play(Write(ratio_formula))

        simplified_ratio = MathTex(
            "= \\frac{\\pi}{4}",
            font_size=45, color=DARK_BLUE
        ).next_to(ratio_formula, RIGHT, buff=0.2)
        self.play(Write(simplified_ratio))
        self.wait(0.3)

        pi_formula = MathTex(
            "\\pi = 4 \\times \\frac{A_{\\text{circle}}}{A_{\\text{square}}}",
            font_size=50, color=DARK_BLUE
        ).next_to(ratio_formula, DOWN, aligned_edge=LEFT, buff=0.7)
        self.play(Write(pi_formula))
        self.wait(0.3)

        self.play(FadeOut(*self.mobjects))


# --- Scene 4: Introducing Random Points ---
class IntroducePointsScene(Scene):
    def construct(self):
        square_side = 4
        circle_radius = square_side / 2

        square = Square(side_length=square_side, color=DARK_BLUE, stroke_width=3)
        circle = Circle(radius=circle_radius, color=BLUE, stroke_width=3)

        self.add(square, circle)

        intro_text = Text("Now, let's 'throw' some random points!", font_size=40, color = BLACK).to_edge(UP)
        self.play(Write(intro_text), run_time = 0.5)
        self.wait(1)

        points = VGroup()
        num_initial_points = 10

        for i in range(num_initial_points):
            x = random.uniform(-circle_radius, circle_radius)
            y = random.uniform(-circle_radius, circle_radius)

            dot_pos = np.array([x, y, 0])

            if x**2 + y**2 <= circle_radius**2:
                dot = Dot(dot_pos, color=GREEN, radius=0.08)
                is_inside_text = Text("Inside Circle", color=GREEN, font_size=25).next_to(dot, RIGHT, buff=0.1)
            else:
                dot = Dot(dot_pos, color=RED, radius=0.08)
                is_inside_text = Text("Outside Circle", color=RED, font_size=25).next_to(dot, RIGHT, buff=0.1)

            points.add(dot)
            self.play(FadeIn(dot), run_time=0.1)
            if i < 4:
                self.play(Write(is_inside_text))
                self.wait(0.2)
                self.play(FadeOut(is_inside_text))

        self.wait(0.5)

        explanation_text = Text("Green dots are inside the circle, red dots are outside.", font_size=35, color = DARK_BLUE).to_edge(DOWN)
        self.play(Write(explanation_text), run_time = 0.5)
        self.wait(0.5)

        self.play(FadeOut(*self.mobjects))

# --- Scene 5: The Simulation in Progress (Small N) ---
class SimulationSmallN(Scene):
    def construct(self):
        square_side = 4
        circle_radius = square_side / 2

        square = Square(side_length=square_side, color=WHITE, stroke_width=1)
        circle = Circle(radius=circle_radius, color=BLUE, stroke_width=1)
        self.add(square, circle)

        total_points = ValueTracker(0)
        inside_circle_points = ValueTracker(0)
        estimated_pi = ValueTracker(0.0)

        total_text = MathTex("N_{\\text{total}}:", font_size=35).to_corner(UL).shift(RIGHT*0.5)
        total_val = always_redraw(
            lambda: DecimalNumber(total_points.get_value(), num_decimal_places=0)
            .next_to(total_text, RIGHT)
        )

        inside_text = MathTex("N_{\\text{inside}}:", font_size=35).next_to(total_text, DOWN, aligned_edge=LEFT)
        inside_val = always_redraw(
            lambda: DecimalNumber(inside_circle_points.get_value(), num_decimal_places=0)
            .next_to(inside_text, RIGHT)
        )

        pi_est_text = MathTex("\\pi \\approx", font_size=40).to_corner(UR).shift(LEFT*0.5)
        pi_est_val = always_redraw(
            lambda: DecimalNumber(estimated_pi.get_value(), num_decimal_places=4)
            .next_to(pi_est_text, RIGHT)
            .set_color(GREEN_SCREEN)
        )

        self.add(total_text, total_val, inside_text, inside_val, pi_est_text, pi_est_val)

        points_group = VGroup()
        num_points_small_n = 200

        status_text = Text("Initial Samples...", font_size=30).to_edge(DOWN)
        self.add(status_text)
        self.wait(0.5)

        for i in range(num_points_small_n):
            x = random.uniform(-circle_radius, circle_radius)
            y = random.uniform(-circle_radius, circle_radius)

            dot_pos = np.array([x, y, 0])

            total_points.increment_value(1)

            if x**2 + y**2 <= circle_radius**2:
                dot = Dot(dot_pos, color=GREEN, radius=0.03)
                inside_circle_points.increment_value(1)
            else:
                dot = Dot(dot_pos, color=RED, radius=0.03)

            points_group.add(dot)
            self.add(dot)

            if total_points.get_value() > 0:
                current_pi_estimate = 4 * (inside_circle_points.get_value() / total_points.get_value())
                estimated_pi.set_value(current_pi_estimate)

            if i % 20 == 0:
                self.wait(0.01)

        self.wait(1)
        self.play(FadeOut(*self.mobjects))

# --- Scene 6: Scaling Up - The Law of Large Numbers ---
class SimulationLargeN(Scene):
    def construct(self):
        square_side = 4
        circle_radius = square_side / 2

        square = Square(side_length=square_side, color=WHITE, stroke_width=1)
        circle = Circle(radius=circle_radius, color=BLUE, stroke_width=1)
        self.add(square, circle)

        # Start with a base of points from previous scene for continuity
        # These are illustrative values; for exact continuation, you'd pass them.
        total_points = ValueTracker(200)
        inside_circle_points = ValueTracker(int(math.pi/4 * 200)) # Approx 157
        estimated_pi = ValueTracker(4 * (inside_circle_points.get_value() / total_points.get_value()))

        # Display counters
        total_text = MathTex("N_{\\text{total}}:", font_size=35).to_corner(UL).shift(RIGHT*0.5)
        total_val = always_redraw(
            lambda: DecimalNumber(total_points.get_value(), num_decimal_places=0)
            .next_to(total_text, RIGHT)
        )

        inside_text = MathTex("N_{\\text{inside}}:", font_size=35).next_to(total_text, DOWN, aligned_edge=LEFT)
        inside_val = always_redraw(
            lambda: DecimalNumber(inside_circle_points.get_value(), num_decimal_places=0)
            .next_to(inside_text, RIGHT)
        )

        pi_est_text = MathTex("\\pi \\approx", font_size=40).to_corner(UR).shift(LEFT*0.5)
        pi_est_val = always_redraw(
            lambda: DecimalNumber(estimated_pi.get_value(), num_decimal_places=4)
            .next_to(pi_est_text, RIGHT)
            .set_color(GREEN_SCREEN)
        )

        true_pi_val = MathTex(f"\\pi_{{\\text{{true}}}} = {math.pi:.5f}...", font_size=30, color=ORANGE_COLOR).next_to(pi_est_text, DOWN, aligned_edge=LEFT)

        self.add(total_text, total_val, inside_text, inside_val, pi_est_text, pi_est_val, true_pi_val)

        # Add initial points to represent continuation from previous scene
        initial_points_on_screen = VGroup()
        for _ in range(int(total_points.get_value())):
            x = random.uniform(-circle_radius, circle_radius)
            y = random.uniform(-circle_radius, circle_radius)
            dot_pos = np.array([x, y, 0])
            dot = Dot(dot_pos, color=GREEN if x**2 + y**2 <= circle_radius**2 else RED, radius=0.03)
            initial_points_on_screen.add(dot)
        self.add(initial_points_on_screen)

        law_of_large_numbers_text = Text("The Law of Large Numbers:", font_size=40).to_edge(DOWN)
        explanation = Text("More points = More Accuracy!", font_size=35, color=YELLOW).next_to(law_of_large_numbers_text, DOWN)

        self.play(Write(law_of_large_numbers_text))
        self.wait(0.5)
        self.play(Write(explanation))
        self.wait(0.5)

        num_points_to_add = 20000 # Add more points for large N simulation
        points_per_frame = 500 # Adjust for desired animation speed

        def update_simulation(dt):
            current_total = total_points.get_value()
            if current_total >= 200 + num_points_to_add: # Ensure we don't exceed target
                self.remove_updater(update_simulation)
                return

            for _ in range(points_per_frame):
                x = random.uniform(-circle_radius, circle_radius)
                y = random.uniform(-circle_radius, circle_radius)

                dot_pos = np.array([x, y, 0])

                total_points.increment_value(1)

                if x**2 + y**2 <= circle_radius**2:
                    dot = Dot(dot_pos, color=GREEN, radius=0.03)
                    inside_circle_points.increment_value(1)
                else:
                    dot = Dot(dot_pos, color=RED, radius=0.03)

                self.add(dot)

                if total_points.get_value() > 0: # Avoid division by zero
                    current_pi_estimate = 4 * (inside_circle_points.get_value() / total_points.get_value())
                    estimated_pi.set_value(current_pi_estimate)

                if total_points.get_value() >= 200 + num_points_to_add:
                    break

        self.add_updater(update_simulation)
        # Calculate a wait time that allows the updater to run through all points
        self.wait(num_points_to_add / points_per_frame * (1/60.0)) # Approx frames * frame_duration (assuming 60fps)

        self.wait(2)

        self.play(FadeOut(*self.mobjects))

# --- Scene 7: Conclusion - The Power of Randomness ---
class ConclusionScene(Scene):
    def construct(self):
        square_side = 4
        circle_radius = square_side / 2
        square = Square(side_length=square_side, color=WHITE, stroke_width=1)
        circle = Circle(radius=circle_radius, color=BLUE, stroke_width=1)

        # Simulate a dense cloud of final points
        final_points_group = VGroup()
        # These numbers are for illustrative density, not precise carry-over
        total_simulated_for_display = 20000
        # Approximately what N_inside would be for 20000 points if pi/4 is the ratio
        simulated_inside = int(total_simulated_for_display * (math.pi / 4))

        for _ in range(total_simulated_for_display):
            x = random.uniform(-circle_radius, circle_radius)
            y = random.uniform(-circle_radius, circle_radius)
            dot_pos = np.array([x, y, 0])
            dot = Dot(dot_pos, color=GREEN if x**2 + y**2 <= circle_radius**2 else RED, radius=0.02)
            final_points_group.add(dot)

        self.add(square, circle, final_points_group)

        final_pi_estimate = 4 * (simulated_inside / total_simulated_for_display)
        final_pi_text = MathTex(f"\\pi \\approx {final_pi_estimate:.5f}", font_size=70, color=GREEN_SCREEN).to_edge(UP)

        self.play(Write(final_pi_text))
        self.wait(1)

        summary_text1 = Text("By simply throwing random 'darts'...", font_size=40).next_to(final_pi_text, DOWN, buff=1)
        summary_text2 = Text("...we can estimate the value of Pi!", font_size=40).next_to(summary_text1, DOWN, buff=0.5)

        self.play(Write(summary_text1))
        self.play(Write(summary_text2))
        self.wait(1.5)

        power_of_mc = Text("This is the power of the Monte Carlo Method!", font_size=45, color=YELLOW).to_edge(DOWN)
        self.play(Write(power_of_mc))
        self.wait(2)

        # No FadeOut here, as this is the last scene and the animation will end.

# --- Main Orchestration Scene ---
class MonteCarloPiAnimation(Scene):
    def construct(self):
        self.camera.background_color = "#282828" # Dark background

        # Call the construct method of each sub-scene directly
        # Each sub-scene is responsible for clearing its own mobjects
        IntroductionScene().construct()
        SetupScene().construct()
        IntroducePointsScene().construct()
        SimulationSmallN().construct()
        SimulationLargeN().construct()
        ConclusionScene().construct()


class ShapesVsCurveIntro(Scene):
    def construct(self):
        # --- 1. Opening Scene: Straightforward Shapes ---
        # Setup: Grid
        grid = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1],
            axis_config={"color": "#606060"}, # Slightly darker gray for subtle grid
            background_line_style={"stroke_opacity": 0.3}
        ).set_opacity(0.5)

        self.play(FadeIn(grid, run_time=1))

        # Rectangle
        rectangle = Rectangle(width=4, height=2, color=BLUE_C, fill_opacity=0.5)
        rect_l_label = Tex("L", color=BLUE_E).next_to(rectangle.get_left(), LEFT).shift(UP*0.5)
        rect_w_label = Tex("W", color=BLUE_E).next_to(rectangle.get_bottom(), DOWN).shift(LEFT*0.5)
        
        self.play(
            Create(rectangle, run_time=1),
        )
        self.play(
            FadeIn(rect_l_label, shift=LEFT*0.2),
            FadeIn(rect_w_label, shift=DOWN*0.2),
            run_time=0.5
        )
        self.wait(0.7)

        # Triangle
        triangle = Triangle(color=GREEN_C, fill_opacity=0.5).scale(1.5).move_to([-2, -1, 0])
        tri_b_label = Tex("B", color=GREEN_E).next_to(triangle.get_bottom(), DOWN).shift(LEFT*0.5)
        tri_h_label = Tex("H", color=GREEN_E).next_to(triangle.get_left(), LEFT).shift(UP*0.5)

        self.play(
            FadeOut(rect_l_label, rect_w_label),
            Transform(rectangle, triangle), # Morph rectangle into triangle
            run_time=1.5
        )
        self.play(
            FadeIn(tri_b_label, shift=DOWN*0.2),
            FadeIn(tri_h_label, shift=LEFT*0.2),
            run_time=0.5
        )
        self.wait(1)

        # Narration for shapes
        straight_text = Text(
            "When we measure shapes like squares or triangles, it's pretty straightforward.",
            font_size=28
        ).to_edge(UP).shift(DOWN*0.5) # Positioning text
        
        self.play(Write(straight_text, run_time=2))
        self.wait(1.5)

        # --- 2. The Shift: Introducing the Curve ---
        self.play(
            FadeOut(triangle, tri_b_label, tri_h_label),
            FadeOut(straight_text),
            FadeOut(grid),
            run_time=1
        )

        circle = Circle(radius=3, color=YELLOW_C, fill_opacity=0.5)

        self.play(
            Create(circle, run_time=2.5), # Standard create animation
        )
        self.wait(0.5)

        # Narration for circle
        curve_text = Text(
            "But what about a shape that's all curve? No straight lines, no sharp corners!",
            font_size=28
        ).to_edge(UP).shift(DOWN*0.5)
        self.play(Write(curve_text, run_time=2))
        self.wait(1.5)

        # --- 3. The Pi Reveal: The Endless Challenge ---
        diameter = Line(circle.get_left(), circle.get_right(), color=RED_D)
        
        self.play(
            Create(diameter, run_time=1),
        )
        self.wait(0.5)

        # Create scrolling random digits
        # This is a bit of a trick: create a long string of random-looking digits, then scroll it.
        random_digits_str = "0351982746193754820615937402853716942085731" * 5 # Repeat for length
        random_digits_mob = Tex(random_digits_str, font_size=28, color=GREY_A)
        
        # Position the digits along the circumference. This approximation is for visual effect.
        random_digits_mob.next_to(circle, DOWN, buff=0.5)
        
        # Create a VGroup for the text and its initial position
        random_digits_group = VGroup(random_digits_mob).move_to(random_digits_mob.get_center())

        # Animate scrolling - make it appear from right and scroll to left
        random_digits_group.shift(RIGHT * (random_digits_mob.width / 2 + MED_LARGE_BUFF))
        
        self.add(random_digits_group)
        self.play(
            random_digits_group.animate.shift(LEFT * (random_digits_mob.width + MED_LARGE_BUFF)),
            run_time=5,
            rate_func=linear,
        )
        
        # Narration for challenge
        challenge_text = Text(
            "How do we find a number that truly describes something so perfectly round, yet so infinite in its detail?",
            font_size=28
        ).to_edge(UP).shift(DOWN*0.5)
        self.play(Transform(curve_text, challenge_text), run_time=1) # Transform previous text
        self.wait(1.5)

        # --- 4. The Resolution: Enter Pi ---
        # Fade out random digits and diameter
        self.play(
            FadeOut(random_digits_group, run_time=0.5),
            FadeOut(diameter, run_time=0.5),
        )

        # Display Pi
        pi_symbol = Tex("$\\\\pi$", font_size=100, color=BLUE_E).move_to(circle.get_center())
        pi_digits = DecimalNumber(
            PI,
            num_decimal_places=20, # Show enough digits to convey endlessness
            font_size=30,
            color=WHITE
        )
        # Position digits around the circle, or just below for clarity
        pi_digits.next_to(circle, DOWN, buff=0.7)

        # Animate Pi appearing
        self.play(
            FadeIn(pi_symbol, scale=2),
            run_time=1
        )
        self.play(
            Create(pi_digits, run_time=3), # Animate digits appearing one by one
            FadeOut(challenge_text), # Fade out the question
            run_time=3
        )

        # Final narration
        final_text = Text(
            "It's through the magical, never-ending number we call Pi.",
            font_size=32
        ).to_edge(UP).shift(DOWN*0.5)
        final_text_part2 = Text(
            "And today, we'll explore how we figure out its incredible value!",
            font_size=32
        ).next_to(final_text, DOWN, buff=0.2)

        self.play(Write(final_text, run_time=1.5))
        self.wait(1)
        self.play(Write(final_text_part2, run_time=1.5))
        self.wait(2)