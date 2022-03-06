import pygame
import numpy as np

# Mass class
class mass():
    instances = []
    # Initialise the object requiring the initial position, mass, and initial velocity of the mass
    def __init__(self, x, y, mass, init_vx, init_vy):
        self.__class__.instances.append(self)
        self.x = x
        self.y = y
        self.mass = mass
        self.colour = BLACK # Sets the colour of all masses
        self.radius = 20 # Sets the pixel radius that all masses will be drawn on the screen
        self.vx = init_vx
        self.vy = init_vy
        # Initialises a list of all springs that are attached to this mass, this will be appended any time a spring object is created that is connected to this mass
        self.springs = []
    
    # Draws the mass on the window when called
    def draw(self, win):
        x = self.x * SCALE + (WIDTH / 2)
        y = self.y * SCALE + (HEIGHT / 2)
        pygame.draw.circle(win, self.colour, (x, y), self.radius)
    
    # Main mass-side physics routine
    def update(self):
        # Sets current total forces on mass to 0
        fx_tot = 0
        fy_tot = 0
        # Loops over all springs attached to the mass, gets the force exerted by that spring.
        # Then determines wether the values it returns should be added or subtracted from the total.
        # The way fx, and fy are defined is that if the mass is object1 of the spring, the forces should be added to the total.
        # If the mass if object2 of the spring, then the forces returned should be subtracted from the total.
        for i in self.springs:
            fx, fy = i.force()
            if self is i.object1:
                fx_tot += fx
                fy_tot += fy
            # Initially second if was elif, this should catch the case where a spring is created attached at both ends to the same mass.
            # hopefully this will stop the mass from flying off
            if self is i.object2: 
                fx_tot -= fx
                fy_tot -= fy
        # Finds the instantanious acceleration of the mass
        ax = fx_tot / self.mass
        ay = fy_tot / self.mass
        # Calculates the new velocity of the mass
        self.vx += ax * TIMESTEP
        self.vy += ay * TIMESTEP
        # Calculates the new position of the mass
        self.x += self.vx * TIMESTEP
        self.y += self.vy * TIMESTEP



# Fixed point class
class wall():
    instances = []
    # Initialise the object requiring the initial position
    def __init__(self,x,y):
        self.__class__.instances.append(self)
        self.x = x
        self.y = y
        # Initialises a list of all springs that are attached to this fixed point, this will be appended any time a spring object is created that is connected to this point.
        # This list is not used for anything like the mass one is, other than so that the spring has something to append to in the event an object it is connected to is not a mass.
        self.springs = []
    
    # Draws the point on the window when called
    def draw(self, win):
        x = self.x * SCALE + (WIDTH / 2)
        y = self.y * SCALE + (HEIGHT / 2)
        pygame.draw.circle(win, BLUE, (x, y), 5) # Fixed points set to be BLUE, obviously can be changed



# Spring class
class spring():
    instances = []
    # Initialise the object requiring the two objects it connects, the stiffness of the spring, and its natural length
    def __init__(self, object_1, object_2, stiffness, nat_len):
        self.__class__.instances.append(self)
        self.object1 = object_1
        self.object2 = object_2
        self.x1 = object_1.x
        self.x2 = object_2.x
        self.y1 = object_1.y
        self.y2 = object_2.y
        self.stiffness = stiffness
        self.nat_len = nat_len
        self.colour = RED # Colour that springs will be drawn in
        # These two lines append the spring object to the list of springs in the objects to which it is connected
        object_1.springs.append(self)
        object_2.springs.append(self)

    # Draws the spring on the window when called
    def draw(self,win):
        x1, x2 = self.x1 * SCALE + (WIDTH / 2), self.x2 * SCALE + (WIDTH / 2)
        y1, y2 = self.y1 * SCALE + (HEIGHT / 2), self.y2 * SCALE + (HEIGHT / 2)
        pygame.draw.line(win, self.colour, (x1, y1), (x2, y2), 2)
    
    # Main spring-side physics routine
    # Called by all masses to which it is connected every iteration (potentially computationally wasteful when connecting two masses, but this is how I made it)
    def force(self):
        # Find the current length of the spring both in x, y, and total
        len_x = self.x2 - self.x1
        len_y = self.y2 - self.y1
        len_tot = np.sqrt(len_x**2 + len_y**2)
        # Find the difference between the current length of the spring and its natural length
        dlen = len_tot - self.nat_len
        # Use this length difference to determine the tension force of the spring
        force = dlen * self.stiffness
        # Split total force into its components while the orientation of the spring is still easily accessible
        fx = force * (len_x / len_tot)
        fy = force * (len_y / len_tot)
        # Return force components
        return fx, fy

    # Updates the position of the spring to match the masses which will have now potentially moved since this is called
    # after mass.update()
    # Not sure if the objects need to be passed as arguments. I didnt know if self.object1 = object_1 would update when the mass object's
    # position changed. If it does, then the following commented out lines would work requiring a change in the main loop to remove the input arguments.
    #def update(self):
    #    self.x1, self.x2 = self.object1.x, self.object2.x
    #    self.y1, self.y2 = self.object1.y, self.object2.y
    def update(self, object_1, object_2): 
        self.x1, self.x2 = object_1.x, object_2.x
        self.y1, self.y2 = object_1.y, object_2.y



pygame.init()

### Set some key values for the simulation
# Sets the zoom factor of the simulation
SCALE = 10
# Sets the rate at which the display will update (processor and monitor speed permitting)
FPS = 60
# Sets the discrete timestep that will be advanced every time the simulation progresses one iteration
TIMESTEP = 0.05   
# Sets the physical size of the pygame window
WIDTH, HEIGHT = 800, 800

# Create the pygame window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mass-Spring Simulation")

# Define colours in RGB format
WHITE = ((255, 255, 255))
BLACK = ((0, 0, 0))
RED = ((255, 0, 0))
BLUE = ((0, 0, 255))

# The main function that will be called
def main():
    # Allows the upcoming while loop to be exited
    run = True

    # Initialises the clock that limits the simulation speed to the defined FPS
    clock = pygame.time.Clock()

    # Masses defined
    mass1 = mass(-3, 0, 20, 0, 1) 
    mass2 = mass(-10, 0, 5, 0, 0)  

    # Fixed points defined
    wall1 = wall(0,0)

    # Springs defined
    spring1 = spring(mass1, wall1, 10, 10)
    spring2 = spring(mass1, mass2, 5, 8)
    spring3 = spring(mass2, wall1, 1, 10)

    # Makes the lists of all instances of the classes globally accessible
    masses = mass.instances
    walls = wall.instances
    springs = spring.instances

    # The time iterating loop in which the simulation computations are carried out
    while run:
        # Advances the clock the appropriate amount
        clock.tick(FPS)
        # Fills the window with white to cover rendered objects from previous iterations
        WIN.fill(WHITE)

        # Draws all of the fixed points onto the screen
        for i in walls:
            i.draw(WIN)

        # Loops through all of the masses in the list of masses
        for i in masses:
            # Performs computations finding the total force on the mass from all of the springs attached to it
            # Then calculates instantanious acceleration of the mass
            # Then updates the mass' position in accordance with the set TIMESTEP
            i.update()
            # Draws the mass in its new position
            i.draw(WIN)

        # Loops through all of the springs in the list of springs
        for i in springs:
            # Updates the endpoints of the spring since the objects it's connected to may now have moved
            i.update(i.object1,i.object2)
            # Draws the new spring
            i.draw(WIN)

        # Makes pygame stop running should the user close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        # Update the display with all the new draws
        pygame.display.update()

    # Quits pygame when the loop has been broken by the window being closed
    pygame.quit()


main()