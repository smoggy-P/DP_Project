from mimetypes import init


class Battery(object):
    """Battery dynamics

    Attributes:
        cap (float): Maximum capacity of battery(kWh)
        alpha_c (float): Charging efficiency
        alpha_d (float): Discharging efficiency
        umax_c (float): Maximum charging rate(kW)
        umax_d (float): Maximum discharging rate(kW)
    """
    def __init__(self):
        self.c = None
        self.cap = 7.0
        self.alpha_c = 0.96
        self.alpha_d = 0.87
        self.umax_c = 4.0
        self.umax_d = 5.0
    
    def step(self, u, dt):
        """step dynamics for battery

        Args:
            u (float): charge rate
            dt (float): time

        Returns:
            float: amount of charge to be moved to/from(+/-) 
                   total amount of charge provided by power supplier(kW)
        """

        # clip the charge rate
        u = max(min(u, self.umax_c), -self.umax_d)

        # when charge to battery
        if u >= 0:
            c_hat = min(self.c + self.alpha_c * u * dt, self.cap)
            result = (c_hat - self.c)/self.alpha_c/dt 
        # when charge from battery
        else:
            c_hat = max(self.c + u * dt / self.alpha_d, 0)
            result = (c_hat - self.c)*self.alpha_d/dt
        return result
    
    def reset(self, init_c):
        self.c = init_c
        

class Demand(object):
    """Dynamics for demand

    Args:
        object (_type_): _description_
    """
    def __init__(self):
        self.w = None
    
    def step(self):
        self.w = self.w
    
    def reset(self, init_w):
        self.w = init_w


class Plant(object):
    """Dynamics for entire model

    Args:
        dt (float): time
        x (float): peak power
    """

    def __init__(self):
        self.battery = Battery()
        self.demand = Demand()
        self.dt = 1/60
        self.x = 0
    
    def step(self, u):
        self.demand.step()
        self.battery.step(u, self.dt)
        self.x = max(self.x, self.demand.w + u)
        return [self.x, self.demand.w, self.battery.c]

    def reset(self):
        self.battery.reset(0)
        self.demand.reset(0)
        self.x = 0
        return [self.x, self.demand.w, self.battery.c]
        
        
