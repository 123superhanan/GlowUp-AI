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
    // Navigates directly into the Drawer group panel stack / triggers drawer open
    router.push("/(drawer)/setting");
  };

  const gotoLogin = () => {
    router.replace("/(auth)/LoginScreen");
  };

  const gotoUpoad = () => {
    router.replace("/PhotoUpload");
  };
  return (
    <SafeAreaView style={styles.container}>
      {/* Real Top Header Row with Hamburger Menu */}
      <View style={styles.headerRow}>
        <TouchableOpacity
          onPress={handleOpenSettings}
          style={styles.hamburgerButton}
          activeOpacity={0.7}
        >
          {/* Pure CSS/Layout Hamburger Lines */}
          <View style={styles.hamburgerLine} />
          <View style={[styles.hamburgerLine, styles.middleLine]} />
          <View style={styles.hamburgerLine} />
        </TouchableOpacity>

        <Text style={styles.headerBrand}>GlowUp AI</Text>
        <View style={styles.headerSpacer} />
      </View>

      {/* Main Screen Content Area */}
      <View style={styles.content}>
        <Text style={styles.title}>Welcome Home</Text>
        <Text style={styles.subtitle}>
          Tap the menu icon in the top left to open your settings panel.
        </Text>

        <Pressable onPress={gotoLogin} style={styles.logoutButton}>
          <Text style={styles.logoutText}>Sign Out</Text>
        </Pressable>

        <Pressable onPress={gotoUpoad} style={styles.logoutButton}>
          <Text style={styles.logoutText}>PhotoUpload</Text>
        </Pressable>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#FFF8F9", // Cohesive uniform premium background
  },
  /* Top Header Configuration */
  headerRow: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 20,
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: "#FFF0F3",
    backgroundColor: "#FFFFFF",
  },
  hamburgerButton: {
    width: 40,
    height: 40,
    justifyContent: "center",
    alignItems: "flex-start",
  },
  hamburgerLine: {
    width: 22,
    height: 2.5,
    backgroundColor: "#2B2D42",
    borderRadius: 2,
    marginVertical: 2,
  },
  middleLine: {
    width: 16, // Stylized layered multi-length menu aesthetic
  },
  headerBrand: {
    fontSize: 18,
    fontWeight: "800",
    color: "#2B2D42",
    letterSpacing: -0.5,
  },
  headerSpacer: {
    width: 40, // Keeps branding perfectly centered by balancing the button size
  },
  /* Body Content */
  content: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    paddingHorizontal: 32,
  },
  title: {
    fontSize: 24,
    fontWeight: "800",
    color: "#2B2D42",
    marginBottom: 8,
    letterSpacing: -0.5,
  },
  subtitle: {
    fontSize: 14,
    color: "#8D99AE",
    textAlign: "center",
    lineHeight: 20,
    marginBottom: 36,
    fontWeight: "500",
  },
  logoutButton: {
    paddingVertical: 16,
    paddingHorizontal: 32,
    backgroundColor: "#FFF0F3",
    borderRadius: 16,
    borderWidth: 1,
    borderColor: "#FFD3DC",
    width: "100%",
    alignItems: "center",
  },
  logoutText: {
    color: "#FF4D6D",
    fontWeight: "700",
    fontSize: 16,
  },
});
