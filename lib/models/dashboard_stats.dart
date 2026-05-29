class DashboardStats {
  final int totalEntries;
  final int totalExits;
  final int activeVisitors;
  final int securityAlerts;
  final double avgConfidence;
  final int camerasOnline;
  final int camerasOffline;
  final List<String> recentThreats;
  final DateTime? lastUpdated;

  const DashboardStats({
    this.totalEntries = 0,
    this.totalExits = 0,
    this.activeVisitors = 0,
    this.securityAlerts = 0,
    this.avgConfidence = 0.0,
    this.camerasOnline = 0,
    this.camerasOffline = 0,
    this.recentThreats = const [],
    this.lastUpdated,
  });

  Map<String, dynamic> toMap() => {
    'totalEntries': totalEntries,
    'totalExits': totalExits,
    'activeVisitors': activeVisitors,
    'securityAlerts': securityAlerts,
    'avgConfidence': avgConfidence,
    'camerasOnline': camerasOnline,
    'camerasOffline': camerasOffline,
    'recentThreats': recentThreats,
    'lastUpdated': lastUpdated?.toIso8601String(),
  };

  factory DashboardStats.fromMap(Map<String, dynamic> m) => DashboardStats(
    totalEntries: m['totalEntries'] as int? ?? m['total_entries'] as int? ?? 0,
    totalExits: m['totalExits'] as int? ?? m['total_exits'] as int? ?? 0,
    activeVisitors: m['activeVisitors'] as int? ?? m['active_visitors'] as int? ?? 0,
    securityAlerts: m['securityAlerts'] as int? ?? m['security_alerts'] as int? ?? 0,
    avgConfidence: (m['avgConfidence'] as num? ?? m['avg_confidence'] as num? ?? 0.0).toDouble(),
    camerasOnline: m['camerasOnline'] as int? ?? m['cameras_online'] as int? ?? 0,
    camerasOffline: m['camerasOffline'] as int? ?? m['cameras_offline'] as int? ?? 0,
    recentThreats: List<String>.from(m['recentThreats'] as List? ?? m['recent_threats'] as List? ?? []),
    lastUpdated: m['lastUpdated'] != null ? DateTime.tryParse(m['lastUpdated'] as String) : null,
  );
}
