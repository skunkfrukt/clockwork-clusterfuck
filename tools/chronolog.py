import json

MAP_SENTINEL = 100

def look():
    print '{r} at {t}:00'.format(r=current_room.upper(), t=current_time)
    print 'Open: [{xx}]  Closed: [{cc}]'.format(xx='|'.join(get_open_exits()),
            cc='|'.join(get_closed_exits()))
	
def get_open_exits():
	all_exits = rooms[current_room]['exits']
	return [x for x in all_exits.keys() if all_exits[x]['open'] == 'always' or
			current_time in all_exits[x]['open']]
			
def get_closed_exits():
	all_exits = rooms[current_room]['exits']
	open_exits = get_open_exits()
	return [x for x in all_exits.keys() if x not in open_exits]
			
rooms = json.load(open('rooms.json'))

current_room = 'yard'
current_time = 18

look()
	
while True:
	cmd = raw_input('> ')
	if cmd == 'quit':
		break
	else:
		if cmd in get_open_exits():
			x = rooms[current_room]['exits'][cmd]
			current_room = x['dest']
			current_time += x['ofst']
			look()
		elif cmd == 'look':
			look()
		elif cmd == 'map':
			visited = set()
			unvisited = [(current_room, current_time)]
			while len(unvisited):
				current_room, current_time = unvisited.pop()
				for x in get_open_exits():
					old_room, old_time = current_room, current_time
					next = rooms[current_room]['exits'][x]
					current_room = next['dest']
					current_time += next['ofst']
					if (current_room, current_time) not in visited:
						unvisited.append((current_room, current_time))
					current_room, current_time = old_room, old_time
				visited.add((current_room, current_time))
				if len(visited) > MAP_SENTINEL:
					print 'Too many rooms visited. Infinite loop?'
					break
			print list(visited)
		elif cmd.startswith('open '):
			dir = cmd.split()[1]
			if dir not in get_closed_exits():
				print 'Not closed, or not a door.'
			else:
				rooms[current_room]['exits'][dir]['open'].append(current_time)
				print 'Opened door from this side.'
				other_room = rooms[current_room]['exits'][dir]['dest']
				for exit_from_other_room in rooms[other_room]['exits'].values():
					if exit_from_other_room['dest'] == current_room:
						exit_from_other_room['open'].append(current_time)
						print 'Opened door from other side.'
		elif cmd.startswith('close '):
			dir = cmd.split()[1]
			if dir not in get_open_exits():
				print 'Not open, or not a door.'
			elif rooms[current_room]['exits'][dir]['open'] == 'always':
				print 'Cannot close an always-open door.'
			else:
				rooms[current_room]['exits'][dir]['open'].remove(current_time)
				print 'Closed door from this side.'
				other_room = rooms[current_room]['exits'][dir]['dest']
				for exit_from_other_room in rooms[other_room]['exits'].values():
					if exit_from_other_room['dest'] == current_room:
						exit_from_other_room['open'].remove(current_time)
						print 'Closed door from other side.'
		elif cmd.startswith('goto '):
			split_cmd = cmd.split()
			room = split_cmd[1]
			time = int(split_cmd[2])
			current_room, current_time = room, time
			look()
		else:
			print 'Nope.'
