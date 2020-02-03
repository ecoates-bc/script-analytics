import re
from matplotlib import pyplot as plt


class TexReader:
    def __init__(self, filename):
        self.file = []
        self.filename = ""

        # reads the tex file and saves each line
        raw_texfile = open(filename, "r")
        self.filename = filename
        for line in raw_texfile:
            self.file.append(line)

        self.scenes = []
        self.characters = []

        self.read_scenes()
        self.read_characters()

    def read_scenes(self):
        scene = None
        for line in self.file:
            if "\scene{" in line:
                name = re.findall("{.+}", line)
                scene = Scene(name[0][1:-1])
                self.scenes.append(scene)
                continue
            if scene is not None:
                scene.add_line(line)

    def print_scene(self):
        print("Number of scenes: " + str(len(self.scenes)))
        for scene in self.scenes:
            print(scene.name + ", " + str(scene.get_elements()) + " elements, "
                  + str(scene.get_total_words()) + " words")
            scene.get_total_words()

    def read_characters(self):
        for line in self.file:
            if "\dg{" in line:
                result = re.findall("{.+}{", line)
                if len(result) > 0:
                    name = result[0][1:-2]
                    if self.no_matching_char(name):
                        character = Character(name)
                        self.characters.append(character)

    def no_matching_char(self, name):
        for character in self.characters:
            if character.name == name:
                return False
        return True

    def print_character(self):
        print("Number of characters: " + str(len(self.characters)))
        for character in self.characters:
            print(character.name)
            for scene in self.scenes:
                freq = character.get_elems_in_scene(scene)
                if freq > 0:
                    print(scene.name + ": " + str(freq) + " elements")

    def plot_scene_by_element(self):
        labels = []
        elems = []
        for scene in self.scenes:
            labels.append(scene.name)
            elems.append(scene.get_elements())
        fig1, ax1 = plt.subplots()
        ax1.pie(elems, labels=labels, autopct=lambda a: str(int(a)) + "%")
        ax1.axis('equal')
        plt.title(self.filename + ": Scene proportion by element")
        plt.show()

    def plot_character_by_element(self):
        labels = []
        elems = []
        for character in self.characters:
            labels.append(character.name)
            acc = 0
            for scene in self.scenes:
                acc += character.get_elems_in_scene(scene)
            elems.append(acc)
        fig1, ax1 = plt.subplots()
        ax1.pie(elems, labels=labels, autopct='%1.f%%')
        ax1.axis('equal')
        plt.title(self.filename + ": Character proportion by element")
        plt.show()


class Scene:
    def __init__(self, name):
        self.name = name
        self.lines = []
        self.characters = []

    def get_elements(self):
        acc = 0
        for line in self.lines:
            if "\\" in line:
                acc += 1
        return acc

    def add_line(self, line):
        self.lines.append(line)

    def get_total_words(self):
        pass2 = []

        # split each TeX line into individual commands
        for line in self.lines:
            pass1 = re.split("{", line)
            # filter out non alphabet characters and commands, split into individual words
            for elem in pass1:
                no_chars = re.sub("[\\\}\.\,]|(dg|ac)", "", elem)
                pass2.append(re.split(" ", no_chars))
        # remove empty strings
        for elem in pass2:
            if elem.__contains__(""):
                pass2.remove(elem)
        # count total number of words
        total_words = 0
        for elem in pass2:
            total_words += len(elem)
        return total_words


class Character:
    def __init__(self, name):
        self.name = name

    def get_elems_in_scene(self, scene):
        acc = 0
        for line in scene.lines:
            if "\dg{" in line:
                result = re.findall("{.+}{", line)
                if len(result) > 0:
                    name = result[0][1:-2]
                    if name == self.name:
                        acc += 1
        return acc
