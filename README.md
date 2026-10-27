<div align="center">

### ⚡️ **CAMOVER**    
CAMOVER, for *camera-rover*.

</div>

----
### Features
- based on a RPI Zero 2 W
- remotly controlled via any connected device any where on the world via a simple website
- simple controls : turn left/right, forward, backward, speed, etc
- send notification throught ntfy
- power management from a tiny micro-controller (XIAO esp32c3) : remtly shutdown or powerup the RPI via home assistant
- realtime battery usage viewer via the XIAO
- (planned) use game controller such as steering wheel
- (planned) see how many people are connected to the website
- (planned) make it autonomous with self hosted ia/simple machine learning
- (planned) better power management, with notifications

### Hardware
```mermaid
flowchart TB
    A[Battery] --> B[Motor Controller]
    A --> C[12v to 5v]
    C --> D[XIAO esp32c3]
    D --> E[Raspberry Zero]
    E --> B
    E --> F[Camera]
```

### Software


**Raspberry Zero**



Two modes : fpv (remtoly controlled) or autonomous (autonomous via ia/machine learning)
```mermaid
flowchart TB
    D[**robot.py** : librairy to easly controll all parts of the robot]
    E[**power-management.py** : run in background independently from main code]
    A[**main.py** : auto start at boot] --> B[fpv.py]
    A --> C[autonomous.py]
    B --> F[runs the website with html/js/css]
    F --> G[**cloudflared**]
    G -.-> H[The Web]
```

**XIAO esp32c3**
```mermaid
flowchart TB
    A[loop] --> B[keeps an eye on battery level]
    A --> C[sends notifications]
    A --> D[listens to home assistant]
    B --> E[sends battery level to RPI]
```

### Previews
<img width="5152" height="3864" alt="IMG_0025" src="https://github.com/user-attachments/assets/337c779a-019d-43ed-9b76-44e2b601b310" />
<img width="1394" height="927" alt="image" src="https://github.com/user-attachments/assets/667d782d-36e7-4488-b1c4-eb0f935dc07f" />
