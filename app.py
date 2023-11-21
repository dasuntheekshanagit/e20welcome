from flask import Flask, render_template, request, session, jsonify
import pickle
import random
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# The list to store winners by registration number
winners = []
groups = {
    1: [6, 3, []],
    2: [6, 3, []],
    3: [7, 2, []],
    4: [7, 2, []],
    5: [7, 2, []],
    6: [7, 2, []],
    7: [7, 2, []],
    8: [7, 2, []],
    9: [7, 2, []],
    10: [7, 2, []]
}
data = {}
girls = 0
boys = 0

def read_data():
    global girls, boys, data
    with open('data.csv', mode='r') as file:
        # Create a CSV reader object
        reader = csv.reader(file)

        # Skip the header row
        next(reader)

        # Loop through each row in the CSV file
        for row in reader:
            # Extract the registration number, name, and gender from the row
            reg_no, name, gender = row
            if gender == 'M':
                boys += 1
            else:
                girls += 1

            # Add the data to the dictionary
            data[reg_no] = {'name': name, 'gender': gender}
    print("Boys:", boys, "Girls:", girls)

class Location:
    def __init__(self, name, description, character=None, clue=None):
        self.name = name
        self.description = description
        self.character = character
        self.clue = clue
        self.paths = {}

    def get_description(self):
        return self.description

    def get_character(self):
        return self.character

    def get_clue(self):
        return self.clue

    def add_path(self, direction, destination):
        self.paths[direction] = destination


class Game:
    def __init__(self):
        self.locations = {}
        # self.current_location = None
        # self.previous_path = []

    def add_location(self, location):
        self.locations[location.name] = location

    # def set_current_location(self, location_name):
    #     if location_name in self.locations:
    #         self.current_location = self.locations[location_name]
    #     else:
    #         print("Location not found.")

    def print_current_description(self, current_location):
        return locationscurrent_location.get_description()

    def interact_with_character(self):
        character = self.current_location.get_character()
        if character:
            return f"{self.current_location.get_clue()}"
        else:
            return f"You are in {self.current_location.name}. No character here."

    def move(self, direction):
        if direction == "..":
            if len(self.previous_path) > 1:
                path = self.previous_path.pop()
                self.set_current_location(path)
                return self.print_current_description()
            if self.current_location.name == "Outside":
                return "Cannot go back from here."
            else:
                self.set_current_location("Outside")
                return self.print_current_description()
        elif direction in self.current_location.paths:
            path = self.current_location.paths[direction].name
            self.set_current_location(path)
            self.previous_path.append(path)
            print(self.previous_path)
            return self.print_current_description()
        else:
            return "Invalid direction."


class Player:
    def __init__(self, registration_number):
        self.registration_number = registration_number
        self.name = data[registration_number]["name"]
        self.gender = data[registration_number]["gender"]
        self.current_location = "outside"  # Set the initial location to outside

    def move_to_location(self, location_name):
        self.current_location = location_name

def initialize_game():
    game = Game()

    # Create locations
    outside = Location("outside", 
        "Hey there Hunter,\n Welcome to the department's doorstep! Exciting times await you inside. The key to winning lies in uncovering hidden clues scattered throughout. Chat up people, tinker with objects; they'll drop hints. Your ticket to victory? Explore the department, unravel the hidden clues, and they'll guide you straight to triumph.\n P.S. The first clue awaits in the welcome letter. \nGood luck!",
        "Welcome Letter",
        "Greetings, knowledge seekers! Your journey begins on the ground floor, where the Open Lab and Front desk is situated. Sahan Nimantha is in the Open Lab and Mr. X is at the front desk are your guides. Choose your path wisely!")
    ground_floor = Location("ground_floor",
                            "The ground floor welcomes you to the heart of the computer engineering department. Here, you'll find the Front Desk, a hub of general information, and the Open Lab, a dynamic space for study and discussions. The air is buzzing with curiosity and the hum of engaged minds",
                            )
    first_floor = Location("first_floor",
                           " As you ascend to the first floor, you step into a realm where knowledge takes tangible form. Lab 2 is a space where programming labs come to life, filled with the energy of practical application. The Computer Networking Lab, adjacent to it, is a gateway to the world of data transfer and communication."
                          )
    second_floor = Location("second_floor",
                            "The second floor unfolds with the Electronics Lab, a haven for hardware enthusiasts where circuits, wires, and hardware dreams come alive. Adjacent to it is the Discussion Room, a collaborative space where ideas flow freely, creating an atmosphere of shared knowledge.")
    third_floor = Location("third_floor",
                           "On the third floor, creativity blossoms in the ESCAL Makerspace. This vibrant space is a playground for innovation, equipped with tools for 3D printing, soldering, and collaborative projects. Here, students bring their ideas to life.")
    fourth_floor = Location("fourth_floor",
                            "On fourth floor hosts computer labs and the Server Room, a mysterious space filled with the rhythmic hum of servers. It's a realm where data flows, and secrets are concealed within the screens of computers.")

    front_desk = Location("front_desk",
                          "Welcome, explorer! If you lean towards technology, venture into the department. Alternatively, for general information, stay on the ground floor",
                        "Mr. X",
                        "If you're drawn to the practical side of computer engineering, where labs come to life, ascend the stairs with eager might, Kavindu's wisdom will guide your quest; listen well to what he suggests."
                        )
    open_lab = Location("open_lab",
                        "In this open space, discussions thrive.",
                        "Sahan Nimantha",
                        "Ah, welcome! The Open Lab is a vibrant space for discussions and study, filled with the hum of curiosity. Connect the dots in networking's spree, where Dr. Asitha molds minds like a sea. In the lab of networks, your clue awaits; unravel the code, open the gates")   

    networking_lab = Location("Networking Lab", 
        "Ascending to the first floor, the ambiance changes to the hum of technology. The Networking Lab, a haven for connectivity experiments, is filled with rows of computers and arrays of wires, offering glimpses into the realm of networking and digital interconnection. Tucked amidst the devices that power the digital world.", 
        "Dr. Asitha", 
        "In the realm of networks, Dr. Asitha bestows. Seek his wisdom about connections and nodes. His hint leads to another, where technology flows.")
    lab2 = Location("Lab 2", 
        "Lab2, a room filled with prototype models, microcontrollers, and intricate circuitry spread across workstations.", 
        "Kavindu", 
        "The third clue guides you to the MakerSpace on the 3rd floor.")
    discussion_room = Location("Discussion Room", 
        "You are in Lab1 where Kavindu is an instructor.", 
        "Kavindu", 
        "The third clue guides you to the MakerSpace on the 3rd floor.")    
    lab1 = Location("Lab1", 
        "You are in Lab1 where Kavindu is an instructor.", 
        "Kavindu", 
        "The third clue guides you to the MakerSpace on the 3rd floor.")
    escal = Location("ESCAL", 
        "Enter the ESCAL Room, a futuristic space resonating with the clinks of metal and the whirring of machinery. This innovative hub houses cutting-edge tools and resources.", 
        "Robot", 
        "The fourth clue indicates the top floor lab where Prof. Roshan is.")
    top_floor_lab = Location("Top_Floor_Lab", 
        "You are in the top floor lab with Prof. Roshan.", 
        "Prof. Roshan", 
        "Congratulations! You found the ticket!")

    # Add locations to the game
    game.add_location(outside)
    game.add_location(ground_floor)
    game.add_location(first_floor)
    game.add_location(second_floor)
    game.add_location(third_floor)
    game.add_location(first_floor)

    game.add_location(front_desk)
    game.add_location(open_lab)

    game.add_location(networking_lab)
    game.add_location(lab1)
    game.add_location(escal)
    game.add_location(top_floor_lab)

    # Set paths between locations
    outside.add_path("ground_floor", ground_floor)

    ground_floor.add_path("first_floor", first_floor)
    ground_floor.add_path("outside", outside)
    ground_floor.add_path("front_desk", front_desk)
    ground_floor.add_path("open_lab", open_lab)

    front_desk.add_path("ground_floor", ground_floor)

    open_lab.add_path("ground_floor", ground_floor)

    first_floor.add_path("second_floor", second_floor)
    first_floor.add_path("ground_floor", ground_floor)

    second_floor.add_path("third_floor", third_floor)
    second_floor.add_path("first_floor", first_floor)
    
    third_floor.add_path("fourth_floor", fourth_floor)
    third_floor.add_path("second_floor", second_floor)

    networking_lab.add_path("lab1", lab1)
    lab1.add_path("makerspace", escal)
    lab1.add_path("networking_lab", networking_lab)
    escal.add_path("top_floor_lab", top_floor_lab)
    escal.add_path("lab1", lab1)
    top_floor_lab.add_path("makerspave", escal)

    # Set the initial location
    game.set_current_location("outside")

    return game

def serialize_player(player):
    return pickle.dumps(player)

def deserialize_player(serialized_player):
    return pickle.loads(serialized_player)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        registration_number = request.form['registration_number']
        if registration_number in winners:
            return "You've already won the game!"
        else:
            if registration_number in data:
                player = Player(registration_number)
                serialized_player = serialize_player(player)
                session['player'] = serialized_player
                return render_template('game_interface.html', registration_number=registration_number, name=player.name)
    return render_template('index.html', winners=winners)


@app.route('/play_game', methods=['POST'])
def play_game():
    game_output = []
    serialized_player = session.get('player')

    if serialized_player is None:
        return "Session expired. Please start again."

    player = deserialize_player(serialized_player)
    user_input = request.form['user_input']
    game = player.game

    if user_input == "ls":
        game_output.append("You have several paths available: " + ", ".join(game.current_location.paths.keys()))
        game_output.append("Someone is here to chat: " + str(game.current_location.character))
    elif user_input == "pwd":
        game_output.append(f"Current location: {game.current_location.name}")
    elif user_input.startswith("less"):
        item = user_input.split(" ", 1)[-1]
        character = game.current_location.get_character()
        if character and item.lower() == character.lower():
            game_output.append(game.interact_with_character())
        else:
            game_output.append(f"You can't interact with {item}.")
    elif user_input == "cd ..":
        game_output.append(game.move(".."))
    elif "cd " in user_input:
        game_output.append(game.move(user_input.split()[-1]))
    else:
        game_output.append("Invalid command. Available actions: ['cd ..', 'ls', 'pwd', 'less', 'cls']")
    
    # Check if the player has won the game
    if game.current_location.name == "Top_Floor_Lab":
        winners.append(player.registration_number)
        game_output.append("Congratulations! You've won the game!")
        
    player.game = game
    serialized_player = serialize_player(player)
    session['player'] = serialized_player
    #return render_template('game_interface.html', registration_number=player.registration_number, game_output=game_output)
    return jsonify({'game_output': game_output})

# Route to generate a random number
@app.route('/generate_number', methods=['GET'])
def generate_number():
    serialized_player = session.get('player')

    if serialized_player is None:
        return "Session expired. Please start again."

    player = deserialize_player(serialized_player)

    num = random.randint(1, 10)
    if player.gender == 'M':
        gender = 0
    else:
        gender = 1
    while not groups[num][gender]:
        num = random.randint(1, 10)
    groups[num][gender] -= 1
    groups[num][2].append(player.registration_number)
    print(num)
    return jsonify({'number': num})

# Route to generate a random number
@app.route('/wheel', methods=['GET'])
def wheel():
    return render_template('sping_wheel.html')

# Route to generate a random number
@app.route('/teams', methods=['GET'])
def teams():
    return render_template('teams.html', groups=groups)

if __name__ == '__main__':
    read_data()
    app.run(debug=True)
