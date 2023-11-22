from flask import Flask, render_template, request, session, jsonify
import pickle
import random
import csv

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# The list to store winners by registration number
winners = ['E/20/122', 'E/20/062', 'E/20/378', 'E/20/032', 'E/20/316', 'E/20/300', 'E/20/361', 'E/20/346', 'E/20/366', 'E/20/439', 'E/20/377', 'E/20/173','E/20/094', 'E/20/318']
groups = {
    1: [4, 3, ['E/20/032', 'E/20/318']],
    2: [5, 1, ['E/20/300', 'E/20/346', 'E/20/439']],
    3: [7, 1, ['E/20/122']],
    4: [6, 2, ['E/20/094']],
    5: [6, 0, ['E/20/377', 'E/20/062', 'E/20/316']],
    6: [7, 0, ['E/20/378', 'E/20/173']],
    7: [7, 2, []],
    8: [7, 2, []],
    9: [7, 2, []],
    10: [5, 2, ['E/20/366', 'E/20/361']]
}
data = {}
girls = 0
boys = 0
game = None

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

def log(logdata):
    with open('log.txt', mode='a+') as file:
        file.write(logdata+"\n")


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
        return self.locations[current_location].get_description()

    def interact_with_character(self, current_location):
        character = self.locations[current_location].get_character()
        if character:
            return f"{self.locations[current_location].get_clue()}"
        else:
            return f"You are in {self.current_location.name}. No character here."

    def move(self, direction, current_location, previous_path):
        if direction == "..":
            print(previous_path)
            if self.locations[current_location].name == "outside":
                return -1
            if len(previous_path) > 1:
                path = previous_path.pop()
                path = previous_path.pop()
                return path
                #self.set_current_location(path)
                #return self.print_current_description()
            previous_path.append("outside")
            return -1
                #self.set_current_location("Outside")
                #return self.print_current_description()
        elif direction in self.locations[current_location].paths:
            path = self.locations[current_location].paths[direction].name
            return path
            # self.set_current_location(path)
            # if path not in self.previous_path:
            #     self.previous_path.append(path)
            #return self.print_current_description()
        else:
            return -2


class Player:
    def __init__(self, registration_number):
        self.registration_number = registration_number
        self.name = data[registration_number]["name"]
        self.gender = data[registration_number]["gender"]
        self.current_location = "outside"
        self.previous_path = ["outside"]
    
    def move(self, direction):
        path = game.move(direction, self.current_location, self.previous_path)
        if path == -2:
            return "Invalid direction"
        elif path == -1:
            return "Cannot go back from here."
        self.previous_path.append(path)
        self.current_location = path
        return game.print_current_description(path)

def initialize_game():
    global game 

    game = Game()

    # Create locations
    outside = Location("outside", 
        "Hey there Hunter,\n Welcome to the department's doorstep! Exciting times await you inside. The key to winning lies in uncovering hidden clues scattered throughout. Chat with people, tinker with objects; they'll give you some hints. Your ticket to victory? Explore the department, unravel the hidden clues, and they'll guide you straight to triumph.\n P.S. The first clue awaits in the welcome letter. \nGood luck!",
        "welcome_letter",
        "Greetings, knowledge seekers! Your journey begins on the ground floor, where the Open Lab and Front desk is situated. Sahan Nimantha who is in the Open Lab and Mr. Wasundara who is at the front desk are your guides. Choose your path wisely!"
        )
    
    ground_floor = Location("ground_floor",
                            "The ground floor welcomes you to the heart of the computer engineering department. Here, you'll find the Front Desk, a hub of general information, and the Open Lab, a dynamic space for study and discussions. The air is buzzing with curiosity and the hum of engaged minds",
                            )
    
    first_floor = Location("first_floor",
                            " As you ascend to the first floor, you step into a realm where knowledge takes a tangible form. Lab 2 is a space where programming labs come to life, filled with the energy of practical application. The Computer Networking Lab, adjacent to it, is a gateway to the world of data transfer and communication."
                          )
   
    second_floor = Location("second_floor",
                            "The second floor unfolds with the Electronics Lab, a haven for hardware enthusiasts where circuits, wires, and hardware dreams come alive. Adjacent to it is the Discussion Room, a collaborative space where ideas flow freely, creating an atmosphere of shared knowledge."
                            )
   
    third_floor = Location("third_floor",
                           "On the third floor, creativity blossoms in the ESCAL Makerspace. This vibrant space is a playground for innovation, equipped with tools for 3D printing, soldering, and collaborative projects. Here, students bring their ideas to a reality"
                           )
   
    fourth_floor = Location("fourth_floor",
                            "On fourth floor hosts computer labs and the Server Room, a mysterious space filled with the rhythmic hum of servers. It's a realm where data flows, and secrets are concealed within the screens of computers."
                            )
   
    front_desk = Location("front_desk",
                        "Welcome, explorer! If you lean towards technology, venture into the department. Alternatively, for general information, stay on the ground floor",
                        "mr_wasundara",
                        "If you're drawn to the practical side of computer engineering, where labs come to life, ascend the stairs with eager might, Kavindu's wisdom will guide your quest; listen well to what he suggests."
                        )
    
    open_lab = Location("open_lab",
                        "In this open space, discussions thrive.",
                        "sahan_nimantha",
                        "Ah, welcome! The Open Lab is a vibrant space for discussions and study, filled with the hum of curiosity. Connect the dots in networking's spree, where Dr. Asitha molds minds like a sea. In the lab of networks, your clue awaits; unravel the code, open the gates"
                        )    
    
    lab2 = Location("lab2",      
                     "If you're drawn to the practical side of computer engineering, this is where programming labs come to life",
                    "mr_kavindu",
                    "Unleash your inner hardware enthusiast. Your journey continues in a space where circuits, wires, and hardware dreams are brought to life"
                    )
    
    networking_lab = Location("networking_lab",
                            "Connect with the world of data transfer and communication. This is the place where networking insights unfold and discussions about routers and switches take.",
                            "mr_asitha",
                            "For collaborative minds and focused discussions, ascend to the floor where ideas flow freely. Seek the place where the power of words and thoughts converge."
                            )
    
    electronics_lab = Location("electronics_lab",
                               "In the Electronics Lab, hardware dreams come to life and circuits weave tales!",
                               "dr_kamalanath",
                               "Embark on a journey of creativity and innovation. A robotic ally awaits in a space where projects come to life. Head to the floor where 3D printing, soldering, and collaboration thrive"
                               )
    
    discussion_room = Location("discussion_room",
                                "The Discussion Room unfolds as a sanctuary for collaborative minds, where ideas dance in the air.",
                               "dr_isuru",
                               "Welcome! The Discussion Room fosters an atmosphere for discussions and focused study. As you explore collaborative minds, In the makerspace, where creativity blooms, a robotic ally awaits. Engage in conversation, unlocking the next chapter in your journey"
                               )
         
    makerspace = Location("makerspace",
                          "In the makerspace, where machines breathe, creativity blooms amidst 3D printing, soldering, and collaborative projects and many more",
                          "robot",
                          "Beep boop!. Climb the stairs to the fourth floor,to the server's abode, where a computer hums in binary code. Decode the message, a clue to unfold, leading you to the ticket of stories untold"
                          )
    
    
    top_floor_lab = Location("top_floor_lab",
                              "If you have an inclination towards the hands-on aspects of computer engineering, this is another space where programming labs come to life.",
                             "dr_damayanthi",
                             "At the pinnacle of knowledge, I await your arrival. Engage in conversation, and the grand prize shall be revealed by Professor Ragel"
                            )
    
    server_room = Location("server_room",
                            "This is where servers hum in rhythmic unity and the place where data flows, ",
                           "server",
                           "Within the rhythmic hum of servers, a computer screen holds the key. Decode the cryptic message to unveil the path to the Dr.Damayanthi, where your last clue awaits"
                           )      
                   
    prof_ragel = Location("ground_floor_office",
                          "The ground floor welcomes you to the heart of the computer engineering department. Here, you'll find the Front Desk, a hub of general information, and the Open Lab, a dynamic space for study and discussions. The air is buzzing with curiosity and the hum of engaged minds",
                          "prof_ragel",
                          "Congratulations! You've won the game!"
                          )                   
                                    
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
    #outside.add_path("front_desk", front_desk)
    outside.add_path("ground_floor", ground_floor)
    
    ground_floor.add_path("front_desk",front_desk)
    ground_floor.add_path("open_lab",open_lab)
    ground_floor.add_path("outside", outside)

    front_desk.add_path("first_floor", first_floor)
    open_lab.add_path("first_floor", first_floor)

    first_floor.add_path("lab2",lab2)
    first_floor.add_path("networking_lab", networking_lab)
    first_floor.add_path("ground_floor", ground_floor)

    lab2.add_path("second_floor", second_floor)
    networking_lab.add_path("second_floor", second_floor)

    second_floor.add_path("electronics_lab",electronics_lab)
    second_floor.add_path("discussion_room", discussion_room)
    second_floor.add_path("first_floor", first_floor)

    electronics_lab.add_path("third_floor", third_floor)
    discussion_room.add_path("third_floor", third_floor)

    third_floor.add_path("makerspace", makerspace)
    third_floor.add_path("second_floor", second_floor)

    makerspace.add_path("fourth_floor", fourth_floor)

    fourth_floor.add_path("server_room", server_room)
    fourth_floor.add_path("top_floor_lab",top_floor_lab)
    #fourth_floor.add_path("ground_floor_office",prof_ragel)
    fourth_floor.add_path("third_floor", third_floor)

    top_floor_lab.add_path("ground_floor_office",prof_ragel)
    server_room.add_path("fourth_floor", fourth_floor)

    # Set the initial location
    #game.set_current_location("First Floor",)

    #return game

def serialize_player(player):
    return pickle.dumps(player)

def deserialize_player(serialized_player):
    return pickle.loads(serialized_player)

@app.route('/', methods=['GET', 'POST'])
def index():
    global winners
    try:
        if request.method == 'POST':
            registration_number = request.form['registration_number']
            print(registration_number, winners)
            if registration_number in winners:
                return render_template('teams.html', groups=groups)
            else:
                if registration_number in data:
                    player = Player(registration_number)
                    serialized_player = serialize_player(player)
                    session['player'] = serialized_player
                    return render_template('game_interface.html', registration_number=registration_number, name=player.name)
        return render_template('index.html', winners=winners)
    except:
        return render_template('index.html', winners=winners)

@app.route('/play_game', methods=['POST'])
def play_game():
    global winners
    try:
        global game
        game_output = []
        serialized_player = session.get('player')

        if serialized_player is None:
            return jsonify({'game_output':"ERROE 505"})
            #return render_template('index.html', winners=winners)

        player = deserialize_player(serialized_player)
        user_input = request.form['user_input']
    
        if user_input == "ls":
            game_output.append("You have several paths available: " + ", ".join(game.locations[player.current_location].paths.keys()))
            game_output.append("Someone is here to chat: " + str(game.locations[player.current_location].character))
        elif user_input == "pwd":
            game_output.append(f"Current location: {game.locations[player.current_location].name}")
        elif user_input.startswith("less"):
            item = user_input.split(" ", 1)[-1]
            character = game.locations[player.current_location].get_character()
            if character and item.lower() == character.lower():
                game_output.append(game.interact_with_character(player.current_location))
            else:
                game_output.append(f"You can't interact with {item}.")
        elif user_input == "cd ..":
            game_output.append(player.move(".."))
        elif "cd " in user_input:
            game_output.append(player.move(user_input.split()[-1]))
        else:
            game_output.append("Invalid command. Available actions: ['cd ..', 'ls', 'pwd', 'less', 'cls']")
        
        # Check if the player has won the game
        if game.locations[player.current_location].get_character == "Prof. Ragel":
            print(player.registration_number)
            #winners.append(player.registration_number)
            log(player.registration_number)
            game_output.append("Congratulations! You've won the game!")
            
        serialized_player = serialize_player(player)
        session['player'] = serialized_player
        #return render_template('game_interface.html', registration_number=player.registration_number, game_output=game_output)
        return jsonify({'game_output': game_output})
    except:
       return jsonify({'game_output':"ERROE 505"})

# Route to generate a random number
@app.route('/generate_number', methods=['GET'])
def generate_number():
    serialized_player = session.get('player')

    if serialized_player is None:
        return "Session expired. Please start again."
    
    player = deserialize_player(serialized_player)

    regnum = player.registration_number
    print(regnum)
    if regnum in winners:
        for i in groups.keys():
            for j in groups[i][2]:
                if j == regnum:
                    num = i
                    return jsonify({'number': num})

    num = random.randint(1, 10)
    if player.gender == 'M':
        gender = 0
    else:
        gender = 1
    while not groups[num][gender]:
        num = random.randint(1, 10)
    groups[num][gender] -= 1
   
    winners.append(player.registration_number)
    groups[num][2].append(player.registration_number)
    log(player.registration_number+","+str(num))
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

@app.route('/clear_session', methods=['GET'])
def clear_session():
    session.clear()
    return "Session cleared"

if __name__ == '__main__':
    read_data()
    initialize_game()
    app.run(debug=True)
