flowchart LR
    RC[RC receiver] -- SBUS --> FC
    GPS[RTK GPS + compass] <-- CAN1 / DroneCAN --> FC
    TEL[Telemetry radio] <-- UART TELEM1 / MAVLink --> FC
    PM[Power module] -- POWER1 --> FC
    FC((Cube Orange<br/>ArduPilot)) <-- UART TELEM2 / MAVLink or DDS --> JET[Jetson Orin Nano]
    CAM[RGB gimbal camera] -- USB or Ethernet --> JET
    FC -- PWM MAIN OUT 1-4 --> ESC[4x ESCs]
    ESC --> MOT[4x brushless motors]
    BAT[6S LiPo] --> PM
    PM --> PDB[Power distribution board]
    PDB --> ESC
    PDB --> BUCK[Step-down converter]
    BUCK --> JET
    BUCK --> CAM

| Component | Example part | Role |
|---|---|---|
| Flight controller | CubePilot Cube Orange (standard carrier board) | Stabilization, control loops, sensor fusion |
| Firmware | ArduPilot | Autonomous missions, geofencing, return-to-launch |
| Onboard computer | NVIDIA Jetson Orin Nano | Vision, autonomy, mission logic |
| GPS | Here3 RTK GNSS | Centimeter-level position, velocity, time, and compass |
| RC receiver | FrSky X4R-SB | Receives pilot commands, outputs SBUS |
| RC transmitter | Any 2.4 GHz transmitter compatible with the receiver | Pilot control and manual override |
| Telemetry radio | SiK 915 MHz telemetry radio pair | MAVLink link to ground station |
| Camera | RGB gimbal camera (USB or Ethernet) | Mapping and inspection imagery |
| Power module | Cube-compatible power module | Battery sensing and power to the Cube |
| Power distribution board | PDB rated for 6S and ESC current | Splits battery power |
| Step-down converter | Regulator rated for 6S input | Powers the Jetson and camera |
| ESCs (x4) | Quad ESCs rated for 6S | Drive the motors from PWM commands |
| Motors (x4) | Brushless motors sized for the airframe | Thrust |
| Battery | 6S LiPo | Main power |

## 4. Connection table

All ports are on the Cube Orange carrier board unless noted.

| Component | Connects to | Interface / protocol | Notes |
|---|---|---|---|
| RC receiver | `RC IN` | SBUS | Stick and switch commands |
| RTK GPS (Here3) | `CAN1` | DroneCAN (CAN) | CAN cable also carries power |
| Telemetry radio | `TELEM1` | UART, MAVLink | Port also powers the radio |
| Jetson Orin Nano | `TELEM2` to Jetson UART pins | UART, MAVLink or DDS | Cross TX/RX, share ground, do not connect 5 V |
| Power module | `POWER1` | Analog voltage and current | Also carries power into the Cube |
| ESCs (x4) | `MAIN OUT 1-4` | PWM | Signal and ground only; leave ESC BEC 5 V wire disconnected |
| Motors (x4) | Their own ESC | 3-phase power | Swap any two wires to reverse direction |
| RGB gimbal camera | Jetson | USB or Ethernet | Powered from step-down converter or PDB per its voltage rating |
| Step-down converter | PDB to Jetson and camera | DC power | Regulated to the Jetson's required input |
| Battery | Power module, then PDB | Power | Raw 6S voltage |

### Jetson UART wiring

| Cube TELEM2 | Jetson |
|---|---|
| TX | RX |
| RX | TX |
| GND | GND |

Do not connect the Cube's 5 V line to the Jetson. On the Orin Nano dev kit, UART1 is typically on pins 8 (TX), 10 (RX) and 6 (GND). Confirm against your carrier board's pinout.

## 5. Power architecture

```
6S LiPo
  |
  +--> Power module --> POWER1 (Cube, sensing + power)
  |         |
  |         v
  +-----> PDB --> ESC 1-4 --> Motors 1-4
            |
            +--> Step-down converter --> Jetson, camera/gimbal
```

- The Cube is powered through the power module, never directly from the PDB.
- The Jetson draws much more current than a flight controller port can supply, so it has its own regulated supply.
