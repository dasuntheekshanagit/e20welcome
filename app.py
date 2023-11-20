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
        self.current_location = None
        self.previous_path = []

    def add_location(self, location):
        self.locations[location.name] = location

    def set_current_location(self, location_name):
        if location_name in self.locations:
            self.current_location = self.locations[location_name]
        else:
            print("Location not found.")

    def print_current_description(self):
        return self.current_location.get_description()

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
            if path not in self.previous_path:
                self.previous_path.append(path)
            return self.print_current_description()
        else:
            return "Invalid direction."


class Player:
    def __init__(self, registration_number):
        self.registration_number = registration_number
        self.name = data[registration_number]["name"]
        self.gender = data[registration_number]["gender"]
        self.game = initialize_game()

def initialize_game():
    game = Game()

    # Create locations
    outside = Location("Outside", 
        "Hey there Hunter,\n Welcome to the department's doorstep! Exciting times await you inside. The key to winning lies in uncovering hidden clues scattered throughout. Chat up people, tinker with objects; they'll drop hints. Your ticket to victory? Explore the department, unravel the hidden clues, and they'll guide you straight to triumph.\n P.S. The first clue awaits in the welcome letter. \nGood luck!",
        "Welcome Letter",
        "Greetings, knowledge seekers! Your journey begins on the ground floor, where the Open Lab and Front desk is situated. Sahan Nimantha is in the Open Lab and Mr. X is at the front desk are your guides. Choose your path wisely!")
    
    ground_floor = Location("Ground Floor",
                            "The ground floor welcomes you to the heart of the computer engineering department. Here, you'll find the Front Desk, a hub of general information, and the Open Lab, a dynamic space for study and discussions. The air is buzzing with curiosity and the hum of engaged minds",
                            )
    
    first_floor = Location("First Floor",
                           " As you ascend to the first floor, you step into a realm where knowledge takes tangible form. Lab 2 is a space where programming labs come to life, filled with the energy of practical application. The Computer Networking Lab, adjacent to it, is a gateway to the world of data transfer and communication."
                          )
   
    second_floor = Location("Second Floor",
                            "The second floor unfolds with the Electronics Lab, a haven for hardware enthusiasts where circuits, wires, and hardware dreams come alive. Adjacent to it is the Discussion Room, a collaborative space where ideas flow freely, creating an atmosphere of shared knowledge.")
   
    third_floor = Location("Third Floor",
                           "On the third floor, creativity blossoms in the ESCAL Makerspace. This vibrant space is a playground for innovation, equipped with tools for 3D printing, soldering, and collaborative projects. Here, students bring their ideas to life.")
   
    fourth_floor = Location("Fourth Floor/ Top Floor",
                            "On fourth floor hosts computer labs and the Server Room, a mysterious space filled with the rhythmic hum of servers. It's a realm where data flows, and secrets are concealed within the screens of computers.")
   
    front_desk = Location("Front Desk",
                          "Welcome, explorer! If you lean towards technology, venture into the department. Alternatively, for general information, stay on the ground floor",
                        "Mr.X",
                        "If you're drawn to the practical side of computer engineering, where labs come to life, ascend the stairs with eager might, Kavindu's wisdom will guide your quest; listen well to what he suggests."
                        )
    
    open_lab = Location("Open Lab",
                        "In this open space, discussions thrive.",
                        "Sahan Nimantha",
                        "Ah, welcome! The Open Lab is a vibrant space for discussions and study, filled with the hum of curiosity. Connect the dots in networking's spree, where Dr. Asitha molds minds like a sea. In the lab of networks, your clue awaits; unravel the code, open the gates")               
                   
    
    lab2 = Location("Lab2",      
                    "If you're drawn to the practical side of computer engineering, this is where programming labs come to life",
                    "Mr. Kavindu",
                    "Unleash your inner hardware enthusiast. Your journey continues in a space where circuits, wires, and hardware dreams are brought to life")
    
    
    networking_lab = Location("Networking Lab",
                            "Connect with the world of data transfer and communication. This is the place where networking insights unfold and discussions about routers and switches take.",
                            "Dr. Asitha",
                            "For collaborative minds and focused discussions, ascend to the floor where ideas flow freely. Seek the place where the power of words and thoughts converge.")
    
    electronics_lab = Location("Electronics Lab",
                               "In the Electronics Lab, hardware dreams come to life and circuits weave tales!",
                               "Dr.Kamalanath",
                               "Embark on a journey of creativity and innovation. A robotic ally awaits in a space where projects come to life. Head to the floor where 3D printing, soldering, and collaboration thrive")
    
    discussion_room = Location("Discussion Room",
                               "The Discussion Room unfolds as a sanctuary for collaborative minds, where ideas dance in the air.",
                               "Dr.Isuru",
                               "Welcome! The Discussion Room fosters an atmosphere for discussions and focused study. As you explore collaborative minds, In the makerspace, where creativity blooms, a robotic ally awaits. Engage in conversation, unlocking the next chapter in your journey")
         
    makerspace = Location("Makerspace",
                          "In the makerspace, where machines breathe, creativity blooms amidst 3D printing, soldering, and collaborative projects and many more",
                          "Robot",
                          "Beep boop!. Climb the stairs to the fourth floor,to the server's abode, where a computer hums in binary code. Decode the message, a clue to unfold, leading you to the ticket of stories untold")
    
    
    top_floor_lab = Location("Top Floor Lab",
                             "If you have an inclination towards the hands-on aspects of computer engineering, this is the space where programming labs come to life.",
                             "Dr.Damayanthi",
                             "At the pinnacle of knowledge, I await your arrival. Engage in conversation, and the grand prize shall be revealed by Professor Ragel")
    
    
    server_room = Location("Server Room",
                           "This is where servers hum in rhythmic unity and the place where data flows, ",
                           "Server",
                           "Within the rhythmic hum of servers, a computer screen holds the key. Decode the cryptic message to unveil the path to the Dr.Damayanthi, where your last clue awaits")
                               
                   
    prof_ragel = Location("Ground Floor",
                          "The ground floor welcomes you to the heart of the computer engineering department. Here, you'll find the Front Desk, a hub of general information, and the Open Lab, a dynamic space for study and discussions. The air is buzzing with curiosity and the hum of engaged minds",
                          "Prof. Ragel",
                          "Congratulations! You've won the game!")                     
                   
                   
                   
                   
                          
    # Add locations to the game
    game.add_location(outside)
    game.add_location(ground_floor)
    game.add_location(first_floor)
    game.add_location(second_floor)
    game.add_location(third_floor)
    game.add_location(fourth_floor)
    game.add_location(front_desk)
    game.add_location(open_lab)
    game.add_location(lab2)
    game.add_location(networking_lab)
    game.add_location(electronics_lab)
    game.add_location(discussion_room)
    game.add_location(makerspace)
    game.add_location(top_floor_lab)
    game.add_location(server_room)
    game.add_location(prof_ragel)

    # Set paths between locations
    outside.add_path("Front Desk", front_desk)
    outside.add_path("Ground Floor", ground_floor)
    ground_floor.add_path("Front Desk",front_desk)
    ground_floor.add_path("Open Lab",open_lab)
    front_desk.add_path("First Floor", first_floor)
    open_lab.add_path("First Floor", first_floor)
    first_floor.add_path("Lab 2",lab2)
    first_floor.add_path("Networking Lab", networking_lab)
    lab2.add_path("Second Floor", second_floor)
    networking_lab.add_path("Second Floor", second_floor)
    second_floor.add_path("Electronics Lab",electronics_lab)
    second_floor.add_path("Discussion Room", discussion_room)
    electronics_lab.add_path("Third Floor", third_floor)
    discussion_room.add_path("Third Floor", third_floor)
    third_floor.add_path("ESCAL Makerspace", makerspace)
    makerspace.add_path("Fourth Floor", fourth_floor)
    fourth_floor.add_path("Server Room", server_room)
    fourth_floor.add_path("Top Floor Lab",top_floor_lab)
    fourth_floor.add_path("Prof. Ragel",prof_ragel)

    # Set the initial location
    game.set_current_location("First Floor",)

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
