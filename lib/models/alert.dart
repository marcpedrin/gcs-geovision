class Alert {
  final String id;
  final String cameraId;
  final String message;
  final String severity; // 'low' | 'medium' | 'high' | 'critical'
  final DateTime timestamp;
  final bool resolved;
  final String? details;
  final String? imageUrl;

  const Alert({
    required this.id,
    required this.cameraId,
    required this.message,
    required this.severity,
    required this.timestamp,
    this.resolved = false,
    this.details,
    this.imageUrl,
  });

  bool get isCritical => severity == 'critical';
  bool get isHigh => severity == 'high';

  Map<String, dynamic> toMap() => {
    'id': id,
    'cameraId': cameraId,
    'message': message,
    'severity': severity,
    'timestamp': timestamp.toIso8601String(),
    'resolved': resolved,
    'details': details,
    'imageUrl': imageUrl,
  };

  factory Alert.fromMap(Map<String, dynamic> m) => Alert(
    id: m['id'] as String,
    cameraId: m['cameraId'] as String? ?? m['camera_id'] as String? ?? '',
    message: m['message'] as String,
    severity: m['severity'] as String? ?? 'medium',
    timestamp: m['timestamp'] != null ? DateTime.tryParse(m['timestamp'] as String) ?? DateTime.now() : DateTime.now(),
    resolved: m['resolved'] as bool? ?? false,
    details: m['details'] as String?,
    imageUrl: m['imageUrl'] as String? ?? m['image_url'] as String?,
  );
}
