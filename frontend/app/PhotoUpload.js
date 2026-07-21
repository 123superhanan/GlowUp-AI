import * as ImagePicker from "expo-image-picker";
import { useState } from "react";
import {
  ActivityIndicator,
  Alert,
  Image,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import { useAuth } from "../context/AuthContext"; // Confirmed dynamic context mapping

export default function PhotoUpload() {
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState(null);

  // 🚀 FIXED: Destructure 'accessToken' directly to match your true AuthContext provider schema!
  const { accessToken } = useAuth();

  const pickImage = async () => {
    const permissionResult =
      await ImagePicker.requestMediaLibraryPermissionsAsync();

    if (permissionResult.granted === false) {
      Alert.alert(
        "Permission Denied",
        "You need to allow access to your photos to use this feature.",
      );
      return;
    }

    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: 1, // Square bounding ratio
      quality: 1,
    });

    if (!result.canceled) {
      setImage(result.assets[0]);
    }
  };

  const uploadAndPredict = async () => {
    if (!image) {
      Alert.alert("Error", "Please select an image first.");
      return;
    }

    // Protect network route against null tokens
    if (!accessToken) {
      Alert.alert(
        "Authentication Error",
        "No active token context found. Please log in again.",
      );
      return;
    }

    setLoading(true);
    setPrediction(null);

    const formData = new FormData();
    const uriParts = image.uri.split(".");
    const fileType = uriParts[uriParts.length - 1];

    formData.append("image", {
      uri: image.uri,
      name: `upload.${fileType}`,
      type: `image/${fileType === "jpg" ? "jpeg" : fileType}`,
    });

    try {
      const response = await fetch(
        "http://localhost:5000/api/predict/predict",
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${accessToken}`, //  FIXED: Inject the matched token variable
            Accept: "application/json",
          },
          body: formData,
        },
      );

      const result = await response.json();

      if (response.ok && result.success) {
        const savedRecord = result.data;
        setPrediction(savedRecord);
        Alert.alert(
          "Success",
          `Face shape detected and saved: ${savedRecord.face_shape}`,
        );
      } else {
        Alert.alert(
          "Inference Failed",
          result.error || result.message || "An unexpected error occurred.",
        );
      }
    } catch (error) {
      console.error("Upload failure trace context:", error);
      Alert.alert(
        "Network Error",
        "Could not connect to the backend server. Verify your server execution state.",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Face Shape Analyzer</Text>

      {/* 🚀 FIXED: Status color condition maps cleanly to your verified token state */}
      <Text style={styles.tokenStatus}>
        Token Validation Status:{" "}
        {accessToken ? "🟢 Authorized Active Token" : "🔴 Missing Auth Token"}
      </Text>

      <TouchableOpacity style={styles.selectButton} onPress={pickImage}>
        <Text style={styles.buttonText}>Pick an Image from Gallery</Text>
      </TouchableOpacity>

      {image && (
        <Image source={{ uri: image.uri }} style={styles.imagePreview} />
      )}

      {image && !loading && (
        <TouchableOpacity
          style={styles.uploadButton}
          onPress={uploadAndPredict}
        >
          <Text style={styles.buttonText}>Analyze & Save Prediction</Text>
        </TouchableOpacity>
      )}

      {loading && (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#FF6B6B" />
          <Text style={styles.loadingText}>
            Running vision inference model...
          </Text>
        </View>
      )}

      {prediction && (
        <View style={styles.resultsBox}>
          <Text style={styles.resultTitle}>Database Output Result:</Text>
          <Text style={styles.resultText}>
            Face Shape: {prediction.face_shape}
          </Text>
          <Text style={styles.resultText}>Record ID: {prediction.id}</Text>
          <Text style={styles.resultText}>
            Recommendation: {prediction.recommendation}
          </Text>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center",
  },
  title: { fontSize: 24, fontWeight: "bold", marginBottom: 10, color: "#333" },
  tokenStatus: { fontSize: 13, color: "#666", marginBottom: 20 },
  selectButton: {
    backgroundColor: "#6C63FF",
    padding: 15,
    borderRadius: 10,
    width: "100%",
    alignItems: "center",
    marginBottom: 20,
  },
  uploadButton: {
    backgroundColor: "#FF6B6B",
    padding: 15,
    borderRadius: 10,
    width: "100%",
    alignItems: "center",
    marginTop: 10,
  },
  buttonText: { color: "white", fontWeight: "bold", fontSize: 16 },
  imagePreview: {
    width: 250,
    height: 250,
    borderRadius: 15,
    marginVertical: 15,
    resizeMode: "cover",
  },
  loadingContainer: { marginVertical: 20, alignItems: "center" },
  loadingText: { marginTop: 10, color: "#666", fontWeight: "500" },
  resultsBox: {
    marginTop: 25,
    padding: 15,
    backgroundColor: "#f8f9fa",
    borderRadius: 10,
    width: "100%",
    borderWidth: 1,
    borderColor: "#e9ecef",
  },
  resultTitle: {
    fontSize: 16,
    fontWeight: "bold",
    marginBottom: 8,
    color: "#2b2b2b",
  },
  resultText: { fontSize: 14, color: "#495057", marginBottom: 4 },
});
