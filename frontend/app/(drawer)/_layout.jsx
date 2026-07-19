import {
  DrawerContentScrollView,
  DrawerItemList,
} from "@react-navigation/drawer";
import { useRouter } from "expo-router";
import { Drawer } from "expo-router/drawer";
import { StyleSheet, Text, TouchableOpacity, View } from "react-native";

// Custom sidebar wrapper component
function CustomDrawerContent(props) {
  const router = useRouter();

  return (
    <DrawerContentScrollView
      {...props}
      contentContainerStyle={styles.drawerContainer}
    >
      <View style={styles.mainContent}>
        {/* Render your default settings and mode navigation links */}
        <DrawerItemList {...props} />
      </View>

      {/* Permanent custom back button at the very bottom of the sliding panel */}
      <TouchableOpacity
        style={styles.backButton}
        onPress={() => router.replace("/(tabs)")}
      >
        <Text style={styles.backButtonText}>⬅ Back to Dashboard</Text>
      </TouchableOpacity>
    </DrawerContentScrollView>
  );
}

export default function DrawerLayout() {
  return (
    <Drawer
      drawerContent={(props) => <CustomDrawerContent {...props} />}
      screenOptions={{
        headerShown: true,
        drawerPosition: "left",
        drawerType: "front",
        drawerActiveTintColor: "#FF4D6D",
      }}
    >
      <Drawer.Screen name="settings" options={{ title: "Settings Profile" }} />
      <Drawer.Screen name="mode" options={{ title: "App Mode" }} />
    </Drawer>
  );
}

const styles = StyleSheet.create({
  drawerContainer: {
    flex: 1,
    justifyContent: "space-between", // Pushes the back button to the bottom
    paddingBottom: 20,
  },
  mainContent: {
    flex: 1,
  },
  backButton: {
    backgroundColor: "#FF4D6D",
    marginHorizontal: 15,
    paddingVertical: 14,
    borderRadius: 10,
    alignItems: "center",
  },
  backButtonText: {
    color: "#fff",
    fontWeight: "bold",
    fontSize: 15,
  },
});
