from collections import namedtuple

from .within_context import within_contexts

StateNode = namedtuple("StateNode", "state_id, physical_id")
Link = namedtuple("Link", "source, target, weight")
Tree = namedtuple("Tree", "path, flow, state_id, physical_id")


def read_net(filename, integer_weights=False, include_states=True):
    states = []
    links = []

    weight_type = int if integer_weights else float

    with open(filename, "r") as f:
        lines = (line for line in f if not line.startswith("#"))

        for context, line in within_contexts(("*states", "*links"), lines):
            if include_states and context == "*states":
                state_id, physical_id, *_ = line.split()
                states.append(StateNode(int(state_id), int(physical_id)))
            elif context == "*links":
                source, target, weight = line.split()
                links.append(Link(int(source), int(target), weight_type(weight)))

    return states, links


def read_tree(filename):
    tree = []

    with open(filename, "r") as f:
        for line in f:
            if line.startswith("#"):
                continue

            path, flow, *_, state_id, physical_id = line.split()
            path = tuple(map(int, path.split(":")))
            tree.append(Tree(path, float(flow), int(state_id), int(physical_id)))

    return tree


if __name__ == "__main__":
    net = read_net("test/training_seed0_order2_0.net")
    print(net[0])
    print(net[1])
    tree = read_tree("test/training_seed0_order2_0_states.tree")
    print(tree)
