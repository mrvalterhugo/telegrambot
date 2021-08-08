while True:
    quantity_per_package = input("enter number: ")
    if not float(quantity_per_package):
        print(quantity_per_package, "is is not a number")
        continue
    print(quantity_per_package, "is a number")