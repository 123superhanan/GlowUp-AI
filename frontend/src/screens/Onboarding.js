import {
  SafeAreaView,
  StatusBar,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";

export default function Onboarding({ navigation }) {
  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" backgroundColor="#FFF8F9" />

      {/* App Bar / Branding */}
      <View style={styles.appBar}>
        <Text style={styles.brandText}>GlowUp AI</Text>
      </View>

      {/* Tactile Preview Card (Interactive Mock GUI) */}
      <View style={styles.interactiveCard}>
        {/* Mock Graphic Container */}
        <View style={styles.graphicContainer}>
          {/* Stylized camera focus rings and glow nodes representing analytical depth */}
          <View style={styles.outerGlowCircle}>
            <View style={styles.innerGlowCircle}>
              <View style={styles.activeCore} />
            </View>
          </View>

          {/* Floating UI Badges directly inside the visual layout */}
          <View style={styles.floatingIndicator}>
            <Text style={styles.indicatorText}>Ready to Scan</Text>
          </View>

          {/* Diagonal Scanner Accent bar */}
          <View style={styles.scannerLine} />
        </View>

        {/* Minimalist Progress Meter */}
        <View style={styles.progressContainer}>
          <View style={styles.progressHeader}>
            <Text style={styles.progressTitle}>Routine Efficiency</Text>
            <Text style={styles.progressValue}>92%</Text>
          </View>
          <View style={styles.progressBarBackground}>
            <View style={styles.progressBarFill} />
          </View>
        </View>
      </View>

      {/* Main Copy & Interactive Actions */}
      <View style={styles.footer}>
        <View style={styles.textBlock}>
          <Text style={styles.title}>
            Your ultimate glow up, curated by AI.
          </Text>
          <Text style={styles.subtitle}>
            Analyze skin health, optimize physical goals, and unlock your full
            aesthetic potential in seconds.
          </Text>
        </View>

        {/* Step Pagination Indicators */}
        <View style={styles.stepContainer}>
          <View style={[styles.stepDot, styles.activeDot]} />
          <View style={styles.stepDot} />
          <View style={styles.stepDot} />
        </View>

        {/* Tactile Solid Touch Button */}
        <TouchableOpacity
          style={styles.primaryButton}
          onPress={() => navigation?.navigate("LoginScreen")}
          activeOpacity={0.9}
        >
          <Text style={styles.primaryButtonText}>Get Started</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#FFF8F9", // Light, warm blush pink off-white backdrop
    paddingHorizontal: 24,
    justifyContent: "space-between",
    paddingBottom: 20,
  },
  appBar: {
    marginTop: 16,
    alignItems: "center",
    justifyContent: "center",
    height: 44,
  },
  brandText: {
    fontSize: 20,
    fontWeight: "800",
    color: "#2B2D42",
    letterSpacing: -0.5,
  },
  interactiveCard: {
    backgroundColor: "#FFFFFF",
    borderRadius: 28,
    height: "45%",
    width: "100%",
    shadowColor: "#FF7597",
    shadowOffset: { width: 0, height: 16 },
    shadowOpacity: 0.12,
    shadowRadius: 24,
    elevation: 8,
    padding: 20,
    justifyContent: "space-between",
  },
  graphicContainer: {
    flex: 1,
    backgroundColor: "#FFF0F3",
    borderRadius: 18,
    overflow: "hidden",
    justifyContent: "center",
    alignItems: "center",
    position: "relative",
  },
  outerGlowCircle: {
    width: 140,
    height: 140,
    borderRadius: 70,
    borderWidth: 2,
    borderColor: "#FFD3DC",
    borderStyle: "dashed",
    justifyContent: "center",
    alignItems: "center",
  },
  innerGlowCircle: {
    width: 90,
    height: 90,
    borderRadius: 45,
    backgroundColor: "rgba(255, 77, 109, 0.08)",
    justifyContent: "center",
    alignItems: "center",
    borderWidth: 1.5,
    borderColor: "#FF7597",
  },
  activeCore: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: "#FF4D6D",
    shadowColor: "#FF4D6D",
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.35,
    shadowRadius: 8,
    elevation: 3,
  },
  floatingIndicator: {
    position: "absolute",
    top: 16,
    left: 16,
    backgroundColor: "#FFFFFF",
    paddingVertical: 6,
    paddingHorizontal: 12,
    borderRadius: 30,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 4,
    elevation: 1,
  },
  indicatorText: {
    fontSize: 11,
    fontWeight: "700",
    color: "#FF4D6D",
    letterSpacing: 0.5,
    textTransform: "uppercase",
  },
  scannerLine: {
    position: "absolute",
    height: 3,
    backgroundColor: "#FF7597",
    width: "100%",
    top: "30%",
    opacity: 0.3,
  },
  progressContainer: {
    marginTop: 16,
  },
  progressHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 8,
  },
  progressTitle: {
    fontSize: 13,
    fontWeight: "700",
    color: "#2B2D42",
  },
  progressValue: {
    fontSize: 13,
    fontWeight: "700",
    color: "#FF4D6D",
  },
  progressBarBackground: {
    height: 6,
    backgroundColor: "#FFF0F3",
    borderRadius: 3,
    width: "100%",
    overflow: "hidden",
  },
  progressBarFill: {
    height: "100%",
    width: "92%",
    backgroundColor: "#FF4D6D",
    borderRadius: 3,
  },
  footer: {
    width: "100%",
    alignItems: "center",
    marginBottom: 16,
  },
  textBlock: {
    alignItems: "center",
    marginBottom: 24,
  },
  title: {
    fontSize: 28,
    fontWeight: "800",
    color: "#2B2D42",
    textAlign: "center",
    lineHeight: 36,
    letterSpacing: -0.4,
    marginBottom: 10,
    paddingHorizontal: 8,
  },
  subtitle: {
    fontSize: 15,
    color: "#8D99AE",
    textAlign: "center",
    lineHeight: 22,
    fontWeight: "500",
    paddingHorizontal: 12,
  },
  stepContainer: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 24,
  },
  stepDot: {
    width: 6,
    height: 6,
    borderRadius: 3,
    backgroundColor: "#FFD3DC",
    marginHorizontal: 4,
  },
  activeDot: {
    backgroundColor: "#FF4D6D",
    width: 20,
  },
  primaryButton: {
    backgroundColor: "#FF4D6D", // Perfectly matched vibrant pink accent
    width: "100%",
    paddingVertical: 18,
    borderRadius: 18,
    alignItems: "center",
    justifyContent: "center",
    shadowColor: "#FF4D6D",
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.25,
    shadowRadius: 16,
    elevation: 4,
  },
  primaryButtonText: {
    color: "#FFFFFF",
    fontWeight: "700",
    fontSize: 16,
    letterSpacing: 0.2,
  },
});
