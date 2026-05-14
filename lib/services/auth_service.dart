import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/user_model.dart';
import 'api_service.dart';

class AuthService extends ChangeNotifier {
  AuthService(this._api);

  final ApiService _api;
  UserModel? _currentUser;
  String? _token;

  UserModel? get currentUser => _currentUser;
  bool get isLoggedIn => _currentUser != null;
  bool get isAdmin => _currentUser?.isAdmin ?? false;
  String? get token => _token;

  // ── RESTORE SESSION ────────────────────────────────────────────────
  Future<void> restoreSession() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('gv_user_token');
    if (token == null) return;

    _api.setToken(token);
    _token = token;

    try {
      final profile = await _api.getProfile();
      _currentUser = UserModel.fromMap(profile['user'] as Map<String, dynamic>);
      notifyListeners();
    } catch (_) {
      await logout();
    }
  }

  // ── LOGIN ──────────────────────────────────────────────────────────
  Future<({bool ok, String? error})> login(String email, String password) async {
    try {
      final response = await _api.login(email, password);
      final token = response['token'] as String?;
      if (token == null) {
        return (ok: false, error: 'Invalid backend response');
      }

      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('gv_user_token', token);
      _api.setToken(token);
      _token = token;

      final profile = await _api.getProfile();
      _currentUser = UserModel.fromMap(profile['user'] as Map<String, dynamic>);
      notifyListeners();
      return (ok: true, error: null);
    } catch (e) {
      return (ok: false, error: e is ApiException ? e.message : e.toString());
    }
  }

  // ── REGISTER ──────────────────────────────────────────────────────
  Future<({bool ok, String? error})> register({
    required String email,
    required String password,
    required String name,
    required String studentId,
    String? phone,
    String? dept,
    String? year,
  }) async {
    try {
      final response = await _api.register({
        'email': email,
        'password': password,
        'name': name,
        'studentId': studentId,
        'phone': phone,
        'dept': dept,
        'year': year,
      });

      final token = response['token'] as String?;
      if (token == null) {
        return (ok: false, error: 'Invalid backend response');
      }

      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('gv_user_token', token);
      _api.setToken(token);
      _token = token;

      _currentUser = UserModel.fromMap(response['user'] as Map<String, dynamic>);
      notifyListeners();
      return (ok: true, error: null);
    } catch (e) {
      return (ok: false, error: e is ApiException ? e.message : e.toString());
    }
  }

  // ── LOGOUT ──────────────────────────────────────────────────────────
  Future<void> logout() async {
    try {
      await _api.post('/auth/logout', {});
    } catch (_) {
      // ignore logout failures when cleaning up local state
    }

    _currentUser = null;
    _token = null;
    _api.setToken(null);

    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('gv_user_token');
    notifyListeners();
  }

  // ── UPDATE PROFILE ──────────────────────────────────────────────────────
  Future<void> updateProfile(UserModel updated) async {
    final response = await _api.updateProfile(updated.toMap());
    _currentUser = UserModel.fromMap(response['user'] as Map<String, dynamic>);
    notifyListeners();
  }
}
