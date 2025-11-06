from sqlalchemy import create_engine, Column, String, Integer, Text, Float, Boolean, DateTime, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import logging
import os
import json

Base = declarative_base()

# ============================================================================
# ORIGINAL MODEL
# ============================================================================

class DocumentAnalysis(Base):
    __tablename__ = "document_analysis"
    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String, nullable=False)
    title = Column(String, nullable=True)
    links = Column(Text, nullable=True)
    error = Column(Text, nullable=True)

# ============================================================================
# ATTACK SIMULATION MODELS
# ============================================================================

class AttackSimulation(Base):
    """Records of all attack simulations executed."""
    __tablename__ = "attack_simulations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    attack_type = Column(String(100), nullable=False)  # phishing, sql_injection, apt, etc.
    attack_category = Column(String(50), nullable=False)  # social_engineering, web_app, network, apt
    target = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False)  # started, running, completed, failed, stopped
    success = Column(Boolean, nullable=True)
    detected = Column(Boolean, nullable=True)
    detection_time_seconds = Column(Float, nullable=True)
    duration_seconds = Column(Float, nullable=True)
    severity_level = Column(Float, nullable=True)  # 0.0 to 1.0

    # Details
    parameters = Column(Text, nullable=True)  # JSON
    results = Column(Text, nullable=True)  # JSON
    error_message = Column(Text, nullable=True)

    # Safety and compliance
    safe_mode_enabled = Column(Boolean, default=True)
    authorization_token = Column(String(255), nullable=True)
    operator = Column(String(100), nullable=True)

    # Relationships
    detections = relationship("ThreatDetection", back_populates="attack_simulation")
    incidents = relationship("IncidentResponse", back_populates="attack_simulation")

    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'attack_type': self.attack_type,
            'attack_category': self.attack_category,
            'target': self.target,
            'status': self.status,
            'success': self.success,
            'detected': self.detected,
            'detection_time_seconds': self.detection_time_seconds,
            'duration_seconds': self.duration_seconds,
            'severity_level': self.severity_level
        }

class ThreatDetection(Base):
    """Records of threats detected by defensive systems."""
    __tablename__ = "threat_detections"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    detection_source = Column(String(100), nullable=False)  # monitoring, ml_model, ids, waf, etc.
    threat_type = Column(String(100), nullable=False)
    threat_category = Column(String(50), nullable=False)
    confidence_score = Column(Float, nullable=False)  # 0.0 to 1.0
    severity_score = Column(Float, nullable=False)  # 0.0 to 1.0

    # Source information
    source_ip = Column(String(50), nullable=True)
    source_port = Column(Integer, nullable=True)
    target_ip = Column(String(50), nullable=True)
    target_port = Column(Integer, nullable=True)

    # Details
    detection_details = Column(Text, nullable=True)  # JSON
    indicators_of_compromise = Column(Text, nullable=True)  # JSON

    # Link to attack simulation if it's part of red team exercise
    attack_simulation_id = Column(Integer, ForeignKey('attack_simulations.id'), nullable=True)
    attack_simulation = relationship("AttackSimulation", back_populates="detections")

    # Action taken
    action_taken = Column(String(100), nullable=True)  # alert, block, quarantine, etc.
    false_positive = Column(Boolean, nullable=True)

class IncidentResponse(Base):
    """Records of automated incident response actions."""
    __tablename__ = "incident_responses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    incident_type = Column(String(100), nullable=False)
    incident_severity = Column(String(50), nullable=False)  # low, medium, high, critical

    # Response details
    response_action = Column(String(100), nullable=False)  # quarantine, block, isolate, etc.
    response_status = Column(String(50), nullable=False)  # initiated, in_progress, completed, failed
    response_time_seconds = Column(Float, nullable=True)

    # Affected resources
    affected_systems = Column(Text, nullable=True)  # JSON list
    affected_users = Column(Text, nullable=True)  # JSON list

    # Details
    response_details = Column(Text, nullable=True)  # JSON
    resolution = Column(Text, nullable=True)

    # Link to attack simulation
    attack_simulation_id = Column(Integer, ForeignKey('attack_simulations.id'), nullable=True)
    attack_simulation = relationship("AttackSimulation", back_populates="incidents")

    # Escalation
    escalated = Column(Boolean, default=False)
    escalation_level = Column(Integer, nullable=True)
    escalation_contact = Column(String(255), nullable=True)

class AttackMetrics(Base):
    """Aggregated metrics and statistics for attack simulations."""
    __tablename__ = "attack_metrics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False)
    attack_category = Column(String(50), nullable=False)

    # Counts
    total_attacks = Column(Integer, default=0)
    successful_attacks = Column(Integer, default=0)
    failed_attacks = Column(Integer, default=0)
    detected_attacks = Column(Integer, default=0)
    undetected_attacks = Column(Integer, default=0)

    # Averages
    avg_detection_time_seconds = Column(Float, nullable=True)
    avg_response_time_seconds = Column(Float, nullable=True)
    avg_attack_duration_seconds = Column(Float, nullable=True)

    # Rates
    detection_rate = Column(Float, nullable=True)  # Percentage
    success_rate = Column(Float, nullable=True)  # Percentage
    false_positive_rate = Column(Float, nullable=True)  # Percentage

class DefensivePosture(Base):
    """Tracks the overall defensive security posture over time."""
    __tablename__ = "defensive_posture"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Overall scores (0.0 to 1.0)
    detection_capability_score = Column(Float, nullable=False)
    response_capability_score = Column(Float, nullable=False)
    prevention_capability_score = Column(Float, nullable=False)
    overall_security_score = Column(Float, nullable=False)

    # Performance metrics
    mean_time_to_detect_seconds = Column(Float, nullable=True)
    mean_time_to_respond_seconds = Column(Float, nullable=True)
    mean_time_to_contain_seconds = Column(Float, nullable=True)

    # Coverage
    attack_surface_coverage_percent = Column(Float, nullable=True)
    monitored_assets_count = Column(Integer, nullable=True)

    # Vulnerabilities
    critical_vulnerabilities = Column(Integer, default=0)
    high_vulnerabilities = Column(Integer, default=0)
    medium_vulnerabilities = Column(Integer, default=0)
    low_vulnerabilities = Column(Integer, default=0)

    # Details
    assessment_notes = Column(Text, nullable=True)

class AuditLog(Base):
    """Immutable audit trail for all system actions."""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    action_type = Column(String(100), nullable=False)
    actor = Column(String(100), nullable=False)  # user, system, module name
    action_category = Column(String(50), nullable=False)  # attack, defense, config, admin

    # Action details
    action_description = Column(Text, nullable=False)
    target_resource = Column(String(255), nullable=True)
    action_result = Column(String(50), nullable=False)  # success, failure, partial

    # Compliance
    compliance_relevant = Column(Boolean, default=False)
    authorization_level = Column(String(50), nullable=True)

    # Details
    action_details = Column(Text, nullable=True)  # JSON

    # Blockchain integration
    blockchain_hash = Column(String(255), nullable=True)
    blockchain_block_number = Column(Integer, nullable=True)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///document_analysis.db")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Connect to the apps, dashboards, modules, tools, payloads, and exploits
# Commented out to avoid circular imports - these can be imported locally where needed
# from app_security.app_vulnerability_scanner import scan_application
# from app import monitoring, threat_intelligence, advanced_threat_intelligence, predictive_analytics, automated_incident_response, ai_red_teaming, apt_simulation, machine_learning_ai, data_visualization, blockchain_logger, cloud_exploitation, iot_exploitation, quantum_computing, edge_computing, serverless_computing, microservices_architecture, cloud_native_applications
# from backend.code_parser import CodeParser
# from backend.pipeline_manager import PipelineManager
# from c2_dashboard import C2Dashboard
# from chatbot.app import scan_network, deploy_exploit
# from chatbot.chatbot import handle_vulnerability_scanning, handle_exploit_deployment
# from dashboard.dashboard import malware_analysis, social_engineering
# from exploits.exploits2 import deploy_exploit as deploy_exploit2
# from exploits.ios_framework_extracted.iOS_Zero_Click_Framework_Updated.exploits import deploy_exploit as deploy_exploit_ios
# from modules.alerts_notifications import AlertsNotifications
# from modules.apt_simulation import APTSimulation

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Verification of component connections
def verify_component_connections():
    try:
        # Check database connection
        session = SessionLocal()
        session.execute(text('SELECT 1'))
        session.close()
        logging.info("Database connection verified.")
        
        # Check app components
        if not all([monitoring, threat_intelligence, advanced_threat_intelligence, predictive_analytics, automated_incident_response, ai_red_teaming, apt_simulation, machine_learning_ai, data_visualization, blockchain_logger, cloud_exploitation, iot_exploitation, quantum_computing, edge_computing, serverless_computing, microservices_architecture, cloud_native_applications]):
            raise ValueError("App component connection check failed")
        logging.info("App components connection verified.")
        
        # Check backend components
        if not all([CodeParser, PipelineManager]):
            raise ValueError("Backend component connection check failed")
        logging.info("Backend components connection verified.")
        
        # Check chatbot components
        if not all([scan_network, deploy_exploit, handle_vulnerability_scanning, handle_exploit_deployment]):
            raise ValueError("Chatbot component connection check failed")
        logging.info("Chatbot components connection verified.")
        
        # Check dashboard components
        if not all([malware_analysis, social_engineering]):
            raise ValueError("Dashboard component connection check failed")
        logging.info("Dashboard components connection verified.")
        
        # Check exploits components
        if not all([deploy_exploit2, deploy_exploit_ios]):
            raise ValueError("Exploits component connection check failed")
        logging.info("Exploits components connection verified.")
        
        # Check modules components
        if not all([AlertsNotifications, APTSimulation]):
            raise ValueError("Modules components connection check failed")
        logging.info("Modules components connection verified.")
        
    except Exception as e:
        logging.error(f"Component connection verification failed: {e}")

# Run verification
verify_component_connections()
