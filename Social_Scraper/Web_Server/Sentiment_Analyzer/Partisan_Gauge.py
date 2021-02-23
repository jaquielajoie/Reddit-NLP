class Partisan_Gauge:
    def __init__(self):
        self.cultural_axis = 0
        self.economic_axis = 0
        self.authoritarian_axis = 0

    def set_cultural_axis(self,cultural_axis):
        self.cultural_axis = cultural_axis

    def set_cultural_axis(self,cultural_axis):
        self.cultural_axis = cultural_axis

    def set_cultural_axis(self,cultural_axis):
        self.cultural_axis = cultural_axis

class DogWhistles:
    def __init__(self):
        self.whistles = {}

    def add_whistle(self, whistle_name, whistle_description, found_on_node):
        whistle_name = str(whistle_name)
        whistle_description = str(whistle_description)
        self.whistles[whistle_name] = whistle_description

class ProperNouns:
    def __init__(self):
        self.proper_nouns = {}

    def add_noun(self, noun_name, noun_description, found_on_node):
        whistle_name = str(noun_name)
        whistle_description = str(noun_description)
        self.proper_nouns[noun_name] = noun_description
