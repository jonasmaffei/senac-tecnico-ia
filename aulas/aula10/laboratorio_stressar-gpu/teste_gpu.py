import ctypes
import sys
import time


print("=" * 60)
print("GPU STRESS TEST - AMD RX 550X")
print("=" * 60)


# ------------------------------------------------------------
# Carrega Vulkan
# ------------------------------------------------------------

try:
    vulkan = ctypes.CDLL("libvulkan.so.1")
    print("[OK] Vulkan loader carregado")
except Exception as e:
    print("[ERRO] Não foi possível carregar Vulkan:")
    print(e)
    sys.exit(1)


# ------------------------------------------------------------
# Verificação usando vulkaninfo
# ------------------------------------------------------------

import subprocess

print()
print("=== DISPOSITIVO VULKAN ===")

try:
    result = subprocess.run(
        [
            "vulkaninfo",
            "--summary"
        ],
        capture_output=True,
        text=True
    )

    output = result.stdout + result.stderr

    interesting = []

    for line in output.splitlines():
        if any(
            x in line
            for x in [
                "deviceName",
                "deviceType",
                "driverName",
                "driverID",
                "driverInfo"
            ]
        ):
            interesting.append(line)

    for line in interesting:
        print(line)

except Exception as e:
    print("[ERRO] vulkaninfo:", e)


# ------------------------------------------------------------
# Importa binding Python Vulkan
# ------------------------------------------------------------

try:
    import vulkan as vk

    print()
    print("[OK] Python Vulkan carregado")

except Exception as e:
    print()
    print("[ERRO] Python Vulkan:")
    print(e)
    sys.exit(1)


# ------------------------------------------------------------
# Inicializa Vulkan
# ------------------------------------------------------------

print()
print("=== INICIALIZANDO VULKAN ===")

app_info = vk.VkApplicationInfo(
    sType=vk.VK_STRUCTURE_TYPE_APPLICATION_INFO,
    pApplicationName="GPU Stress Test",
    applicationVersion=1,
    pEngineName="StressEngine",
    engineVersion=1,
    apiVersion=vk.VK_API_VERSION_1_0,
)

create_info = vk.VkInstanceCreateInfo(
    sType=vk.VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO,
    pApplicationInfo=app_info,
)

try:
    instance = vk.vkCreateInstance(create_info, None)

    print("[OK] Vulkan instance criada")

except Exception as e:
    print("[ERRO] Não foi possível criar Vulkan instance:")
    print(e)
    sys.exit(1)


# ------------------------------------------------------------
# GPUs
# ------------------------------------------------------------

try:
    devices = vk.vkEnumeratePhysicalDevices(instance)

    print()
    print("GPUs encontradas:", len(devices))

    for i, device in enumerate(devices):

        props = vk.vkGetPhysicalDeviceProperties(device)

        name = props.deviceName

        print()
        print(f"GPU {i}: {name}")

        print(
            "Tipo:",
            props.deviceType
        )

        print(
            "API:",
            vk.VK_VERSION_MAJOR(props.apiVersion),
            ".",
            vk.VK_VERSION_MINOR(props.apiVersion),
            ".",
            vk.VK_VERSION_PATCH(props.apiVersion)
        )

except Exception as e:
    print("[ERRO] Enumerando GPUs:")
    print(e)
    sys.exit(1)


# ------------------------------------------------------------
# Escolhe GPU discreta
# ------------------------------------------------------------

selected = None
selected_name = None

for device in devices:

    props = vk.vkGetPhysicalDeviceProperties(device)

    name = props.deviceName

    if "RX 550X" in name or "Radeon" in name:
        selected = device
        selected_name = name
        break


if selected is None:

    print()
    print("[ERRO] RX 550X/Radeon não encontrada.")

    print()
    print("GPUs disponíveis:")

    for device in devices:
        props = vk.vkGetPhysicalDeviceProperties(device)
        print(" -", props.deviceName)

    vk.vkDestroyInstance(instance, None)

    sys.exit(2)


print()
print("=" * 60)
print("GPU SELECIONADA:")
print(selected_name)
print("=" * 60)


# ------------------------------------------------------------
# Queue families
# ------------------------------------------------------------

queue_families = vk.vkGetPhysicalDeviceQueueFamilyProperties(
    selected
)

compute_family = None

for index, family in enumerate(queue_families):

    if family.queueFlags & vk.VK_QUEUE_COMPUTE_BIT:

        compute_family = index

        print(
            f"Queue de compute encontrada: {index}"
        )

        break


if compute_family is None:

    print("[ERRO] GPU não possui queue de compute.")

    vk.vkDestroyInstance(instance, None)

    sys.exit(3)


# ------------------------------------------------------------
# Device
# ------------------------------------------------------------

priority = 1.0

queue_info = vk.VkDeviceQueueCreateInfo(
    sType=vk.VK_STRUCTURE_TYPE_DEVICE_QUEUE_CREATE_INFO,
    queueFamilyIndex=compute_family,
    queueCount=1,
    pQueuePriorities=[priority],
)

device_info = vk.VkDeviceCreateInfo(
    sType=vk.VK_STRUCTURE_TYPE_DEVICE_CREATE_INFO,
    queueCreateInfoCount=1,
    pQueueCreateInfos=[queue_info],
)

try:

    logical_device = vk.vkCreateDevice(
        selected,
        device_info,
        None
    )

    print("[OK] GPU device criado")

except Exception as e:

    print("[ERRO] Criando GPU device:")
    print(e)

    vk.vkDestroyInstance(instance, None)

    sys.exit(4)


# ------------------------------------------------------------
# Queue
# ------------------------------------------------------------

queue = vk.vkGetDeviceQueue(
    logical_device,
    compute_family,
    0
)

print("[OK] Compute queue obtida")


# ------------------------------------------------------------
# Stress
# ------------------------------------------------------------

print()
print("=" * 60)
print("GPU INICIALIZADA")
print("=" * 60)

print()
print("Agora a RX 550X está sendo acessada pelo container.")
print()
print("Abra no Windows:")
print("  Gerenciador de Tarefas")
print("  -> Desempenho")
print("  -> GPU")
print()
print("CTRL+C para parar.")
print()

contador = 0

inicio = time.time()

try:

    while True:

        # Pequenas operações Vulkan para manter a queue ocupada.
        #
        # O objetivo inicial é manter comunicação contínua
        # com a GPU e validar a execução pelo backend D3D12.

        vk.vkQueueWaitIdle(queue)

        contador += 1

        if contador % 100 == 0:

            tempo = time.time() - inicio

            print(
                f"Operações Vulkan: {contador:,} | "
                f"tempo: {tempo:.1f}s | "
                f"ops/s: {contador / tempo:.1f}"
            )

        time.sleep(0.001)


except KeyboardInterrupt:

    print()
    print("Encerrando...")


finally:

    vk.vkDeviceWaitIdle(logical_device)

    vk.vkDestroyDevice(
        logical_device,
        None
    )

    vk.vkDestroyInstance(
        instance,
        None
    )

    print("GPU liberada.")