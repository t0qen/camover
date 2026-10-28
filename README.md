<div align="center">

### ⚡️ **CAMOVER**    
CAMOVER, for *camera-rover*.

</div>

----

<div align="center">
    
A tiny **tracked robot** remotly controllable from **anywhere** in the world throught an easy-to-use website.

</div>


> [!TIP]
> Try it **yourself** : https://camover.lostpacket.org
>
> The user is *demo* and the password often changes, to prevent too much people for being connected at same time.
>
> Ask me (discord: t0qen) to try it ! Or wait for global tests.
>



### ✅️ Features
- based on a RPI Zero 2 W
- remotly controlled via any connected device any where on the world via a simple website
- simple controls : turn left/right, forward, backward, speed, etc
- send notification throught ntfy
- power management from a tiny micro-controller (XIAO esp32c3) : remtly shutdown or powerup the RPI via home assistant
- realtime battery usage viewer via the XIAO
- (planned) use game controller such as steering wheel
- see how many people are connected to the website in the same time
- (planned) being able to control more accuratly the robot while several peoples are connected together
- (planned) make it autonomous with self hosted ia/simple machine learning
- power management, with notifications and emergency shutdown

### 🔌️ Hardware
```mermaid
flowchart TB
    A[Battery] --> B[Motor Controller]
    A --> C[12v to 5v]
    C --> D[XIAO esp32c3]
    D --> E[Raspberry Zero]
    E --> B
    E --> F[Camera]
```
**Components**
- camera 8 Mpx IMX219 B0390 
- motor controller MDD3A
- convertissor DC-DC 60 W DFR1025 
- Raspberry Pi Zero 2 W
- motors come from this [kit](https://www.dfrobot.com/product-1837.html)
- capacitors for stabilisation and filtering
- XIAO esp32c3
- standard relay
- 11.1V 2200mAh 25C lithium battery
- other random and cheap components like leds, etc

### 📜️ Software


**Raspberry Zero**



Two modes : fpv (remtoly controlled) or autonomous (autonomous via ia/machine learning)
```mermaid
flowchart TB
    D[**robot.py** : librairy to easly controll all parts of the robot]
    E[**power-management.py** : run in background independently from main code]
    A[**main.py** : auto start at boot] --> B[fpv.py]
    A --> C[autonomous.py]
    B --> F[runs the website with html/js/css]
    F --> G[auth]
    G --> H[**cloudflared**]
    I -.-> J[The Web]
```

**XIAO esp32c3**
```mermaid
flowchart TB
    A[loop] --> B[keeps an eye on battery level]
    A --> C[sends notifications]
    A --> D[listens to home assistant]
    B --> E[sends battery level to RPI]
```

### 📷️ Previews
<img width="5152" height="3864" alt="IMG_0025" src="https://github.com/user-attachments/assets/337c779a-019d-43ed-9b76-44e2b601b310" />
<img width="1383" height="902" alt="image" src="https://github.com/user-attachments/assets/eefe973e-66bc-475d-9c42-0e6475f6aa19" />

Photo from the very beginning of the project
<img width="970" height="821" alt="image" src="https://github.com/user-attachments/assets/76c3df07-b2ad-4f4b-862f-0c821da5622b" />

