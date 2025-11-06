# 🛡️ PROJECT RED SWORD - PRODUCTION DEPLOYMENT GUIDE

## Executive Summary

**Project Red Sword** is now configured for production red team operations with comprehensive safety controls. This guide provides step-by-step instructions for deploying and operating the platform in your production monitoring environment.

### Deployment Overview
- **Environment**: Production Monitoring
- **Mode**: Safe Demo (No External APIs)
- **Focus**: Red Team Attack Simulations
- **Attack Scope**: Social Engineering, Web Applications, Network, APT Scenarios
- **Safety Level**: Maximum (multiple layers of protection)

---

## 📋 Table of Contents

1. [Quick Start (5 Minutes)](#quick-start)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Safety Mechanisms](#safety-mechanisms)
6. [Running Attack Simulations](#running-attack-simulations)
7. [Monitoring & Defense](#monitoring--defense)
8. [Emergency Procedures](#emergency-procedures)
9. [Troubleshooting](#troubleshooting)
10. [Best Practices](#best-practices)

---

## 🚀 Quick Start

### Fastest Path to Running (5 Minutes)

```bash
cd /home/EXQUISITE/Project-Red-Sword

# 1. Run health check
python3 scripts/health_check.py --fix

# 2. Start the platform
./scripts/start_red_team.sh

# 3. Access dashboards
# Open browser to: http://localhost:5006
```

That's it! The platform will start with all safety features enabled.

---

## ✅ Prerequisites

### System Requirements
- **Operating System**: Linux (Ubuntu 20.04+ recommended)
- **Python**: 3.8 or higher
- **RAM**: Minimum 4GB, Recommended 8GB+
- **Disk Space**: 10GB minimum
- **Network**: Isolated test network recommended

### Required Permissions
- Ability to create network connections
- Ability to run Python processes
- Read/write access to project directory

### Optional Services
- **RabbitMQ**: For message queuing (optional)
- **Kafka**: For high-volume event streaming (optional)
- **Docker**: For containerized deployment (optional)

---

## 📦 Installation

### Step 1: Install Dependencies

```bash
# Update system packages
sudo apt-get update

# Install Python and pip
sudo apt-get install -y python3 python3-pip python3-venv

# Install system dependencies
sudo apt-get install -y build-essential libssl-dev libffi-dev

# Clone or navigate to project
cd /home/EXQUISITE/Project-Red-Sword

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### Step 2: Verify Installation

```bash
# Run health check
python3 scripts/health_check.py --mode full

# Expected output: All checks should pass
```

---

## ⚙️ Configuration

### Environment Variables (.env)

The `.env` file is already configured with safe defaults:

```bash
# Key Settings (Already Configured)
DEMO_MODE=true                  # No external API calls
SAFE_MODE=true                  # Safety features enabled
ENABLE_KILL_SWITCH=true         # Emergency stop available
MAX_CONCURRENT_ATTACKS=5        # Limited concurrent attacks
ATTACK_RATE_LIMIT=10            # 10 attacks per minute max
```

### Attack Configuration (config/attack_config.yaml)

Controls what attacks are enabled and their parameters:

```yaml
# Example: Enable/disable attack types
social_engineering:
  enabled: true
  phishing:
    enabled: true
    max_targets_per_campaign: 50

web_application:
  enabled: true
  sql_injection:
    enabled: true
    max_payloads: 100
```

### Target Configuration (config/targets.yaml)

**CRITICAL**: Only targets listed here can be attacked:

```yaml
test_environment:
  hosts:
    - hostname: "test-webapp-01"
      ip: "192.168.100.10"
      attack_types:
        - "sql_injection"
        - "xss"
```

**⚠️ WARNING**: Ensure all listed targets are authorized for testing!

### Safety Configuration (config/safe_mode.yaml)

Enforces safety controls:

```yaml
safe_mode:
  enabled: true
  enforcement_level: "strict"  # strict, moderate, permissive

network_segmentation:
  enforce: true
  allowed_networks:
    - "192.168.0.0/16"  # Only attack internal networks
```

---

## 🛡️ Safety Mechanisms

### Layer 1: Configuration Safety
- ✅ Safe mode enabled by default
- ✅ Demo mode (no external APIs)
- ✅ Rate limiting (max 10 attacks/min)
- ✅ Target whitelisting required
- ✅ Network segmentation enforced

### Layer 2: Runtime Safety
- ✅ Resource limits (CPU, memory)
- ✅ Attack timeout (5 minutes max)
- ✅ Concurrent attack limits
- ✅ Real-time monitoring active
- ✅ Automatic artifact cleanup

### Layer 3: Emergency Controls
- ✅ Kill switch script available
- ✅ Graceful shutdown (Ctrl+C)
- ✅ Automatic stop on violations
- ✅ Manual override capability
- ✅ Stop signal file (.stop_attacks)

### Layer 4: Audit & Compliance
- ✅ All actions logged to database
- ✅ Blockchain-based audit trail
- ✅ Incident reports generated
- ✅ Immutable audit logs
- ✅ Compliance mode enabled

---

## ⚔️ Running Attack Simulations

### Method 1: Automated Startup Script

```bash
./scripts/start_red_team.sh
```

This script:
1. Runs pre-flight safety checks
2. Initializes database
3. Starts monitoring systems
4. Launches Panel dashboards
5. Enables all safety features

### Method 2: Manual Start

```bash
source venv/bin/activate
python app.py
```

### Method 3: Panel Serve

```bash
panel serve app.py --port 5006 --show
```

### Accessing Dashboards

Once started, access these URLs:

1. **Home Page**
   `http://localhost:5006/home`
   - System overview
   - Links to all dashboards
   - Quick start guide

2. **Attack Control Panel**
   `http://localhost:5006/attack_control`
   - Launch attacks
   - View running simulations
   - Control attack parameters

3. **Defense Monitoring**
   `http://localhost:5006/defense_monitoring`
   - Real-time threat visualization (1M data points!)
   - Detection analytics
   - Network traffic analysis

4. **AI Image Classification Demo**
   `http://localhost:5006/app`
   - CLIP model image classification

### Running Specific Attack Types

#### Social Engineering (Phishing)

```python
from modules.advanced_social_engineering import AdvancedSocialEngineering

social_eng = AdvancedSocialEngineering()
result = social_eng.simulate_phishing_campaign(
    targets=["testuser1@test.local"],
    template="password_reset"
)
```

#### Web Application (SQL Injection)

```python
from modules.exploit_payloads import ExploitPayloads

exploits = ExploitPayloads()
result = exploits.test_sql_injection(
    target="http://192.168.100.10",
    payloads=["' OR '1'='1", "UNION SELECT NULL--"]
)
```

#### Network Attacks (DNS Tunneling)

```python
from modules.network_exploitation import NetworkExploitation

network = NetworkExploitation()
result = network.dns_tunneling_test(
    target_dns="192.168.100.30",
    payload_size=512
)
```

#### APT Simulation

```python
from modules.apt_simulation import APTSimulation

apt = APTSimulation()
result = apt.run_multi_stage_attack(
    stages=["reconnaissance", "initial_compromise", "lateral_movement"]
)
```

---

## 🔍 Monitoring & Defense

### Real-Time Monitoring

The `RealTimeMonitoring` module automatically:
- Detects attack patterns
- Calculates anomaly scores
- Triggers alerts on threshold breaches
- Logs all detections to database

### Viewing Detections

```python
from database.models import ThreatDetection, SessionLocal

session = SessionLocal()
detections = session.query(ThreatDetection).filter(
    ThreatDetection.confidence_score > 0.8
).all()

for detection in detections:
    print(f"{detection.timestamp}: {detection.threat_type} - {detection.confidence_score}")
```

### Attack Simulation Logs

```python
from database.models import AttackSimulation, SessionLocal

session = SessionLocal()
attacks = session.query(AttackSimulation).filter(
    AttackSimulation.status == "completed"
).all()

for attack in attacks:
    print(f"{attack.attack_type}: Success={attack.success}, Detected={attack.detected}")
```

### Metrics Dashboard

View aggregated metrics:

```python
from database.models import AttackMetrics, SessionLocal
from datetime import datetime, timedelta

session = SessionLocal()
metrics = session.query(AttackMetrics).filter(
    AttackMetrics.date >= datetime.now() - timedelta(days=7)
).all()

for metric in metrics:
    print(f"{metric.date}: Detection Rate={metric.detection_rate}%")
```

---

## 🚨 Emergency Procedures

### Emergency Kill Switch

**Immediately stop all attacks:**

```bash
python3 scripts/kill_all_simulations.py --yes
```

**With reason logging:**

```bash
python3 scripts/kill_all_simulations.py --reason "Security incident detected"
```

**Force kill (SIGKILL):**

```bash
python3 scripts/kill_all_simulations.py --force --yes
```

### Graceful Shutdown

Press `Ctrl+C` in the terminal running the application.

### Creating Stop Signal

```bash
touch .stop_attacks
```

All running attack modules will check for this file and stop gracefully.

### Incident Response Workflow

1. **Detect**: Monitor logs for unexpected behavior
2. **Stop**: Execute kill switch
3. **Assess**: Review incident reports in `reports/incidents/`
4. **Investigate**: Query database for attack logs
5. **Remediate**: Fix vulnerabilities found
6. **Document**: Update incident report
7. **Resume**: Restart with updated configurations

---

## 🔧 Troubleshooting

### Common Issues

#### Issue: "Module not found" errors

```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt
```

#### Issue: Database errors

```bash
# Solution: Reinitialize database
rm red_team_operations.db
python3 -c "from database.models import Base, engine; Base.metadata.create_all(bind=engine)"
```

#### Issue: Permission denied on scripts

```bash
# Solution: Make scripts executable
chmod +x scripts/*.py scripts/*.sh
```

#### Issue: Port 5006 already in use

```bash
# Solution: Kill existing process or use different port
lsof -ti:5006 | xargs kill -9
# or
panel serve app.py --port 5007
```

#### Issue: Attacks not running

```bash
# Check for stop signal files
ls -la | grep -E '\.stop|\.kill'
rm .stop_attacks .kill_switch

# Verify safe mode settings
grep SAFE_MODE .env

# Check targets configuration
cat config/targets.yaml
```

### Diagnostic Commands

```bash
# Check system health
python3 scripts/health_check.py --mode full

# View recent logs
tail -f logs/attack_simulation.log

# Check running processes
ps aux | grep python

# View database contents
sqlite3 red_team_operations.db "SELECT * FROM attack_simulations ORDER BY timestamp DESC LIMIT 10;"
```

---

## 📖 Best Practices

### Before Starting Attacks

1. ✅ Run health check: `python3 scripts/health_check.py`
2. ✅ Verify targets are authorized
3. ✅ Confirm network segmentation
4. ✅ Enable monitoring systems
5. ✅ Notify relevant teams
6. ✅ Create backup: `cp red_team_operations.db backups/`
7. ✅ Review safe mode settings

### During Attack Simulations

1. ✅ Monitor dashboards continuously
2. ✅ Watch for unexpected behavior
3. ✅ Track detection rates
4. ✅ Log all observations
5. ✅ Stay within authorized scope
6. ✅ Respect rate limits
7. ✅ Document findings in real-time

### After Attack Simulations

1. ✅ Execute kill switch to ensure cleanup
2. ✅ Review all logs and reports
3. ✅ Analyze detection effectiveness
4. ✅ Document vulnerabilities found
5. ✅ Update defensive configurations
6. ✅ Generate final report
7. ✅ Archive simulation data
8. ✅ Plan remediation activities

### Security Best Practices

1. **Network Isolation**
   - Run simulations in isolated networks
   - Never attack production systems directly
   - Use VLANs or air-gapped networks

2. **Authorization**
   - Obtain written approval before testing
   - Define clear scope and limitations
   - Document all authorized targets

3. **Data Protection**
   - Never exfiltrate real data to external systems
   - Use mock/test data when possible
   - Encrypt sensitive logs

4. **Compliance**
   - Follow all regulatory requirements
   - Maintain audit trails
   - Document all activities
   - Store logs securely

5. **Coordination**
   - Notify SOC before testing
   - Coordinate with IT operations
   - Have incident response team on standby
   - Establish communication channels

---

## 📊 Performance Optimization

### For High-Volume Simulations

```bash
# Increase resource limits in .env
MAX_CONCURRENT_ATTACKS=10
MAX_MEMORY_PER_MODULE=1024
MAX_CPU_PER_MODULE=75

# Enable message queues for better performance
RABBITMQ_ENABLED=true
KAFKA_ENABLED=true
```

### For Large-Scale Data Visualization

```python
# Use Datashader for millions of data points
from modules.data_visualization import DataVisualization

viz = DataVisualization()
threat_data = viz.generate_sample_threat_data(n_points=10000000)
img = viz.datashader_threat_scatter(threat_data)
```

---

## 🗄️ Database Management

### Backup Database

```bash
# Manual backup
cp red_team_operations.db backups/red_team_$(date +%Y%m%d_%H%M%S).db

# Automated backup (runs before each simulation)
# Controlled by: AUTO_BACKUP_BEFORE_SIMULATION=true in .env
```

### Query Attack History

```sql
sqlite3 red_team_operations.db

-- Recent attacks
SELECT timestamp, attack_type, target, success, detected
FROM attack_simulations
ORDER BY timestamp DESC LIMIT 10;

-- Detection rate by attack type
SELECT attack_type,
       COUNT(*) as total,
       SUM(CASE WHEN detected THEN 1 ELSE 0 END) as detected_count,
       (SUM(CASE WHEN detected THEN 1 ELSE 0 END) * 100.0 / COUNT(*)) as detection_rate
FROM attack_simulations
GROUP BY attack_type;

-- Average detection time
SELECT AVG(detection_time_seconds) as avg_detection_time_sec
FROM attack_simulations
WHERE detected = 1;
```

### Export Reports

```bash
# Export to CSV
sqlite3 -header -csv red_team_operations.db "SELECT * FROM attack_simulations;" > attack_report.csv

# Export to JSON
python3 << EOF
from database.models import AttackSimulation, SessionLocal
import json

session = SessionLocal()
attacks = session.query(AttackSimulation).all()
data = [attack.to_dict() for attack in attacks]

with open('attack_report.json', 'w') as f:
    json.dump(data, f, indent=2)
EOF
```

---

## 📝 Reporting

### Daily Reports

Automatically generated in `reports/generated/`:
- Attack summary
- Detection analytics
- Vulnerability findings
- Remediation recommendations

### Generating Manual Reports

```python
from datetime import datetime, timedelta
from database.models import AttackSimulation, ThreatDetection, SessionLocal

session = SessionLocal()

# Get attacks from last 24 hours
yesterday = datetime.now() - timedelta(days=1)
attacks = session.query(AttackSimulation).filter(
    AttackSimulation.timestamp >= yesterday
).all()

# Generate summary
print(f"Total Attacks: {len(attacks)}")
print(f"Successful: {sum(1 for a in attacks if a.success)}")
print(f"Detected: {sum(1 for a in attacks if a.detected)}")
print(f"Detection Rate: {(sum(1 for a in attacks if a.detected) / len(attacks) * 100):.2f}%")
```

---

## 🎓 Training & Education

### Recommended Training Path

**Week 1**: Defensive Operations
- Run monitoring systems
- Analyze detection logs
- Practice incident response
- Tune defensive thresholds

**Week 2**: Attack Basics
- Social engineering simulations
- Web application testing
- Network reconnaissance
- Review detection effectiveness

**Week 3**: Advanced Attacks
- APT multi-stage simulations
- Data exfiltration techniques
- Lateral movement
- Evasion techniques

**Week 4**: Full Red vs Blue
- Coordinated exercises
- Live attack/defense scenarios
- Comprehensive reporting
- Lessons learned

### Learning Resources

- **Datashader Integration**: See `DATASHADER_SETUP.md`
- **Module Documentation**: See `docs/` directory
- **API Reference**: See `docs/api_reference.md`
- **Troubleshooting**: See `docs/troubleshooting.md`

---

## 🔐 Security Considerations

### Authorization

**CRITICAL**: This platform contains offensive security tools. Usage requires:
1. Written authorization from management
2. Clear scope definition
3. Defined rules of engagement
4. Incident response plan
5. Insurance and legal protection

### Legal Compliance

- Only test systems you own or have explicit permission to test
- Follow all applicable laws and regulations
- Maintain comprehensive audit trails
- Document all activities
- Never attack unauthorized systems

### Ethical Use

Project Red Sword is designed for:
- ✅ Authorized penetration testing
- ✅ Red team exercises
- ✅ Security research
- ✅ Defensive capability improvement
- ✅ Training and education

It is NOT for:
- ❌ Unauthorized access
- ❌ Malicious attacks
- ❌ Data theft
- ❌ Service disruption
- ❌ Illegal activities

---

## 📞 Support & Contact

### Emergency Contacts

Defined in `config/targets.yaml`:
- Security Operations Center: soc@localhost
- Incident Response: incident-response@localhost

### Documentation

- Main README: `README.md`
- API Reference: `docs/api_reference.md`
- Troubleshooting: `docs/troubleshooting.md`
- Feature Overview: `docs/feature_overview.md`

### Community

- GitHub Issues: https://github.com/your-org/project-red-sword/issues
- Security Reports: security@your-org.com

---

## ✅ Deployment Checklist

Before going live, verify:

- [ ] Health check passes: `python3 scripts/health_check.py`
- [ ] All dependencies installed
- [ ] Database initialized
- [ ] Configuration files present
- [ ] Safe mode enabled
- [ ] Kill switch tested
- [ ] Targets authorized
- [ ] Network segmented
- [ ] Monitoring active
- [ ] Logs configured
- [ ] Backups enabled
- [ ] Authorization documented
- [ ] Team notified
- [ ] Incident response ready
- [ ] Emergency contacts available

---

## 🎉 You're Ready!

Your Project Red Sword platform is now configured and ready for production red team operations. Start with the quick start command:

```bash
./scripts/start_red_team.sh
```

**Remember**: Always operate within authorized scope, maintain safety controls, and document all activities. Good hunting! 🎯

---

**Document Version**: 1.0.0
**Last Updated**: November 4, 2024
**Maintainer**: Security Team
**Classification**: INTERNAL USE ONLY
