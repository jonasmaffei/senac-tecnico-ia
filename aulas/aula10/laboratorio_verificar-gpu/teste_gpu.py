import os

print("=== TESTE DE GPU NO CONTAINER ===")
print()

print("Dispositivo /dev/dxg:")

if os.path.exists("/dev/dxg"):
    print("GPU-PV disponível dentro do container!")
    print("✓ /dev/dxg encontrado")
else:
    print("✗ /dev/dxg NÃO encontrado")