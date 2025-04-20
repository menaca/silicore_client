# 🖥️ Silicore Client
Turn any PC into a remotely controlled smart device.

Ever wanted to check your PC's status, take screenshots or shutdown remotely?
Silicore Client turns your Windows computer into a secure, silent and remotely controllable system using only Firebase – no servers, no hassle.

> 📱 Pair this client with the [Silicore Mobile App](https://github.com/menaca/silicore) to control your computer from phone.

## 📸 Preview

### 🪟 Running on Windows (First Starting or Disconnected from Phone)
![silicore_client](https://github.com/user-attachments/assets/88f0fa89-3798-42ef-beed-4712f30152a2)

## 🚀 Features

- 🔁 **Real-time Monitoring**: CPU, RAM, Disk, Battery, Screen, and Network info updated every 10 seconds.
- 📸 **Screenshot Capture**: Takes a screenshot and uploads it to Firestore as base64.
- 🧠 **Remote Task Manager**: View and terminate running processes.
- 🔌 **Shutdown Command**: Remotely power off your PC.
- 🔒 **One-time Pairing**: Secure device linking via 6-digit pairing code.
- 🪄 **Dynamic UI**: Automatically opens/closes based on connection status
- ☁️ **Fully Firebase-Powered**: No third-party servers or storage.

## ⚙️ How It Works

1.  On first launch, a unique document is created in `computers` collection.
    
2.  A **6-digit pairing code** is generated and displayed on screen.
    
3.  Once paired with Silicore Mobile App, the connection window auto-closes.
    
4.  Every 10 seconds:
    
    -   🔁 System info is refreshed
        
    -   🔍 Firestore is checked for remote commands

## 🔐 Security

-   ✅ One-time pairing code required for connection
    
-   ✅ Client remains hidden unless a connection is pending

-   ✅ No login required, no private information required.
    
## 🧪 Supported Commands

| Command Name | Description |
|--|--|
| `screenshot` | Captures a screenshot and uploads as base64 |
|`update_tasklist`| Sends running processes to Firestore |
|`kill_process`| Kills specific PIDs sent from the app |
|`shutdown`| Shuts down the system |

All command results are written back to the same document under appropriate fields.    

## 📦 Requirements

-   Python 3.8+
    
-   Firebase Project with Firestore enabled
    
-   Firebase Admin SDK credentials (`serviceAccountKey.json`)
    

## Python Packages:

`pip install firebase-admin pyautogui psutil py-cpuinfo` 


## 🚀 Getting Started

Follow these instructions to set up and run Silicore Client on your local machine.

### 🧩 Folder Structure

```
silicore_client/
├── client.py
└── serviceAccountKey.json
├── config/
│   └── firebase_setup.py
├── core/
│   ├── command_handler.py
│   ├── computer_client.py
│   ├── system_info.py
│   ├── task_manager.py
│   └── utils.py
└── ui/
    └── connection_ui.py
```

### Installation

Clone the repository:

```bash
git clone https://github.com/menaca/silicore_client.git
cd silicore_client
```

Install Python Packages:

```
pip install firebase-admin pyautogui psutil py-cpuinfo
```

Run the app:

```bash
python client.py
```

## 📱 Silicore Mobile App

The Flutter-based Silicore Mobile App allows you to:

- 🔑 Enter the pairing code to link with your computer
- 📊 Monitor real-time system performance
- 📸 Capture screenshots
- 🧠 View and manage running processes
- 🔌 Send remote shutdown command

👉 [Check out the Mobile App Repository](https://github.com/menaca/silicore)

> Do you want to control your computer from your phone and get instant information? Silicore is for you

Check out all my projects [menapps](https://www.instagram.com/menapps).
    
