import time
import json
import logging
import os

class ELKLoggingMiddleware:
    """
    Middleware log TOÀN BỘ request/response cho ELK - Phiên bản gọn nhẹ
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """Cấu hình logger"""
        logger = logging.getLogger('elk_logger')
        
        if not logger.handlers:
            log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
            os.makedirs(log_dir, exist_ok=True)
            
            log_file = os.path.join(log_dir, 'elk.json.log')
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            logger.addHandler(file_handler)
            logger.setLevel(logging.INFO)
            logger.propagate = False
        
        return logger
    
    def __call__(self, request):
        # Log request
        request._start_time = time.time()
        self._log_request(request)
        
        # Process response
        response = self.get_response(request)
        
        # Log response
        self._log_response(request, response)
        
        return response
    
    def _log_request(self, request):
        """Log request details - GỌN NHẸ"""
        log_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "level": "INFO",
            "type": "request",
            "method": request.method,
            "path": request.path,
            "full_path": request.get_full_path(),
            "user_agent": self._get_safe_user_agent(request.META.get('HTTP_USER_AGENT', '')),
            "ip": self._get_client_ip(request),
            "user": self._get_user_info(request),
            "query_params": dict(request.GET),
        }
        
        self.logger.info(json.dumps(log_data, ensure_ascii=False))
        print(f"🔍 ELK Request: {request.method} {request.path}")
    
    def _log_response(self, request, response):
        """Log response details - GỌN NHẸ"""
        duration = time.time() - getattr(request, '_start_time', time.time())
        
        log_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "level": "INFO",
            "type": "response", 
            "method": request.method,
            "path": request.path,
            "status_code": response.status_code,
            "duration_ms": round(duration * 1000, 2),
            "content_length": len(response.content) if hasattr(response, 'content') else 0,
            "user": self._get_user_info(request),
            "ip": self._get_client_ip(request),
        }
        
        # Phân loại log level theo status code
        if 400 <= response.status_code < 500:
            log_data["level"] = "WARNING"
        elif response.status_code >= 500:
            log_data["level"] = "ERROR"
            
        self.logger.info(json.dumps(log_data, ensure_ascii=False))
        print(f"✅ ELK Response: {response.status_code} - {duration:.3f}s")
    
    def _get_client_ip(self, request):
        """Lấy IP client"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', '')
    
    def _get_user_info(self, request):
        """Lấy thông tin user - CHỈ ID VÀ USERNAME"""
        if request.user.is_authenticated:
            return {
                "id": request.user.id,
                "username": request.user.username,
                # ĐÃ XÓA EMAIL VÀ PERMISSIONS
            }
        return {"authenticated": False}
    
    def _get_safe_user_agent(self, user_agent):
        """Làm gọn user agent - CHỈ LẤY BROWSER CHÍNH"""
        if not user_agent:
            return ""
        
        # Chỉ lấy phần browser chính
        browsers = ['Chrome', 'Firefox', 'Safari', 'Edge', 'Opera']
        for browser in browsers:
            if browser in user_agent:
                return browser
        return "Other"