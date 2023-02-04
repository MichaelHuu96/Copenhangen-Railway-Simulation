import os, sys, enum
from Algorithms import Algorithms
from datetime import timedelta
from matplotlib.markers import MarkerStyle

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(PROJECT_ROOT)
dirname = os.path.dirname(__file__)

class CarriersStates(enum.Enum):
    IDLE = 1
    LOADING = 2
    MOVING = 3
    STOPPING = 4
    UNUSED = 0

class Carrier:

    # Max amount of passengers on Carrier
    _maxPassengers = 5
    # Max speed of Carrier in m/s
    _maxSpeed = 22.22
    # Acceleration of carrier
    _maxAcceleration = 1.5
    _maxDeaceleration = -1.4
    # Time for Passengers to load in
    _loadingDuration = 1

    # chain strategy
    _safety_delay = 1

    # Initialisation of the carrier
    def __init__(self, uid, atStation, tickTime, stations, connections, env):
        # carriers identifier:
        self._uid = uid
        self._tickTime = tickTime
        # Algorithms:
        self._algorithms = Algorithms(connections, stations)
        # connections to update positions:
        self._connections = connections
        self._currentConnection = None
        # carrier environment:
        self._env = env
        # Passengers on the carrier
        self._passengers = []
        # Time when last trip started
        self._departureTime = 0
        # Speed of carrier
        self._speed = 0
        # Path the train should take
        self._path = []
        self._destination = ""
        self._distanceToDestination = 0
        self._distanceLeftDestination = 0
        # current acceleration
        self._acceleration = 0
        # '' when not at a station otherwise Station
        self._stations = stations
        self._atStation = atStation
        # Is the carrier moving
        self._isMoving = False
        # Is the carrier decelerating
        self._decelerating = False
        # 0 when at a station otherwise station
        self._movingTo = ""
        self._movingFrom = ""
        # Different distances
        self._distanceToStation = 0
        self._distanceMovedStation = 0
        self._breakingDistance = 0
        self.state: CarriersStates = CarriersStates.UNUSED
        self._mass = 1300*175
        self.total_energy = 0
        self.total_distance = 0
        self.CHAIN_STARTEGY = True
    
    def setupPlot(self, ax):
        self.dot, = ax.plot(0,0)

    def get_map_position(self, station_a, station_b, moved_distance:float, total_dictance:float) -> (float, float):
        l = moved_distance/total_dictance
        return l*station_b.x+(1-l)*station_a.x, l*station_b.y+(1-l)*station_a.y
        
    def updatePlotPosition(self, tick_lenght):
        while True:
            if self._isMoving:
                newx, newy = self.get_map_position(
                            self._stations[self._movingFrom], 
                            self._stations[self._movingTo], 
                            self._distanceMovedStation, 
                            self._distanceToStation)
                self.dot.set_xdata(newx)
                self.dot.set_ydata(newy)
                if self._passengers:
                    self.dot._marker = MarkerStyle('o', fillstyle='full')
                else:
                    self.dot._marker = MarkerStyle('o',fillstyle='none')
            else:
                self.dot.set_xdata(self._atStation.x)
                self.dot.set_ydata(self._atStation.y)
                self.dot._marker = MarkerStyle('.')
            yield self._env.timeout(tick_lenght)
        

    def deploy(self):
        # loop of the process, never stops
        while True:
            yield self._env.process(self._atStation.enqueue(self))


    def idle(self, loading):
        self.state = CarriersStates.IDLE
        with loading.request() as request:
            yield request
            yield self._env.process(self._atStation.getPassengers(self, self._maxPassengers))
            # load passengers
            self.state = CarriersStates.LOADING
            yield self._env.timeout(self._loadingDuration)

        yield self._env.process(self.departure())
    
    def chain_idle(self, loading):
        self.state = CarriersStates.IDLE
        with loading.request() as request:
            yield request
            if self._atStation.request_empty_carriers:
                self._atStation.sendEmptyCarrier(self)
                yield self._env.timeout(self._safety_delay)
            else:
                yield self._env.process(self._atStation.getPassengers(self, self._maxPassengers))
                # load passengers
                self.state = CarriersStates.LOADING
                yield self._env.timeout(self._loadingDuration)
        yield self._env.process(self.departure())
    
    def departure(self):
        # remove full path
        # compute path from algorithms
        shortestPath = self._algorithms.get_path(self._atStation.name, self._destination)
        self._path = shortestPath.nodes
        self._distanceToDestination = shortestPath.total_cost
        self._distanceLeftDestination = self._distanceToDestination
        self._movingFrom = self._path.pop(0)
        self._movingTo = self._path.pop(0)
        self._currentConnection = self._connections[self._movingFrom][
                self._movingTo
            ]
        self._distanceToStation = self._currentConnection.distance
        yield self._env.process(self.moving())

    def moving(self):
        self.state = CarriersStates.MOVING
        self._isMoving = True
        self._acceleration = self._maxAcceleration
        self._departureTime = self._env.now
        while self._isMoving:
            yield self._env.process(self.updateNewPosition())

    def updateConnection(self):
        self._movingFrom = self._movingTo
        self._movingTo = self._path.pop(0)
        self._currentConnection = self._connections[self._movingFrom][
                self._movingTo
            ]

    def updateAcceleration(self):
        if self._distanceLeftDestination < self._breakingDistance:
            self._acceleration = self._maxDeaceleration
        elif self._speed >= self._maxSpeed:
            self._acceleration = 0
        else:
            self._acceleration = self._maxAcceleration

    def updateSpeed(self):
        # speed = speed0 + a * t
        self._speed = max(min(self._speed + self._acceleration * self._tickTime, self._maxSpeed),0)

    def updateDistance(self):
        # distance = speed0 * t + 0.5 * acceleration t^2
        distance_moved = self._speed * self._tickTime + 0.5 * self._acceleration * self._tickTime**2
        self._distanceMovedStation += distance_moved
        self._distanceLeftDestination -= distance_moved
        self.total_distance += distance_moved
        if self._acceleration > 0:
            self.total_energy += self._acceleration*distance_moved*self._mass

    def updateNewPosition(self):
        yield self._env.timeout(self._tickTime)
        # COMPUTE DISTANCES
        # break_distance = speed^2/2acceleration
        self._breakingDistance = abs(self._speed**2 / (
            2 * self._maxDeaceleration
        ))
        self.updateAcceleration()
        self.updateSpeed()
        self.updateDistance()
        # CHECK IF REACHED
        # reached next station:
        while self._distanceMovedStation > self._distanceToStation:
            # reached destination:
            if not self._path:
                self._atStation = self._currentConnection.station_end
                self._isMoving = False
                break
            self.updateConnection()
            self._distanceToStation = self._currentConnection.distance
            self._distanceMovedStation -= self._distanceToStation
    
    def stop_in(self, station):
        # to stop the last process
        # soft braking system
        self.state = CarriersStates.STOPPING
        self._acceleration = 0
        self._distanceToDestination = 0
        self._distanceLeftDestination = 0
        self._distanceMovedStation = 0
        self._movingTo = ""
        self._movingFrom = ""
        self._distanceMoved = 0
        self._atStation = station
        for p in self._passengers:
            p.arrived(self._env.simulation_start + timedelta(seconds=self._env.now))
        self._passengers = []
        if self.CHAIN_STARTEGY:
            yield self._env.process(self.chain_idle(self._atStation.loader))
        else:
            yield self._env.process(self.idle(self._atStation.loader))

    def printDistance(self,file,tick):
        with open(os.path.join(dirname, "../others/plotters/data/"+file), 'w') as f:
            original_stdout = sys.stdout
            sys.stdout = f # Change the standard output to the file we created.
            while True:
                print(f'{self.total_distance:.3f}')
                yield self._env.timeout(tick)
            sys.stdout = original_stdout # Reset the standard output to its original value
    
    def printKiniticEnergy(self,file,tick):
        with open(os.path.join(dirname, "../others/plotters/data/"+file), 'w') as f:
            original_stdout = sys.stdout
            sys.stdout = f # Change the standard output to the file we created.
            while True:
                print(f'{self.total_energy:.3f}')
                yield self._env.timeout(tick)
            sys.stdout = original_stdout # Reset the standard output to its original value

    def printSpeed(self,tick):
        while True:
            print(f'{self._speed:.3f}')
            yield self._env.timeout(tick)

    def printEvents(self):
        preState = CarriersStates.UNUSED
        while True:
            if self.state != preState:
                preState = self.state
                print(f'{self._env.now}: carrier [{self._uid}] {self.state.name},')
                if self.state == CarriersStates.MOVING:
                    print(f'\t moving from {self._movingFrom} to {self._movingTo},')
                    print(f'\t with {[ x for x in self._passengers]}')
                elif self.state == CarriersStates.IDLE:
                    print(f'\t in {self._atStation.name}')
                elif self.state == CarriersStates.LOADING:
                    print(f'\t to {self._destination}')
                elif self.state == CarriersStates.STOPPING:
                    print(f'\t in {self._atStation.name}')
                print()
            yield self._env.timeout(1)

    def printTime(self, tick):
        while True:
            print(f't:{self._env.now}')
            yield self._env.timeout(tick)

    def getUID(self):
        return self._uid
