class Camera {
  final String id;
  final String name;
  final String location;
  final bool active;
  final double? lat;
  final double? lng;
  final String? streamUrl;
  final DateTime? lastUpdate;

  const Camera({
    required this.id,
    required this.name,
    required this.location,
    required this.active,
    this.lat,
    this.lng,
    this.streamUrl,
    this.lastUpdate,
  });

  Map<String, dynamic> toMap() => {
    'id': id,
    'name': name,
    'location': location,
    'active': active,
    'lat': lat,
    'lng': lng,
    'streamUrl': streamUrl,
    'lastUpdate': lastUpdate?.toIso8601String(),
  };

  factory Camera.fromMap(Map<String, dynamic> m) => Camera(
    id: m['id'] as String,
    name: m['name'] as String,
    location: m['location'] as String,
    active: m['active'] as bool? ?? false,
    lat: (m['lat'] as num?)?.toDouble(),
    lng: (m['lng'] as num?)?.toDouble(),
    streamUrl: m['streamUrl'] as String?,
    lastUpdate: m['lastUpdate'] != null ? DateTime.tryParse(m['lastUpdate'] as String) : null,
  );
}
