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
        <Text style={styles.brandText}>GLOWUP AI</Text>

        {/* Typography Section */}
        <View style={styles.textContainer}>
          <Text style={styles.title}>Your beauty, upgraded.</Text>
          <Text style={styles.subtitle}>
            Answer a few simple questions and unlock your personalized routine
            configuration.
          </Text>
        </View>

        {/* Action Controls */}
        <View style={styles.buttonGroup}>
          <TouchableOpacity
            style={styles.primaryBtn}
            onPress={() => router.push("/(auth)/RegisterScreen")}
            activeOpacity={0.8}
          >
            <Text style={styles.primaryText}>Get Started</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.secondaryBtn}
            onPress={() => router.push("/(auth)/LoginScreen")}
            activeOpacity={0.6}
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
    backgroundColor: "#FFFFFF",
  },
  content: {
    flex: 1,
    paddingHorizontal: 24,
    paddingTop: 32,
    paddingBottom: 24,
    justifyContent: "space-between",
  },
  brandText: {
    fontSize: 14,
    fontWeight: "800",
    color: "#000000",
    letterSpacing: 2,
  },
  textContainer: {
    marginVertical: "auto",
  },
  title: {
    fontSize: 36,
    fontWeight: "800",
    color: "#000000",
    marginBottom: 12,
    letterSpacing: -0.5,
  },
  subtitle: {
    fontSize: 16,
    color: "#000000",
    lineHeight: 24,
    fontWeight: "400",
    opacity: 0.7,
  },
  buttonGroup: {
    width: "100%",
    gap: 12,
  },
  primaryBtn: {
    width: "100%",
    backgroundColor: "#FF4D6D",
    paddingVertical: 18,
    borderRadius: 12,
    alignItems: "center",
  },
  primaryText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "700",
  },
  secondaryBtn: {
    width: "100%",
    paddingVertical: 14,
    alignItems: "center",
  },
  secondaryText: {
    color: "#000000",
    fontSize: 15,
    fontWeight: "600",
  },
});
