FILE FREEFORM = DDE58710-41CD-4306-DBFB-3FA90BB1D2DD {
    SECTION UI = "uefiplat.cfg"
    SECTION RAW = Binaries/instantnoodlep/RawFiles/uefiplat.cfg
}

  INF MdeModulePkg/Core/Dxe/DxeMain.inf
  INF MdeModulePkg/Universal/PCD/Dxe/Pcd.inf

!if $(INSTANTNOODLEP_VENDOR_HW) == 1
  INF Binaries/instantnoodlep/QcomPkg/Drivers/EnvDxe/EnvDxe.inf
!endif

  INF MdeModulePkg/Universal/ReportStatusCodeRouter/RuntimeDxe/ReportStatusCodeRouterRuntimeDxe.inf
  INF MdeModulePkg/Universal/StatusCodeHandler/RuntimeDxe/StatusCodeHandlerRuntimeDxe.inf
  INF MdeModulePkg/Core/RuntimeDxe/RuntimeDxe.inf
  INF ArmPkg/Drivers/CpuDxe/CpuDxe.inf
  INF ArmPkg/Drivers/ArmGicDxe/ArmGicDxe.inf
  INF EmbeddedPkg/MetronomeDxe/MetronomeDxe.inf
  INF ArmPkg/Drivers/TimerDxe/TimerDxe.inf

!if $(INSTANTNOODLEP_VENDOR_HW) == 1
  INF Binaries/instantnoodlep/QcomPkg/Drivers/SmemDxe/SmemDxe.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/DALSYSDxe/DALSYSDxe.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/HWIODxe/HWIODxe.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/ChipInfoDxe/ChipInfoDxe.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/PlatformInfoDxe/PlatformInfoDxe.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/OcdtDxe/OplusProject.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/HALIOMMUDxe/HALIOMMUDxe.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/ULogDxe/ULogDxe.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/CmdDbDxe/CmdDbDxe.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/PwrUtilsDxe/PwrUtilsDxe.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/NpaDxe/NpaDxe.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/RpmhDxe/RpmhDxe.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/VcsDxe/VcsDxe.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/ClockDxe/ClockDxe.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/ShmBridgeDxe/ShmBridgeDxeLA.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/TzDxe/ScmDxeLA.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/TLMMDxe/TLMMDxe.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/I2CDxe/I2CDxe.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/SPMIDxe/SPMIDxe.inf
!endif

  INF MdeModulePkg/Universal/ResetSystemRuntimeDxe/ResetSystemRuntimeDxe.inf

!if $(INSTANTNOODLEP_VENDOR_HW) == 1
  INF Binaries/instantnoodlep/QcomPkg/Drivers/PmicDxe/PmicDxeLa.inf
!endif

  INF MdeModulePkg/Universal/Disk/DiskIoDxe/DiskIoDxe.inf
  INF MdeModulePkg/Universal/Disk/PartitionDxe/PartitionDxe.inf
  INF MdeModulePkg/Universal/Disk/UnicodeCollation/EnglishDxe/EnglishDxe.inf

!if $(INSTANTNOODLEP_VENDOR_HW) == 1
!if $(INSTANTNOODLEP_STORAGE) == 1
  # INF Binaries/instantnoodlep/QcomPkg/Drivers/SdccDxe/SdccDxe.inf
  # Beta line (GF final architecture): the vendor UFSDxe stays out of
  # dispatch, so the device keeps the state xbl_sec initialized and the
  # kernel takes the handoff directly. The SMMU is left untouched - the
  # SmmuBypassDxe experiment is off because writing the SMMU this early
  # hangs the box (same failure GFander documents and abandoned).
  # INF Binaries/instantnoodlep/QcomPkg/Drivers/UFSDxe/UFSDxe.inf
!endif
!endif

  INF FatPkg/EnhancedFatDxe/Fat.inf

!if $(INSTANTNOODLEP_VENDOR_HW) == 1
!if $(INSTANTNOODLEP_TRUSTZONE) == 1
  INF Binaries/instantnoodlep/QcomPkg/Drivers/TzDxe/TzDxeLA.inf
!endif
!endif

  INF MdeModulePkg/Universal/Variable/RuntimeDxe/VariableRuntimeDxe.inf

!if $(INSTANTNOODLEP_VENDOR_HW) == 1
  INF Binaries/instantnoodlep/QcomPkg/Drivers/DDRInfoDxe/DDRInfoDxe.inf
!if $(INSTANTNOODLEP_TRUSTZONE) == 1
  INF Binaries/instantnoodlep/QcomPkg/Drivers/FeatureEnablerDxe/FeatureEnablerDxe.inf
!endif
!endif

!if $(USE_CUSTOM_DISPLAY_DRIVER) == 1
  INF Binaries/instantnoodlep/QcomPkg/Drivers/DisplayDxe/DisplayDxe.inf
!else
  INF SiliciumPkg/Drivers/SimpleFbDxe/SimpleFbDxe.inf
!endif

!if $(INSTANTNOODLEP_VENDOR_HW) == 1
!if $(INSTANTNOODLEP_TRUSTZONE) == 1
  INF Binaries/instantnoodlep/QcomPkg/Drivers/PILProxyDxe/PILProxyDxe.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/PILDxe/PILDxe.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/SPSSDxe/SPSSDxe.inf
!endif
!endif

  INF MdeModulePkg/Universal/WatchdogTimerDxe/WatchdogTimer.inf
  INF MdeModulePkg/Universal/SecurityStubDxe/SecurityStubDxe.inf
  INF EmbeddedPkg/EmbeddedMonotonicCounter/EmbeddedMonotonicCounter.inf
  INF EmbeddedPkg/RealTimeClockRuntimeDxe/RealTimeClockRuntimeDxe.inf
  INF MdeModulePkg/Universal/PrintDxe/PrintDxe.inf
  INF MdeModulePkg/Universal/DevicePathDxe/DevicePathDxe.inf
  INF MdeModulePkg/Universal/CapsuleRuntimeDxe/CapsuleRuntimeDxe.inf
  INF MdeModulePkg/Universal/HiiDatabaseDxe/HiiDatabaseDxe.inf
  INF MdeModulePkg/Universal/SetupBrowserDxe/SetupBrowserDxe.inf

  INF UniXNUPkg/Driver/UniXNURamDiskDxe/UniXNURamDiskDxe.inf
  INF DarwinBootPkg/Driver/DarwinBoot.inf
  INF UniXNUPkg/Driver/UniXNUDxe/UniXNUDxe.inf

  INF MdeModulePkg/Universal/BdsDxe/BdsDxe.inf

!if $(INSTANTNOODLEP_VENDOR_HW) == 1
  INF Binaries/instantnoodlep/QcomPkg/Drivers/SPIDxe/SPIDxe.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/UsbPwrCtrlDxe/UsbPwrCtrlDxe.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/QcomChargerDxe/QcomChargerDxeLA.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/ChargerExDxe/ChargerExDxe.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/UsbfnDwc3Dxe/UsbfnDwc3Dxe.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/XhciPciEmulationDxe/XhciPciEmulationDxe.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/XhciDxe/XhciDxe.inf
!endif

  INF MdeModulePkg/Bus/Usb/UsbBusDxe/UsbBusDxe.inf
  INF MdeModulePkg/Bus/Usb/UsbKbDxe/UsbKbDxe.inf
  INF MdeModulePkg/Bus/Usb/UsbMassStorageDxe/UsbMassStorageDxe.inf

!if $(INSTANTNOODLEP_VENDOR_HW) == 1
  INF Binaries/instantnoodlep/QcomPkg/Drivers/UsbMsdDxe/UsbMsdDxe.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/UsbDeviceDxe/UsbDeviceDxe.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/UsbConfigDxe/UsbConfigDxe.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/ButtonsDxe/ButtonsDxe.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/TsensDxe/TsensDxe.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/LimitsDxe/LimitsDxe.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/GpiDxe/GpiDxe.inf
  INF Binaries/instantnoodlep/QcomPkg/Drivers/RNGDxe/RngDxe.inf
!endif

  INF EmbeddedPkg/SimpleTextInOutSerial/SimpleTextInOutSerial.inf
  INF MdeModulePkg/Universal/Console/ConPlatformDxe/ConPlatformDxe.inf
  INF MdeModulePkg/Universal/Console/ConSplitterDxe/ConSplitterDxe.inf
  INF MdeModulePkg/Universal/Console/GraphicsConsoleDxe/GraphicsConsoleDxe.inf

# Boot menu application; BDS starts it through the option UniXNUDxe registers.
INF UniXNUPkg/Application/UniXNU/UniXNU.inf
  # Open-source UFS stack (adapter first, then pass-thru, SCSI bus and disk).
