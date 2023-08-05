from shopping.cars_enum import CarsEnum
import cars.sample as sample


class CarList:

    def list_brand_models(self, brand):
        if brand == CarsEnum.nissan.name:
            return sample.nissan_car.get_models()
        elif brand == CarsEnum.fiat.name:
            return sample.fiat_car.get_models()
        else:
            print("No such brand")

    def main(self):
        pass


if __name__ == "__main__":
    car = input("Either nissan or fiat?")
    CarList().list_brand_models(car)
