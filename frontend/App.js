import { NavigationContainer } from "@react-navigation/native";
import { createStackNavigator } from "@react-navigation/stack";
import { AuthProvider, useAuth } from "./context/AuthContext";

import MainTabs from "./src/screens/(tabs)/MainTabs";
import GlowUpDashboard from "./src/screens/GlowUpDashboard";
import LoginScreen from "./src/screens/LoginScreen";
import Onboarding from "./src/screens/Onboarding";
import PhotoUpload from "./src/screens/PhotoUpload";
import RegisterScreen from "./src/screens/RegisterScreen";
import Report from "./src/screens/Report";

const Stack = createStackNavigator();

// This component handles routing based on auth state
function AppNavigator() {
  const { user, loading } = useAuth();

  if (loading) {
    return null; // Or show a splash screen
  }

  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      {user ? (
        // User is logged in → show main app
        <>
          <Stack.Screen name="MainTabs" component={MainTabs} />
          <Stack.Screen name="GlowUpDashboard" component={GlowUpDashboard} />
          <Stack.Screen name="PhotoUpload" component={PhotoUpload} />
          <Stack.Screen name="Report" component={Report} />
        </>
      ) : (
        // User is NOT logged in → show auth flow
        <>
          <Stack.Screen name="Onboarding" component={Onboarding} />
          <Stack.Screen name="LoginScreen" component={LoginScreen} />
          <Stack.Screen name="RegisterScreen" component={RegisterScreen} />
        </>
      )}
    </Stack.Navigator>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <NavigationContainer>
        <AppNavigator />
      </NavigationContainer>
    </AuthProvider>
  );
}
