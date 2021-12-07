# Movie Cinema Simulation - Average Waiting Time of Customers < 15 minutes

import simpy
import random
import time

#empty list to keep each customer's time before they can see the movies 
waiting_time = [] 

#Environment class which will be extended from object
class Cinema(object):

    #Set parameters that can be controlled and limit the processes by using simpy.Resource
    def __init__(self, this, num_staff, num_counters, num_customers):
        self.this = this
        self.staff = simpy.Resource(this, num_staff)
        self.counter = simpy.Resource(this, num_counters)
        self.customers = simpy.Resource(this, num_customers)

    #Using yield statement to return a generator object to the one who calls the function that contains yield. (retain state of the fx as customers wait)
    #Using timeout statement to model the time (triggered the event after certain amount of time has passed)
    #fx for customers deciding movie
    def decide_movie(self, customers):
        yield self.this.timeout(random.randint(1, 4))    ##Customers spend 1-3 minutes deciding a movie ticket on average.   

    #fx for customers purchasing ticket
    def purchase_ticket(self, customers):
        yield self.this.timeout(random.randint(1, 4))       #Customers spend 1-3 minutes purchasing a movie ticket on average. 

    #fx for customers buying foods / goodies
    def buy_things(self, customers):
        yield self.this.timeout(random.randint(1, 6))       #Customers spend 1-5 minutes buying foods / goodies on average.

    #fx for staff checking ticket
    def check_ticket(self, customers):
        yield self.this.timeout(random.uniform(5 / 60, 10 / 60))        #Staff spend 5-10 seconds checking ticket on average. 


#fx for customers in order to watch the movie
#Customers will request an act to finish each of these functions called from the class. (the customer needs to wait until that act becomes available if all of the act are occupied)
def watch_movie(this, customers, cinema):

    #customers arrive at Cinema
    arrival_time = this.now

    #start with decide movie
    yield this.process(cinema.decide_movie(customers))

    #check first if this act available or not; if yes, fx below will yield this act. if not, customers need to wait.
    with cinema.staff.request() as request:
        yield request
        yield this.process(cinema.purchase_ticket(customers))
    
    #customers have option to buy food / goodies
    if random.choice([True, False]):            #customers will either buy something from the counter or proceed to the cinema hall
        with cinema.counter.request() as request:
            yield request
            yield this.process(cinema.buy_things(customers))

    #last step is to get the ticket checked
    with cinema.staff.request() as request:
        yield request
        yield this.process(cinema.check_ticket(customers))

    #watch movie (process completed)
    #calculate waiting time
    
    waiting_time.append(this.now - arrival_time)

#pass the inputs to the function to run the simulation
def run_cinema(this, num_staff, num_counters, num_customers):
    cinema = Cinema(this, num_staff, num_counters, num_customers)
    
    for customers in range(num_customers):          #pass the customer who are in queue line before simulation started to go through all the processes
        this.process(watch_movie(this, customers, cinema))
    
    while True:
        yield this.timeout(random.uniform(10 / 60, 20 / 60))        #set customers arrive at cinema every 10-20 seconds on average
        this.process(watch_movie(this, customers, cinema))

#fx to calculate average customers' waiting time    
def calculate_waiting_time(waiting_time):
    for (num,cus) in enumerate(waiting_time):       #display all the customers' waiting time
        time.sleep(0.1)
        print('customer', num+1, ':', "%.2f" % cus, 'minutes')    

    avg_wt = sum(waiting_time) / len(waiting_time)
    minutes, frac_minutes = divmod(avg_wt, 1)       #covert avg_wt into minute and second format
    seconds = frac_minutes * 60
    return round(minutes), round(seconds)

#fx to get input from users instead of set the parameters in the code
def get_user_input():
    while True:
        try:
            num_staff = int(input("Total staff: "))
            num_counters = int(input("Total counters: "))
            num_customers = int(input("Total customers in the queue: "))
            simtime = int(input("Simulation duration in minutes: "))
            break;     
        except ValueError:
            print("Try again. Please provide number > 0")          #repeat if the input is not interger or less than 1
        continue
    inputs = [num_staff, num_counters, num_customers, simtime]
    return inputs

#main fx
def main():
    random.seed(30)
    num_staff, num_counters, num_customers, simtime = get_user_input()

    #simulation starts here
    this = simpy.Environment()
    this.process(run_cinema(this, num_staff, num_counters, num_customers))     #run all the processes at cinema
    this.run(until=simtime)

    print('---------------------------------------------', 
        '\nStimulation is running.....\n',)

    #output of this simulation
    mins, secs = calculate_waiting_time(waiting_time)
    print('---------------------------------------------',
        '\nThere are', len(waiting_time), 'customers during', simtime, 'minutes simulation',
        f"\nThe average waiting time for customer is {mins} minutes and {secs} seconds.",
    )

if __name__ == '__main__':
    main()












"""def run_cinema(this, num_staff, num_counters, num_customers, theater): 
    cinema = Cinema(this, num_staff, num_counters, num_customers)
    
    for customers in range(num_customers):          #pass the customer who are in queue line to go through all the processes
        movie = random.choice(theater.movies)
        num_tickets = random.randint(1, 6)
        if theater.available[movie]:
            this.process(Customer(this, movie, num_tickets, theater))
            this.process(watch_movie(this, customers, cinema))
        else:
            random.choice([True, False])
            if random.choice == True:
                movie = random.choice(theater.movies)
                if theater.available[movie]:
                    this.process(Customer(this, movie, num_tickets, theater))
                    this.process(watch_movie(this, customers, cinema))
            else:
                break
    
    while True:
        yield this.timeout(random.uniform(10 / 60, 20 / 60))        #set customers arrive at cinema every 10-20 seconds
        movie = random.choice(theater.movies)
        print(movie)
        num_tickets = random.randint(1, 6)
        if theater.available[movie]:
            this.process(Customer(this, movie, num_tickets, theater))      
            this.process(watch_movie(this, customers, cinema))     #pass customers that just arrived to go through all the processes
        else:
            random.choice([True, False])
            if random.choice == True:
                movie = random.choice(theater.movies)
                if theater.available[movie]:
                    this.process(Customer(this, movie, num_tickets, theater))
                    this.process(watch_movie(this, customers, cinema))
            else:
                break
    return movie """