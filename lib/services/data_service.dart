import 'package:flutter/foundation.dart';
import '../models/entry_log.dart';
import '../models/visitor.dart';
import 'api_service.dart';

/// DataService manages all data fetching from the backend API.
/// Replaces DbService for real-time backend integration.
class DataService extends ChangeNotifier {
  DataService(this._api);

  final ApiService _api;

  // ── LOADING STATES ────────────────────────────────────────────────────────
  bool _loadingCameras = false;
  bool _loadingAlerts = false;
  bool _loadingEntryLogs = false;
  bool _loadingVisitors = false;

  bool get loadingCameras => _loadingCameras;
  bool get loadingAlerts => _loadingAlerts;
  bool get loadingEntryLogs => _loadingEntryLogs;
  bool get loadingVisitors => _loadingVisitors;

  // ── DATA CACHES ───────────────────────────────────────────────────────────
  List<dynamic> _cameras = [];
  List<dynamic> _alerts = [];
  List<EntryLog> _entryLogs = [];
  List<Visitor> _visitors = [];

  List<dynamic> get cameras => _cameras;
  List<dynamic> get alerts => _alerts;
  List<EntryLog> get entryLogs => _entryLogs;
  List<Visitor> get visitors => _visitors;

  // ── ERROR STATES ──────────────────────────────────────────────────────────
  String? _camerasError;
  String? _alertsError;
  String? _entryLogsError;
  String? _visitorsError;

  String? get camerasError => _camerasError;
  String? get alertsError => _alertsError;
  String? get entryLogsError => _entryLogsError;
  String? get visitorsError => _visitorsError;

  // ── PAGINATION ────────────────────────────────────────────────────────────
  int _alertPage = 1;
  int _alertTotal = 0;
  int _entryLogsPage = 1;
  int _entryLogsTotal = 0;

  int get alertPage => _alertPage;
  int get alertTotal => _alertTotal;
  int get entryLogsPage => _entryLogsPage;
  int get entryLogsTotal => _entryLogsTotal;

  // ── CAMERAS ───────────────────────────────────────────────────────────────

  Future<void> fetchCameras() async {
    _setLoadingCameras(true);
    _camerasError = null;
    try {
      final result = await _api.getCameraList();
      _cameras = result;
      if (kDebugMode) print('[DataService] Loaded ${_cameras.length} cameras');
    } catch (e) {
      _camerasError = e is ApiException ? e.message : e.toString();
      if (kDebugMode) print('[DataService] Error fetching cameras: $_camerasError');
    } finally {
      _setLoadingCameras(false);
    }
  }

  Future<Map<String, dynamic>> getCameraStatus(String cameraId) async {
    try {
      return await _api.getCameraStatus(cameraId);
    } catch (e) {
      if (kDebugMode) print('[DataService] Error getting camera status: $e');
      rethrow;
    }
  }

  void _setLoadingCameras(bool value) {
    _loadingCameras = value;
    notifyListeners();
  }

  // ── ALERTS ────────────────────────────────────────────────────────────────

  Future<void> fetchAlerts({int page = 1, int limit = 20}) async {
    _setLoadingAlerts(true);
    _alertsError = null;
    try {
      final result = await _api.getAlerts(page: page, limit: limit);
      _alerts = result['alerts'] ?? [];
      _alertPage = result['page'] ?? page;
      _alertTotal = result['total'] ?? 0;
      if (kDebugMode) print('[DataService] Loaded ${_alerts.length} alerts (page $_alertPage)');
    } catch (e) {
      _alertsError = e is ApiException ? e.message : e.toString();
      if (kDebugMode) print('[DataService] Error fetching alerts: $_alertsError');
    } finally {
      _setLoadingAlerts(false);
    }
  }

  Future<void> createAlert({
    required String cameraId,
    required String message,
    String severity = 'medium',
  }) async {
    try {
      await _api.createAlert(
        cameraId: cameraId,
        message: message,
        severity: severity,
      );
      // Refresh alerts after creating
      await fetchAlerts();
      if (kDebugMode) print('[DataService] Alert created successfully');
    } catch (e) {
      if (kDebugMode) print('[DataService] Error creating alert: $e');
      rethrow;
    }
  }

  void _setLoadingAlerts(bool value) {
    _loadingAlerts = value;
    notifyListeners();
  }

  // ── ENTRY LOGS ────────────────────────────────────────────────────────────

  Future<void> fetchEntryLogs({
    String? userId,
    int page = 1,
    int limit = 50,
  }) async {
    _setLoadingEntryLogs(true);
    _entryLogsError = null;
    try {
      final result = await _api.getEntryLogs(
        userId: userId,
        page: page,
        limit: limit,
      );
      final logs = (result['logs'] as List?)?.cast<Map<String, dynamic>>() ?? [];
      _entryLogs = logs.map((m) => EntryLog.fromMap(m)).toList();
      _entryLogsPage = result['page'] ?? page;
      _entryLogsTotal = result['total'] ?? 0;
      if (kDebugMode) print('[DataService] Loaded ${_entryLogs.length} entry logs');
    } catch (e) {
      _entryLogsError = e is ApiException ? e.message : e.toString();
      if (kDebugMode) print('[DataService] Error fetching entry logs: $_entryLogsError');
    } finally {
      _setLoadingEntryLogs(false);
    }
  }

  void _setLoadingEntryLogs(bool value) {
    _loadingEntryLogs = value;
    notifyListeners();
  }

  // ── VISITORS ──────────────────────────────────────────────────────────────

  Future<void> fetchVisitors() async {
    _setLoadingVisitors(true);
    _visitorsError = null;
    try {
      final result = await _api.getVisitors();
      final visitorMaps =
          (result as List?)?.cast<Map<String, dynamic>>() ?? [];
      _visitors = visitorMaps.map((m) => Visitor.fromMap(m)).toList();
      if (kDebugMode) print('[DataService] Loaded ${_visitors.length} visitors');
    } catch (e) {
      _visitorsError = e is ApiException ? e.message : e.toString();
      if (kDebugMode) print('[DataService] Error fetching visitors: $_visitorsError');
    } finally {
      _setLoadingVisitors(false);
    }
  }

  Future<void> createVisitor(Map<String, dynamic> data) async {
    try {
      await _api.createVisitor(data);
      // Refresh visitors after creating
      await fetchVisitors();
      if (kDebugMode) print('[DataService] Visitor created successfully');
    } catch (e) {
      if (kDebugMode) print('[DataService] Error creating visitor: $e');
      rethrow;
    }
  }

  Future<void> updateVisitor(int visitorId, Map<String, dynamic> data) async {
    try {
      await _api.updateVisitor(visitorId, data);
      // Refresh visitors after updating
      await fetchVisitors();
      if (kDebugMode) print('[DataService] Visitor updated successfully');
    } catch (e) {
      if (kDebugMode) print('[DataService] Error updating visitor: $e');
      rethrow;
    }
  }

  Future<void> deleteVisitor(int visitorId) async {
    try {
      await _api.deleteVisitor(visitorId);
      // Refresh visitors after deleting
      await fetchVisitors();
      if (kDebugMode) print('[DataService] Visitor deleted successfully');
    } catch (e) {
      if (kDebugMode) print('[DataService] Error deleting visitor: $e');
      rethrow;
    }
  }

  void _setLoadingVisitors(bool value) {
    _loadingVisitors = value;
    notifyListeners();
  }

  // ── BATCH LOAD ────────────────────────────────────────────────────────────

  Future<void> loadAllData() async {
    await Future.wait([
      fetchCameras(),
      fetchAlerts(),
      fetchEntryLogs(),
      fetchVisitors(),
    ]);
  }

  // ── REFRESH ───────────────────────────────────────────────────────────────

  Future<void> refreshAllData() async {
    _alerts.clear();
    _entryLogs.clear();
    _alertPage = 1;
    _entryLogsPage = 1;
    await loadAllData();
  }
}
