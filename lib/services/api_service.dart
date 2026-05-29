import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

/// Thrown when the server returns a non-2xx status code.
class ApiException implements Exception {
  final int statusCode;
  final String message;
  const ApiException(this.statusCode, this.message);

  @override
  String toString() => 'ApiException($statusCode): $message';
}

class ApiService {
  // FastAPI backend URL for local and emulator development.
  // - Desktop / web: http://127.0.0.1:8000/api
  // - Android emulator: http://10.0.2.2:8000/api
  static const String baseUrl = 'http://127.0.0.1:8000/api';
  static const String baseUrlAlt = 'http://10.0.2.2:8000/api'; // Android emulator

  static const Duration _timeout = Duration(seconds: 15);

  final http.Client _client = http.Client();
  String? _token;

  void setToken(String? token) {
    _token = token;
    if (kDebugMode) debugPrint('[API] Token set: ${token != null ? 'YES' : 'NO'}');
  }

  // ── Generic HTTP ──────────────────────────────────────────────────────────

  Future<Map<String, dynamic>> get(String endpoint, {String? overrideUrl}) async {
    final url = overrideUrl ?? '$baseUrl$endpoint';
    try {
      if (kDebugMode) debugPrint('[API] GET: $url');
      final res = await _client
          .get(Uri.parse(url), headers: _headers())
          .timeout(_timeout);
      if (kDebugMode) debugPrint('[API] GET Response: ${res.statusCode}');
      return _handle(res);
    } catch (e) {
      if (kDebugMode) debugPrint('[API] GET Error: $e');
      rethrow;
    }
  }

  Future<Map<String, dynamic>> post(
      String endpoint, Map<String, dynamic> body, {String? overrideUrl}) async {
    final url = overrideUrl ?? '$baseUrl$endpoint';
    try {
      if (kDebugMode) debugPrint('[API] POST: $url with body: $body');
      final res = await _client
          .post(Uri.parse(url),
              headers: _headers(), body: jsonEncode(body))
          .timeout(_timeout);
      if (kDebugMode) debugPrint('[API] POST Response: ${res.statusCode}');
      return _handle(res);
    } catch (e) {
      if (kDebugMode) debugPrint('[API] POST Error: $e');
      rethrow;
    }
  }

  Future<Map<String, dynamic>> put(
      String endpoint, Map<String, dynamic> body, {String? overrideUrl}) async {
    final url = overrideUrl ?? '$baseUrl$endpoint';
    try {
      if (kDebugMode) debugPrint('[API] PUT: $url with body: $body');
      final res = await _client
          .put(Uri.parse(url),
              headers: _headers(), body: jsonEncode(body))
          .timeout(_timeout);
      if (kDebugMode) debugPrint('[API] PUT Response: ${res.statusCode}');
      return _handle(res);
    } catch (e) {
      if (kDebugMode) debugPrint('[API] PUT Error: $e');
      rethrow;
    }
  }

  Future<void> delete(String endpoint, {String? overrideUrl}) async {
    final url = overrideUrl ?? '$baseUrl$endpoint';
    try {
      if (kDebugMode) debugPrint('[API] DELETE: $url');
      final res = await _client
          .delete(Uri.parse(url), headers: _headers())
          .timeout(_timeout);
      if (kDebugMode) debugPrint('[API] DELETE Response: ${res.statusCode}');
      _handle(res);
    } catch (e) {
      if (kDebugMode) debugPrint('[API] DELETE Error: $e');
      rethrow;
    }
  }

  // ── AUTHENTICATION ────────────────────────────────────────────────────────

  Future<Map<String, dynamic>> login(String email, String password) async {
    final data = await post('/auth/login', {
      'email': email,
      'password': password,
    });
    final token = data['token'] as String?;
    if (token == null) {
      throw const ApiException(200, 'Token missing in response');
    }
    _token = token;
    return data;
  }

  Future<Map<String, dynamic>> register(Map<String, dynamic> body) async {
    return post('/auth/register', body);
  }

  Future<void> logout() async {
    try {
      await post('/auth/logout', {});
    } finally {
      _token = null;
    }
  }

  // ── USER / PROFILE ────────────────────────────────────────────────────────

  Future<Map<String, dynamic>> getProfile() async {
    return get('/users/me');
  }

  Future<Map<String, dynamic>> updateProfile(
      Map<String, dynamic> body) async {
    return put('/users/me', body);
  }

  // ── CAMERAS & STATUS ──────────────────────────────────────────────────────

  Future<List<dynamic>> getCameraList() async {
    final data = await get('/cameras');
    return data['cameras'] ?? [];
  }

  Future<Map<String, dynamic>> getCameraStatus(String cameraId) async {
    return get('/cameras/$cameraId/status');
  }

  // ── ALERTS ────────────────────────────────────────────────────────────────

  Future<Map<String, dynamic>> getAlerts({int page = 1, int limit = 20}) async {
    final data = await get('/alerts?page=$page&limit=$limit');
    return {
      'alerts': data['alerts'] ?? [],
      'page': data['page'] ?? page,
      'total': data['total'] ?? 0,
    };
  }

  Future<void> createAlert({
    required String cameraId,
    required String message,
    String severity = 'medium',
  }) async {
    await post('/alerts', {
      'camera_id': cameraId,
      'message': message,
      'severity': severity,
    });
  }

  // ── ENTRY LOGS ────────────────────────────────────────────────────────────

  Future<Map<String, dynamic>> getEntryLogs({
    String? userId,
    int page = 1,
    int limit = 50,
  }) async {
    String query = '?page=$page&limit=$limit';
    if (userId != null) {
      query += '&user_id=${Uri.encodeQueryComponent(userId)}';
    }
    final data = await get('/entry_logs$query');
    return {
      'logs': data['logs'] ?? [],
      'page': data['page'] ?? page,
      'total': data['total'] ?? 0,
    };
  }

  // ── VISITORS ──────────────────────────────────────────────────────────────

  Future<List<dynamic>> getVisitors() async {
    final data = await get('/visitors');
    return data['visitors'] ?? [];
  }

  Future<Map<String, dynamic>> createVisitor(Map<String, dynamic> body) async {
    final data = await post('/visitors', body);
    return data['visitor'] ?? data;
  }
  Future<Map<String, dynamic>> checkoutVisitor(String visitorId) async {
    return put('/visitors/$visitorId/checkout', {});
  }

  // ── DASHBOARD STATISTICS ───────────────────────────────────────────

  Future<Map<String, dynamic>> getDashboardStats() async {
    return get('/dashboard/stats');
  }

  // ── FACE ENROLLMENT ────────────────────────────────────────────────

  Future<Map<String, dynamic>> initiateFaceEnrollment(String userId) async {
    return post('/face/enroll/init', {'user_id': userId});
  }

  Future<Map<String, dynamic>> uploadFaceFrame(
    String sessionId,
    String base64Image, {
    String? label,
  }) async {
    return post('/face/enroll/frame', {
      'session_id': sessionId,
      'frame': base64Image,
      'label': label ?? 'capture',
    });
  }

  Future<Map<String, dynamic>> completeFaceEnrollment(String sessionId) async {
    return post('/face/enroll/complete', {'session_id': sessionId});
  }

  // ── THREATS / SECURITY ANALYSIS ────────────────────────────────────

  Future<Map<String, dynamic>> getThreats({
    int page = 1,
    int limit = 20,
    String? severity,
  }) async {
    String query = '?page=$page&limit=$limit';
    if (severity != null) {
      query += '&severity=${Uri.encodeQueryComponent(severity)}';
    }
    final data = await get('/threats$query');
    return {
      'threats': data['threats'] ?? [],
      'page': data['page'] ?? page,
      'total': data['total'] ?? 0,
    };
  }

  Future<Map<String, dynamic>> getThreatDetail(String threatId) async {
    return get('/threats/$threatId');
  }

  Future<Map<String, dynamic>> updateThreatStatus(
    String threatId, {
    required String status, // 'resolved' | 'escalated' | 'investigating'
    String? notes,
  }) async {
    return put('/threats/$threatId', {
      'status': status,
      'notes': notes,
    });
  }

  // ── LIVE STREAM / CCTV ──────────────────────────────────────────────

  Future<String> getCctvStreamUrl(String cameraId) async {
    final data = await get('/cameras/$cameraId/stream');
    return data['url'] as String? ?? '';
  }

  Future<Map<String, dynamic>> triggerManualSnapshot(String cameraId) async {
    return post('/cameras/$cameraId/snapshot', {});
  }

  // ── HEALTH & STATUS ────────────────────────────────────────────────

  Future<Map<String, dynamic>> getSystemHealth() async {
    return get('/health');
  }

  // ── BULK OPERATIONS ────────────────────────────────────────────────

  Future<List<dynamic>> getRecentEvents({int limit = 50}) async {
    final data = await get('/events?limit=$limit');
    return data['events'] ?? [];
  }

  Future<Map<String, dynamic>> exportData({
    required String format, // 'csv' | 'pdf'
    required String dataType, // 'entries' | 'visitors' | 'threats'
    Map<String, String>? filters,
  }) async {
    final body = {
      'format': format,
      'dataType': dataType,
      if (filters != null) ...filters,
    };
    return post('/export', body);
  }
  Future<Map<String, dynamic>> updateVisitor(
      int visitorId, Map<String, dynamic> body) async {
    final data = await put('/visitors/$visitorId', body);
    return data['visitor'] ?? data;
  }

  Future<void> deleteVisitor(int visitorId) async {
    await delete('/visitors/$visitorId');
  }

  // ── FACE ENROLLMENT ───────────────────────────────────────────────────────

  Future<Map<String, dynamic>> uploadFaceImage(
      String imagePath, String mode) async {
    try {
      if (kDebugMode) debugPrint('[API] Uploading face from: $imagePath');
      
      // Multipart form-data for file upload
      final request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseUrl/face/enroll'),
      );
      request.headers.addAll(_headers());
      request.fields['mode'] = mode;
      
      final file = File(imagePath);
      if (await file.exists()) {
        request.files.add(
          await http.MultipartFile.fromPath('image', imagePath),
        );
      }

      final response = await request.send().timeout(_timeout);
      if (kDebugMode) debugPrint('[API] Face upload response: ${response.statusCode}');
      
      final respData = await response.stream.bytesToString();
      if (response.statusCode >= 200 && response.statusCode < 300) {
        return jsonDecode(respData) as Map<String, dynamic>;
      } else {
        String msg;
        try {
          msg = (jsonDecode(respData) as Map)['message'] ?? respData;
        } catch (_) {
          msg = respData;
        }
        throw ApiException(response.statusCode, msg);
      }
    } catch (e) {
      if (kDebugMode) debugPrint('[API] Face upload error: $e');
      rethrow;
    }
  }

  Future<Map<String, dynamic>> verifyFace(String imagePath) async {
    try {
      if (kDebugMode) debugPrint('[API] Verifying face from: $imagePath');
      
      final request = http.MultipartRequest(
        'POST',
        Uri.parse('$baseUrl/face/verify'),
      );
      request.headers.addAll(_headers());
      
      final file = File(imagePath);
      if (await file.exists()) {
        request.files.add(
          await http.MultipartFile.fromPath('image', imagePath),
        );
      }

      final response = await request.send().timeout(_timeout);
      if (kDebugMode) debugPrint('[API] Face verification response: ${response.statusCode}');
      
      final respData = await response.stream.bytesToString();
      if (response.statusCode >= 200 && response.statusCode < 300) {
        return jsonDecode(respData) as Map<String, dynamic>;
      } else {
        String msg;
        try {
          msg = (jsonDecode(respData) as Map)['message'] ?? respData;
        } catch (_) {
          msg = respData;
        }
        throw ApiException(response.statusCode, msg);
      }
    } catch (e) {
      if (kDebugMode) debugPrint('[API] Face verification error: $e');
      rethrow;
    }
  }

  // ── INTERNAL ──────────────────────────────────────────────────────────────

  Map<String, String> _headers() => {
        HttpHeaders.contentTypeHeader: 'application/json',
        HttpHeaders.acceptHeader: 'application/json',
        if (_token != null)
          HttpHeaders.authorizationHeader: 'Bearer $_token',
      };

  Map<String, dynamic> _handle(http.Response res) {
    if (res.statusCode >= 200 && res.statusCode < 300) {
      if (res.body.isEmpty) return {};
      return jsonDecode(res.body) as Map<String, dynamic>;
    }
    String msg;
    try {
      msg = (jsonDecode(res.body) as Map)['message'] ?? res.body;
    } catch (_) {
      msg = res.body;
    }
    throw ApiException(res.statusCode, msg);
  }

  void dispose() => _client.close();
}