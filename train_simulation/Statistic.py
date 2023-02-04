class Statistic:

    def __init__(self):
        self.data = {'passengers': 0}

    def update_ride_end(self, person):
        if person.start_station in self.data.keys():
            if person.destination in self.data[str(person.start_station)].keys():
                self.data[str(person.start_station)][str(person.destination)].append(person.travel_time)
            else:
                self.data[str(person.start_station)][str(person.destination)]= [person.travel_time]
        else:
            self.data[str(person.start_station)] = {str(person.destination): [person.travel_time]}
            print
        self.data['passengers'] = self.data['passengers'] + 1
        print(self.data)
