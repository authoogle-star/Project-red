# Attack Launcher Scripts - Simple Usage Guide

## 🎯 What These Scripts Do

Instead of typing complex Python commands like:
```bash
python3 -c "from modules.apt_simulation import APTSimulation; apt = APTSimulation(); print(apt.simulate_attack())"
```

You can now just run simple scripts!

## 📋 Available Attack Launchers

### 1. APT Simulation
```bash
./scripts/run_apt_attack.sh
```
Launches an Advanced Persistent Threat (APT) simulation with random attack scenario.

**What it does:**
- Randomly selects from: targeted attack, spear phishing, or watering hole
- Logs all activity
- Displays results in formatted output

### 2. Phishing Attack
```bash
./scripts/run_phishing_attack.sh
```
Launches a phishing attack simulation with interactive options.

**What it does:**
- Lets you choose attack type: standard phishing, spear phishing, or whaling
- Lets you specify a target email address
- Simulates the attack safely
- Logs all activity

### 3. Network Exploitation
```bash
./scripts/run_network_attack.sh
```
Launches a network exploitation simulation with interactive options.

**What it does:**
- Lets you choose method: DNS tunneling, ICMP tunneling, or TCP/IP stack exploitation
- Lets you specify a target IP address
- Simulates the network attack
- Logs all activity

## 🚀 Quick Start

1. **Make sure the Red Team server is running in one terminal:**
   ```bash
   ./scripts/start_red_team.sh
   ```

2. **Open a NEW terminal window and run an attack:**
   ```bash
   cd /home/EXQUISITE/Project-Red-Sword
   ./scripts/run_apt_attack.sh
   ```

3. **View the results** - they'll display in the terminal!

## 💡 Understanding the Setup

### Why Two Terminal Windows?

- **Terminal 1**: Runs the dashboard server (must stay open)
- **Terminal 2**: Runs the actual attack simulations

Think of it like:
- Terminal 1 = The control tower (dashboard)
- Terminal 2 = The pilots (attacks)

### What About That Python Command?

The old complex command:
```bash
python3 -c "from modules.apt_simulation import APTSimulation; apt = APTSimulation(); print(apt.simulate_attack())"
```

**Breaking it down:**
- `python3 -c` = Run Python code from command line
- `"..."` = The Python code to run
- `\` = Line continuation (splits long commands across lines)
- `from X import Y` = Load the attack module
- `apt = APTSimulation()` = Create an attack object
- `print(apt.simulate_attack())` = Run the attack and show results

**But now you don't need to remember this!** Just use the launcher scripts.

## 📊 Viewing Results

### Real-Time Logs
```bash
# In another terminal window
tail -f logs/attack_simulation.log
```

### Database Query
```bash
sqlite3 red_team_operations.db "SELECT * FROM attack_simulations ORDER BY timestamp DESC LIMIT 5;"
```

### Dashboard
The dashboard at http://localhost:5006/red_team_dashboard shows instructions, but the actual attacks run via these scripts.

## 🛡️ Safety Features

All scripts automatically:
- ✅ Check that safe mode is enabled
- ✅ Verify virtual environment is active
- ✅ Log all activities
- ✅ Use only whitelisted targets
- ✅ Respect rate limits

## 🛑 Emergency Stop

If something goes wrong:
```bash
python3 scripts/kill_all_simulations.py --yes
```

Or just press `Ctrl+C` in any running terminal.

## 📝 Example Session

```bash
# Terminal 1: Start the server
./scripts/start_red_team.sh
# (Server starts, dashboard opens at http://localhost:5006/red_team_dashboard)
# (Leave this running)

# Terminal 2: Run attacks
cd /home/EXQUISITE/Project-Red-Sword
source venv/bin/activate

# Run APT attack
./scripts/run_apt_attack.sh

# Run phishing attack with options
./scripts/run_phishing_attack.sh
# Choose option 2 (Spear Phishing)
# Enter target: executive@company.com

# View logs
tail -f logs/attack_simulation.log
```

## ❓ Common Questions

**Q: Do I need to keep the dashboard open?**
A: The dashboard is optional - it just shows information. The attacks run independently.

**Q: Can I run multiple attacks at once?**
A: Yes! Open multiple terminal windows and run different scripts. Safe mode will rate-limit them.

**Q: Where do the results go?**
A: Results are displayed in the terminal, logged to `logs/attack_simulation.log`, and stored in the database.

**Q: Is this actually attacking anything?**
A: No! With `SAFE_MODE=true`, all attacks are simulated. They demonstrate the attack logic without actually exploiting systems.

## 🔧 Make Scripts Executable

If you get "Permission denied" errors:
```bash
chmod +x scripts/run_*.sh
```

## 📚 Next Steps

1. Try running each attack launcher
2. View the logs to see what happened
3. Query the database to see stored results
4. Experiment with different targets and options
5. Check the dashboard for system overview

---

**Happy (Safe) Hacking! 🛡️**
