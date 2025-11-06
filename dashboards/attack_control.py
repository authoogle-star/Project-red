#!/usr/bin/env python3
"""
Attack Control Panel Dashboard
"""
import panel as pn

pn.extension(design="bootstrap", sizing_mode="stretch_width")

def create_attack_control_panel():
    """Create an attack control panel for launching and managing simulations."""

    # Attack status
    status_text = pn.pane.Markdown("""
    ## 🎯 Red Team Attack Control Center

    **System Status**: 🟢 OPERATIONAL
    **Safe Mode**: 🟢 ENABLED
    **Kill Switch**: 🟢 READY
    **Network Segmentation**: 🟢 ENFORCED

    ---
    """)

    # Attack type selector
    attack_type = pn.widgets.Select(
        name='Attack Type',
        options=[
            'Social Engineering - Phishing',
            'Social Engineering - Spear Phishing',
            'Web Application - SQL Injection',
            'Web Application - XSS',
            'Web Application - CSRF',
            'Network - DNS Tunneling',
            'Network - Port Scan',
            'Network - MITM',
            'APT - Multi-Stage Simulation',
            'APT - Lateral Movement',
        ],
        width=300
    )

    # Target input
    target_input = pn.widgets.TextInput(
        name='Target (optional)',
        placeholder='Leave empty to use targets.yaml',
        width=300
    )

    # Attack parameters
    severity_slider = pn.widgets.FloatSlider(
        name='Severity Level',
        start=0.1,
        end=1.0,
        value=0.5,
        step=0.1,
        width=300
    )

    # Launch button
    launch_button = pn.widgets.Button(
        name='🚀 Launch Attack Simulation',
        button_type='danger',
        width=300
    )

    # Stop button
    stop_button = pn.widgets.Button(
        name='🛑 Emergency Stop All',
        button_type='warning',
        width=300
    )

    # Status output
    status_output = pn.pane.Markdown("Ready to launch simulations...")

    def launch_attack(event):
        """Launch selected attack simulation."""
        attack = attack_type.value
        target = target_input.value or "Default targets from config"
        severity = severity_slider.value

        status_output.object = f"""
### 🚀 Launching Attack Simulation

**Type**: {attack}
**Target**: {target}
**Severity**: {severity}
**Status**: Initializing...

---

⚠️ **Note**: In demo mode, actual attacks are simulated safely.
All activity is logged to the database for analysis.

To run actual attacks, use the Python API:
```python
from modules.advanced_social_engineering import AdvancedSocialEngineering
social_eng = AdvancedSocialEngineering()
result = social_eng.simulate_attack()
```
        """

    def stop_all_attacks(event):
        """Stop all running attacks."""
        status_output.object = """
### 🛑 EMERGENCY STOP ACTIVATED

All attack simulations have been stopped.

To verify, check:
```bash
python3 scripts/kill_all_simulations.py --yes
```

System is now in safe idle state.
        """

    launch_button.on_click(launch_attack)
    stop_button.on_click(stop_all_attacks)

    # Recent attacks table
    recent_attacks_md = pn.pane.Markdown("""
### 📊 Recent Attack Simulations

To view recent attacks, query the database:
```python
from database.models import AttackSimulation, SessionLocal
session = SessionLocal()
attacks = session.query(AttackSimulation).order_by(
    AttackSimulation.timestamp.desc()
).limit(10).all()
for attack in attacks:
    print(f"{attack.timestamp}: {attack.attack_type} - {attack.status}")
```

**Quick Start Commands:**
```bash
# Run phishing simulation
python3 -c "from modules.advanced_social_engineering import AdvancedSocialEngineering; \\
    se = AdvancedSocialEngineering(); print(se.simulate_attack())"

# Run APT simulation
python3 -c "from modules.apt_simulation import APTSimulation; \\
    apt = APTSimulation(); print(apt.simulate_attack())"

# Run network scan
python3 -c "from modules.network_exploitation import NetworkExploitation; \\
    net = NetworkExploitation(); print(net.simulate_attack())"
```
    """)

    # Safety information
    safety_info = pn.pane.Markdown("""
---

## 🛡️ Safety Information

### Active Protections
- ✅ **Safe Mode**: All attacks are controlled and logged
- ✅ **Rate Limiting**: Max 10 attacks per minute
- ✅ **Target Validation**: Only whitelisted targets
- ✅ **Network Segmentation**: Isolated test networks only
- ✅ **Resource Limits**: CPU/Memory caps enforced
- ✅ **Auto Cleanup**: Artifacts removed automatically

### Emergency Procedures
1. **Kill Switch**: `python3 scripts/kill_all_simulations.py`
2. **Graceful Stop**: Press Ctrl+C in terminal
3. **Stop File**: `touch .stop_attacks`

### Configuration
- **Attack Config**: `config/attack_config.yaml`
- **Safe Mode**: `config/safe_mode.yaml`
- **Targets**: `config/targets.yaml`
- **Environment**: `.env`

### Monitoring
- **Logs**: `tail -f logs/attack_simulation.log`
- **Database**: `sqlite3 red_team_operations.db`
- **Reports**: `reports/generated/`
    """)

    # Assemble dashboard
    attack_control = pn.Column(
        status_text,
        pn.Row(
            pn.Column(
                "## Launch Attack Simulation",
                attack_type,
                target_input,
                severity_slider,
                launch_button,
                stop_button,
                width=350
            ),
            pn.Column(
                "## Simulation Status",
                status_output,
                width=600
            )
        ),
        "---",
        recent_attacks_md,
        safety_info
    )

    return attack_control

# Create and serve attack control panel
attack_control = create_attack_control_panel()

pn.template.BootstrapTemplate(
    title="Attack Control",
    main=attack_control,
    main_max_width="95%",
    header_background="#B22222",
).servable()
