import { useRouter } from "expo-router";
import {
  Pressable,
  SafeAreaView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";

export default function HomeIndex() {
  const router = useRouter();

  const handleOpenSettings = () => {
    router.push("/(drawer)/setting");
  };

  const gotoLogin = () => {
    router.replace("/(auth)/LoginScreen");
  };

  const gotoUpload = () => {
    router.replace("/PhotoUpload");
  };

  return (
    <SafeAreaView style={styles.container}>
      {/* Top Header Row with Hamburger Menu */}
      <View style={styles.headerRow}>
        <TouchableOpacity
          onPress={handleOpenSettings}
          style={styles.hamburgerButton}
          activeOpacity={0.7}
        >
          <View style={styles.hamburgerLine} />
          <View style={styles.hamburgerLine} />
          <View style={styles.hamburgerLine} />
        </TouchableOpacity>

        <Text style={styles.headerBrand}>GLOWUP AI</Text>
        <View style={styles.headerSpacer} />
      </View>

      {/* Main Screen Content Area */}
      <View style={styles.content}>
        <View style={styles.textContainer}>
          <Text style={styles.title}>Welcome Home</Text>
          <Text style={styles.subtitle}>
            Tap the menu icon in the top left to open your settings panel.
          </Text>
        </View>

        <View style={styles.buttonGroup}>
          <Pressable onPress={gotoUpload} style={styles.primaryBtn}>
            <Text style={styles.primaryText}>Upload Photo</Text>
          </Pressable>

          <Pressable onPress={gotoLogin} style={styles.secondaryBtn}>
            <Text style={styles.secondaryText}>Sign Out</Text>
          </Pressable>
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
  /* Top Header Configuration */
  headerRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 24,
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: "#EEEEEE",
    backgroundColor: "#FFFFFF",
  },
  hamburgerButton: {
    width: 32,
    height: 32,
    justifyContent: "center",
    alignItems: "flex-start",
    gap: 4,
  },
  hamburgerLine: {
    width: 20,
    height: 2,
    backgroundColor: "#000000",
  },
  headerBrand: {
    fontSize: 14,
    fontWeight: "800",
    color: "#000000",
    letterSpacing: 2,
  },
  headerSpacer: {
    width: 32,
  },
  /* Body Content */
  content: {
    flex: 1,
    paddingHorizontal: 24,
    paddingTop: 32,
    paddingBottom: 24,
    justifyContent: "space-between",
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
