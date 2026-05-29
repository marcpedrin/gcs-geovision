import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';
import '../../theme/app_theme.dart';
import '../../services/data_service.dart';
import '../../models/entry_log.dart';
import '../../widgets/admin_sidebar.dart';
import '../../widgets/common_widgets.dart';

class DashboardScreen extends StatefulWidget {
  const DashboardScreen({super.key});
  @override
  State<DashboardScreenState> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  @override
  void initState() {
    super.initState();
    // Fetch data from backend when screen loads
    Future.microtask(() {
      final data = context.read<DataService>();
      data.loadAllData();
    });
  }

  @override
  Widget build(BuildContext context) {
    final theme = context.watch<ThemeNotifier>();
    final data = context.watch<DataService>();

    return AdminShell(
      activeRoute: '/admin/dashboard',
      breadcrumb: 'Dashboard',
      pageTitle: 'Security Command Centre',
      topbarActions: [
        GestureDetector(
          onTap: () => data.refreshAllData(),
          child: _topbarBtn('↺ Refresh', theme),
        ),
      ],
      rightPanel: _buildRightPanel(context, theme, data),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          // Page title
          Text('Security Command Centre',
              style: GoogleFonts.inter(
                fontSize: 22,
                fontWeight: FontWeight.w800,
                color: theme.textPrimary,
                letterSpacing: -.3,
              )),
          const SizedBox(height: 4),
          Text(
              'Real-time overview of campus security, entries, threats, and system health.',
              style: GoogleFonts.inter(fontSize: 13, color: theme.textSecondary)),
          const SizedBox(height: 16),

          // Stats
          _buildStatsGrid(theme, data),
          const SizedBox(height: 16),

          // 2-column: alerts + feed
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(child: _buildAlerts(context, theme, data)),
              const SizedBox(width: 20),
              Expanded(child: _buildLiveFeed(context, theme, data)),
            ],
          ),
          const SizedBox(height: 20),

          // CCTV preview
          _buildCctvSection(context, theme, data),
          const SizedBox(height: 20),

          // System health
          _buildSystemHealth(theme),
        ]),
      ),
    );
  }

  Widget _topbarBtn(String label, ThemeNotifier theme) => Container(
    padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 7),
    decoration: BoxDecoration(
      color: theme.bgCard,
      border: Border.all(color: theme.border),
      borderRadius: BorderRadius.circular(GeoRadius.sm),
    ),
    child: Text(label,
        style: GoogleFonts.inter(
          fontSize: 12,
          fontWeight: FontWeight.w500,
          color: theme.textSecondary,
        )),
  );

  // ── STATS GRID ────────────────────────────────────────────────────────
  Widget _buildStatsGrid(ThemeNotifier theme, DataService data) => Row(
    children: [
      Expanded(
          child: StatCard(
        theme: theme,
        icon: '📖',
        value: data.entryLogs.length.toString(),
        label: 'Entry Logs Loaded',
        trend: 'Real-time',
      )),
      const SizedBox(width: 12),
      Expanded(
          child: StatCard(
        theme: theme,
        icon: '🚨',
        value: data.alerts.length.toString(),
        label: 'Active Alerts',
        trend: '${data.alerts.length} events',
        iconBg: GeoColors.dangerGhost,
        iconColor: GeoColors.danger,
      )),
      const SizedBox(width: 12),
      Expanded(
          child: StatCard(
        theme: theme,
        icon: '📹',
        value: data.cameras.length.toString(),
        label: 'Cameras',
        trend: '${data.cameras.length} Configured',
      )),
      const SizedBox(width: 12),
      Expanded(
          child: StatCard(
        theme: theme,
        icon: '👥',
        value: data.visitors.length.toString(),
        label: 'Visitors Today',
        trend: '${data.visitors.length} On Campus',
        iconBg: GeoColors.successGhost,
      )),
    ],
  );

  // ── ALERTS ─────────────────────────────────────────────────────────
  Widget _buildAlerts(BuildContext context, ThemeNotifier theme,
          DataService data) =>
      SectionCard(
        theme: theme,
        title: '⚠️ Recent Alerts',
        count: data.alerts.length.toString(),
        redCount: data.alerts.isNotEmpty,
        linkLabel: 'View All →',
        onLink: () => context.go('/admin/entries'),
        child: data.alertsError != null
            ? Center(
                child: Padding(
                  padding: const EdgeInsets.symmetric(vertical: 20),
                  child: Text(
                    'Error: ${data.alertsError}',
                    style: GoogleFonts.inter(color: GeoColors.danger),
                  ),
                ),
              )
            : data.loadingAlerts
                ? const Center(
                    child: Padding(
                      padding: EdgeInsets.symmetric(vertical: 20),
                      child: CircularProgressIndicator(),
                    ),
                  )
                : data.alerts.isEmpty
                    ? Center(
                        child: Padding(
                          padding: const EdgeInsets.symmetric(vertical: 20),
                          child: Text(
                            'No alerts',
                            style: GoogleFonts.inter(
                                color: theme.textSecondary),
                          ),
                        ),
                      )
                    : Column(
                        children: data.alerts
                            .take(3)
                            .map((alert) {
                              final severity = alert['severity'] ?? 'low';
                              final isHighSeverity =
                                  severity == 'high' || severity == 'critical';
                              final color = isHighSeverity
                                  ? GeoColors.danger
                                  : GeoColors.warning;
                              return Padding(
                                padding:
                                    const EdgeInsets.symmetric(vertical: 8),
                                child: _alertItem(
                                  theme,
                                  '🚨',
                                  alert['message'] ?? 'Unknown alert',
                                  'Camera: ${alert['camera_id'] ?? 'Unknown'}',
                                  severity.toUpperCase(),
                                  isHighSeverity,
                                  color,
                                ),
                              );
                            })
                            .toList(),
                      ),
      );

  Widget _alertItem(ThemeNotifier theme, String icon, String title, String meta,
      String badge, bool critical, Color color) {
    final ghost = critical
        ? GeoColors.dangerGhost
        : GeoColors.warningGhost;
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(GeoRadius.md),
        border: Border(left: BorderSide(color: color, width: 3)),
      ),
      child: Row(children: [
        Container(
          width: 34,
          height: 34,
          decoration: BoxDecoration(
              color: ghost,
              borderRadius: BorderRadius.circular(GeoRadius.md)),
          child: Center(child: Text(icon, style: const TextStyle(fontSize: 15))),
        ),
        const SizedBox(width: 12),
        Expanded(
            child: Column(crossAxisAlignment: CrossAxisAlignment.start,
                children: [
              Text(title,
                  style: GoogleFonts.inter(
                    fontSize: 13,
                    fontWeight: FontWeight.w600,
                    color: theme.textPrimary,
                  )),
              Text(meta,
                  style: GoogleFonts.inter(
                      fontSize: 11, color: theme.textTertiary)),
            ])),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 9, vertical: 2),
          decoration: BoxDecoration(
              color: ghost,
              borderRadius: BorderRadius.circular(GeoRadius.full)),
          child: Text(badge,
              style: GoogleFonts.inter(
                fontSize: 10,
                fontWeight: FontWeight.w700,
                color: color,
                letterSpacing: .5,
              )),
        ),
      ]),
    );
  }

  // ── LIVE FEED ─────────────────────────────────────────────────────
  Widget _buildLiveFeed(BuildContext context, ThemeNotifier theme,
          DataService data) =>
      SectionCard(
        theme: theme,
        title: '🟢 Live Entry Feed',
        count: 'Real-time',
        linkLabel: 'Full Log →',
        onLink: () => context.go('/admin/entries'),
        child: data.entryLogsError != null
            ? Center(
                child: Padding(
                  padding: const EdgeInsets.symmetric(vertical: 20),
                  child: Text(
                    'Error: ${data.entryLogsError}',
                    style: GoogleFonts.inter(color: GeoColors.danger),
                  ),
                ),
              )
            : data.loadingEntryLogs
                ? const Center(
                    child: Padding(
                      padding: EdgeInsets.symmetric(vertical: 20),
                      child: CircularProgressIndicator(),
                    ),
                  )
                : data.entryLogs.isEmpty
                    ? Center(
                        child: Padding(
                          padding: const EdgeInsets.symmetric(vertical: 20),
                          child: Text(
                            'No entries logged',
                            style: GoogleFonts.inter(
                                color: theme.textSecondary),
                          ),
                        ),
                      )
                    : Column(
                        children: data.entryLogs
                            .take(6)
                            .map((log) => Padding(
                              padding: const EdgeInsets.only(bottom: 8),
                              child: _feedRow(theme, log),
                            ))
                            .toList(),
                      ),
      );

  Widget _feedRow(ThemeNotifier theme, EntryLog log) {
    final confColor = log.type == 'denied'
        ? GeoColors.danger
        : (log.confidence ?? 75) < 75
            ? GeoColors.warning
            : GeoColors.success;
    final typeLabel =
        log.typeLabel;

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 10),
      decoration: BoxDecoration(
        border: Border.all(color: theme.border),
        borderRadius: BorderRadius.circular(GeoRadius.md),
      ),
      child: Row(children: [
        AvatarCircle(
          initials: log.initials ?? 'UN',
          gradient: _parseGradient(log.color),
          size: 36,
          fontSize: 12,
        ),
        const SizedBox(width: 12),
        Expanded(
            child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
              Text(log.name,
                  style: GoogleFonts.inter(
                    fontSize: 13,
                    fontWeight: FontWeight.w600,
                    color: theme.textPrimary,
                  )),
              Text(
                  '${log.userId} · ${log.gate} · ${_fmtTime(log.timestamp)}',
                  style: GoogleFonts.inter(
                      fontSize: 11, color: theme.textTertiary),
                  overflow: TextOverflow.ellipsis),
            ])),
        Column(crossAxisAlignment: CrossAxisAlignment.end, children: [
          Text('${(log.confidence ?? 0).toStringAsFixed(1)}%',
              style: GoogleFonts.inter(
                fontSize: 13,
                fontWeight: FontWeight.w700,
                color: confColor,
              )),
          Text(typeLabel,
              style:
                  GoogleFonts.inter(fontSize: 11, color: theme.textTertiary)),
        ]),
      ]),
    );
  }

  // ── CCTV GRID ─────────────────────────────────────────────────────
  Widget _buildCctvSection(BuildContext context, ThemeNotifier theme,
          DataService data) =>
      Container(
        decoration: BoxDecoration(
          color: theme.bgCard,
          border: Border.all(color: theme.border),
          borderRadius: BorderRadius.circular(GeoRadius.lg),
        ),
        child: Column(children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: Row(children: [
              Text('📹 Live Cameras',
                  style: GoogleFonts.inter(
                    fontSize: 14,
                    fontWeight: FontWeight.w700,
                    color: theme.textPrimary,
                  )),
              const SizedBox(width: 10),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 3),
                decoration: BoxDecoration(
                    color: theme.bgBadge,
                    borderRadius: BorderRadius.circular(GeoRadius.full)),
                child: Text('${data.cameras.length} Cameras',
                    style: GoogleFonts.inter(
                      fontSize: 11,
                      fontWeight: FontWeight.w600,
                      color: theme.textSecondary,
                    )),
              ),
              const Spacer(),
              GestureDetector(
                onTap: () => context.go('/admin/cctv'),
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 5),
                  decoration: BoxDecoration(
                    border: Border.all(color: GeoColors.primaryGhost),
                    borderRadius: BorderRadius.circular(GeoRadius.sm),
                  ),
                  child: Text('Full Feed →',
                      style: GoogleFonts.inter(
                        fontSize: 11,
                        fontWeight: FontWeight.w600,
                        color: GeoColors.primary,
                      )),
                ),
              ),
            ]),
          ),
          Divider(height: 1, color: theme.border),
          Padding(
            padding: const EdgeInsets.all(20),
            child: data.loadingCameras
                ? const Center(child: CircularProgressIndicator())
                : data.cameras.isEmpty
                    ? Center(
                        child: Text('No cameras available',
                            style: GoogleFonts.inter(
                                color: theme.textSecondary)),
                      )
                    : Row(
                        children: data.cameras
                            .take(4)
                            .map((camera) => Expanded(
                              child: _cctvCell(
                                camera['name'] ?? 'Unknown',
                                camera['status'] == 'online',
                                theme,
                              ),
                            ))
                            .toList(),
                      ),
          ),
        ]),
      );

  Widget _cctvCell(String name, bool online, ThemeNotifier theme) => Padding(
    padding: const EdgeInsets.symmetric(horizontal: 7),
    child: AspectRatio(
      aspectRatio: 16 / 9,
      child: ClipRRect(
        borderRadius: BorderRadius.circular(GeoRadius.md),
        child: Stack(children: [
          Positioned.fill(
              child: Container(
            color: const Color(0xFF111111),
            child: const Center(
                child: Text('📹', style: TextStyle(fontSize: 28))),
          )),
          if (online)
            Positioned(
                top: 8,
                left: 8,
                child: Row(children: [
                  const LiveDot(),
                  const SizedBox(width: 4),
                  Text('LIVE',
                      style: GoogleFonts.inter(
                        fontSize: 9,
                        fontWeight: FontWeight.w700,
                        color: Colors.white,
                      )),
                ])),
          Positioned(
              bottom: 0,
              left: 0,
              right: 0,
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
                decoration: const BoxDecoration(
                    gradient: LinearGradient(
                  begin: Alignment.bottomCenter,
                  end: Alignment.topCenter,
                  colors: [Color(0xD9000000), Colors.transparent],
                )),
                child: Text(name,
                    style: GoogleFonts.inter(
                      fontSize: 10,
                      fontWeight: FontWeight.w600,
                      color: Colors.white,
                    ),
                    overflow: TextOverflow.ellipsis),
              )),
        ]),
      ),
    ),
  );

  // ── SYSTEM HEALTH ─────────────────────────────────────────────────
  Widget _buildSystemHealth(ThemeNotifier theme) => SectionCard(
    theme: theme,
    title: '⚙️ System Health',
    child: Row(children: [
      Expanded(
          child: HealthCard(
        theme: theme,
        label: 'AI Recognition',
        value: '95%',
        sub: 'CPU Load · Online',
        progress: .95,
        barColor: GeoColors.success,
        status: 'online',
      )),
      const SizedBox(width: 14),
      Expanded(
          child: HealthCard(
        theme: theme,
        label: 'Database',
        value: '68%',
        sub: 'Storage Used · Online',
        progress: .68,
        barColor: const Color(0xFF555555),
        status: 'online',
      )),
      const SizedBox(width: 14),
      Expanded(
          child: HealthCard(
        theme: theme,
        label: 'CCTV Network',
        value: 'Online',
        sub: 'All Systems Nominal',
        progress: 1,
        barColor: GeoColors.success,
        status: 'online',
      )),
      const SizedBox(width: 14),
      Expanded(
          child: HealthCard(
        theme: theme,
        label: 'Gate Control',
        value: 'Online',
        sub: 'All Gates Operational',
        progress: 1,
        barColor: GeoColors.success,
        status: 'online',
      )),
    ]),
  );

  // ── RIGHT PANEL ───────────────────────────────────────────────────
  Widget _buildRightPanel(BuildContext context, ThemeNotifier theme,
          DataService data) =>
      Container(
        width: 320,
        color: theme.bgCard,
        child: Column(children: [
          Divider(height: 1, color: theme.border),
          // Status header
          Container(
            padding: const EdgeInsets.symmetric(vertical: 22, horizontal: 20),
            decoration: BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topCenter,
                end: Alignment.bottomCenter,
                colors: [theme.bgBadge, theme.bgCard],
              ),
              border: Border(bottom: BorderSide(color: theme.border)),
            ),
            child: Column(children: [
              Text('SYSTEM STATUS',
                  style: GoogleFonts.inter(
                    fontSize: 14,
                    fontWeight: FontWeight.w700,
                    color: theme.textPrimary,
                  )),
              const SizedBox(height: 10),
              const LiveBadge(label: 'MONITORING LIVE'),
            ]),
          ),
          Expanded(
              child: SingleChildScrollView(
                  child: Column(children: [
            // Data summary
            _panelSection(
              theme,
              'DATA SUMMARY',
              Column(children: [
                _panelRow(theme, '📖 Entry Logs',
                    '${data.entryLogs.length} entries', GeoColors.primary),
                _panelRow(theme, '🚨 Alerts',
                    '${data.alerts.length} alerts', GeoColors.danger),
                _panelRow(
                    theme, '📹 Cameras', '${data.cameras.length} cameras', GeoColors.primary),
                _panelRow(
                    theme, '👥 Visitors', '${data.visitors.length} visitors', GeoColors.success),
              ]),
            ),
            // Actions
            Padding(
              padding: const EdgeInsets.all(16),
              child: GestureDetector(
                onTap: () => context.go('/admin/entries'),
                child: Container(
                  width: double.infinity,
                  padding: const EdgeInsets.symmetric(vertical: 12),
                  decoration: BoxDecoration(
                    color: GeoColors.primary,
                    borderRadius: BorderRadius.circular(GeoRadius.md),
                  ),
                  child: Center(
                      child: Text('📋 View Full Activity Log',
                          style: GoogleFonts.inter(
                            fontSize: 13,
                            fontWeight: FontWeight.w700,
                            color: Colors.white,
                          ))),
                ),
              ),
            ),
          ]))),
        ]),
      );

  Widget _panelSection(ThemeNotifier theme, String title, Widget child) =>
      Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          border: Border(bottom: BorderSide(color: theme.border)),
        ),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Text(title,
              style: GoogleFonts.inter(
                fontSize: 11,
                fontWeight: FontWeight.w700,
                color: theme.textTertiary,
                letterSpacing: .8,
              )),
          const SizedBox(height: 14),
          child,
        ]),
      );

  Widget _panelRow(
      ThemeNotifier theme, String label, String value, Color color) =>
      Padding(
        padding: const EdgeInsets.symmetric(vertical: 9),
        child: Row(children: [
          Expanded(
              child: Text(label,
                  style: GoogleFonts.inter(
                    fontSize: 12,
                    fontWeight: FontWeight.w500,
                    color: theme.textPrimary,
                  ))),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
            decoration: BoxDecoration(
              color: color.withOpacity(.1),
              borderRadius: BorderRadius.circular(GeoRadius.full),
            ),
            child: Text(value,
                style: GoogleFonts.inter(
                  fontSize: 12,
                  fontWeight: FontWeight.w700,
                  color: color,
                )),
          ),
        ]),
      );

  String _fmtTime(DateTime d) =>
      '${d.hour.toString().padLeft(2, '0')}:${d.minute.toString().padLeft(2, '0')}';

  List<Color> _parseGradient(String? colorStr) {
    if (colorStr == null || colorStr.isEmpty) {
      return [GeoColors.primary, GeoColors.primaryDark];
    }
    try {
      final parts = colorStr.split(',');
      return parts
          .map((hex) =>
              Color(int.parse(hex.trim().replaceAll('#', '0xFF'))))
          .toList();
    } catch (_) {
      return [GeoColors.primary, GeoColors.primaryDark];
    }
  }
}
