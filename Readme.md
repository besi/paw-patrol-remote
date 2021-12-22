## Remote using ESPNow


### Preparation

    cd
    wget https://github.com/glenn20/micropython-espnow-images/blob/main/20210903_espnow-g20-v1.17/firmware-esp32-GENERIC.bin
    IMAGE=firmware-esp32-GENERIC.bin
    PORT=/dev/cu.usbserial-145320
    PORT=/dev/cu.usbserial-02531274
    esptool.py --port $PORT erase_flash
    esptool.py --chip auto --port $PORT write_flash -z 0x1000 $IMAGE
