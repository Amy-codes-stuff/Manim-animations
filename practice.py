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


class StyledText(Scene):
    def construct(self):
        text = Text("Styled Text", font_size=72, color=YELLOW)
        text.move_to(UP)  # move the text upward
        self.play(FadeIn(text))
        self.wait(1)

from manim import *

class SimpleNeuralNetwork(Scene):
    def construct(self):
        # Define layer structure
        layer_sizes = [2, 4, 4, 1]
        layers = []

        # X distance between layers
        layer_spacing = 2.5

        # Draw neurons as circles in each layer
        for i, layer_size in enumerate(layer_sizes):
            layer = VGroup()
            for j in range(layer_size):
                neuron = Circle(radius=0.2, color=BLUE)
                neuron.move_to(RIGHT * i * layer_spacing + UP * (j - layer_size / 2 + 0.5))
                layer.add(neuron)
            layers.append(layer)

        # Add all neurons to the scene
        for layer in layers:
            self.add(layer)

        # Connect layers with lines
        for i in range(len(layers) - 1):
            for neuron1 in layers[i]:
                for neuron2 in layers[i + 1]:
                    line = Line(neuron1.get_right(), neuron2.get_left(), stroke_color=GREY, stroke_opacity=0.5)
                    self.add(line)

        # Optional: Add layer labels
        input_label = Text("Input Layer").next_to(layers[0], DOWN)
        hidden1_label = Text("Hidden Layer 1").next_to(layers[1], DOWN)
        hidden2_label = Text("Hidden Layer 2").next_to(layers[2], DOWN)
        output_label = Text("Output Layer").next_to(layers[3], DOWN)

        self.add(input_label, hidden1_label, hidden2_label, output_label)

        self.wait(3)




from manim import *

class AnimatedNeuralNetwork(Scene):
    def construct(self):
        layer_sizes = [2, 4, 4, 1]
        layers = []
        layer_spacing = 2.5

        # 1. Create neurons layer by layer
        for i, size in enumerate(layer_sizes):
            layer = VGroup()
            for j in range(size):
                neuron = Circle(radius=0.2, color=BLUE)
                neuron.move_to(RIGHT * i * layer_spacing + UP * (j - size / 2 + 0.5))
                layer.add(neuron)
            layers.append(layer)

        # 2. Group entire network and shift left
        network = VGroup(*layers)
        network.shift(LEFT * 4)

        # 3. Animate neurons
        for layer in layers:
            for neuron in layer:
                self.play(Create(neuron), run_time=0.2)

        # 4. Animate connections
        for i in range(len(layers) - 1):
            for neuron1 in layers[i]:
                for neuron2 in layers[i + 1]:
                    line = Line(
                        neuron1.get_right(), neuron2.get_left(),
                        stroke_color=GREY, stroke_opacity=0.5
                    )
                    self.play(GrowFromCenter(line), run_time=0.05)
                    self.add(line)

        # 5. Add and animate labels with font size
        input_label = Text("Input Layer", font_size=20).next_to(layers[0], DOWN)
        hidden1_label = Text("Hidden Layer 1", font_size=20).next_to(layers[1], DOWN)
        hidden2_label = Text("Hidden Layer 2", font_size=20).next_to(layers[2], DOWN)
        output_label = Text("Output Layer", font_size=20).next_to(layers[3], DOWN)

        for label in [input_label, hidden1_label, hidden2_label, output_label]:
            self.play(FadeIn(label), run_time=0.3)

        self.wait(2)
