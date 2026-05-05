class ArtDisplay:
    def __init__(self, name, art_type, worth):
        if worth <= 0:
            raise ValueError("Invalid worth value")
        self.name = name
        self.art_type = art_type
        self.worth = worth

    def __repr__(self):
        return f"{self.name} is a {self.art_type} that has an estimated worth of {self.worth} million dollars."

    def __gt__(self, other):
        return self.worth > other.worth


class MuseumSubscriber:
    def __init__(self, name, entries_left, favorites):
        self.name = name
        self.entries_left = int(entries_left)
        self.favorites = favorites

    def __repr__(self):
        return f"{self.name} has {self.entries_left} entries left."

    def set_entry(self):
        if self.entries_left == 0:
            print("Please renew your subscription.")
        else:
            self.entries_left -= 1
            print(f"Welcome! {self.entries_left} entries left.")

    def get_favorites(self):
        return self.favorites


class Museum:
    def __init__(self, art_displays):
        self.art_displays = art_displays[:]
        self.subscribers = []

    def __repr__(self):
        result = "This museum contains the following displays:\n"
        for art in self.art_displays:
            result += str(art) + "\n"
        return result

    def get_art_displays(self):
        return self.art_displays

    def get_art_display(self, name):
        for art in self.art_displays:
            if art.name == name:
                return art
        return None

    def add_art_display(self, art_display):
        self.art_displays.append(art_display)

    def add_subscriber(self, subscriber):
        self.subscribers.append(subscriber)

    def subscriber_entry(self, name):
        for subscriber in self.subscribers:
            if subscriber.name == name:
                subscriber.set_entry()
                return

    def find_loved_disp(self):
        if len(self.subscribers) == 0:
            return []

        loved_count = {}

        for subscriber in self.subscribers:
            for favorite in subscriber.get_favorites():
                if favorite.name not in loved_count:
                    loved_count[favorite.name] = 0
                loved_count[favorite.name] += 1

        max_count = max(loved_count.values())

        return [name for name, count in loved_count.items() if count == max_count]


def create_museum(filename):
    try:
        museum = Museum([])

        with open(filename, "r") as file:
            lines = file.read().splitlines()

        for line in lines:
            if line == "":
                continue

            data = line.split(",")

            if data[0] == "artDisplay":
                name = data[1]
                art_type = data[2]
                worth = int(data[3])

                try:
                    museum.add_art_display(ArtDisplay(name, art_type, worth))
                except ValueError:
                    museum.add_art_display(ArtDisplay(name, art_type, 1))

            elif data[0] == "subscriber":
                name = data[1]
                entries_left = data[2]
                favorites = [
                    museum.art_displays[int(data[3]) - 1],
                    museum.art_displays[int(data[4]) - 1],
                    museum.art_displays[int(data[5]) - 1]
                ]

                museum.add_subscriber(MuseumSubscriber(name, entries_left, favorites))

        print("The museum was created successfully.")
        return museum

    except IOError:
        print(f"Unable to load {filename} due to an IO Error")
