import {
  Alert,
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import { useAuth } from "../../../context/AuthContext";

export default function ProfileTab({ navigation }) {
  const { user, logout } = useAuth();

  const handleLogout = () => {
    Alert.alert(
      "Logout",
      "Are you sure you want to sign out of your account?",
      [
        { text: "Cancel", style: "cancel" },
        {
          text: "Logout",
          style: "destructive",
          onPress: async () => {
            await logout();
            // Use getParent() to ensure we escape the tab context and target the root stack
            const rootNav = navigation.getParent() || navigation;
            rootNav.replace("LoginScreen");
          },
        },
      ],
    );
  };

  // Helper to extract initials for the stylized avatar placeholder
  const getInitials = (nameString) => {
    if (!nameString) return "AH";
    const parts = nameString.split(" ");
    if (parts.length >= 2) return `${parts[0][0]}${parts[1][0]}`.toUpperCase();
    return nameString.slice(0, 2).toUpperCase();
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        contentContainerStyle={styles.content}
        showsVerticalScrollIndicator={false}
      >
        {/* Profile Header Block */}
        <View style={styles.profileHeader}>
          <View style={styles.avatarContainer}>
            <Text style={styles.avatarText}>
              {getInitials(user?.name || "Abdul Hanan")}
            </Text>
          </View>
          <Text style={styles.name}>{user?.name || "Abdul Hanan"}</Text>
          <Text style={styles.email}>{user?.email || "hanan@example.com"}</Text>
        </View>

        {/* Stats Grid Dashboard Card */}
        <View style={styles.statsContainer}>
          <View style={styles.statItem}>
            <Text style={styles.statNumber}>0</Text>
            <Text style={styles.statLabel}>Reports</Text>
          </View>
          <View style={styles.statDivider} />
          <View style={styles.statItem}>
            <Text style={styles.statNumber}>0%</Text>
            <Text style={styles.statLabel}>Avg Score</Text>
          </View>
          <View style={styles.statDivider} />
          <View style={styles.statItem}>
            <Text style={styles.statNumber}>0</Text>
            <Text style={styles.statLabel}>Days Active</Text>
          </View>
        </View>

        {/* Navigation Option List */}
        <View style={styles.menuContainer}>
          <TouchableOpacity
            style={styles.menuItem}
            onPress={() => navigation?.navigate("Settings")}
            activeOpacity={0.7}
          >
            <Text style={styles.menuText}>Account Settings</Text>
            <View style={styles.arrowContainer}>
              <Text style={styles.menuArrow}>›</Text>
            </View>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.menuItem}
            onPress={() =>
              Alert.alert("Support", "Contact our team at support@glowup.ai")
            }
            activeOpacity={0.7}
          >
            <Text style={styles.menuText}>Help & Support</Text>
            <View style={styles.arrowContainer}>
              <Text style={styles.menuArrow}>›</Text>
            </View>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.menuItem}
            onPress={() =>
              Alert.alert(
                "Privacy Policy",
                "Your personal biometric data is fully encrypted locally.",
              )
            }
            activeOpacity={0.7}
          >
            <Text style={styles.menuText}>Privacy Policy</Text>
            <View style={styles.arrowContainer}>
              <Text style={styles.menuArrow}>›</Text>
            </View>
          </TouchableOpacity>
        </View>

        {/* System Interactive Controls */}
        <TouchableOpacity
          style={styles.logoutButton}
          onPress={handleLogout}
          activeOpacity={0.8}
        >
          <Text style={styles.logoutText}>Sign Out</Text>
        </TouchableOpacity>

        <Text style={styles.version}>GlowUp AI v1.0.0</Text>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#FFF8F9", // Matching cohesive off-white pink baseline
  },
  content: {
    paddingHorizontal: 20,
    paddingTop: 30,
    paddingBottom: 40,
  },
  profileHeader: {
    alignItems: "center",
    marginBottom: 28,
  },
  avatarContainer: {
    width: 88,
    height: 88,
    borderRadius: 44,
    backgroundColor: "#FF4D6D",
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 14,
    shadowColor: "#FF4D6D",
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.2,
    shadowRadius: 12,
    elevation: 4,
  },
  avatarText: {
    fontSize: 24,
    fontWeight: "800",
    color: "#FFFFFF",
    letterSpacing: 0.5,
  },
  name: {
    fontSize: 24,
    fontWeight: "800",
    color: "#2B2D42",
    letterSpacing: -0.5,
  },
  email: {
    fontSize: 14,
    color: "#8D99AE",
    marginTop: 4,
    fontWeight: "500",
  },
  statsContainer: {
    flexDirection: "row",
    justifyContent: "space-around",
    alignItems: "center",
    backgroundColor: "#FFFFFF",
    paddingVertical: 20,
    borderRadius: 24,
    marginBottom: 20,
    shadowColor: "#FF7597",
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.05,
    shadowRadius: 16,
    elevation: 3,
  },
  statItem: {
    alignItems: "center",
    flex: 1,
  },
  statDivider: {
    width: 1,
    height: 32,
    backgroundColor: "#FFF0F3",
  },
  statNumber: {
    fontSize: 22,
    fontWeight: "800",
    color: "#FF4D6D",
  },
  statLabel: {
    fontSize: 12,
    color: "#8D99AE",
    marginTop: 4,
    fontWeight: "600",
    letterSpacing: 0.2,
  },
  menuContainer: {
    backgroundColor: "#FFFFFF",
    borderRadius: 24,
    marginBottom: 24,
    shadowColor: "#FF7597",
    shadowOffset: { width: 0, height: 10 },
    shadowOpacity: 0.05,
    shadowRadius: 16,
    elevation: 3,
    overflow: "hidden",
  },
  menuItem: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingVertical: 18,
    paddingHorizontal: 20,
    borderBottomWidth: 1,
    borderBottomColor: "#FFF0F3",
  },
  menuText: {
    fontSize: 15,
    color: "#2B2D42",
    fontWeight: "600",
  },
  arrowContainer: {
    backgroundColor: "#FFF8F9",
    width: 24,
    height: 24,
    borderRadius: 12,
    alignItems: "center",
    justifyContent: "center",
  },
  menuArrow: {
    fontSize: 16,
    color: "#FF7597",
    fontWeight: "700",
    marginTop: -2, // Optical alignment for standard text chevron
  },
  logoutButton: {
    backgroundColor: "#FFF0F3",
    paddingVertical: 16,
    borderRadius: 16,
    alignItems: "center",
    justifyContent: "center",
    borderWidth: 1,
    borderColor: "#FFD3DC",
    marginTop: 4,
  },
  logoutText: {
    color: "#FF4D6D",
    fontSize: 16,
    fontWeight: "700",
  },
  version: {
    textAlign: "center",
    color: "#8D99AE",
    fontSize: 12,
    fontWeight: "500",
    marginTop: 24,
    letterSpacing: 0.5,
  },
});
