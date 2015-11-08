# Input Value - current domain for which mrv is being checked, node selected, color assigned
# Returns - New modified domain
def modify_domain(current_domain, node_idx, color_assigned):
    new_domain = [list(x) for x in current_domain]
    new_domain[node_idx] = []
    for i in range(len(GRAPH)):
        if GRAPH[node_idx][i] == 1:
            if color_assigned in new_domain[i]:
                new_domain[i].remove(color_assigned)
    return new_domain


# Input Value - current domain for which mrv is being checked
# Returns - the node index having minimum remaining values
def min_remaining_value(current_domain):
    mrv = 2147483647
    mrv_node_idx = -1
    for i in range(len(current_domain)):
        if node_colors[i] == -1:
            if len(current_domain[i]) < mrv:
                mrv = len(current_domain[i])
                mrv_node_idx = i
            elif len(current_domain[i]) == mrv:
                if sum(GRAPH[mrv_node_idx]) < sum(GRAPH[i]):
                    mrv = len(current_domain[i])
                    mrv_node_idx = i
    return mrv_node_idx, mrv


# Input Value - node selected
# Returns - color giving maximum mrv
def least_constraining_value(node_idx):
    if node_colors.count(-1) == 1:
        return domain[-1][node_idx][0]
    else:
        mrv_values = []
        for x in domain[-1][node_idx]:
            new_domain = modify_domain(domain[-1], node_idx, x)
            node_colors[node_idx] = x
            temp_node, temp_mrv = min_remaining_value(new_domain)
            node_colors[node_idx] = -1
            mrv_values.append(temp_mrv)
        max_mrv = max(mrv_values)
        max_mrv_giving_color_idx = mrv_values.index(max_mrv)
        return domain[-1][node_idx][max_mrv_giving_color_idx]


# Input Value - node selected, color assigned
# Modifies the global variable state to make them consistent
def assign_color(node_idx, chosen_color):
    new_domain = modify_domain(domain[-1], node_idx, chosen_color)
    domain[-1].append(list(node_colors))
    domain[-1].append(node_idx)
    domain[-1].append(chosen_color)
    domain.append(new_domain)
    node_colors[node_idx] = chosen_color
    
    
# Returns - If the domain of a node which is not colored yet has already exhausted
def domainExhausted():
    for i in range(len(GRAPH)):
        if (domain[-1][i] == []) and (node_colors[i] == -1):
            return True
    return False
        

#
# Global Variables and main functions
#
    

# Adjacency matrix of the graph
# Graph 1: Colorability 3
"""
GRAPH = [[0, 1, 0, 0, 0, 1, 0],
        [1, 0, 1, 0, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 1, 0],
        [1, 1, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]]
"""
"""
# Graph 2: Colorability 3
GRAPH = [[0, 1, 1, 0, 1, 1],
        [1, 0, 1, 1, 0, 1],
        [1, 1, 0, 1, 1, 0],
        [0, 1, 1, 0, 1, 1],
        [1, 0, 1, 1, 0, 1],
        [1, 1, 0, 1, 1, 0]]
"""
# Graph 3: Colorability 3
GRAPH = [[0, 1, 0, 0, 1, 1, 0, 0, 0, 0],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0, 0, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
        [1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 1, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
        [0, 0, 0, 1, 0, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 1, 1, 0, 0]]
"""
# Graph 4: Colorability 3
GRAPH = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
"""


# Global Variable Initialization
num_colors = raw_input('Enter the number of colors available')
num_colors = int(num_colors)
domain = [[range(1, num_colors + 1) for i in range(len(GRAPH))]]
# domain = [[[2, 3], [2, 3], [2, 3], [2, 3], [2, 3], [], [1, 2, 3]]]
node_colors = [-1 for i in range(len(GRAPH))]


# Main Code
while -1 in node_colors:
    node_idx, mrv = min_remaining_value(domain[-1])
    chosen_color = least_constraining_value(node_idx)
    assign_color(node_idx, chosen_color)
    if domainExhausted():
        print 'Backtrack'
        domain.pop(-1)
        flag = True
        while flag:
            domain.pop(-1)
            if len(domain) == 0:
                flag = False
            elif len(domain[-1][domain[-1][-2]]) > 1:
                flag = False
        if len(domain) != 0:
            if len(domain[-1][domain[-1][-2]]) > 1:
                domain[-1][domain[-1][-2]].remove(domain[-1][-1])
                node_colors = list(domain[-1][-3])
                domain[-1].pop(-1)
                domain[-1].pop(-1)
                domain[-1].pop(-1)
        else:
            print "The graph can't be colored with", num_colors, "colors." 
            break
    
    
if -1 not in node_colors:
    print 'Colors assigned to the nodes are:', node_colors
    print 'Graph is', max(node_colors), 'colorable'
