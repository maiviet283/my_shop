import logging
import json
from datetime import datetime

# Get logger
logger = logging.getLogger('my_shop')

def log_user_action(user, action, details=None, request=None):
    """Log hành động của user"""
    log_data = {
        'type': 'user_action',
        'user_id': user.id,
        'username': user.username,
        'action': action,
        'details': details or {},
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    
    extra = {'log_data': log_data}
    if request:
        extra['request'] = request
    
    logger.info(f"User action: {action}", extra=extra)

def log_business_event(event_type, data, request=None):
    """Log sự kiện business"""
    log_data = {
        'type': 'business_event',
        'event_type': event_type,
        'data': data,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    
    extra = {'log_data': log_data}
    if request:
        extra['request'] = request
    
    logger.info(f"Business event: {event_type}", extra=extra)

def log_security_event(event_type, severity, details, request=None):
    """Log sự kiện bảo mật"""
    log_data = {
        'type': 'security_event',
        'event_type': event_type,
        'severity': severity,
        'details': details,
        'timestamp': datetime.utcnow().isoformat() + 'Z'
    }
    
    extra = {'log_data': log_data}
    if request:
        extra['request'] = request
    
    if severity == 'high':
        logger.error(f"Security event: {event_type}", extra=extra)
    elif severity == 'medium':
        logger.warning(f"Security event: {event_type}", extra=extra)
    else:
        logger.info(f"Security event: {event_type}", extra=extra)