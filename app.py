import random

def generate_phrasal_verb():
    verbs = ["give", "take", "put", "get", "make", "look", "come", "go", "turn", "run"]
    particles = ["up", "down", "in", "out", "on", "off", "away", "back", "over", "through"]
    
    verb = random.choice(verbs)
    particle = random.choice(particles)
    
    return "{0} {1}".format(verb, particle)

# Example usage
random_phrasal_verb = generate_phrasal_verb()
print("Random phrasal verb: {}".format(random_phrasal_verb))
