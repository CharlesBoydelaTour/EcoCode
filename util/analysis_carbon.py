from codecarbon import OfflineEmissionsTracker

def carbon_tracker(func, country="FRA", *args):
    tracker = OfflineEmissionsTracker(country_iso_code=country)
    tracker.start()
    func(*args)
    tracker.stop()
    
if __name__ == "__main__":
    def is_pair(n): 
        if n % 2 == 0:  
            return True 
        else : 
            return False
    @carbon_tracker
    def main(n=100000000):
        for i in range(n):
            is_pair(i)
