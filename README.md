# Tic Tac Toe

This is a two-player networked Tic Tac Toe game built using Python and Pygame. It consists of a client (`game.py`) and a server (`server.py`) allowing two players to connect over a network and play the classic game.

---

## 🎮 Features

- Multiplayer support over LAN or internet
- Graphical user interface using Pygame
- Win detection and automatic board reset
- Visual indicators for player turn
- Simple communication protocol using sockets

---


## 🛠️ Requirements

- Python 3.x
- `pygame` library

Install requirements:
```bash
pip install pygame
```

---

## 🚀 Running the Game

### Start the server
```bash
python server.py 0.0.0.0 5555
```

### Start the game client
```bash
python game.py <server_ip> 5555
```

Or use the fallback `config` file:
```
<server_ip>:5555
```

<img width="626" height="565" alt="image" src="https://github.com/user-attachments/assets/cab6772f-f0d0-48b1-a2e5-83922dcc89f2" />
