import csv

csv_input = open('search_output_completo1.csv', 'r')
csv_reader = csv.reader(csv_input)
nodes_list = []
edge_list = []
for row in csv_reader:
	nodes_list.append(row)

def generate_nodes_file():
	output = open('nodes.csv', 'w')
	output.write('Id,Label,Size'+'\n')
	for node in nodes_list:
		size = str(int(float(node[1])/1000))
		size = str( ((int(node[1])-10000) * (1000-200))/(18480000-10000) + 200)
		output.write(node[0]+','+node[0]+','+ size+'\n')

def generate_edges_file():
	output = open('edges.csv', 'w')
	output.write('Source,Target,Type'+'\n')
	for edge in edge_list:
		output.write(edge[0]+','+edge[1]+','+'Undirected'+'\n')

def generate_edges():
	for node in nodes_list:
		for related_node in node[2:]:
			if(len(related_node) > 0):
				edge_list.append([node[0], related_node])

# huehuehue too dumb for production. fix this. Time complexity too fucking high 
def remove_mutual_edges(): 
	for i,edge in enumerate(edge_list):
		for j,edge_temp in enumerate(edge_list[i+1:]):
			if(set(edge) == set(edge_temp)):
				print('edge: '+str(edge) + " / " +'edge_temp: '+str(edge_temp) + ' / '+str(i) + ' / ' +str(j))
				edge_list.pop(j)

# mix with remove_mutual_edges maybe?
def remove_self_loop_edges():
	for edge in edge_list:
		if(edge[0] == edge[1]):
			print('edge1: '+str(edge[0]) + " / " +'edge_2: '+str(edge[1]))
			edge_list.remove(edge)

generate_edges()
remove_self_loop_edges()
remove_mutual_edges()
generate_nodes_file()
generate_edges_file()