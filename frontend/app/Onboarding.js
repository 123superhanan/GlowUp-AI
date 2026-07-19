import { useRouter } from "expo-router";
import {
  SafeAreaView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";

export default function Onboarding() {
  const router = useRouter();

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        {/* Brand Header */}
        <View style={styles.badge}>
          <Text style={styles.badgeText}>GLOWUP AI</Text>
        </View>

        {/* Central Stylized Visual Frame */}
        <View style={styles.heroFrame}>
          <View style={styles.circleOuter}>
            <View style={styles.circleInner} />
          </View>
        </View>

        {/* Typography Section */}
        <View style={styles.textContainer}>
          <Text style={styles.title}>Your beauty, upgraded.</Text>
          <Text style={styles.subtitle}>
            Answer a few simple questions and unlock your personalized routine
            configuration.
          </Text>
        </View>

        {/* Form Interactive Controls */}
        <View style={styles.buttonGroup}>
          <TouchableOpacity
            style={styles.primaryBtn}
            onPress={() => router.push("/(auth)/RegisterScreen")}
            activeOpacity={0.9}
          >
            <Text style={styles.primaryText}>Get Started</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.secondaryBtn}
            onPress={() => router.push("/(auth)/LoginScreen")}
            activeOpacity={0.7}
          >
            <Text style={styles.secondaryText}>I already have an account</Text>
          </TouchableOpacity>
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#FFF8F9", // Seamless signature off-white pink canvas
  },
  content: {
    flex: 1,
    paddingHorizontal: 24,
    paddingTop: 40,
    paddingBottom: 24,
    justifyContent: "space-between",
    alignItems: "center",
  },
  badge: {
    backgroundColor: "#FFF0F3",
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: "#FFD3DC",
  },
  badgeText: {
    color: "#FF4D6D",
    fontWeight: "800",
    fontSize: 12,
    letterSpacing: 1.5,
  },
  heroFrame: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    width: "100%",
  },
  circleOuter: {
    width: 200,
    height: 200,
    borderRadius: 100,
    backgroundColor: "#FFFFFF",
    justifyContent: "center",
    alignItems: "center",
    shadowColor: "#FF7597",
    shadowOffset: { width: 0, height: 12 },
    shadowOpacity: 0.08,
    shadowRadius: 24,
    elevation: 4,
  },
  circleInner: {
    width: 140,
    height: 140,
    borderRadius: 70,
    backgroundColor: "#FFF0F3",
    borderWidth: 2,
    borderColor: "#FFD3DC",
    borderStyle: "dashed",
  },
  textContainer: {
    alignItems: "center",
    marginBottom: 32,
    paddingHorizontal: 8,
  },
  title: {
    fontSize: 32,
    fontWeight: "800",
    color: "#2B2D42",
    textAlign: "center",
    marginBottom: 12,
    letterSpacing: -0.5,
  },
  subtitle: {
    fontSize: 15,
    color: "#8D99AE",
    textAlign: "center",
    lineHeight: 22,
    fontWeight: "500",
  },
  buttonGroup: {
    width: "100%",
    gap: 12,
  },
  primaryBtn: {
    width: "100%",
    backgroundColor: "#FF4D6D",
    paddingVertical: 16,
    borderRadius: 16,
    alignItems: "center",
    shadowColor: "#FF4D6D",
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.15,
    shadowRadius: 12,
    elevation: 3,
  },
  primaryText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "700",
  },
  secondaryBtn: {
    width: "100%",
    paddingVertical: 16,
    alignItems: "center",
  },
  secondaryText: {
    color: "#FF4D6D",
    fontSize: 15,
    fontWeight: "700",
  },
});
