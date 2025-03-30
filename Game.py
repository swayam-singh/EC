import pygame
import random
from pygame.sprite import Sprite
from pygame import image

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Evolving Fighting Game AI")

# Colors
WHITE = (255, 255, 255)

# Load character sprites from an asset library
player_img = image.load("C:/Users/Singh/Desktop/EC/assets/player_idle.png")
ai_img = image.load("C:/Users/Singh/Desktop/EC/assets/ai_idle.png")

# Define possible moves
MOVES = ["Punch", "Kick", "Block"]

# Fitness function - AI wins get higher scores
def fitness(ai_move, player_move):
    if ai_move == player_move:
        return 0  # Draw
    elif (ai_move == "Punch" and player_move == "Kick") or \
         (ai_move == "Kick" and player_move == "Block") or \
         (ai_move == "Block" and player_move == "Punch"):
        return 1  # AI wins
    return -1  # AI loses

# Generate initial population of strategies
def generate_population(size=10):
    return [random.choices(MOVES, k=3) for _ in range(size)]

# Select best strategies based on fitness
def selection(population, player_move):
    scored = [(strategy, sum(fitness(m, player_move) for m in strategy)) for strategy in population]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [s[0] for s in scored[:5]]  # Keep top 5

# Crossover - mix two strategies
def crossover(parent1, parent2):
    point = random.randint(1, 2)
    return parent1[:point] + parent2[point:]

# Mutation - randomly change a move
def mutate(strategy):
    if random.random() < 0.3:  # 30% chance of mutation
        idx = random.randint(0, 2)
        strategy[idx] = random.choice(MOVES)
    return strategy

# Evolve population
def evolve(population, player_move):
    selected = selection(population, player_move)
    next_gen = selected[:]
    while len(next_gen) < len(population):
        parent1, parent2 = random.sample(selected, 2)
        child = crossover(parent1, parent2)
        next_gen.append(mutate(child))
    return next_gen

# Main game loop
def game_loop():
    clock = pygame.time.Clock()
    population = generate_population()
    running = True
    player_move = None
    ai_move = None
    result = ""

    while running:
        screen.fill(WHITE)
        screen.blit(player_img, (150, 200))
        screen.blit(ai_img, (550, 200))
        
        font = pygame.font.Font(None, 36)
        text = font.render("Choose Your Move: Punch, Kick, Block", True, (0, 0, 0))
        screen.blit(text, (200, 50))
        
        if player_move:
            player_text = font.render(f"Player: {player_move}", True, (0, 0, 0))
            ai_text = font.render(f"AI: {ai_move}", True, (0, 0, 0))
            result_text = font.render(f"Result: {result}", True, (0, 0, 0))
            screen.blit(player_text, (200, 350))
            screen.blit(ai_text, (500, 350))
            screen.blit(result_text, (350, 400))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    player_move = "Punch"
                elif event.key == pygame.K_k:
                    player_move = "Kick"
                elif event.key == pygame.K_b:
                    player_move = "Block"
                
                if player_move:
                    ai_move = random.choice(random.choice(population))
                    result = "Win" if fitness(ai_move, player_move) == 1 else "Lose" if fitness(ai_move, player_move) == -1 else "Draw"
                    population = evolve(population, player_move)
        
        clock.tick(30)
    
    pygame.quit()

if __name__ == "__main__":
    game_loop()
