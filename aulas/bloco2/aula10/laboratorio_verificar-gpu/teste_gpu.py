import os

print("=== TESTE DE GPU NO CONTAINER ===")
print()

print("Dispositivo /dev/dxg:")

if os.path.exists("/dev/dxg"):
    print("GPU-PV disponivel dentro do container!")
    print("OK /dev/dxg encontrado")
else:
    print("X /dev/dxg NAO encontrado")