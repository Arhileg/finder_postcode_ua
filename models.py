class Address:
    def __init__(self, adress='') -> dict:
        self.__city =''
        self.__street = ''
        self.__streettype = ''
        self.__building = ''
        self.__room = ''
        if adress:
            mass = adress.split(',')
            if len(mass)==3:
                mass.append('')
            self.city = mass[0]
            self.street = mass[1]
            self.building = mass[2]
            self.room = mass[3]
            
    def __str__(self):
        return f'city:"{self.city}" | streettype:"{self.streettype}" | street:"{self.street}" | building:"{self.building}" | room:"{self.room}"'
    
    def __repr__(self) -> str:
        return f'city:"{self.city}" | streettype:"{self.streettype}" | street:"{self.street}" | building:"{self.building}" | room:"{self.room}"'
    
    
    @property
    def city(self) -> str:
        return self.__city
    
    @city.setter
    def city(self, city:str) -> str:
        self.__city = self.parse_value(city, ['м. '])
    
    @property
    def street(self) -> str:
        return self.__street
    
    @street.setter
    def street(self, street:str) -> str:
        street = street.strip().lower()
        self.__street = self.parse_value(street, ['вул. ', 'бул. ', 'пр-т ', 'пр. '])
        if len(street)>len(self.__street): 
            res=''.join(street.split(self.__street))             #get diff
        else: 
            res=''.join(self.__street.split(street))             #get diff
        self.streettype = res
    
    @property
    def streettype(self) -> str:
        return self.__streettype
    
    @streettype.setter
    def streettype(self, streettype:str) -> str:
        dict_street_types = {'вул. ': 'вулиця', 'бул. ': 'бульвар', 'пр-т ': 'проспект', 'пр. ': 'провулок'}
        self.__streettype = dict_street_types.get(streettype, 'error')
    
    @property
    def building(self) -> str:
        return self.__building
    
    @building.setter
    def building(self, building:str) -> str:
        self.__building = self.parse_value(building, ['буд.', 'б.'])
        if r'/' in self.__building:
            # import ipdb; ipdb.set_trace()
            
            mass = self.__building.split('/')
            self.__building = mass[0]
            self.__room = mass[1]
    
    @property
    def room(self) -> str:
        return self.__room
    
    @room.setter
    def room(self, room:str) -> str:
        if not self.__room:
            self.__room = self.parse_value(room, ['кв.'])
    
    def parse_value(self, value:str, temple:list) -> str:
        for t in temple:
            if t in value:
                return value.replace(t, '').strip().lower()
        return value.lower()