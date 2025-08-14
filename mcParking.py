class mcParking:
    def __init__(self, address, lat, lon, rate=None, servicetime=None, description=None, symbol='Parking'):
        self.address = address
        self.lat = lat
        self.lon = lon
        self.rate = rate
        self.servicetime = servicetime
        self.description = description
        self.symbol = symbol

    def __repr__(self):
        return f"mcParkering(address={self.address}, lat={self.lat}, lon={self.lon}, rate={self.rate}, servicetime={self.servicetime}, description={self.description}, symbol={self.symbol})"
