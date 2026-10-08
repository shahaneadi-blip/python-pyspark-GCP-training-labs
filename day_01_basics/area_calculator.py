import math


def main():
    shape = input("Shape (circle/rectangle/triangle): ").strip().lower()
    if shape == "circle":
        radius = float(input("Radius: "))
        area = math.pi * radius**2
    elif shape == "rectangle":
        length = float(input("Length: "))
        width = float(input("Width: "))
        area = length * width
    elif shape == "triangle":
        base = float(input("Base: "))
        height = float(input("Height: "))
        area = base * height / 2
    else:
        print("Unsupported shape.")
        return
    print(f"Area: {area:.2f}")


if __name__ == "__main__":
    main()
