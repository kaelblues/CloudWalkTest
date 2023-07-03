import re

def read_run_logFile(filename):
    game_data = {}
    current_game = None

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()

            # check if the game started
            if line.startswith('InitGame:'):
                if current_game is not None:
                    # stores Last matches data
                    game_data[current_game]['killsum'] = sum(game_data[current_game]['kills'].values())
                current_game = line.split(' ')[1]
                game_data[current_game] = {'players': [], 'kills': {}}

            # check death row
            elif line.find('killed') != -1:
                match = re.search(r'(.+?) killed (.+?) by', line)
                if match:
                    killer = match.group(1)
                    victim = match.group(2)
                    if killer == '<world>':
                        game_data[current_game]['kills'].setdefault(victim, 0)
                        game_data[current_game]['kills'][victim] -= 1
                    else:
                        game_data[current_game]['kills'].setdefault(killer, 0)
                        game_data[current_game]['kills'][killer] += 1

                    # update players list
                    if killer != '<world>' and killer not in game_data[current_game]['players']:
                        game_data[current_game]['players'].append(killer)
                    if victim not in game_data[current_game]['players']:
                        game_data[current_game]['players'].append(victim)

    # stores Last matches data
    if current_game is not None:
        game_data[current_game]['killsum'] = sum(game_data[current_game]['kills'].values())

    return game_data

log_file = 'log.txt' 
game_data = read_run_logFile(log_file)

# show colected data
for game, data in game_data.items():
    print(f"Jogo: {game}")
    print(f"Total de kills: {data['killsum']}")
    print(f"Jogadores: {data['players']}")
    print("Kills:")
    for player, kills in data['kills'].items():
        print(f"  {player}: {kills}")
    print()
