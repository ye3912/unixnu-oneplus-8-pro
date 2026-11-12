##
#  Copyright (c) 2011 - 2022, ARM Limited. All rights reserved.
#  Copyright (c) 2014, Linaro Limited. All rights reserved.
#  Copyright (c) 2015 - 2020, Intel Corporation. All rights reserved.
#  Copyright (c) 2018, Bingxing Wang. All rights reserved.
#  Copyright (c) 2024, Microsoft Corporation.
#
#  SPDX-License-Identifier: BSD-2-Clause-Patent
##

################################################################################
#
# Defines Section - statements that will be processed to create a Makefile.
#
################################################################################
[Defines]
  PLATFORM_NAME                  = instantnoodlep
  PLATFORM_GUID                  = 7A1C4E90-3B62-4E1D-9C77-5F2B8D46A013
  PLATFORM_VERSION               = 0.1
  DSC_SPECIFICATION              = 0x00010005
  OUTPUT_DIRECTORY               = Build/instantnoodlepPkg
  SUPPORTED_ARCHITECTURES        = AARCH64
  BUILD_TARGETS                  = RELEASE|DEBUG
  SKUID_IDENTIFIER               = DEFAULT
  FLASH_DEFINITION               = instantnoodlepPkg/instantnoodlep.fdf
  USE_CUSTOM_DISPLAY_DRIVER      = 0

  #
  # 0 = SM8250
  # 1 = SM8250-AB
  # 2 = SM8250-AC
  #
  SOC_TYPE                       = 0

  #
  # 1 = include the Qualcomm DXE drivers extracted from this device's firmware.
  # 0 = core-only image (edk2 + Silicium + UniXNU), used to isolate a vendor driver.
  #
  INSTANTNOODLEP_VENDOR_HW       = 1

  #
  # 1 = include SdccDxe/UFSDxe. 0 while the SM8250 UFS initialisation fails on this
  # board: the payload arrives through the boot image ramdisk, so storage is not needed
  # to reach the boot manager. The kernel now carries its own cold-start driver, so the
  # vendor path stays out of the image.
  #
  INSTANTNOODLEP_STORAGE         = 0

  #
  # 1 = include TzDxeLA, FeatureEnablerDxe and the PIL/SPSS loaders. They reach the
  # TrustZone application through QseeCom, which is read from the tz partition, so they
  # cannot start while storage is off.
  #
  INSTANTNOODLEP_TRUSTZONE       = 0

!include KonaPkg/KonaPkg.dsc.inc

[PcdsFixedAtBuild]
  #
  # DDR Memory
  #
  gArmTokenSpaceGuid.PcdSystemMemoryBase|0x80000000

  #
  # UEFI Stack
  #
  gArmPlatformTokenSpaceGuid.PcdCPUCoresStackBase|0x9FF90000
  gArmPlatformTokenSpaceGuid.PcdCPUCorePrimaryStackSize|0x40000

  #
  # SMBIOS
  #
  gSiliciumPkgTokenSpaceGuid.PcdSmbiosSystemManufacturer|"OnePlus"
  gSiliciumPkgTokenSpaceGuid.PcdSmbiosSystemModel|"8 Pro"
  gSiliciumPkgTokenSpaceGuid.PcdSmbiosSystemRetailModel|"instantnoodlep"
  gSiliciumPkgTokenSpaceGuid.PcdSmbiosSystemRetailSku|"8Pro_instantnoodlep"
  gSiliciumPkgTokenSpaceGuid.PcdSmbiosSystemBoardModel|"8 Pro"

  #
  # Simple Frame Buffer
  #
  # The panel is 1440x3168 (Samsung AMS678UW01), but the bootloader brings it up at
  # 1080x2376 and leaves that framebuffer live. SimpleFbDxe draws straight into it, so
  # these values must match the bootloader's mode, not the panel's native area.
  # Confirmed on hardware: 1440x3168 skews every row by 360 pixels, 1080x2376 aligns.
  #
  gSiliciumPkgTokenSpaceGuid.PcdFrameBufferWidth|1080
  gSiliciumPkgTokenSpaceGuid.PcdFrameBufferHeight|2376
  gSiliciumPkgTokenSpaceGuid.PcdFrameBufferColorDepth|32

  #
  # Platform PEI
  #
  gQcomPkgTokenSpaceGuid.PcdPlatformType|"LA"

  #
  # Variables: no persistent store is reachable without a working UFS driver, so the
  # variable services keep their store in RAM. Persistence returns with storage.
  #
  gEfiMdeModulePkgTokenSpaceGuid.PcdEmuVariableNvModeEnable|TRUE
  # This firmware volume includes UniXNU but omits MsBootPolicy and UFPLoader.
  gSiliciumPkgTokenSpaceGuid.PcdRegisterStorageAndFfuBootOptions|FALSE

  gUniXNUPkgTokenSpaceGuid.PcdUniXNUDeviceModel|"instantnoodlep"
  gAdvLoggerPkgTokenSpaceGuid.PcdAdvancedLoggerPages|256


[LibraryClasses]
  #
  # Memory Libraries
  #
  MemoryMapLib|instantnoodlepPkg/Library/MemoryMapLib/MemoryMapLib.inf

  #
  # QCOM Libraries
  #
  ConfigurationMapLib|instantnoodlepPkg/Library/ConfigurationMapLib/ConfigurationMapLib.inf
  # This firmware volume omits the Qualcomm MassStorage application.
  PlatformBootOptionsLib|SiliciumNullPkg/Library/PlatformBootOptionsLibNull/PlatformBootOptionsLibNull.inf

  #
  # UniXNU and DarwinBoot
  #
  FdtLib|MdePkg/Library/BaseFdtLib/BaseFdtLib.inf
  HobLib|MdePkg/Library/DxeHobLib/DxeHobLib.inf
  UniXNULib|UniXNUPkg/Library/UniXNULib/UniXNULib.inf
  AdvancedLoggerAccessLib|AdvLoggerPkg/Library/AdvancedLoggerAccessLib/AdvancedLoggerAccessLib.inf
  QrEncoderLib|MsGraphicsPkg/Library/QrEncoderLib/QrEncoderLib.inf

[LibraryClasses.common.DXE_CORE]
  DebugLib|AdvLoggerPkg/Library/BaseDebugLibAdvancedLogger/BaseDebugLibAdvancedLogger.inf
  AssertLib|AdvLoggerPkg/Library/AssertLib/AssertLib.inf
  AdvancedLoggerLib|AdvLoggerPkg/Library/AdvancedLoggerLib/DxeCore/AdvancedLoggerLib.inf
  AdvancedLoggerHdwPortLib|AdvLoggerPkg/Library/AdvancedLoggerHdwPortLib/AdvancedLoggerHdwPortLib.inf

[LibraryClasses.common.DXE_DRIVER, LibraryClasses.common.UEFI_DRIVER, LibraryClasses.common.UEFI_APPLICATION]
  DebugLib|AdvLoggerPkg/Library/BaseDebugLibAdvancedLogger/BaseDebugLibAdvancedLogger.inf
  AssertLib|AdvLoggerPkg/Library/AssertLib/AssertLib.inf
  AdvancedLoggerLib|AdvLoggerPkg/Library/AdvancedLoggerLib/Dxe/AdvancedLoggerLib.inf
  AdvancedLoggerHdwPortLib|AdvLoggerPkg/Library/AdvancedLoggerHdwPortLib/AdvancedLoggerHdwPortLib.inf

[LibraryClasses]
  UefiScsiLib|MdePkg/Library/UefiScsiLib/UefiScsiLib.inf

[Components]
  #
  # ACPI Tables
  #
  instantnoodlep/AcpiTables.inf

  #
  # Core modules the vendor dispatch list uses that the shared platform includes do
  # not declare. They are built from source.
  #
  MdeModulePkg/Universal/FvSimpleFileSystemDxe/FvSimpleFileSystemDxe.inf
  MdeModulePkg/Universal/ReportStatusCodeRouter/RuntimeDxe/ReportStatusCodeRouterRuntimeDxe.inf
  MdeModulePkg/Universal/SecurityStubDxe/SecurityStubDxe.inf

  #
  # UniXNU boot manager, payload volume publishing and the XNU loader.
  #
  UniXNUPkg/Application/UniXNU/UniXNU.inf
  UniXNUPkg/Driver/UniXNUDxe/UniXNUDxe.inf
  UniXNUPkg/Driver/UniXNURamDiskDxe/UniXNURamDiskDxe.inf
  DarwinBootPkg/Driver/DarwinBoot.inf
  ArmPkg/Drivers/CpuDxe/CpuDxe.inf {
    <LibraryClasses>
      CpuExceptionHandlerLib|UefiCpuPkg/Library/CpuExceptionHandlerLib/DxeCpuExceptionHandlerLibAdv.inf
  }
  UniXNUPkg/Driver/AdvancedLogDxe/AdvancedLogDxe.inf

  #
  # Open-source UFS stack: the Qualcomm adapter keeps the link ABL left behind and
  # EDK2's UfsPassThru performs the fDeviceInit query the vendor binary omits.
  #
