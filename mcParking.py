'''
MC Parking Stockholm - A script that generate a GPX file with all
motorcycle parking spots in Stockholm.
Copyright (C) 2025 Anders Markoff

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

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
