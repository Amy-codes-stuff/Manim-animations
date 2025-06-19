from manim import *

class newAnimation(Scene):
    def construct(self):
        grid = NumberPlane(
                    background_line_style={
                        "stroke_color": GREY,
                        "stroke_width": 1,
                        "stroke_opacity": 0.6,
                    }
                )        
        box = Rectangle(stroke_color =RED, fill_color = BLUE, fill_opacity = 0.5, height = 1, width = 1 )
        self.add(grid)
        self.add(box)
        self.play(box.animate.shift(RIGHT*2), run_time = 2)
        self.play(box.animate.shift(UP*5), run_time = 2)
        self.play(box.animate.shift(LEFT*2+DOWN*3), run_time = 2)
        self.play(box.animate.shift(RIGHT*4), run_time = 2)



class updater(Scene):
    def construct(self):
        grid = NumberPlane(
                    background_line_style={
                        "stroke_color": GREY,
                        "stroke_width": 1,
                        "stroke_opacity": 0.6,
                    }
                )
        
        rectangle = RoundedRectangle(stroke_width = 8, stroke_color = WHITE,
        fill_color = BLUE_B, width = 4.5, height = 2).shift(UP*3+LEFT*4)

        mathtext = MathTex("\\frac{3}{4} = 0.75"
        ).set_color_by_gradient(GREEN, PINK).set_height(1.5)
        mathtext.move_to(rectangle.get_center())
        mathtext.add_updater(lambda x : x.move_to(rectangle.get_center()))

        self.play(FadeIn(rectangle))
        self.play(Write(mathtext), run_time=2)
        self.play(rectangle.animate.shift(RIGHT*1.5+DOWN*5), run_time=3)
        mathtext.clear_updaters()
        self.play(rectangle.animate.shift(LEFT*2 + UP*5), run_time=3)
        self.wait()


class shapeinshape(Scene):
    def construct(self):

        r = ValueTracker(0.5) #Tracks the value of the radius
        
        circle = always_redraw(lambda : 
        Circle(radius = r.get_value(), stroke_color = YELLOW, 
        stroke_width = 5))

        line_radius = always_redraw(lambda : 
        Line(start = circle.get_center(), end = circle.get_bottom(), stroke_color = RED_B, stroke_width = 5)
        )

        line_circumference = always_redraw(lambda : 
        Line(stroke_color = YELLOW, stroke_width = 5
        ).set_length(2 * r.get_value() * PI).next_to(circle, DOWN, buff=0.2)
        )

        triangle = always_redraw(lambda : 
        Polygon(circle.get_top(), circle.get_left(), circle.get_right(), fill_color = GREEN_C)
        )

        self.play(LaggedStart(
            Create(circle), DrawBorderThenFill(line_radius), DrawBorderThenFill(triangle),
            run_time = 4, lag_ratio = 0.75
        ))
        self.play(ReplacementTransform(circle.copy(), line_circumference), run_time = 2)
        self.play(r.animate.set_value(2), run_time = 5)


from manim import *

class GraphingIntro(Scene):
    def construct(self):

        # Background grid with labeled coordinates
        backg_plane = NumberPlane(
            x_range=[-7, 7, 1],
            y_range=[-4, 4, 1]
        ).add_coordinates()

        # Main axes in the upper-right
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 3, 1],
            x_length=5,
            y_length=3,
            axis_config={"include_tip": True, "numbers_to_exclude": [0]}
        ).add_coordinates()

        # Move axes to upper right
        axes.to_edge(UR)

        # Axis labels
        axis_labels = axes.get_axis_labels(x_label="x", y_label="f(x)")

        # Graph: y = √x from x=0 to x=4
        graph = axes.plot(lambda x: x ** 0.5, x_range=[0, 4], color=YELLOW)

        # Group all graph-related objects
        graphing_stuff = VGroup(axes, graph, axis_labels)

        # Animations:
        self.play(FadeIn(backg_plane), run_time=6)
        self.play(backg_plane.animate.set_opacity(0.3))
        self.wait()
        self.play(DrawBorderThenFill(axes), Write(axis_labels), run_time=2)
        self.wait()
        self.play(Create(graph), run_time=2)
        self.play(graphing_stuff.animate.shift(DOWN * 4), run_time=3)
        self.wait()
        self.play(axes.animate.shift(LEFT * 3), run_time=3)
        self.wait()



from manim import *

class GraphWithPlane(Scene):  # Renamed for clarity
    def construct(self):

        # Background grid
        backg_plane = NumberPlane(x_range=[-7, 7, 1], y_range=[-4, 4, 1])
        backg_plane.add_coordinates()

        # Main graph plane
        my_plane = NumberPlane(
            x_range=[-6, 6], x_length=5,
            y_range=[-10, 10], y_length=5
        )
        my_plane.add_coordinates()
        my_plane.shift(RIGHT * 3)

        # Define the function f(x) = 0.1 * (x - 5) * x * (x + 5)
        my_function = my_plane.plot(
            lambda x: 0.1 * (x - 5) * x * (x + 5),
            x_range=[-6, 6],
            color=GREEN_B
        )

        # Function label
        label = MathTex("f(x)=0.1x(x-5)(x+5)").next_to(my_plane, UP, buff=0.2)

        # Area under the curve from x = -5 to 5
        area = my_plane.get_area(
            graph=my_function,
            x_range=[-5, 5],
            color=[BLUE, YELLOW]
        )

        # Horizontal line at f(-2)
        horiz_line = Line(
            start=my_plane.c2p(0, my_function.underlying_function(-2)),
            end=my_plane.c2p(-2, my_function.underlying_function(-2)),
            stroke_color=YELLOW,
            stroke_width=10
        )

        # Animations
        self.play(FadeIn(backg_plane), run_time=3)
        self.play(backg_plane.animate.set_opacity(0.2))
        self.wait()

        self.play(DrawBorderThenFill(my_plane), run_time=2)
        self.wait()

        self.play(Create(my_function), Write(label), run_time=2)
        self.wait()

        self.play(FadeIn(area), run_time=2)
        self.wait()

        self.play(Create(horiz_line), run_time=2)
        self.wait()

class vector(Scene):
    def construct(self):

        plane = NumberPlane(
            x_range=[-5, 5, 1], y_range=[-4, 4, 1], x_length=10, y_length=7
        )
        plane.add_coordinates()
        plane.shift(RIGHT * 2)

        vect1 = Line(
            start=plane.coords_to_point(0, 0),
            end=plane.coords_to_point(3, 2),
            stroke_color=YELLOW,
        ).add_tip()
        vect1_name = (
            MathTex("\\vec{v}").next_to(vect1, RIGHT, buff=0.1).set_color(YELLOW)
        )

        vect2 = Line(
            start=plane.coords_to_point(0, 0),
            end=plane.coords_to_point(-2, 1),
            stroke_color=RED,
        ).add_tip()
        vect2_name = MathTex("\\vec{w}").next_to(vect2, LEFT, buff=0.1).set_color(RED)

        vect3 = Line(
            start=plane.coords_to_point(3, 2),
            end=plane.coords_to_point(1, 3),
            stroke_color=RED,
        ).add_tip()

        vect4 = Line(
            start=plane.coords_to_point(0, 0),
            end=plane.coords_to_point(1, 3),
            stroke_color=GREEN,
        ).add_tip()
        vect4_name = (
            MathTex("\\vec{v} + \\vec{w}")
            .next_to(vect4, LEFT, buff=0.1)
            .set_color(GREEN)
        )

        stuff = VGroup(
            plane, vect1, vect1_name, vect2, vect2_name, vect3, vect4, vect4_name
        )

        box = RoundedRectangle(
            height=1.5, width=1.5, corner_radius=0.1, stroke_color=PINK
        ).to_edge(DL)

        self.play(DrawBorderThenFill(plane), run_time=2)
        self.wait()
        self.play(
            GrowFromPoint(vect1, point=vect1.get_start()), Write(vect1_name), run_time=2
        )
        self.wait()
        self.play(
            GrowFromPoint(vect2, point=vect2.get_start()), Write(vect2_name), run_time=2
        )
        self.wait()
        self.play(
            Transform(vect2, vect3),
            vect2_name.animate.next_to(vect3, UP, buff=0.1),
            run_time=2,
        )
        self.wait()
        self.play(
            LaggedStart(GrowFromPoint(vect4, point=vect4.get_start())),
            Write(vect4_name),
            run_time=3,
            lag_ratio=1,
        )
        self.wait()
        self.add(box)
        self.wait()
        self.play(stuff.animate.move_to(box.get_center()).set(width=1.2), run_time=3)
        self.wait()


