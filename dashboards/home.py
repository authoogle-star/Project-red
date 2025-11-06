#!/usr/bin/env python3
"""
Home Page Dashboard
"""
import panel as pn

pn.extension(design="bootstrap", sizing_mode="stretch_width")

def create_home_page():
    """Create a home page with links to all dashboards."""

    home_content = pn.Column(
        pn.pane.Markdown("""
# 🛡️ PROJECT RED SWORD - Red Team Operations Platform

Welcome to the Red Team Attack Simulation and Defense Monitoring Platform.

---

## 📊 Available Dashboards

### [🎯 Attack Control Panel](./attack_control)
Launch and manage attack simulations across multiple categories:
- Social Engineering (Phishing, Spear Phishing)
- Web Application Attacks (SQL Injection, XSS, CSRF)
- Network Attacks (Port Scanning, DNS Tunneling, MITM)
- APT Simulations (Multi-stage attacks, Lateral Movement)

### [🛡️ Defense Monitoring](./defense_monitoring)
Real-time security monitoring with Datashader visualizations:
- Live threat detection heatmaps
- Network traffic analysis (1M+ data points)
- Attack detection timeline
- Security metrics and KPIs

### [🤖 AI Image Classification](./image_classification)
Demo: CLIP model image classification interface

---

## 🚀 Quick Start

### Launch Your First Attack Simulation

```bash
# Terminal 1: Start the platform (already running)
./scripts/start_red_team.sh

# Terminal 2: Run a simulation
python3 -c "from modules.apt_simulation import APTSimulation; \\
    apt = APTSimulation(); print(apt.simulate_attack())"
```

### View Attack Logs

```bash
# Real-time logs
tail -f logs/attack_simulation.log

# Database query
sqlite3 red_team_operations.db \\
    "SELECT * FROM attack_simulations ORDER BY timestamp DESC LIMIT 5;"
```

### Emergency Stop

```bash
# Kill all running simulations
python3 scripts/kill_all_simulations.py --yes
```

---

## 📖 Documentation

- **Deployment Guide**: `PRODUCTION_DEPLOYMENT_GUIDE.md`
- **Datashader Setup**: `DATASHADER_SETUP.md`
- **Configuration**: `config/`
- **Scripts**: `scripts/`

---

## ⚙️ System Status

**Environment**: Production Monitoring
**Mode**: Safe Demo (No External APIs)
**Safe Mode**: ✅ ENABLED
**Network Segmentation**: ✅ ENFORCED
**Rate Limiting**: ✅ ACTIVE (10 attacks/min)
**Kill Switch**: ✅ READY
**Monitoring**: ✅ ACTIVE
**Logging**: ✅ ACTIVE

---

## 🔒 Safety Features

1. **Configuration Safety** - Safe mode, rate limits, target whitelisting
2. **Runtime Safety** - Resource limits, timeouts, automatic cleanup
3. **Emergency Controls** - Kill switch, graceful shutdown, stop signals
4. **Audit & Compliance** - Database logging, blockchain audit trail
5. **Network Segmentation** - Isolated networks, no external access

---

## 📞 Need Help?

- **Documentation**: Check `PRODUCTION_DEPLOYMENT_GUIDE.md`
- **Health Check**: `python3 scripts/health_check.py`
- **Logs**: `logs/attack_simulation.log`
- **Database**: `red_team_operations.db`

---

**Version**: 1.0.0
**Last Updated**: November 4, 2024
**Status**: 🟢 Operational
        """),
        width=900
    )

    return home_content

# Create and serve the home page
home_page = create_home_page()

pn.template.BootstrapTemplate(
    title="Red Sword Home",
    main=home_page,
    main_max_width="95%",
    header_background="#8B0000",
).servable()
