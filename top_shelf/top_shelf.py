class Bottle(object):
    def __init__(self, name, distillery, price, age = "N/A"):
        self.name = str(name).title()
        self.distillery = distillery.title() if type(distillery) == str else -1
        try:
            self.price = "{:.2f}".format(float(price))
        except ValueError:
            self.price = -1
        self.age = str(age) if type(age) == int or age == "N/A" else -1
