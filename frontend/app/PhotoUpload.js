import * as ImagePicker from "expo-image-picker";
import { useRouter } from "expo-router";
import { useState } from "react";
import {
  ActivityIndicator,
  Alert,
  Image,
  SafeAreaView,
  ScrollView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import { useAuth } from "../context/AuthContext";

export default function PhotoUpload() {
  const router = useRouter();
  const [image, setImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState(null);

  const { accessToken } = useAuth();

  // Safe Back Navigation Handler
  const handleBack = () => {
    if (router.canGoBack()) {
      router.back();
    } else {
      router.replace("/(tabs)/index");
    }
  };

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
      aspect: [1, 1],
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
            Authorization: `Bearer ${accessToken}`,
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
    <SafeAreaView style={styles.container}>
      {/* Header Navigation */}
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.backButton}
          onPress={handleBack}
          activeOpacity={0.7}
        >
          <Text style={styles.backArrow}>←</Text>
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Analyzer</Text>
        <View
          style={[
            styles.statusDot,
            { backgroundColor: accessToken ? "#10B981" : "#EF4444" },
          ]}
        />
      </View>

      {/* Scrollable Container to prevent empty page truncation */}
      <ScrollView
        contentContainerStyle={styles.scrollContent}
        showsVerticalScrollIndicator={false}
      >
        <View style={styles.titleSection}>
          <Text style={styles.title}>Face Shape Analysis</Text>
          <Text style={styles.subtitle}>
            Upload a clear photo to run model inference and receive styled
            recommendations.
          </Text>
        </View>

        {/* Upload Frame Card */}
        <TouchableOpacity
          style={styles.imageCard}
          onPress={pickImage}
          activeOpacity={0.9}
        >
          {image ? (
            <Image source={{ uri: image.uri }} style={styles.imagePreview} />
          ) : (
            <View style={styles.placeholderContainer}>
              <View style={styles.iconCircle}>
                <Text style={styles.uploadIcon}>↑</Text>
              </View>
              <Text style={styles.placeholderText}>Tap to select photo</Text>
              <Text style={styles.placeholderSubtext}>
                JPG or PNG up to 10MB
              </Text>
            </View>
          )}
        </TouchableOpacity>

        {/* Action Button */}
        {image && !loading && (
          <TouchableOpacity
            style={styles.actionButton}
            onPress={uploadAndPredict}
            activeOpacity={0.8}
          >
            <Text style={styles.actionButtonText}>Analyze Image</Text>
          </TouchableOpacity>
        )}

        {/* Loading Indicator */}
        {loading && (
          <View style={styles.loadingContainer}>
            <ActivityIndicator size="small" color="#111827" />
            <Text style={styles.loadingText}>Analyzing facial features...</Text>
          </View>
        )}

        {/* Database Output Result Card */}
        {prediction && (
          <View style={styles.resultsCard}>
            <View style={styles.resultHeader}>
              <Text style={styles.resultLabel}>DETECTED SHAPE</Text>
              <Text style={styles.resultShape}>{prediction.face_shape}</Text>
            </View>
            <View style={styles.divider} />
            <Text style={styles.recommendationTitle}>Recommendation</Text>
            <Text style={styles.recommendationText}>
              {prediction.recommendation}
            </Text>
            <Text style={styles.recordId}>ID: {prediction.id}</Text>
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#F8F9FA",
  },
  header: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
    paddingHorizontal: 20,
    paddingVertical: 12,
  },
  backButton: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: "#FFFFFF",
    justifyContent: "center",
    alignItems: "center",
    borderWidth: 1,
    borderColor: "#E5E7EB",
  },
  backArrow: {
    fontSize: 18,
    color: "#111827",
    fontWeight: "500",
  },
  headerTitle: {
    fontSize: 15,
    fontWeight: "600",
    color: "#111827",
    letterSpacing: -0.2,
  },
  statusDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
  },
  scrollContent: {
    flexGrow: 1,
    paddingHorizontal: 20,
    paddingTop: 10,
    paddingBottom: 40,
  },
  titleSection: {
    marginBottom: 20,
  },
  title: {
    fontSize: 26,
    fontWeight: "700",
    color: "#111827",
    letterSpacing: -0.5,
    marginBottom: 6,
  },
  subtitle: {
    fontSize: 14,
    color: "#6B7280",
    lineHeight: 20,
  },
  imageCard: {
    width: "100%",
    height: 280,
    borderRadius: 16,
    backgroundColor: "#FFFFFF",
    borderWidth: 1,
    borderColor: "#E5E7EB",
    borderStyle: "dashed",
    overflow: "hidden",
    justifyContent: "center",
    alignItems: "center",
    marginBottom: 16,
  },
  imagePreview: {
    width: "100%",
    height: "100%",
    resizeMode: "cover",
  },
  placeholderContainer: {
    alignItems: "center",
  },
  iconCircle: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: "#F3F4F6",
    justifyContent: "center",
    alignItems: "center",
    marginBottom: 10,
  },
  uploadIcon: {
    fontSize: 18,
    color: "#374151",
    fontWeight: "600",
  },
  placeholderText: {
    fontSize: 14,
    fontWeight: "600",
    color: "#111827",
  },
  placeholderSubtext: {
    fontSize: 12,
    color: "#9CA3AF",
    marginTop: 2,
  },
  actionButton: {
    backgroundColor: "#111827",
    paddingVertical: 14,
    borderRadius: 12,
    alignItems: "center",
    justifyContent: "center",
  },
  actionButtonText: {
    color: "#FFFFFF",
    fontSize: 15,
    fontWeight: "600",
  },
  loadingContainer: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    paddingVertical: 14,
  },
  loadingText: {
    marginLeft: 10,
    fontSize: 14,
    color: "#4B5563",
    fontWeight: "500",
  },
  resultsCard: {
    marginTop: 16,
    backgroundColor: "#FFFFFF",
    borderRadius: 16,
    padding: 18,
    borderWidth: 1,
    borderColor: "#E5E7EB",
  },
  resultHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
  },
  resultLabel: {
    fontSize: 11,
    fontWeight: "700",
    color: "#6B7280",
    letterSpacing: 0.8,
  },
  resultShape: {
    fontSize: 16,
    fontWeight: "700",
    color: "#2563EB",
    textTransform: "capitalize",
  },
  divider: {
    height: 1,
    backgroundColor: "#F3F4F6",
    marginVertical: 12,
  },
  recommendationTitle: {
    fontSize: 12,
    fontWeight: "600",
    color: "#374151",
    marginBottom: 4,
  },
  recommendationText: {
    fontSize: 14,
    color: "#4B5563",
    lineHeight: 20,
  },
  recordId: {
    fontSize: 11,
    color: "#9CA3AF",
    marginTop: 10,
  },
});
