// frontend/App.tsx
import * as ImagePicker from "expo-image-picker";
import { useState } from "react";
import {
  Alert,
  Image,
  ImageBackground,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import { colors } from "./constants/colors";

const App = () => {
  const [showMainApp, setShowMainApp] = useState<boolean>(false);
  const [image, setImage] = useState<string | null>(null);

  const takePhoto = async () => {
    const result = await ImagePicker.launchCameraAsync();
    if (!result.canceled) setImage(result.assets[0].uri);
  };

  const pickImage = async () => {
    const result = await ImagePicker.launchImageLibraryAsync();
    if (!result.canceled) setImage(result.assets[0].uri);
  };

  // --- WELCOME STATE LAYER ---
  if (!showMainApp) {
    return (
      <ImageBackground
        source={{
          uri: "https://images.unsplash.com/photo-1581091226033-d5c48150dbaa?w=800",
        }}
        style={styles.container}
        imageStyle={{ opacity: 0.15 }}
      >
        <View style={styles.welcomeHero}>
          <View style={styles.brandingGroup}>
            <Text style={styles.title}>StockWise</Text>
            <Text style={styles.subtitle}>AI-Powered Inventory Management</Text>
          </View>

          <View style={styles.pitchGroup}>
            <Text style={styles.welcomeHeading}>
              Smart Stocking Made Simple
            </Text>
            <Text style={styles.welcomeBody}>
              Scan receipts instantly, automate tracking, and forecast demand
              with custom AI models.
            </Text>
          </View>
        </View>

        <TouchableOpacity
          style={styles.getStartedBtn}
          onPress={() => setShowMainApp(true)}
        >
          <Text style={styles.getStartedText}>Get Started</Text>
        </TouchableOpacity>
      </ImageBackground>
    );
  }

  // --- CORE APP SCANNER LAYER ---
  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backBtn}
          onPress={() => {
            setShowMainApp(false);
            setImage(null);
          }}
        >
          <Text style={styles.backBtnText}>← Back</Text>
        </TouchableOpacity>
        <Text style={styles.appBarTitle}>Scan Receipt</Text>
      </View>

      {image ? (
        <Image source={{ uri: image }} style={styles.image} />
      ) : (
        <View style={styles.imagePlaceholder}>
          <Text style={styles.placeholderIcon}>📸</Text>
          <Text style={styles.placeholderText}>No receipt selected yet</Text>
        </View>
      )}

      <TouchableOpacity style={styles.actionBtn} onPress={takePhoto}>
        <Text style={styles.btnText}>Take Photo</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.actionBtn} onPress={pickImage}>
        <Text style={styles.btnText}>Choose from Gallery</Text>
      </TouchableOpacity>

      {image && (
        <TouchableOpacity
          style={styles.analyzeBtn}
          onPress={() =>
            Alert.alert(
              "Success",
              "Analyzing receipt details via AI Service...",
            )
          }
        >
          <Text style={styles.analyzeText}>Scan Receipt</Text>
        </TouchableOpacity>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 24,
    backgroundColor: colors.background.primary,
  },

  // Welcome Screen Specifics
  welcomeHero: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  brandingGroup: {
    alignItems: "center",
    marginBottom: 40,
  },
  title: {
    fontSize: 44,
    fontWeight: "800",
    color: colors.text.primary,
    letterSpacing: -1,
  },
  subtitle: {
    fontSize: 14,
    fontWeight: "500",
    color: colors.text.muted,
    marginTop: 4,
    textTransform: "uppercase",
    letterSpacing: 1,
  },
  pitchGroup: {
    alignItems: "center",
    paddingHorizontal: 20,
  },
  welcomeHeading: {
    fontSize: 24,
    fontWeight: "700",
    color: colors.text.primary,
    textAlign: "center",
    marginBottom: 12,
  },
  welcomeBody: {
    fontSize: 15,
    color: colors.text.secondary,
    textAlign: "center",
    lineHeight: 22,
  },
  getStartedBtn: {
    backgroundColor: colors.button.primary,
    paddingVertical: 16,
    borderRadius: 16,
    shadowColor: colors.shadow.sage,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 8,
    elevation: 3,
  },
  getStartedText: {
    color: colors.text.inverse,
    textAlign: "center",
    fontSize: 16,
    fontWeight: "700",
  },

  // Inside Dashboard/Scanner Layer
  header: {
    marginTop: 40,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 30,
    position: "relative",
    width: "100%",
  },
  backBtn: {
    position: "absolute",
    left: 0,
    paddingVertical: 6,
  },
  backBtnText: {
    color: colors.text.muted,
    fontSize: 15,
    fontWeight: "600",
  },
  appBarTitle: {
    fontSize: 20,
    fontWeight: "700",
    color: colors.text.primary,
  },
  imagePlaceholder: {
    width: "100%",
    height: 280,
    borderRadius: 20,
    backgroundColor: colors.secondary.sageLight,
    justifyContent: "center",
    alignItems: "center",
    marginBottom: 24,
    borderWidth: 2,
    borderColor: colors.secondary.sageMuted,
    borderStyle: "dashed",
  },
  placeholderIcon: {
    fontSize: 42,
    marginBottom: 10,
    opacity: 0.7,
  },
  placeholderText: {
    color: colors.text.secondary,
    fontSize: 14,
    fontWeight: "500",
  },
  image: {
    width: "100%",
    height: 280,
    borderRadius: 20,
    marginBottom: 24,
  },
  actionBtn: {
    backgroundColor: colors.background.card,
    paddingVertical: 15,
    borderRadius: 14,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: colors.border.light,
    shadowColor: colors.shadow.light,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.04,
    shadowRadius: 4,
    elevation: 1,
  },
  btnText: {
    color: colors.text.primary,
    textAlign: "center",
    fontSize: 15,
    fontWeight: "600",
  },
  analyzeBtn: {
    backgroundColor: colors.button.primaryPressed,
    paddingVertical: 16,
    borderRadius: 14,
    marginTop: 10,
    shadowColor: colors.shadow.sage,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2,
    shadowRadius: 6,
    elevation: 2,
  },
  analyzeText: {
    color: colors.text.inverse,
    textAlign: "center",
    fontSize: 15,
    fontWeight: "700",
  },
});

export default App;
