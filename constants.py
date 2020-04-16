class Constants:
    # Platform constants
    platform_type_WIN_32 = "WINDOWS32"
    platform_type_WIN_64 = "WINDOWS64"
    platform_type_LINUX_32 = "LINUX32"
    platform_type_LINUX_64 = "LINUX64"
    platform_type_MAC = "MAC"

    # Driver Paths
    driver_path = {
        platform_type_WIN_32: "drivers/geckodriver_windows_32",
        platform_type_WIN_64: "drivers/geckodriver_windows_64",
        platform_type_LINUX_32: "drivers/geckodriver_linux_32",
        platform_type_LINUX_64: "drivers/geckodriver_linux_64",
        platform_type_MAC: "drivers/geckodriver_mac",
    }
