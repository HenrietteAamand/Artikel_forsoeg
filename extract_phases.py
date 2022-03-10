class Extract_phases_class():
    def __init__(self, timelimits: list) -> None:
        self.timelimits = timelimits

    def extract(self, testperson_nr: int):
        where_to_start = (testperson_nr-1)*4 
        pass